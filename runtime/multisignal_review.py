"""Deterministic enrichment-only correlation across Ops, Loki and Tempo evidence."""
from __future__ import annotations

import json
from typing import Any


def _unavailable(bundle: dict[str, Any]) -> list[str]:
    return [
        str(item.get("id"))
        for item in bundle.get("observations", [])
        if isinstance(item, dict) and item.get("status") == "unavailable"
    ]


def _log_trace_index(bundle: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    indexed: dict[str, dict[str, set[str]]] = {}
    for observation in bundle.get("observations", []):
        value = observation.get("value") if isinstance(observation, dict) else None
        if not isinstance(value, dict):
            continue
        for stream in value.get("result") or []:
            if not isinstance(stream, dict):
                continue
            labels = stream.get("stream") if isinstance(stream.get("stream"), dict) else {}
            for entry in stream.get("values") or []:
                if not isinstance(entry, list) or len(entry) < 2:
                    continue
                try:
                    payload = json.loads(entry[1])
                except (TypeError, json.JSONDecodeError):
                    continue
                trace_id = str(payload.get("trace_id") or "").strip()
                if not trace_id:
                    continue
                slot = indexed.setdefault(trace_id, {"services": set(), "events": set(), "levels": set()})
                service = str(payload.get("service") or labels.get("app") or "").strip()
                event = str(payload.get("event") or "").strip()
                level = str(payload.get("level") or "").strip()
                if service:
                    slot["services"].add(service)
                if event:
                    slot["events"].add(event)
                if level:
                    slot["levels"].add(level)
    return indexed


def _exact_trace_summary(observation: dict[str, Any], trace_id: str) -> dict[str, Any]:
    value = observation.get("value") if isinstance(observation.get("value"), dict) else {}
    trace = value.get("trace") if isinstance(value.get("trace"), dict) else {}
    batches = trace.get("batches") if isinstance(trace, dict) else None
    resource_spans = trace.get("resourceSpans") if isinstance(trace, dict) else None
    return {
        "traceID": trace_id,
        "lookup": "exact",
        "batchCount": len(batches) if isinstance(batches, list) else None,
        "resourceSpanCount": len(resource_spans) if isinstance(resource_spans, list) else None,
    }


def _tempo_trace_index(bundle: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    indexed: dict[str, list[dict[str, Any]]] = {}
    for observation in bundle.get("observations", []):
        if not isinstance(observation, dict):
            continue
        value = observation.get("value") if isinstance(observation.get("value"), dict) else None
        if not isinstance(value, dict):
            continue

        for trace in value.get("traces") or []:
            if not isinstance(trace, dict):
                continue
            trace_id = str(trace.get("traceID") or trace.get("traceId") or "").strip()
            if trace_id:
                indexed.setdefault(trace_id, []).append(trace)

        if observation.get("status") == "observed" and observation.get("signal") == "trace_by_id":
            provenance = observation.get("provenance") if isinstance(observation.get("provenance"), dict) else {}
            trace_id = str(value.get("trace_id") or provenance.get("trace_id") or "").strip()
            if trace_id:
                indexed.setdefault(trace_id, []).append(_exact_trace_summary(observation, trace_id))
    return indexed


def correlate_multisignal_evidence(
    ops_review: dict[str, Any],
    loki_bundle: dict[str, Any],
    tempo_bundle: dict[str, Any],
) -> dict[str, Any]:
    """Correlate log trace IDs with Tempo search/exact results without changing Ops decisions."""
    unavailable = sorted(set(_unavailable(loki_bundle) + _unavailable(tempo_bundle)))
    logs = _log_trace_index(loki_bundle)
    traces = _tempo_trace_index(tempo_bundle)
    matches = sorted(set(logs) & set(traces))

    correlations: list[dict[str, Any]] = []
    for trace_id in matches[:50]:
        log_data = logs[trace_id]
        correlations.append({
            "trace_id": trace_id,
            "log_services": sorted(log_data["services"]),
            "log_events": sorted(log_data["events"]),
            "log_levels": sorted(log_data["levels"]),
            "tempo_summaries": traces[trace_id][:10],
            "evidence_refs": ["loki", "tempo"],
        })

    if unavailable:
        status = "source_unavailable"
    elif correlations:
        status = "correlated"
    elif logs:
        status = "logs_without_matching_trace"
    else:
        status = "no_trace_ids"

    blocking = [
        finding.get("id")
        for finding in ops_review.get("findings", [])
        if finding.get("severity") in {"P0", "P1"}
    ]
    learning_candidates: list[dict[str, Any]] = []
    if unavailable:
        learning_candidates.append({
            "type": "evidence_gap",
            "refs": unavailable,
            "proposal": "repair the Loki/Tempo evidence path before promoting multi-signal correlation into blocking decisions",
        })
    elif blocking and not correlations:
        learning_candidates.append({
            "type": "correlation_gap",
            "refs": blocking,
            "proposal": "preserve the existing Ops decision and improve bounded log/trace correlation through an evaluation fixture",
        })

    return {
        "schema_version": "1.0",
        "review_type": "multi_signal_enrichment",
        "status": status,
        "decision_effect": "enrichment_only",
        "ops_state": ops_review.get("state"),
        "release_guidance": ops_review.get("release_guidance"),
        "blocking_findings": blocking,
        "correlation_count": len(correlations),
        "correlations": correlations,
        "source_unavailable": unavailable,
        "learning_candidates": learning_candidates,
    }
