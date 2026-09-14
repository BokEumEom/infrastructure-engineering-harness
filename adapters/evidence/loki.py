"""Read-only Loki evidence adapter for Infrastructure Engineering Agent."""
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
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"
    if data.get("status") != "success":
        return None, str(data.get("error") or data.get("errorType") or "Loki API request failed")
    return data, None


def collect_loki_evidence(
    *,
    base_url: str,
    queries: dict[str, dict[str, Any]],
    lookback_seconds: int = 900,
    scope: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Collect bounded Loki query-range observations without mutating state."""
    if lookback_seconds <= 0:
        raise ValueError("lookback_seconds must be positive")

    observed = _now()
    start = observed - timedelta(seconds=lookback_seconds)
    base = base_url.rstrip("/")
    observations: list[dict[str, Any]] = []

    for qid, spec in queries.items():
        query = str(spec.get("query") or "").strip()
        if not query:
            raise ValueError(f"query {qid!r} must define a non-empty 'query'")
        limit = max(1, min(int(spec.get("limit", 50)), 500))
        params = urlencode({
            "query": query,
            "start": str(int(start.timestamp() * 1_000_000_000)),
            "end": str(int(observed.timestamp() * 1_000_000_000)),
            "limit": str(limit),
            "direction": "backward",
        })
        url = f"{base}/loki/api/v1/query_range?{params}"
        data, error = _get_json(url, headers=headers)
        provenance: dict[str, Any] = {
            "reference": f"{base}/loki/api/v1/query_range",
            "query": query,
            "lookback_seconds": lookback_seconds,
        }
        if headers and headers.get("Host"):
            provenance["host_header"] = headers["Host"]
        if error:
            observations.append({
                "id": f"loki.{qid}",
                "source_type": "logs",
                "source": "loki",
                "component": spec.get("component", "unknown"),
                "signal": spec.get("signal", qid),
                "value": {"error": error},
                "status": "unavailable",
                "provenance": provenance,
            })
            continue

        result = (data or {}).get("data", {})
        streams = result.get("result", []) if isinstance(result, dict) else []
        entry_count = 0
        trace_ids: set[str] = set()
        for stream in streams if isinstance(streams, list) else []:
            for value in stream.get("values") or []:
                entry_count += 1
                if not isinstance(value, list) or len(value) < 2:
                    continue
                try:
                    parsed = json.loads(value[1])
                except (TypeError, json.JSONDecodeError):
                    continue
                trace_id = str(parsed.get("trace_id") or "")
                if trace_id:
                    trace_ids.add(trace_id)

        observations.append({
            "id": f"loki.{qid}",
            "source_type": "logs",
            "source": "loki",
            "component": spec.get("component", "unknown"),
            "signal": spec.get("signal", qid),
            "value": {
                "resultType": result.get("resultType") if isinstance(result, dict) else None,
                "result": streams,
                "stream_count": len(streams) if isinstance(streams, list) else 0,
                "entry_count": entry_count,
                "trace_ids": sorted(trace_ids)[:50],
            },
            "status": "observed",
            "provenance": provenance,
        })

    return {
        "schema_version": "1.0",
        "adapter_id": "loki-http-api",
        "observed_at": observed.isoformat(),
        "collection_mode": "read_only",
        "scope": {"base_url": base, "lookback_seconds": lookback_seconds, **(scope or {})},
        "observations": observations,
    }
