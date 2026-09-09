# Live Ops Review and Revalidation

The Infrastructure Engineering Agent can turn live Kubernetes and Prometheus evidence into a bounded operational assessment without mutating the target environment.

This workflow is intentionally evidence-first:

```text
Kubernetes read-only evidence ──┐
                                ├─> ops-review
Prometheus read-only evidence ──┘      │
                                       v
                          findings + evidence refs
                                       │
                           human/GitOps remediation
                                       │
                 new Kubernetes + Prometheus evidence
                                       │
                                ops-review
                                       │
                                ops-compare
                                       │
                 resolved / persistent / regression
```

## Review command

```bash
./agent ops-review \
  --k8s /tmp/platform-lab-k8s-evidence.json \
  --prometheus /tmp/platform-lab-prometheus-evidence.json \
  --output /tmp/platform-lab-ops-review.json
```

The review emits:

```json
{
  "state": "healthy | at_risk | acute | insufficient_evidence",
  "release_guidance": "continue | hold | insufficient_evidence",
  "findings": [],
  "learning_candidates": []
}
```

Every finding contains an ID, severity, observation, impact, evidence references, recommendation and explicit verification obligations.

The first deterministic review rules cover operational evidence such as:

- Kubernetes node readiness;
- unhealthy Pods and Deployment availability;
- Argo CD reconciliation state;
- Kubernetes Warning events;
- platform-api and dependency Prometheus target health;
- Envoy liveness;
- request error ratio and SLO burn rate;
- P95 latency;
- container restarts / OOMKilled state;
- HPA saturation;
- OpenTelemetry Collector failed/refused spans.

A rule is not proof that remediation succeeded. It is an evidence-backed assessment that must be closed by new observations.

## Revalidation

After a reviewed GitOps change, collect fresh evidence and create another review.

```bash
./agent ops-compare \
  --before /tmp/before-review.json \
  --after /tmp/after-review.json \
  --output /tmp/revalidation.json
```

The comparison records:

- `resolved`: findings present before and absent after;
- `persistent`: findings present in both reviews;
- `new`: findings that appeared after the change;
- `regressed`: true if the state worsened or a new finding appeared;
- `verified_recovery`: true only when previous findings are resolved, no new/persistent findings remain and the final review is healthy.

This prevents an Agent from declaring success merely because it executed a change.

## Self-improvement boundary

The Agent does **not** silently rewrite `AGENTS.md`, Skills, thresholds or production policy based on one incident.

Instead the runtime emits explicit `learning_candidates`.

Examples:

```text
evidence_gap
  -> an adapter/query was missing or unavailable

persistent_finding
  -> the remediation hypothesis or runbook may be weak

regression
  -> the change created a new operational problem

review_feedback
  -> repeated findings may indicate missing context/capability coverage
```

These candidates should be reviewed through the Harness context-backpass / evaluation process before changing Agent context or Skills.

```text
runtime failure pattern
      ↓
learning candidate
      ↓
reproducible scenario / evidence fixture
      ↓
Skill or context proposal
      ↓
human review
      ↓
eval / regression suite
      ↓
merge only if Agent behavior improves without regressions
```

This is the intended form of self-improvement: measured and reviewable, not autonomous prompt mutation.

## Production-adoption boundary

`ops-review` is suitable as a read-only diagnosis/review layer, not an autonomous production operator by itself.

Before production mutation is enabled, require at least:

1. environment-specific least-privilege credentials and binding;
2. change-review / human gates for production-impacting actions;
3. audited action adapters with rollback/recovery contracts;
4. incident evaluation fixtures measuring false positives and false negatives;
5. durable observability and independent alert delivery;
6. post-change revalidation using independent evidence;
7. Skill/context changes gated by evaluation rather than self-editing.

The default safety posture remains read-only evidence collection plus reviewed recommendations.
