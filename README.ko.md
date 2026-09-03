# Infrastructure Engineering Agent

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Infrastructure / Operations / DevOps / SRE / FinOps / Security 업무를 조사·검토·계획·검증하는 provider-neutral **Infrastructure Engineering Agent**입니다.

> **에이전트의 판단은 열어두고, 권한과 사실의 경계는 Runtime이 통제합니다.**

> **상태: Research Preview.** Agent contract, Skills, Resource Graph, deterministic scenario, evaluation plumbing, local CLI는 현재 사용할 수 있습니다. Live adapter, persistent runtime, controlled execution은 experimental 단계입니다.

Repository 이름 `infrastructure-engineering-harness`는 기존 링크와 호환성을 위해 유지합니다. **제품의 중심은 Infrastructure Engineering Agent이고, Harness는 Agent 내부의 control plane입니다.**

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

`demo`는 Repository의 fixture만 사용하며 Cloud account, Kubernetes cluster, observability system, production environment에는 연결하지 않습니다. `DEMO PASS`는 deterministic contract가 일관된다는 의미이며 live Agent 성능을 증명하지 않습니다.

## 하나의 Agent, 여러 Engineering Capability

사용자가 먼저 "이건 Ops인가 SRE인가"를 결정할 필요가 없습니다.

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

예:

- "이 Terraform 변경 검토해줘"
- "payment-api latency가 왜 증가했지?"
- "이 배포 파이프라인 개선해줘"
- "이 서비스 Error Budget 괜찮아?"
- "인프라 비용 증가 원인을 찾아줘"
- "IAM과 Trust Boundary 검토해줘"

이 영역들은 처음부터 별도 Agent가 아니라 하나의 Agent 내부 Capability/Lens입니다.

## Architecture

```text
Organizational Knowledge + Live Environment
                    ↓
              Minimal Context
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
          ↙         ↓         ↘
      Context     Skills    Capabilities
          ↘         ↓         ↙
                   Action
                    ↓
       Agent Runtime / Harness Control Plane
 Evidence · Resource Provenance · State · Guard
 Permission · Approval · Audit · Verification
                    ↓
          Infrastructure Backend
                    ↓
 AWS / K8s / CI/CD / Observability / Cost / Security
                    ↓
          Independent Verification
                    ↓
             Verified Outcome
```

Agent는 reasoning과 다음 행동의 판단을 담당합니다. Credential, 독립적인 사실 판정, Approval state, Production 권한, 완료 인증은 Agent가 소유하지 않습니다.

## Agent Contract / Backend

제품 계약은 [agents/infrastructure_engineering/agent.yaml](agents/infrastructure_engineering/agent.yaml)에 있습니다.

Provider-neutral Backend interface는 [agents/infrastructure_engineering/backend.py](agents/infrastructure_engineering/backend.py)에 있습니다.

```text
discover / evidence
       ↓
  model judgment
       ↓
  stage_change
       ↓
review / approval
       ↓
apply_approved_change
       ↓
 verify_outcome
```

Platform credential은 Backend/Runtime 내부에 있고 모델에게 전달하지 않습니다. Chat에서 "승인"이라고 입력하는 것과 독립적인 execution authorization은 다릅니다.

## 핵심 구성

- **Agent Contract** — Infrastructure Engineering Agent의 역할, Capability, 권한, Backend, 완료 경계
- **Minimal Agent Context** — 항상 로드되는 최소 Truth / Authorization / Verification 규칙
- **Workflow Surface** — 고정 reasoning route를 강제하지 않는 사용자 intent
- **Context Pack** — provenance, freshness, evidence gap을 가진 pull-oriented context
- **Skill / Capability** — 필요할 때 progressively load하는 Engineering guidance
- **Resource Graph** — 실제 Resource/Dependency와 discovery provenance
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — 내부 Event Log / Tool Pipeline / Guard / Approval / Sandbox / State
- **Engineering Loop** — Goal + State + Constraint + Terminal Condition 중심의 adaptive reconciliation
- **Knowledge Consolidation** — Observation → Verified Fact → Assessment → Learning Candidate → Durable Knowledge
- **Skill Lift / Context Lift / Harness Lift** — Guidance가 실제 Agent 성능을 향상시키는지 검증
- **Artifact Reflex** — Paperthin 기반 artifact hygiene, SSOT, eval integrity

## Safety

- Read-only discovery / Evidence 수집이 기본 권한입니다.
- Production 변경 대상 Resource는 먼저 discovery/binding 되어야 합니다.
- Tool output을 자동으로 Verified Fact로 승격하지 않습니다.
- `verified_by: agent`는 허용하지 않습니다.
- Chat text는 Production authorization이 아닙니다.
- Production mutation / destructive action / privilege expansion / financial commitment는 독립적인 승인이 필요합니다.
- Hard boundary는 Prompt 반복보다 Runtime / Schema / Policy / Backend에서 강제합니다.

## Reference Models

DeepSeek Harness, NVIDIA SkillEvaluator/ACES, Paperthin, gstack, GBrain, WikiSkill, Kubernetes Controller, SRE/DORA/FinOps와 함께 Anthropic의 **commerce-agents**를 Reference Model로 사용합니다.

특히 Commerce Agents의 **Agent product surface → Backend contract → Provenance Gate → Staged Write → Host Approval → Runtime Enforcement** 구조를 Infrastructure 영역에 맞게 참고합니다.

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
