# Evidence Adapters

Evidence adapters connect provider-specific systems to the provider-neutral Engineering Evidence contract.

Examples include Kubernetes, AWS/Azure/GCP, Prometheus, Grafana, Datadog, CloudWatch, GitHub, CI/CD, cost, and security systems.

## Contract

An adapter should:

1. collect read-only by default;
2. preserve source provenance and observation time;
3. return provider-specific observations using `schemas/evidence-adapter-result.schema.json`;
4. normalize through a deterministic adapter boundary;
5. never mark its own result as a Loop `verified_fact`;
6. never infer production authorization from read access.

`adapters/evidence/base.py` normalizes an adapter result into the existing `evidence.schema.json` bundle while preserving provenance.

```text
Provider API
   ↓
Read-only Adapter
   ↓
Adapter Result
   ↓
Normalization
   ↓
Engineering Evidence
   ↓
Independent Verification / Loop
```

A provider result may be useful evidence while still being incomplete, stale, mis-scoped, or contradicted by another source. The Engineering control plane owns those decisions.
