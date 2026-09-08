"""Prometheus read-only evidence adapter."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from typing import Any, Callable, Dict, Iterable, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import urlopen


@dataclass(frozen=True)
class PrometheusQuery:
    name: str
    query: str
    component: str
    signal: str
    unit: Optional[str] = None


Transport = Callable[[str], Dict[str, Any]]


class PrometheusEvidenceAdapter:
    """Collect selected Prometheus instant queries as unverified observations."""

    def __init__(self, base_url: str, *, transport: Optional[Transport] = None, adapter_id: str = "prometheus-readonly") -> None:
        self.base_url = base_url.rstrip("/")
        self.transport = transport or self._http_query
        self.adapter_id = adapter_id

    def collect(self, queries: Iterable[PrometheusQuery], *, observed_at: str, scope: Dict[str, Any]) -> Dict[str, Any]:
        observations: list[dict[str, Any]] = []
        latest_sample_at: Optional[datetime] = None

        for query in queries:
            response = self.transport(query.query)
            for index, sample in enumerate(_samples(response)):
                sample_at, value, metric = sample
                if latest_sample_at is None or sample_at > latest_sample_at:
                    latest_sample_at = sample_at
                resource = _resource_for(metric, query.component)
                observation = {
                    "id": f"prometheus:{query.name}:{index}",
                    "source_type": "metrics",
                    "source": "prometheus",
                    "component": query.component,
                    "signal": query.signal,
                    "value": _parse_value(value),
                    "observed_at": _format_dt(sample_at),
                    "provenance": {
                        "reference": f"prometheus:{query.name}:{resource}",
                        "query": query.query,
                        "resource": resource,
                    },
                }
                if query.unit:
                    observation["unit"] = query.unit
                observations.append(observation)

        if not observations:
            raise ValueError("Prometheus query set returned no observations")

        result = {
            "schema_version": "1.0",
            "adapter_id": self.adapter_id,
            "observed_at": observed_at,
            "collection_mode": "read_only",
            "scope": scope,
            "observations": observations,
        }
        observed_dt = _parse_dt(observed_at)
        if latest_sample_at is not None:
            result["freshness_seconds"] = max(0, int((observed_dt - latest_sample_at).total_seconds()))
        return result

    def _http_query(self, query: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v1/query?{urlencode({'query': query})}"
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))


def _samples(response: Dict[str, Any]) -> Iterable[Tuple[datetime, Any, Dict[str, Any]]]:
    if response.get("status") != "success":
        raise ValueError("Prometheus query did not succeed")

    data = response.get("data") or {}
    result_type = data.get("resultType")
    result = data.get("result")
    if result_type == "scalar":
        yield _sample_value(result, {})
        return
    if result_type == "vector":
        for series in result or []:
            yield _sample_value(series.get("value"), series.get("metric") or {})
        return
    raise ValueError(f"unsupported Prometheus result type: {result_type}")


def _sample_value(value: Any, metric: Dict[str, Any]) -> Tuple[datetime, Any, Dict[str, Any]]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("Prometheus sample must contain [timestamp, value]")
    return datetime.fromtimestamp(float(value[0]), timezone.utc), value[1], metric


def _parse_value(value: Any) -> Any:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return value
    return int(parsed) if parsed.is_integer() else parsed


def _parse_dt(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _format_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resource_for(metric: Dict[str, Any], fallback: str) -> str:
    for key in ("resource", "service", "job", "instance"):
        if metric.get(key):
            return str(metric[key])
    return fallback
