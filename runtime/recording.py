"""Runtime recording and deterministic integrity replay."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any
from uuid import uuid4

from .kernel import RuntimeEventLog


def _digest_payload(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ReplayCheck:
    valid: bool
    code: str


def build_recording(
    event_log: RuntimeEventLog,
    *,
    source: str,
    runtime_revision: str,
    agent: str,
    model: str,
    final_status: str,
) -> dict[str, Any]:
    if source not in {"fixture", "live"}:
        raise ValueError("source must be fixture or live")
    events = [
        {
            "run_id": event.run_id,
            "seq": event.seq,
            "type": event.type,
            "data": event.data,
            "timestamp": event.timestamp,
            "model_visible": event.model_visible,
            "ignorable": event.ignorable,
        }
        for event in event_log.events
    ]
    payload = {
        "schema_version": "1.0",
        "recording_id": f"recording-{uuid4().hex[:12]}",
        "source": source,
        "runtime_revision": runtime_revision,
        "agent": agent,
        "model": model,
        "run_id": event_log.run_id,
        "final_status": final_status,
        "events": events,
    }
    return {**payload, "sha256": _digest_payload(payload)}


def verify_recording(recording: dict[str, Any]) -> ReplayCheck:
    digest = recording.get("sha256")
    payload = {key: value for key, value in recording.items() if key != "sha256"}
    if not isinstance(digest, str) or _digest_payload(payload) != digest:
        return ReplayCheck(False, "RECORDING_DIGEST_MISMATCH")

    events = recording.get("events", [])
    for expected, event in enumerate(events):
        if event.get("seq") != expected:
            return ReplayCheck(False, "RECORDING_SEQUENCE_INVALID")
        if event.get("run_id") != recording.get("run_id"):
            return ReplayCheck(False, "RECORDING_RUN_ID_MISMATCH")
    return ReplayCheck(True, "RECORDING_REPLAY_OK")
