# Infrastructure Engineering Harness

[English](README.md) | **한국어**

Infrastructure Knowledge와 현재 Evidence를 구조화해 **검토 가능한 인프라 엔지니어링 판단**으로 연결하는 Provider-neutral, Cross-agent Harness입니다.

> **Infrastructure Knowledge → Context → Agent → Decision/Proposal → Human Review → Infrastructure**

Claude Code 하나만을 위한 프로젝트가 아니라 **Codex, Kiro, Claude Code 및 `AGENTS.md` 기반 Agent**에서 재사용할 수 있도록 구성합니다. 특정 Cloud, 특정 Runtime, 특정 Observability 제품이나 Terraform 같은 하나의 변경 방식에 종속되지 않습니다. 핵심은 실행 이전의 Architecture, Decision, 운영 이력, Policy, Evidence, Eval, Change Control을 Agent가 사용할 수 있는 형태로 만드는 것입니다.

## 왜 필요한가

Agent는 이미 IaC, Manifest, Script, Configuration, Runbook, 운영 절차를 빠르게 생성할 수 있습니다. 더 어려운 문제는 다음 질문에 답할 Context를 제공하는 것입니다.

- 왜 이 변경이 현재 시스템에 적절한가?
- 과거 ADR이나 Incident가 어떤 제약을 만드는가?
- 현재 어떤 Evidence가 진단을 뒷받침하는가?
- Blast Radius와 Rollback은 무엇인가?
- 어디까지 Agent가 제안하고, 어디부터 독립적인 Production Control이 맡아야 하는가?

## 핵심 구조

```text
Durable Infrastructure Knowledge          Optional Live Evidence
Service Catalog / ADR / Incident          Metrics / Logs / Traces
Policy / Runbook / Architecture           Runtime / Deploy / Status
              │                                  │
              └──────────────┬───────────────────┘
                             ▼
                    Progressive Context
                             ▼
                    Infrastructure Agent
                             ▼
                   Evidence-based Decision
                             ▼
                      Change Proposal
                             ▼
          Validation / Policy / Eval / Review
                             ▼
       PR / Change Ticket / Approved Runbook
                             ▼
                       Human Approval
                             ▼
                      Infrastructure
```

자세한 구조는 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), Production 적용 단계는 [docs/PRODUCTION-READINESS.md](docs/PRODUCTION-READINESS.md)를 참고하세요.

## Agent 지원

### Codex

Repository root의 `AGENTS.md`를 기본 Operating Contract로 사용합니다. `AGENTS.md`에 모든 지식을 넣지 않고 구조화된 Context로 안내하는 Map 역할을 하도록 설계했습니다.

### Kiro

Kiro도 `AGENTS.md`를 지원합니다. 추가로 `.kiro/steering/infrastructure-harness.md`를 Workspace Steering Adapter로 제공합니다.

### Claude Code

Claude Code에서는 Plugin Adapter를 사용할 수 있습니다.

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

제공 Skill:

```text
/infra-harness:incident-analysis
/infra-harness:change-review
/infra-harness:architecture-review
```

## 사용 방식

모든 Service Repository에 Agent 파일을 추가할 필요는 없습니다. 두 가지 방식으로 적용할 수 있습니다.

### Mode A — Embedded Context

Service 또는 Infrastructure Repository가 자신의 운영 Knowledge를 직접 소유하는 방식입니다.

```text
service-repository/
├── AGENTS.md
├── application-or-infrastructure-files/
└── .infra-context/
    ├── service-catalog.yaml
    ├── architecture/
    ├── adr/
    ├── incidents/
    ├── policies/
    └── runbooks/
```

사용 예:

```text
AGENTS.md와 .infra-context를 사용해 현재 Latency Incident를 분석해줘.
Evidence와 Assumption을 분리하고 Hypothesis를 우선순위로 정리해.
Production 변경은 수행하지 마.
```

### Mode B — Central Harness / Platform Workspace

Platform, SRE, Infrastructure Team이 Service Repository를 수정하지 않고 중앙에서 운영하는 방식입니다.

```text
infrastructure-harness-workspace/
├── AGENTS.md
├── schemas/
├── evals/
├── workflows/
├── adapters/
└── contexts/
    ├── payment-platform/
    ├── identity-platform/
    └── shared-network/

Service Repository / Monitoring / Runtime System
                    │
                    └── Read-only Source
```

이 방식에서는 Harness Repository가 Reasoning/Control Workspace가 되고, Service Repository, Deployment History, Monitoring, Cloud/Runtime API, Status Feed는 Read-only Evidence Source가 됩니다.

사용 예:

```text
contexts/payment-platform을 기준으로 payment-platform 장애를 분석해줘.
payment 서비스 Repository는 Read-only Source로만 확인해.
현재 Evidence가 있으면 사용하고, Hypothesis와 Verification을 먼저 작성한 뒤
근거가 충분한 경우에만 Change Proposal을 만들어줘.
```

여러 Repository에 걸쳐 하나의 Architecture가 구성되는 조직에서는 Central Mode가 더 자연스러울 수 있습니다.

## Provider-neutral Context Contract

Embedded Mode와 Central Mode 모두 동일한 Knowledge Category를 사용합니다.

```text
service-catalog.yaml
architecture/
adr/
incidents/
policies/
runbooks/
```

Reference Context와 Eval은 ECS, Kubernetes, 특정 Database, AWS, 특정 Observability 제품을 전제로 하지 않습니다. 대신 `compute`, `datastore`, `messaging`, `network`, `storage`, `identity`, `external_dependency` 같은 Capability 단위로 표현합니다.

## Schema와 CI Validation

`schemas/`에는 다음 Machine-readable Contract가 있습니다.

- Service Catalog
- Incident
- ADR
- Policy
- Live Evidence / Provenance
- Change Proposal
- Eval Suite

검증:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

동일한 검증을 GitHub Actions에서도 실행합니다.

## Live Evidence Adapter는 선택 사항

Core Harness는 외부 연동 없이도 Architecture/Change Review에 사용할 수 있습니다. 현재 상태가 필요한 경우에만 Read-only Adapter를 추가합니다.

**Datadog은 필수가 아닙니다.** Prometheus, OpenTelemetry Backend, Cloud-native Monitoring, 다른 APM 또는 Repository 기반 Evidence를 사용할 수 있습니다. Cloud Provider 역시 Core 가정이 아니라 Adapter입니다.

모든 Tool 결과는 Agent가 판단하기 전에 `schemas/evidence.schema.json` 형태로 Normalize하는 것을 권장합니다. 자세한 내용은 [adapters/README.md](adapters/README.md)를 참고하세요.

## Evidence와 Provenance

중요한 Recommendation은 Evidence ID로 추적할 수 있어야 합니다. Source Type, Observation Time, Component, Signal과 가능한 경우 Query/Resource Reference까지 남깁니다.

목표는 **"Agent가 그렇게 말했기 때문"을 운영 근거로 사용하지 않는 것**입니다.

## Provider-neutral Eval

`evals/standard/incident-scenarios.json`에는 **30개의 Golden Incident Scenario**가 포함됩니다.

Compute, Datastore, Messaging, Cache, Network, Identity, Deployment, Storage, External Dependency, Partial Failure, Telemetry Gap 등을 다루며 특정 AWS Service나 Container Platform 이름이 정답이 되지 않도록 구성했습니다.

```bash
python scripts/check_eval_output.py \
  evals/standard/incident-scenarios.json \
  dependency-latency-001 \
  examples/eval-output/dependency-latency-001.json
```

## Terraform 또는 IaC는 필수가 아닙니다

이 Harness는 Terraform Workflow가 아니며 Infrastructure-as-Code 사용을 요구하지 않습니다.

환경에 따라 Change Proposal 이후의 실행 Artifact가 달라질 수 있습니다.

```text
IaC 환경
Evidence → Proposal → Code/Config Diff → Plan/Dry Run → PR → Approval → Deployment

Non-IaC Managed Service
Evidence → Proposal → Change Ticket → Approved Console/API Procedure → Approval → Operator Execution

운영 절차 기반 환경
Evidence → Proposal → Reviewed Runbook → Maintenance Window → Approval → Operator Execution

Hybrid 환경
Evidence → Proposal → Script/Config/API Change → Validation → Controlled Pipeline 또는 Operator
```

Terraform을 사용하지 않을 수 있는 예로는 Vendor-managed SaaS, Managed Network Appliance, Legacy System, Database Operation, Hardware Platform, 다른 Control System으로 관리되는 Cloud Resource, 승인된 Console/API Workflow를 사용하는 조직 등이 있습니다.

Harness가 요구하는 것은 "Terraform을 생성하는 것"이 아니라 다음과 같은 Engineering Control입니다.

- Evidence를 명시할 것
- Risk와 Blast Radius를 설명할 것
- Validation을 정의할 것
- Rollback 또는 Recovery를 정의할 것
- Agent 외부의 독립적인 승인/실행 경로를 사용할 것

## Production Change Workflow

기본 Harness는 Production을 직접 변경하지 않고 Review 가능한 Proposal에서 멈춥니다.

```text
Evidence → Recommendation → Change Proposal → Validation → Review Artifact → Human Approval → Execution System
```

Review Artifact는 **Pull Request, Change Ticket, Approved Runbook, Plan, Controlled Procedure**가 될 수 있습니다.

`schemas/change-proposal.schema.json`은 Evidence Reference, Risk, Blast Radius, Validation, Rollback, Approval을 요구합니다. [workflows/change-proposal.md](workflows/change-proposal.md)에 Workflow를 정의했습니다.

## 실제 Incident 예시

Request-serving Service의 End-to-end Latency는 높지만 Service Compute는 정상이고 Critical Datastore Dependency가 Saturation 상태라고 가정합니다.

Agent는 다음처럼 판단해야 합니다.

```text
Current Evidence
├── service compute utilization: normal
├── dependency connection utilization: high
└── dependency operation latency: high

Historical Context
└── previous dependency saturation incident

Decision
├── primary hypothesis: dependency saturation
├── 근거 없이 정상 Compute를 Scale하지 않음
├── connection pressure / slow operation / recent change 확인
└── Verification 이후에만 Reversible Change Proposal 생성
```

Service가 Container, VM, Serverless, Physical Host, Managed Platform 중 어디에서 동작하든 동일한 판단 구조를 사용할 수 있어야 합니다.

## Safety Model

Agent Hook은 Defense-in-depth이지 **Security Boundary가 아닙니다**. 실제 Production Enforcement는 Least-privilege IAM/RBAC, CI/CD Approval, Protected Branch, Change Management Control, Policy-as-Code, Audit Log, Deployment/Operations Authorization처럼 모델 외부에서 강제해야 합니다.

Production Pilot은 Read-only 권한부터 시작하는 것을 권장합니다.

## 빠른 시작

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

Embedded Mode에서는 `examples/.infra-context`를 대상 Repository에 복사합니다. Central Mode에서는 동일한 Context 구조를 Harness Workspace의 Service/Domain별 디렉터리 아래에 둡니다. Secret이나 민감한 Payload는 Agent Context에 넣지 않습니다.

## Design Principles

1. Evidence before action
2. 전체 Knowledge를 한 번에 넣지 않는 Progressive Disclosure
3. ADR과 Incident History를 First-class Context로 관리
4. Cloud/Observability Vendor는 Core가 아니라 Adapter
5. IaC는 선택 사항이지만 Engineering Control은 필수
6. Recommendation에 Provenance 포함
7. Production Change는 Reviewable하고 Reversible하게 설계
8. 실제 Authorization은 Agent 외부에서 독립적으로 강제
9. Agent의 판단을 Provider-neutral Eval로 Regression Test

## License

MIT
