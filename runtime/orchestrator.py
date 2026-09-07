"""Provider-neutral Agent Turn Runtime orchestration.

The orchestrator owns execution flow, not truth or authority. It converges every
channel-normalized TurnRequest onto one model/tool/verification loop while using the
Runtime Event Log as the canonical record of what the Agent saw and did.

This reference implementation is intentionally read-only. Production mutation must
remain behind the governed ToolPipeline / ChangeControl / backend boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Any, Protocol

from .channel import TurnRequest
from .kernel import RuntimeEventLog
from .observability import AgentTrace


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    execution_authority: str = "read"


@dataclass(frozen=True)
class ModelStep:
    text: str
    tool_calls: tuple[ToolCall, ...] = ()
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


@dataclass(frozen=True)
class ModelInput:
    request: TurnRequest
    turn_index: int
    context: dict[str, Any]
    surface: dict[str, Any]
    tool_results: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class VerificationDecision:
    verified: bool
    code: str
    evidence_refs: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TurnOutcome:
    run_id: str
    status: str
    final_text: str
    model_turns: int
    tool_calls: int
    verification: VerificationDecision | None
    event_log: RuntimeEventLog


class ContextResolver(Protocol):
    async def resolve(self, request: TurnRequest) -> dict[str, Any]: ...


class SurfaceResolver(Protocol):
    async def resolve(self, request: TurnRequest) -> dict[str, Any]: ...


class ModelAdapter(Protocol):
    async def complete(self, model_input: ModelInput) -> ModelStep: ...


class ReadOnlyToolExecutor(Protocol):
    async def execute(self, call: ToolCall) -> dict[str, Any]: ...


class OutcomeVerifier(Protocol):
    async def verify(
        self,
        *,
        request: TurnRequest,
        final_text: str,
        event_log: RuntimeEventLog,
    ) -> VerificationDecision: ...


class AgentOrchestrator:
    """Thin deterministic application runtime around one Infrastructure Agent.

    Responsibilities:
    - normalize one turn lifecycle around Context / Skills / Tools;
    - call the model and execute read-only tool requests;
    - keep the Runtime Event Log canonical;
    - emit trace spans correlated to the same event log;
    - require independent verification before returning `verified` completion.

    Non-responsibilities:
    - deciding engineering truth;
    - granting production authorization;
    - bypassing provenance/approval/change-control for writes.
    """

    def __init__(
        self,
        *,
        context_resolver: ContextResolver,
        surface_resolver: SurfaceResolver,
        model: ModelAdapter,
        tool_executor: ReadOnlyToolExecutor,
        verifier: OutcomeVerifier,
        max_model_turns: int = 8,
        max_tool_calls: int = 24,
    ) -> None:
        if max_model_turns < 1 or max_tool_calls < 0:
            raise ValueError("invalid orchestration budgets")
        self.context_resolver = context_resolver
        self.surface_resolver = surface_resolver
        self.model = model
        self.tool_executor = tool_executor
        self.verifier = verifier
        self.max_model_turns = max_model_turns
        self.max_tool_calls = max_tool_calls

    async def run(self, request: TurnRequest) -> TurnOutcome:
        log = RuntimeEventLog(run_id=request.request_id)
        trace = AgentTrace(trace_id=f"trace-{request.request_id}", event_log=log)
        root = trace.start_span("agent-turn", kind="agent", attributes={"channel": request.channel})
        log.append(
            "run/started",
            {
                "request_id": request.request_id,
                "channel": request.channel,
                "principal_id": request.principal_id,
                "session_id": request.session_id,
            },
        )

        context = await self.context_resolver.resolve(request)
        surface = await self.surface_resolver.resolve(request)
        log.append(
            "context/snapshot",
            {"context": context, "surface": surface, "user_text": request.text},
            model_visible=True,
        )

        tool_results: list[dict[str, Any]] = []
        tool_count = 0
        final_text = ""

        for turn_index in range(self.max_model_turns):
            model_span = trace.start_span("model-turn", kind="model", parent_span_id=root.span_id)
            started = monotonic()
            log.append(
                "model/request",
                {
                    "turn_index": turn_index,
                    "request_text": request.text,
                    "context": context,
                    "surface": surface,
                    "tool_results": tuple(tool_results),
                },
                model_visible=True,
            )
            step = await self.model.complete(
                ModelInput(
                    request=request,
                    turn_index=turn_index,
                    context=context,
                    surface=surface,
                    tool_results=tuple(tool_results),
                )
            )
            model_duration_ms = int((monotonic() - started) * 1000)
            trace.end_span(model_span, duration_ms=model_duration_ms)
            log.append(
                "model/response",
                {
                    "turn_index": turn_index,
                    "text": step.text,
                    "tool_calls": [
                        {
                            "name": call.name,
                            "arguments": call.arguments,
                            "execution_authority": call.execution_authority,
                        }
                        for call in step.tool_calls
                    ],
                    "duration_ms": model_duration_ms,
                    "input_tokens": step.input_tokens,
                    "output_tokens": step.output_tokens,
                    "cache_read_tokens": step.cache_read_tokens,
                    "cache_write_tokens": step.cache_write_tokens,
                },
                model_visible=True,
            )
            final_text = step.text

            if not step.tool_calls:
                verify_span = trace.start_span(
                    "independent-verification",
                    kind="verification",
                    parent_span_id=root.span_id,
                )
                verify_started = monotonic()
                verification = await self.verifier.verify(
                    request=request,
                    final_text=final_text,
                    event_log=log,
                )
                verify_duration_ms = int((monotonic() - verify_started) * 1000)
                trace.end_span(verify_span, duration_ms=verify_duration_ms)
                log.append(
                    "verification/result",
                    {
                        "verified": verification.verified,
                        "code": verification.code,
                        "details": verification.details,
                        "duration_ms": verify_duration_ms,
                    },
                    evidence_refs=list(verification.evidence_refs),
                )
                status = "verified" if verification.verified else "unverified"
                log.append("run/ended", {"status": status})
                trace.end_span(root, duration_ms=sum((s.duration_ms or 0) for s in trace.spans if s is not root))
                return TurnOutcome(
                    run_id=log.run_id,
                    status=status,
                    final_text=final_text,
                    model_turns=turn_index + 1,
                    tool_calls=tool_count,
                    verification=verification,
                    event_log=log,
                )

            for call in step.tool_calls:
                if tool_count >= self.max_tool_calls:
                    log.append("run/ended", {"status": "tool_budget_exceeded"})
                    trace.end_span(root, duration_ms=sum((s.duration_ms or 0) for s in trace.spans if s is not root))
                    return TurnOutcome(
                        run_id=log.run_id,
                        status="tool_budget_exceeded",
                        final_text=final_text,
                        model_turns=turn_index + 1,
                        tool_calls=tool_count,
                        verification=None,
                        event_log=log,
                    )
                if call.execution_authority not in {"none", "read"}:
                    raise PermissionError(
                        "reference orchestrator is read-only; governed workflow/change execution "
                        "must use ToolPipeline/ChangeControl and an authorized backend"
                    )
                tool_span = trace.start_span(call.name, kind="tool", parent_span_id=root.span_id)
                tool_started = monotonic()
                log.append(
                    "tool/requested",
                    {
                        "tool_name": call.name,
                        "arguments": call.arguments,
                        "execution_authority": call.execution_authority,
                    },
                    model_visible=True,
                )
                value = await self.tool_executor.execute(call)
                tool_duration_ms = int((monotonic() - tool_started) * 1000)
                trace.end_span(tool_span, duration_ms=tool_duration_ms)
                normalized = {
                    "tool_name": call.name,
                    "ok": bool(value.get("ok", True)),
                    "value": value,
                    "duration_ms": tool_duration_ms,
                }
                log.append("tool/result", normalized, model_visible=True)
                tool_results.append(normalized)
                tool_count += 1

        log.append("run/ended", {"status": "model_turn_budget_exceeded"})
        trace.end_span(root, duration_ms=sum((s.duration_ms or 0) for s in trace.spans if s is not root))
        return TurnOutcome(
            run_id=log.run_id,
            status="model_turn_budget_exceeded",
            final_text=final_text,
            model_turns=self.max_model_turns,
            tool_calls=tool_count,
            verification=None,
            event_log=log,
        )
