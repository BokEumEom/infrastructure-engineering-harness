# Dependency latency runbook

Use when a service's request latency increases and one or more critical dependencies may be degraded.

## Verify

1. Confirm user-visible latency/error impact and start time.
2. Check whether request-serving compute is saturated.
3. Compare dependency latency, utilization, saturation, and error signals.
4. Check recent deployment and configuration changes.
5. Compare with relevant incident history.
6. Verify whether the issue is isolated to one dependency or shared across the network path.

## Do not

- scale a healthy service tier solely because end-to-end latency is high
- recommend a production change without evidence identifying the bottleneck
- assume the monitoring product or cloud platform

## Output

Return ranked hypotheses, supporting/contradicting evidence, the minimum verification steps, and only then a reversible remediation proposal.
