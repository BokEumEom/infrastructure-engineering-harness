"""SQLite-backed persistent memory for the Infrastructure Engineering Agent.

Memory is external runtime state, not model truth. User-scope writes require the
user or trusted runtime; model writes are limited to session working memory.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4


ALLOWED_SCOPES = {"user", "session"}
ALLOWED_KINDS = {"preference", "working_context", "task_checkpoint"}
SECRET_LIKE_KEYS = {"password", "passwd", "secret", "token", "api_key", "credential", "private_key"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _contains_secret_like_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in SECRET_LIKE_KEYS:
                return True
            if _contains_secret_like_key(child):
                return True
    elif isinstance(value, list):
        return any(_contains_secret_like_key(item) for item in value)
    return False


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    scope: str
    owner_id: str
    session_id: str | None
    kind: str
    content: dict[str, Any]
    source: str
    created_at: str
    updated_at: str
    expires_at: str | None
    deleted_at: str | None


class PersistentMemoryStore:
    """Small persistent memory reference store using Python's stdlib SQLite.

    This is intentionally not Organizational Knowledge or verified engineering
    evidence. Callers must fence/label memory when injecting it into model context.
    """

    def __init__(self, path: str | Path):
        self.path = str(path)
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_memory (
              memory_id TEXT PRIMARY KEY,
              scope TEXT NOT NULL,
              owner_id TEXT NOT NULL,
              session_id TEXT,
              kind TEXT NOT NULL,
              content_json TEXT NOT NULL,
              source TEXT NOT NULL,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              expires_at TEXT,
              deleted_at TEXT
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_agent_memory_lookup ON agent_memory(scope, owner_id, session_id, kind)"
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "PersistentMemoryStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def _validate_write(
        *, scope: str, kind: str, actor: str, session_id: str | None, content: dict[str, Any]
    ) -> None:
        if scope not in ALLOWED_SCOPES:
            raise ValueError("scope must be user or session")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"unsupported memory kind: {kind}")
        if actor not in {"user", "model", "trusted_runtime"}:
            raise ValueError("actor must be user, model, or trusted_runtime")
        if scope == "user" and actor == "model":
            raise PermissionError("model cannot directly persist user-scope memory")
        if scope == "session" and not session_id:
            raise ValueError("session memory requires session_id")
        if _contains_secret_like_key(content):
            raise ValueError("secret-like fields must not be stored in agent memory")

    def put(
        self,
        *,
        scope: str,
        owner_id: str,
        kind: str,
        content: dict[str, Any],
        source: str,
        actor: str,
        session_id: str | None = None,
        expires_at: str | None = None,
        memory_id: str | None = None,
    ) -> MemoryRecord:
        self._validate_write(
            scope=scope, kind=kind, actor=actor, session_id=session_id, content=content
        )
        memory_id = memory_id or f"memory-{uuid4().hex[:12]}"
        now = _utc_now()
        existing = self._conn.execute(
            "SELECT created_at FROM agent_memory WHERE memory_id = ?", (memory_id,)
        ).fetchone()
        created_at = existing["created_at"] if existing else now
        self._conn.execute(
            """
            INSERT INTO agent_memory(
              memory_id, scope, owner_id, session_id, kind, content_json, source,
              created_at, updated_at, expires_at, deleted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
            ON CONFLICT(memory_id) DO UPDATE SET
              scope=excluded.scope,
              owner_id=excluded.owner_id,
              session_id=excluded.session_id,
              kind=excluded.kind,
              content_json=excluded.content_json,
              source=excluded.source,
              updated_at=excluded.updated_at,
              expires_at=excluded.expires_at,
              deleted_at=NULL
            """,
            (
                memory_id,
                scope,
                owner_id,
                session_id,
                kind,
                json.dumps(content, sort_keys=True, ensure_ascii=False),
                source,
                created_at,
                now,
                expires_at,
            ),
        )
        self._conn.commit()
        result = self.get(memory_id)
        assert result is not None
        return result

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            memory_id=row["memory_id"],
            scope=row["scope"],
            owner_id=row["owner_id"],
            session_id=row["session_id"],
            kind=row["kind"],
            content=json.loads(row["content_json"]),
            source=row["source"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            expires_at=row["expires_at"],
            deleted_at=row["deleted_at"],
        )

    def get(self, memory_id: str, *, now: str | None = None) -> MemoryRecord | None:
        now = now or _utc_now()
        row = self._conn.execute(
            """
            SELECT * FROM agent_memory
            WHERE memory_id = ?
              AND deleted_at IS NULL
              AND (expires_at IS NULL OR expires_at > ?)
            """,
            (memory_id, now),
        ).fetchone()
        return self._row_to_record(row) if row else None

    def list(
        self,
        *,
        scope: str,
        owner_id: str,
        session_id: str | None = None,
        kind: str | None = None,
        now: str | None = None,
    ) -> tuple[MemoryRecord, ...]:
        if scope not in ALLOWED_SCOPES:
            raise ValueError("scope must be user or session")
        now = now or _utc_now()
        clauses = ["scope = ?", "owner_id = ?", "deleted_at IS NULL", "(expires_at IS NULL OR expires_at > ?)"]
        params: list[Any] = [scope, owner_id, now]
        if scope == "session":
            if not session_id:
                raise ValueError("session memory lookup requires session_id")
            clauses.append("session_id = ?")
            params.append(session_id)
        if kind:
            clauses.append("kind = ?")
            params.append(kind)
        rows = self._conn.execute(
            "SELECT * FROM agent_memory WHERE " + " AND ".join(clauses) + " ORDER BY updated_at DESC",
            params,
        ).fetchall()
        return tuple(self._row_to_record(row) for row in rows)

    def forget(self, memory_id: str, *, actor: str) -> bool:
        if actor not in {"user", "trusted_runtime"}:
            raise PermissionError("only user or trusted runtime can forget persistent memory")
        now = _utc_now()
        cursor = self._conn.execute(
            "UPDATE agent_memory SET deleted_at = ?, updated_at = ? WHERE memory_id = ? AND deleted_at IS NULL",
            (now, now, memory_id),
        )
        self._conn.commit()
        return cursor.rowcount > 0
