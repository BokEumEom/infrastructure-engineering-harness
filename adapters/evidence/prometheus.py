"""Read-only Prometheus evidence adapter for Infrastructure Engineering Agent."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        return None, str(data.get("error") or data.get("errorType") or "Prometheus API request failed")
    return data, None


def collect_prometheus_evidence(
    *,
    base_url: str,
    queries: dict[str, dict[str, str]],
    scope: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Collect instant-query observations from a Prometheus HTTP API."""
    observed_at = _now()
    base = base_url.rstrip("/")
    observations: list[dict[str, Any]] = []

    runtime_url = f"{base}/api/v1/status/runtimeinfo"
    runtime, runtime_error = _get_json(runtime_url, headers=headers)
    if runtime_error:
        observations.append({
            "id": "prometheus.runtime",
            "source_type": "status",
            "source": "prometheus",
            "component": "prometheus",
            "signal": "runtime_info",
            "value": {"error": runtime_error},
            "status": "unavailable",
            "provenance": {"reference": runtime_url},
        })
    else:
        observations.append({
            "id": "prometheus.runtime",
            "source_type": "status",
            "source": "prometheus",
            "component": "prometheus",
            "signal": "runtime_info",
            "value": (runtime or {}).get("data", {}),
            "status": "available",
            "provenance": {"reference": runtime_url},
        })

    for qid, spec in queries.items():
        query = spec.get("query", "").strip()
        if not query:
            raise ValueError(f"query {qid!r} must define a non-empty 'query'")
        params = urlencode({"query": query})
        url = f"{base}/api/v1/query?{params}"
        data, error = _get_json(url, headers=headers)
        provenance = {"reference": f"{base}/api/v1/query", "query": query}
        if headers and headers.get("Host"):
            provenance["host_header"] = headers["Host"]
        if error:
            observations.append({
                "id": f"prometheus.{qid}",
                "source_type": "metrics",
                "source": "prometheus",
                "component": spec.get("component", "unknown"),
                "signal": spec.get("signal", qid),
                "value": {"error": error},
                "status": "unavailable",
                "provenance": provenance,
            })
            continue

        result = (data or {}).get("data", {})
        observations.append({
            "id": f"prometheus.{qid}",
            "source_type": "metrics",
            "source": "prometheus",
            "component": spec.get("component", "unknown"),
            "signal": spec.get("signal", qid),
            "value": {
                "resultType": result.get("resultType"),
                "result": result.get("result", []),
            },
            "status": "observed",
            "provenance": provenance,
        })

    return {
        "schema_version": "1.0",
        "adapter_id": "prometheus-http-api",
        "observed_at": observed_at,
        "collection_mode": "read_only",
        "scope": {"base_url": base, **(scope or {})},
        "observations": observations,
    }
