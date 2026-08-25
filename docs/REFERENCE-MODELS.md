# Reference Models

Infrastructure Engineering Harness combines mature infrastructure feedback models with emerging agent Loop Engineering rather than replacing established practice.

Loop Engineering is an **emerging agent engineering term**, not an infrastructure industry standard. The harness therefore uses it as an execution pattern while grounding safety and operations in established engineering models.

| Reference | Contribution |
| --- | --- |
| IBM Loop Engineering | Goal, action, observation and adjustment cycles with verifiable stopping criteria |
| LongHorizon-Harness | Explicit task state outside growing agent context; independently verified facts; manage/execute/audit separation |
| LoopsBench | Long-horizon dependency structure and completed work retained as regression obligations |
| Kubernetes Controllers | Desired-state vs actual-state control loops and reconciliation |
| OpenGitOps | Declarative/versioned desired state and continuous reconciliation |
| Google SRE | SLI/SLO, error budgets, reliability policy, escalation and learning |
| DORA | Service-level baseline, constraint improvement, progress validation and repetition |
| FinOps Framework | Iterative Inform → Optimize → Operate and measured technology value |
| MCP | Provider-neutral tool boundary for evidence and workflow actions |
| Independent authorization | Boundary for irreversible, destructive, financial, or production-impacting actions |

## IBM Loop Engineering

IBM describes loop engineering as designing agentic workflows that iteratively guide agents through goals, action, observation and adjustment. This harness adopts bounded loops but adds infrastructure-specific reconciliation, independent authorization and provenance.

https://www.ibm.com/think/topics/loop-engineering

## LongHorizon-Harness

LongHorizon-Harness frames long-running agent execution as task-state management. Its Manage-Execute-Audit model keeps task state explicit outside execution and updates it with independently verified environment facts. This motivates `loop-state`, external `verified_facts`, and one-iteration-at-a-time execution.

https://arxiv.org/abs/2608.01964

## LoopsBench

LoopsBench evaluates sustained agent loops using dependency DAGs and keeps completed units as regression obligations. The harness generalizes this beyond coding: recovered reliability, data integrity, security scope, delivery stability and cost traceability can remain obligations in later iterations.

https://arxiv.org/abs/2608.00267

## Kubernetes Controllers and OpenGitOps

Kubernetes controllers continually observe actual state and try to move it toward desired state. OpenGitOps adds declarative/versioned desired state and continuous reconciliation. The harness applies the same idea to engineering outcomes even when Terraform, Kubernetes or GitOps are not used.

https://kubernetes.io/docs/concepts/architecture/controller/
https://opengitops.dev/

## Google SRE

SRE provides the reliability control signals used by the SRE loops: SLI/SLO, error budget, incident response and error-budget policy.

https://sre.google/sre-book/service-level-objectives/
https://sre.google/workbook/error-budget-policy/

## DORA

DORA recommends application/service-level measurement, establishing a baseline, identifying the dominant constraint, making an improvement, checking progress and repeating. `delivery-improvement` follows this pattern and protects stability as a regression obligation.

https://dora.dev/guides/dora-metrics/

## FinOps Framework

FinOps is performed iteratively through Inform, Optimize and Operate. `finops-optimization` adds realized-value verification so expected savings are compared with actual cost/value and reliability outcomes.

https://www.finops.org/framework/
https://www.finops.org/framework/phases/

## Synthesis

```text
Desired Outcome
       ↓
Observe Actual State
       ↓
Resolve Organizational Context
       ↓
Domain Skill(s)
       ↓
Decision / Proposal
       ↓
Independent Action or Human Gate
       ↓
Independent Verification
       ↓
Regression Check
       ↓
Reconcile → continue or terminal
                       ↓
                      Learn
                       ↓
 Incident / Runbook / ADR or Policy candidate / Measurement / Eval
                       ↓
                    Next Loop
```

The model does not own truth, completion, or authorization. Environment evidence, deterministic checks, provider controls and human approvals remain independent parts of the loop.
