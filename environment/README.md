# Environment Discovery and Resource Binding

The environment layer turns live infrastructure discovery into a provider-neutral Resource Graph. It does not replace the Service Catalog, ADRs, Policies, or other durable organizational knowledge.

```text
Cloud / Kubernetes / CI/CD / Observability
                  ↓
          Read-only Discovery
                  ↓
            Resource Graph
                  ↓
       Context Resolution / Binding
                  ↓
          Bound Capability
                  ↓
       Evidence Collection / Review
```

## Resource Graph

`schemas/resource-graph.schema.json` models the discovered runtime environment as resources plus typed relationships. Every discovered resource carries provenance (`adapter`, `reference`, `observed_at`).

Discovery facts are ephemeral environment observations. They may enrich task context, but they do not silently rewrite durable knowledge.

## Bound Capability

A Bound Capability combines an existing trusted capability with:

- explicit resource ids;
- evidence sources;
- permission scope;
- execution authority inherited from the capability source;
- human-gate requirements.

Binding may only narrow authority. A third-party `reference_only` capability remains `execution_authority: none` even when bound to a real production resource.

`environment/binding.py` is a deterministic reference implementation.

## Evidence boundary

Resource discovery answers **what appears to exist and how resources relate**. Evidence adapters answer **what a current operational signal says**. Engineering Loops decide whether an observation has been independently verified strongly enough to update `verified_facts`.

```text
Discovery != verified engineering fact
Adapter result != verified engineering fact
Agent conclusion != verified engineering fact
```

Promotion to a Loop verified fact still requires environment/tool/human/test verification under the existing Evidence contract.
