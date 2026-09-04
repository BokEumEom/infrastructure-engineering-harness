"""Provider-neutral context assembly, prompt-cache layout, and latency accounting.

The runtime keeps stable context prefixes deterministic so model-provider prompt
caching can be used when available, without making caching a provider dependency.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from typing import Iterable


TIERS = ("global", "session", "volatile")


@dataclass(frozen=True)
class ContextSection:
    name: str
    content: str
    tier: str

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"tier must be one of {TIERS}")


@dataclass(frozen=True)
class PromptAssembly:
    sections: tuple[ContextSection, ...]
    stable_prefix: str
    volatile_suffix: str
    stable_prefix_sha256: str
    estimated_total_tokens: int
    estimated_cacheable_tokens: int
    estimated_volatile_tokens: int


@dataclass(frozen=True)
class LatencyBudget:
    max_model_turns: int | None = None
    max_tool_calls: int | None = None
    max_accounted_ms: int | None = None


@dataclass
class LatencyTracker:
    model_turns: int = 0
    tool_calls: int = 0
    model_ms: int = 0
    tool_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    _events: list[dict[str, int]] = field(default_factory=list)

    def record_model_turn(
        self,
        *,
        duration_ms: int,
        input_tokens: int,
        output_tokens: int,
        cache_read_tokens: int = 0,
        cache_write_tokens: int = 0,
    ) -> None:
        values = (duration_ms, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens)
        if any(value < 0 for value in values):
            raise ValueError("latency/token metrics must be non-negative")
        self.model_turns += 1
        self.model_ms += duration_ms
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.cache_read_tokens += cache_read_tokens
        self.cache_write_tokens += cache_write_tokens
        self._events.append({"kind": 1, "duration_ms": duration_ms})

    def record_tool_batch(self, *, duration_ms: int, tool_calls: int) -> None:
        if duration_ms < 0 or tool_calls < 0:
            raise ValueError("latency/tool metrics must be non-negative")
        self.tool_ms += duration_ms
        self.tool_calls += tool_calls
        self._events.append({"kind": 2, "duration_ms": duration_ms})

    def summary(self) -> dict[str, float | int]:
        denominator = self.input_tokens or 1
        return {
            "model_turns": self.model_turns,
            "tool_calls": self.tool_calls,
            "model_ms": self.model_ms,
            "tool_ms": self.tool_ms,
            "accounted_ms": self.model_ms + self.tool_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "cache_read_ratio": round(self.cache_read_tokens / denominator, 6),
        }

    def budget_failures(self, budget: LatencyBudget) -> tuple[str, ...]:
        failures: list[str] = []
        if budget.max_model_turns is not None and self.model_turns > budget.max_model_turns:
            failures.append("MODEL_TURN_BUDGET_EXCEEDED")
        if budget.max_tool_calls is not None and self.tool_calls > budget.max_tool_calls:
            failures.append("TOOL_CALL_BUDGET_EXCEEDED")
        accounted_ms = self.model_ms + self.tool_ms
        if budget.max_accounted_ms is not None and accounted_ms > budget.max_accounted_ms:
            failures.append("LATENCY_BUDGET_EXCEEDED")
        return tuple(failures)


def _estimate_tokens(text: str) -> int:
    # Provider-neutral approximation for budgeting only. Never use this as billing truth.
    return (len(text) + 3) // 4


def _render(sections: Iterable[ContextSection]) -> str:
    return "\n\n".join(f"## {section.name}\n{section.content}" for section in sections)


def assemble_prompt_context(sections: Iterable[ContextSection]) -> PromptAssembly:
    """Order stable material first and volatile material last.

    The stable prefix consists of global + session sections. The volatile suffix
    contains per-turn evidence/user state. Callers should avoid inserting volatile
    content into the stable prefix because that destroys provider cache reuse.
    """
    materialized = tuple(sections)
    ordered = tuple(sorted(materialized, key=lambda item: TIERS.index(item.tier)))
    stable = tuple(section for section in ordered if section.tier in {"global", "session"})
    volatile = tuple(section for section in ordered if section.tier == "volatile")
    stable_prefix = _render(stable)
    volatile_suffix = _render(volatile)
    total = "\n\n".join(part for part in (stable_prefix, volatile_suffix) if part)
    return PromptAssembly(
        sections=ordered,
        stable_prefix=stable_prefix,
        volatile_suffix=volatile_suffix,
        stable_prefix_sha256=hashlib.sha256(stable_prefix.encode("utf-8")).hexdigest(),
        estimated_total_tokens=_estimate_tokens(total),
        estimated_cacheable_tokens=_estimate_tokens(stable_prefix),
        estimated_volatile_tokens=_estimate_tokens(volatile_suffix),
    )
