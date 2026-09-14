"""Read-only Tempo evidence adapter for Infrastructure Engineering Agent."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_json(
    url: str,
    *,
    timeout: int = 10,
    headers: dict[str, str] | None = None,
) -> tuple[dict[str, Any] | None, str | None]:
    request_headers = {
        "Accept": "application/json",
        "User-Agent": "infrastructure-engineering-agent/1",
    }
    if headers:
        request_headers.update(headers)
    request = Request(url, headers=request_headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return None, str(exc)
    try:
        return json.loads(payload), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _requested_trace_ids(
    trace_id: str | None,
    trace_ids: list[str] | None,
) -> list[str]:
    ordered: list[str] = []
    for raw in ([trace_id] if trace_id else []) + list(trace_ids or []):
        value = str(raw or "").strip()
        if value and value not in ordered:
            ordered.append(value)
    return ordered


def collect_tempo_evidence(
    *,
    base_url: str,
    searches: dict[str, dict[str, Any]],
    lookback_seconds: int = 900,
    trace_id: str | None = None,
    trace_ids: list[str] | None = None,
    scope: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Collect bounded Tempo search results and optional exact trace lookups."""
    if lookback_seconds <= 0:
        raise ValueError("lookback_seconds must be positive")

    observed = _now()
    start = observed - timedelta(seconds=lookback_seconds)
    base = base_url.rstrip("/")
    observations: list[dict[str, Any]] = []

    for sid, spec in searches.items():
        limit = max(1, min(int(spec.get("limit", 20)), 100))
        params: dict[str, str] = {
            "start": str(int(start.timestamp())),
            "end": str(int(observed.timestamp())),
            "limit": str(limit),
        }
        tags = str(spec.get("tags") or "").strip()
        if tags:
            params["tags"] = tags
        url = f"{base}/api/search?{urlencode(params)}"
        data, error = _get_json(url, headers=headers)
        provenance: dict[str, Any] = {
            "reference": f"{base}/api/search",
            "lookback_seconds": lookback_seconds,
        }
        if tags:
            provenance["tags"] = tags
        if headers and headers.get("Host"):
            provenance["host_header"] = headers["Host"]
        if error:
            observations.append({
                "id": f"tempo.{sid}",
                "source_type": "traces",
                "source": "tempo",
                "component": spec.get("component", "unknown"),
                "signal": spec.get("signal", sid),
                "value": {"error": error},
                "status": "unavailable",
                "provenance": provenance,
            })
            continue

        traces = (data or {}).get("traces", [])
        observations.append({
            "id": f"tempo.{sid}",
            "source_type": "traces",
            "source": "tempo",
            "component": spec.get("component", "unknown"),
            "signal": spec.get("signal", sid),
            "value": {
                "traces": traces,
                "trace_count": len(traces) if isinstance(traces, list) else 0,
                "metrics": (data or {}).get("metrics", {}),
            },
            "status": "observed",
            "provenance": provenance,
        })

    requested = _requested_trace_ids(trace_id, trace_ids)
    for index, tid in enumerate(requested, start=1):
        url = f"{base}/api/traces/{tid}"
        data, error = _get_json(url, headers=headers)
        provenance: dict[str, Any] = {
            "reference": f"{base}/api/traces/{tid}",
            "trace_id": tid,
            "lookup": "exact",
        }
        if headers and headers.get("Host"):
            provenance["host_header"] = headers["Host"]
        status = "observed"
        if error is not None:
            status = "not_found" if "404" in error else "unavailable"
        observations.append({
            "id": "tempo.trace" if len(requested) == 1 else f"tempo.trace.{index}",
            "source_type": "traces",
            "source": "tempo",
            "component": "trace",
            "signal": "trace_by_id",
            "value": {"trace_id": tid, "trace": data} if error is None else {"trace_id": tid, "error": error},
            "status": status,
            "provenance": provenance,
        })

    return {
        "schema_version": "1.0",
        "adapter_id": "tempo-http-api",
        "observed_at": observed.isoformat(),
        "collection_mode": "read_only",
        "scope": {"base_url": base, "lookback_seconds": lookback_seconds, **(scope or {})},
        "observations": observations,
    }
