# Live Kubernetes Evidence

The Infrastructure Engineering Agent can collect a bounded read-only evidence bundle from the Kubernetes cluster selected by `kubectl`.

This is an evidence adapter, not an authorization path and not an automatic production change mechanism.

## Command

```bash
./agent k8s-evidence \
  --namespace demo-app \
  --output /tmp/platform-lab-k8s-evidence.json
```

Windows:

```powershell
agent.cmd k8s-evidence --namespace demo-app --output k8s-evidence.json
```

Use `--context <name>` to avoid relying on the current kubectl context.

By default the command emits normalized Engineering Evidence. Use `--adapter-result` only when debugging the provider adapter boundary.

## What is collected

The adapter uses read-only `kubectl` operations to summarize:

- current context and Kubernetes version;
- node readiness and scheduling state;
- cluster Pod health and restart counts;
- target Namespace labels and policy state;
- Deployment status;
- HPA state;
- PDB state;
- NetworkPolicy inventory;
- ServiceAccount inventory;
- recent Warning events;
- Gateway API Gateway and HTTPRoute status when installed;
- Argo CD Application status when installed;
- node and Pod utilization when Metrics Server is available.

Unavailable optional APIs are recorded as `status: unavailable` observations instead of being promoted to facts.

## Evidence boundary

```text
kubectl read-only observation
        ↓
Kubernetes evidence adapter
        ↓
Engineering Evidence + provenance
        ↓
Infrastructure / SRE / Security review
        ↓
change proposal if required
        ↓
independent post-change verification
```

The adapter never marks its own observations as verified facts. This preserves the Harness invariant that tool output is evidence with provenance, while verified completion belongs to an independent verification step.

## Platform Engineering Lab workflow

From `infrastructure-engineering-harness`:

```bash
./agent k8s-evidence \
  --namespace demo-app \
  --output /tmp/platform-lab-k8s-evidence.json
```

Use the generated evidence bundle together with the desired state from `platform-engineering-lab` for:

1. architecture review;
2. SRE/reliability review;
3. security review;
4. observability gap analysis;
5. change prioritization;
6. post-change regression verification.

The next evidence adapter for this workflow should target Prometheus so Kubernetes runtime state and service-level metrics can be reviewed together.
