# Optional Live Evidence Adapters

Adapters connect the harness to current infrastructure state. They are **optional** and should be read-only by default.

The core does not require AWS, Datadog, Kubernetes, Prometheus, OpenTelemetry, or any other product.

## Adapter responsibility

An adapter should:

1. collect only the minimum evidence required for the task;
2. avoid mutation operations;
3. normalize observations to `schemas/evidence.schema.json`;
4. preserve provenance such as source, query/resource identifier, and observation time;
5. redact secrets and sensitive payloads;
6. declare limitations and freshness.

## Common adapter categories

- `cloud` — cloud control-plane/runtime state
- `metrics` — metrics systems
- `logs` — log systems
- `traces` — tracing/APM systems
- `deployment` — CI/CD and release history
- `source` — Git and configuration history
- `status` — provider/service health feeds

A Datadog adapter can implement metrics/logs/traces, but it is only one option. Prometheus, OpenTelemetry backends, cloud-native monitoring, or another observability platform can produce the same normalized evidence.

## Normalized output example

```json
{
  "schema_version": "1.0",
  "bundle_id": "EV-2026-0001",
  "observed_at": "2026-08-25T07:00:00Z",
  "observations": [
    {
      "id": "obs-1",
      "source_type": "metrics",
      "source": "primary-metrics",
      "component": "primary-datastore",
      "signal": "connection_utilization",
      "value": 96,
      "unit": "percent",
      "provenance": {"reference": "query-or-resource-id"}
    }
  ]
}
```

Do not make tool-specific response formats part of Skill logic. Normalize first, reason second.
