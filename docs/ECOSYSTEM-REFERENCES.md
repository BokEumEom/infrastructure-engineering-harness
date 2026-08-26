# Infrastructure Agent Ecosystem References

This project treats adjacent open-source projects as reference implementations for specific layers rather than as competitors or mandatory dependencies.

| Project | Reference area | Harness use |
| --- | --- | --- |
| RunWhen Local | environment discovery and environment-specific operational knowledge | Resource Graph, Resource-bound Capability design |
| OpenSRE | realistic infrastructure/SRE scenarios and RCA evaluation | scenario fixtures, required evidence, red herrings, prohibited actions |
| HolmesGPT | production investigation across observability/cloud/Kubernetes data sources | Evidence Adapter breadth and investigation patterns |
| DeepSeek Harness | durable agent runtime, Skill discovery, guarded tool execution, approval/sandbox | Runtime Kernel |
| Atmos | infrastructure execution runtime across IaC/Kubernetes/Helm workflows | future authorized Execution Backend reference |

## RunWhen Local

Reference: https://github.com/runwhen-contrib/runwhen-local

The useful pattern is to discover live resources first, then specialize operational knowledge to the actual environment. This harness implements that idea as a provider-neutral Resource Graph plus Bound Capability rather than generating a new permanent Skill for every resource.

## OpenSRE

Reference: https://github.com/tracer-cloud/opensre

The useful pattern is scenario realism: known ground truth, evidence that must be discovered, misleading but plausible signals, and actions the agent must not take. `evals/scenarios/` adopts this structure while remaining compatible with the existing Domain Eval, Skill Lift, Context Lift and Loop Eval layers.

## HolmesGPT

Reference: https://github.com/HolmesGPT/holmesgpt

The useful pattern is broad connection to real operational data. This harness keeps the provider integrations behind `adapters/evidence/` so vendor-specific results are normalized with provenance before entering engineering reasoning.

## DeepSeek Harness

Reference: https://github.com/deepseek-ai/deepseek-harness

DeepSeek Harness remains the primary Runtime Kernel reference: append-only event history, replayability, scoped Skill discovery, guarded tool execution, approval and sandbox mechanics. Infrastructure-specific Evidence, authorization and Engineering Loop semantics remain hard invariants in this project.

## Atmos

Reference: https://github.com/cloudposse/atmos

Atmos is relevant to the future execution plane. The Harness should decide what is safe and justified to execute, under which approval and verification contract; an execution backend may own the provider-specific mechanics.

## Adoption rule

Reference projects may influence contracts or adapters, but they do not receive implicit trust or production authority. External implementation code or Skills remain subject to source pinning, local review, policy, authorization, Eval and independent verification.
