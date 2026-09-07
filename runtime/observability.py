"""Provider-neutral trace/span observability for Infrastructure Engineering Agent runs."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


ALLOWED_SPAN_KINDS = {"agent", "model", "tool", "backend", "verification", "delegate"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AgentSpan:
    span_id: str
    trace_id: str
    name: str
    kind: str
    parent_span_id: str | None
    started_at: str
    ended_at: str | None = None
    duration_ms: int | None = None
    status: str = "running"
    attributes: dict[str, Any] = field(default_factory=dict)


class AgentTrace:
    """Small in-memory reference trace.

    It mirrors the hierarchy expected from an AIOps runtime without depending on
    AgentCore, OpenTelemetry, or a specific observability vendor. Provider adapters may
    export these spans later.
    """

    def __init__(self, *, trace_id: str | None = None) -> None:
        self.trace_id = trace_id or f"trace-{uuid4().hex[:16]}"
        self._spans: list[AgentSpan] = []

    @property
    def spans(self) -> tuple[AgentSpan, ...]:
        return tuple(self._spans)

    def start_span(
        self,
        name: str,
        *,
        kind: str,
        parent_span_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> AgentSpan:
        if kind not in ALLOWED_SPAN_KINDS:
            raise ValueError(f"unsupported span kind: {kind}")
        if parent_span_id is not None and not any(s.span_id == parent_span_id for s in self._spans):
            raise ValueError("parent span must belong to this trace")
        span = AgentSpan(
            span_id=f"span-{uuid4().hex[:16]}",
            trace_id=self.trace_id,
            name=name,
            kind=kind,
            parent_span_id=parent_span_id,
            started_at=_now(),
            attributes=dict(attributes or {}),
        )
        self._spans.append(span)
        return span

    def end_span(
        self,
        span: AgentSpan,
        *,
        duration_ms: int,
        status: str = "ok",
        attributes: dict[str, Any] | None = None,
    ) -> AgentSpan:
        if span not in self._spans:
            raise ValueError("span does not belong to this trace")
        if span.ended_at is not None:
            raise ValueError("span already ended")
        if duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")
        span.duration_ms = duration_ms
        span.ended_at = _now()
        span.status = status
        if attributes:
            span.attributes.update(attributes)
        return span

    def summary(self) -> dict[str, Any]:
        ended = [span for span in self._spans if span.duration_ms is not None]
        by_kind: dict[str, int] = {}
        duration_by_kind: dict[str, int] = {}
        for span in ended:
            by_kind[span.kind] = by_kind.get(span.kind, 0) + 1
            duration_by_kind[span.kind] = duration_by_kind.get(span.kind, 0) + int(span.duration_ms or 0)
        return {
            "trace_id": self.trace_id,
            "span_count": len(self._spans),
            "completed_span_count": len(ended),
            "count_by_kind": by_kind,
            "duration_ms_by_kind": duration_by_kind,
        }
