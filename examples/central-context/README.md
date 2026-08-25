# Central Context Mode

Service repositories do not need to contain `AGENTS.md` or `.infra-context`.

A Platform/SRE/Infrastructure team can operate a separate workspace:

```text
infrastructure-harness-workspace/
├── AGENTS.md
├── contexts/
│   ├── payment-platform/
│   │   ├── service-catalog.yaml
│   │   ├── architecture/
│   │   ├── adr/
│   │   ├── incidents/
│   │   ├── policies/
│   │   ├── runbooks/
│   │   └── domains/
│   │       ├── sre.yaml
│   │       ├── devops.yaml
│   │       └── finops.yaml
│   └── shared-platform/
└── read-only sources
```

The source repository, deployment system, observability tools, runtime APIs and cost datasets can remain external read-only inputs. Normalize current observations to the evidence schema before using them as justification for a material decision.

Example request:

```text
Analyze payment-platform using contexts/payment-platform.
Use the SRE and FinOps packs because the proposed capacity reduction affects both cost and reliability.
Treat the service repository and monitoring/cost systems as read-only sources.
Do not execute a production change; produce evidence, trade-offs, verification and a change proposal if justified.
```
