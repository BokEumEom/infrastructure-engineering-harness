# Infrastructure Engineering Agent

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Infrastructure / Operations / DevOps / SRE / FinOps / Security 업무를 조사·검토·계획·검증하는 provider-neutral **Infrastructure Engineering Agent**입니다.

> **에이전트의 판단은 열어두고, 실행 흐름은 Orchestrator가 조율하며, 권한과 사실의 경계는 Harness / Control Plane이 통제합니다.**

> **상태: Research Preview.** Agent contract, reference Turn Runtime, Skills, Resource Graph, deterministic scenario, evaluation plumbing, local CLI는 사용할 수 있습니다. Live adapter, persistent production runtime, controlled execution은 experimental 단계입니다.

Repository 이름 `infrastructure-engineering-harness`는 기존 링크와 호환성을 위해 유지합니다. **제품은 Infrastructure Engineering Agent이고, Orchestrator는 Agent를 실행하며, Harness는 내부 control plane입니다.**

## 먼저 실행해보기

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

Windows:

```powershell
agent.cmd setup
agent.cmd demo
```

기존 `./harness` / `harness.cmd` 명령도 Research Preview 동안 호환됩니다.

자세한 내용: [한국어 Quickstart](QUICKSTART.ko.md)

`demo`는 fixture만 사용하며 Cloud account, Kubernetes cluster, observability system, production environment에는 연결하지 않습니다. `DEMO PASS`는 deterministic contract plumbing이 일관된다는 의미이며 live Agent 성능을 증명하지 않습니다.

## 하나의 Agent, 여러 Engineering Capability

```text
Infrastructure Engineering Agent
        │
        ├─ Infrastructure
        ├─ Operations
        ├─ DevOps / Delivery
        ├─ SRE / Reliability
        ├─ FinOps
        └─ Security
```

이 영역들은 처음부터 별도 Agent가 아니라 하나의 Agent 내부 Capability/Lens입니다. Specialist delegate는 규모와 평가 결과가 필요성을 증명할 때만 선택적으로 사용합니다.

## Architecture

```text
CLI / Web / Slack / GitHub / MCP / API
                    ↓
          Agent Orchestrator / Turn Runtime
                    ↓
          Context + Memory + Skills + Tools
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
                    ↓
               Tool Executor
                    ↓
          Harness / Control Plane
 Provenance · Scope · Guard · Approval · Audit
          Change Control · Recording
                    ↓
            Capability Backends
                    ↓
 AWS / K8s / CI/CD / Observability / Cost / Security
                    ↓
          Independent Verification
             ↙              ↘
           완료        반복 조정이 필요할 때
                           ↓
                    Engineering Loop
```

- **Agent** — reasoning과 다음 행동 판단
- **Orchestrator** — Turn lifecycle과 model/tool 흐름
- **Harness / Control Plane** — 권한, provenance, approval, audit, change safety
- **Independent Verification** — 실제 목표가 달성되었는지 독립적으로 확인

Orchestrator가 존재해도 Production 권한이나 사실 판정 권한이 생기지 않습니다.

## Agent Turn Runtime

`runtime/orchestrator.py`는 provider-neutral reference Turn Runtime입니다.

```text
TurnRequest
   ↓
Context + Available Surface
   ↓
Model
   ↓
필요한 read-only Tool
   ↓
Model continuation
   ↓
Independent Verification
   ↓
verified / unverified
```

Reference Orchestrator는 의도적으로 read-only입니다. Production workflow/change는 Resource Provenance, `ToolPipeline`, `ChangeControl`, 독립 승인, authorized backend 경계를 계속 통과해야 합니다.

> **Orchestrator owns flow, not truth or authority.**

## 모델이 보는 Surface

모델은 기본적으로 세 가지를 알면 됩니다.

```text
Context
Skills
Tools
```

Domain, Capability, Binding, Workflow, Loop는 runtime 내부 metadata입니다. 고정된 `Domain → Skill → Capability Routing → Loop` 체인을 강제하지 않습니다.

`capability-routing`은 필요한 경우 사용할 수 있는 implementation planning Skill이지 필수 architecture node가 아닙니다.

## Runtime Event Log = 실행 SSOT

```text
Runtime Event Log
  ├─ Trace / Span
  ├─ Latency / Cache Metrics
  ├─ Recording
  └─ Evaluation
```

실행 중 모델이 본 것, Tool 요청/결과, verification 결과의 canonical record는 append-only Runtime Event Log입니다. Trace, Metrics, Recording은 별도 truth store가 아니라 동일한 Runtime Event를 기반으로 연결되거나 파생되어야 합니다.

## 핵심 구성

- **Agent Orchestrator / Turn Runtime** — 모든 channel을 하나의 Turn lifecycle로 통합
- **Context Pack** — provenance, freshness, evidence gap을 가진 bounded Context
- **Skills / Tools** — 필요할 때 progressively expose하는 guidance/action
- **Capability Registry** — 내부 source/trust/risk/availability metadata
- **Resource Graph** — 실제 Resource/Dependency와 discovery provenance
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Event Log, Tool Pipeline, Guard, Approval, State 등의 reference control-plane primitive
- **Harness / Control Plane** — Provenance, Scope, Approval, Change Control, Audit, Recording
- **Engineering Loop** — 반복적인 external-state reconciliation이 필요한 작업에서만 사용
- **Knowledge Consolidation** — Observation → Verified Fact → Assessment → Learning Candidate → Durable Knowledge
- **Skill Lift / Context Lift / Harness Lift** — Guidance가 실제 Agent 성능을 높이는지 검증
- **Artifact Reflex** — Paperthin에서 흡수한 artifact hygiene, SSOT, eval-integrity 원칙

## Safety

- Read-only discovery / Evidence 수집이 기본 권한입니다.
- Production 변경 대상은 trusted Resource Graph에서 provenance가 확인되고 Bound Capability scope 안에 있어야 합니다.
- Tool output은 자동으로 Verified Fact가 되지 않습니다.
- `verified_by: agent`는 허용하지 않습니다.
- Chat text, Orchestrator state, delegate, channel은 Production authorization이 아닙니다.
- Approval은 정확한 staged revision에 묶이고 apply 직전에 다시 검증됩니다.
- Production mutation / destructive action / privilege expansion / financial commitment는 독립적인 authorization이 필요합니다.

## Reference Models

Primary structural reference는 의도적으로 적게 유지합니다.

- **Anthropic Commerce Agents** — Agent product / standard model-tool loop / Backend / Runtime safety
- **Anthropic Context Engineering** — minimal context / progressive disclosure / unhobbling
- **Samsung Account AgentCore AIOps** — production observability / channel convergence / task-specific evaluation / scale-out pressure
- **Kubernetes Controllers + LongHorizon-Harness** — reconciliation / external task state
- **NVIDIA ACES / SkillEvaluator** — artifact/effect evaluation

Supporting reference는 DeepSeek Harness(event/runtime extensibility), GBrain(memory taxonomy), Backpass(context evolution), Paperthin(artifact/eval hygiene), LoopsBench(long-running eval), MCP/OpenGitOps를 사용합니다. Google SRE / DORA / FinOps는 Engineering domain truth의 기준입니다.

> **Reference widely, expose narrowly.**

자세한 내용: [docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md)

## 참여

- 실제 운영 경험을 비식별화해 [Scenario](contrib/scenarios/README.md) 추가
- Agent 실행 후 [Validation Report](validation-reports/README.md) 제출
- Cloud / Kubernetes / Prometheus / CI/CD read-only Adapter 구현
- Skill Eval / Harness Lift / negative case 추가
- Reference Model 제안

[CONTRIBUTING.md](CONTRIBUTING.md)

## 주요 명령

```text
./agent setup
./agent demo
./agent validate
./agent scenario evals/scenarios/sre-dependency-saturation.json
./agent doctor
```

기존 `./harness` 명령도 호환됩니다.

## 언어 정책

English가 machine-readable technical contract의 canonical source입니다. 한국어·일본어·중국어 README와 Quickstart는 first-class entry documentation으로 유지합니다.

[Localization Policy](docs/LOCALIZATION.md)

## License

MIT
