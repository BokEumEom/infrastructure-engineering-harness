# Live Prometheus Evidence

The Infrastructure Engineering Agent can collect read-only Prometheus instant-query evidence through the HTTP API.

The adapter is intentionally generic: environment-specific PromQL lives in a JSON query profile outside the Harness.

## Command

```bash
./agent prometheus-evidence \
  --url http://127.0.0.1:9090 \
  --query-file ../platform-engineering-lab/observability/agent-prometheus-queries.json \
  --namespace demo-app \
  --service platform-api \
  --output /tmp/platform-lab-prometheus-evidence.json
```

The Prometheus endpoint may be a local port-forward, a read-only internal endpoint, or another explicitly scoped URL.

## Query profile

The JSON file maps evidence IDs to PromQL and metadata:

```json
{
  "service_up": {
    "component": "example-service",
    "signal": "target_up",
    "query": "min(up{namespace=\"example\"})"
  }
}
```

Provider-specific query details remain in the target environment repository so the Harness does not silently assume metric names, labels, SLOs, or thresholds.

## Evidence boundary

The adapter performs only Prometheus HTTP GET requests against status and instant-query endpoints.

```text
Prometheus HTTP API
        ↓
read-only adapter
        ↓
query result + exact PromQL provenance
        ↓
Engineering Evidence
        ↓
SRE / Infrastructure review
```

A missing series, failed query, or unreachable endpoint is represented as unavailable evidence. It is not converted into an application-health fact.

## Combined Kubernetes review

For a live Kubernetes environment, collect both bundles:

```bash
./agent k8s-evidence \
  --namespace demo-app \
  --output /tmp/k8s-evidence.json

./agent prometheus-evidence \
  --url http://127.0.0.1:9090 \
  --query-file /path/to/queries.json \
  --namespace demo-app \
  --service platform-api \
  --output /tmp/prometheus-evidence.json
```

The review can then compare runtime state and service telemetry without promoting repository configuration or Agent output to verified operational truth.
