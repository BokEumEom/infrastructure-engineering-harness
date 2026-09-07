"""Channel-neutral ingress contract for the Infrastructure Engineering Agent."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


ALLOWED_CHANNELS = {"cli", "web", "slack", "github", "mcp", "api", "test"}


@dataclass(frozen=True)
class TurnRequest:
    request_id: str
    channel: str
    principal_id: str
    session_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_turn_request(
    *,
    channel: str,
    principal_id: str,
    session_id: str,
    text: str,
    metadata: dict[str, Any] | None = None,
) -> TurnRequest:
    """Normalize every product surface into the same Agent Turn Runtime input.

    Authentication and authorization happen before this function. Channel metadata may
    describe the transport, but it must never expand model/tool authority.
    """
    if channel not in ALLOWED_CHANNELS:
        raise ValueError(f"unsupported channel: {channel}")
    if not principal_id or not session_id or not text.strip():
        raise ValueError("principal_id, session_id and non-empty text are required")
    return TurnRequest(
        request_id=f"request-{uuid4().hex[:16]}",
        channel=channel,
        principal_id=principal_id,
        session_id=session_id,
        text=text,
        metadata=dict(metadata or {}),
    )
