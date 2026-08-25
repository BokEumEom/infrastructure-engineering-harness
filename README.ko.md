# Infrastructure Engineering Harness

[English](README.md) | **한국어**

Infrastructure Knowledge와 현재 Evidence를 구조화해 **Infrastructure Engineering, SRE, DevOps, FinOps, Security의 검토 가능한 Engineering Decision과 통제된 구현**으로 연결하는 Provider-neutral, Cross-agent Harness입니다.

> **Knowledge → Context → Decision Skill → Capability → Loop → Verified Outcome → Learning → Next Loop**

**Codex, Kiro, Claude Code 및 Repository-aware Agent**에서 사용할 수 있으며 특정 Cloud, Runtime, IaC Tool, Observability, CI/CD, Cost, Security Product 또는 Ticketing Platform을 전제로 하지 않습니다.

## 왜 필요한가

Agent는 이미 IaC, Configuration, Script, Pipeline, Runbook과 운영 절차를 생성할 수 있습니다. 더 어려운 문제는 **무엇을 왜 바꿔야 하는지, 어떤 Evidence가 있는지, 어떤 제약을 지켜야 하는지, 어떤 구현 지식을 선택해야 하는지, 실제 결과가 기대한 상태가 되었는지 어떻게 검증할지**입니다.

이 Harness는 역할을 분리합니다.

```text
Organizational Knowledge + Current Evidence
                    ↓
               Domain Lens
                    ↓
               Decision Skill
          무엇을 왜 해야 하는가?
                    ↓
             Capability Routing
            어떻게 구현할 것인가?
                    ↓
       Implementation / Verification Skill
                    ↓
          Review 가능한 Local Artifact
                    ↓
       Validation + Human/Policy Gate
                    ↓
        독립적으로 승인된 Execution
                    ↓
           Loop Verification + Learn
```

기술별 구현 지식이나 외부 Skill이 Architecture Decision이나 Production 권한으로 바로 이어지지 않도록 분리하는 것이 핵심입니다.

자세한 내용은 [Architecture](docs/ARCHITECTURE.md), [Capability Model](docs/CAPABILITY-MODEL.md), [Loop Engineering](loops/README.md), [Reference Models](docs/REFERENCE-MODELS.md), [Production Readiness](docs/PRODUCTION-READINESS.md)를 참고하세요.

## 구축과 운영

Harness는 다음 Lifecycle을 지원하도록 설계합니다.

```text
Design → Build → Deploy → Operate → Observe → Improve → Learn
  ↑                                                   │
  └───────────────────────────────────────────────────┘
```

주요 사용 범위:

- Architecture / Migration Review
- Infrastructure·Application Platform 구축 계획
- IaC / Configuration / CI/CD / Deployment Artifact 생성
- Observability / Alerting 설계
- Runbook / 운영 절차 생성
- Incident 분석과 Recovery 검증
- SLO / Error Budget 검토
- Change Review / Rollback 설계
- FinOps Optimization / 실제 절감 효과 검증
- Security / Trust Boundary 검토
- MCP / Workflow Tool 보안 검토
- Supply Chain / Access Review 계획
- MCP 기반 Jira / Linear Ticket Workflow

기본 Harness는 **Production 실행 권한을 직접 소유하지 않습니다.** 실행에 필요한 Artifact와 검증 절차를 만들 수 있지만 Level 3 Controlled Execution은 별도 Credential, Authorization, Policy, Audit Control이 필요합니다.

### 예시: 새 서비스 구축

```text
사용자 요구사항
  "Container 기반 Public API를 구축하고
   CI/CD, Vendor-neutral Telemetry, Runbook을 만들어줘."
                    ↓
architecture-review + sre-review + security-review
                    ↓
Engineering Decision / Constraint
                    ↓
capability-routing
                    ↓
Kubernetes / Helm / CI/CD / OpenTelemetry / Runbook Capability
                    ↓
Local Manifest / Pipeline / Telemetry Config / Runbook
                    ↓
change-review
                    ↓
승인 후 External Execution
                    ↓
change-validation Loop
```

실제 Platform 정보가 없으면 Agent가 AWS, Kubernetes, GitHub Actions, GitLab CI, Terraform 등을 임의로 선택하지 않습니다.

### 예시: 기존 서비스 운영

```text
Latency Alert / 사용자 제보
          ↓
incident-analysis
          ↓
Current Evidence + Historical Context
          ↓
Verified Hypothesis
          ↓
필요한 경우 capability-routing
          ↓
Observability / Runbook / Platform Capability
          ↓
Mitigation Proposal / 운영 Artifact
          ↓
incident-response Loop
          ↓
Recovery 검증 → Regression Check → Learn
```

## Domain Packs

공통 Core를 다섯 개 Engineering Lens가 재사용합니다.

| Pack | 주요 용도 | 추가 Context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | Architecture, Capacity, Migration, Dependency, Change Risk | Architecture, ADR, Runtime/Capacity Evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, Error Budget, Incident, Reliability, Toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | Build/Release/Deployment, Rollback, Delivery Performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | Allocation, Usage Efficiency, Commitment, Unit Economics | `domains/finops.yaml` |
| [Security](domains/security/README.md) | Trust Boundary, Identity/Privilege, Sensitive Data, External Integration, Supply Chain | `domains/security.yaml` |

역할은 다음처럼 구분합니다.

```text
Domain      → 어떤 질문과 제약을 봐야 하는가?
Decision    → 무엇을 왜 해야 하는가?
Capability  → 어떻게 구현하거나 검증할 것인가?
Loop        → 언제 반복하고, 검증하고, 중단하고, 학습할 것인가?
```

## Decision Skill과 Capability Skill

Agent가 직접 발견하는 Local Skill은 호환성을 위해 `skills/`에 유지합니다.

```text
Decision
├── architecture-review
├── incident-analysis
├── change-review
├── sre-review
├── delivery-review
├── finops-review
└── security-review

Control / Workflow
├── capability-routing
├── loop-engineering
└── ticketing
```

Kubernetes, CI/CD, Observability, Security Tool처럼 기술별 구축·운영 지식은 모든 Prompt에 넣지 않고 `capabilities/registry.yaml`에서 필요한 것만 선택합니다.

### 외부 Capability Reference

첫 번째 외부 Reference Source는 다음 Repository입니다.

```text
BagelHole/DevOps-Security-Agent-Skills
revision: 0365f57a079b1332f95cf26e31dd2d5332a8399f
license: MIT
trust: pinned_reference
execution: reference_only
```

현재 Registry에서는 160개 전체를 가져오지 않고 다음 일부만 연결했습니다.

- Kubernetes Operations
- Helm Charts
- GitHub Actions / GitLab CI
- OpenTelemetry
- Alerting / On-call
- Runbook Creation
- Threat Modeling
- MCP Server Security
- SBOM / Software Supply Chain
- Policy-as-Code
- Access Review

외부 Capability를 사용할 때는:

1. Registry에 고정된 Immutable Revision만 사용합니다.
2. 필요한 Skill만 Progressive하게 읽습니다.
3. Command, Script, Asset은 Reference로 취급합니다.
4. 외부 Script나 Command를 자동 실행하지 않습니다.
5. 필요한 패턴은 Local Code/Config/Runbook/Procedure로 다시 작성합니다.
6. Local Evidence, Policy, Security Review, Change Review를 적용합니다.
7. 실행은 독립적으로 승인된 Tool/System에서 수행합니다.
8. 실제 결과는 Loop에서 다시 검증합니다.

조직이 특정 Capability를 검토하고 내부화하면 `pinned_reference`에서 Managed Local Source로 승격할 수 있습니다.

[Capabilities](capabilities/README.md), [Capability Model](docs/CAPABILITY-MODEL.md)을 참고하세요.

## Capability Routing 사용 예시

```text
/infra-harness:capability-routing

Decision:
이 서비스는 Containerized Workload로 운영하고,
Rolling Deployment와 99.9% Availability Objective,
Vendor-neutral Telemetry를 사용한다.

이 Decision을 실제 Build Artifact로 만들어줘.
capabilities/registry.yaml을 기준으로 최소 Capability만 선택하고,
Production 변경은 실행하지 말고, 알 수 없는 Platform 정보는 추측하지 마.
```

흐름:

```text
Decision refs
    ↓
Capability Selection
    ↓
Source + Pinned Revision
    ↓
Local Artifact Generation
    ↓
Validation
    ↓
Change / Security Review
    ↓
External Execution 또는 Approval Gate
```

[Capability Routing Example](examples/capability-routing/README.md)을 참고하세요.

## Loop Engineering

Loop Engineering은 Skill/Capability 위에 있는 실행 제어 계층입니다. 한 번의 분석으로 안전하게 끝낼 수 없는 작업에서 사용합니다.

| Loop | 목적 |
| --- | --- |
| `incident-response` | 장애 분석 → 가설 검증 → Mitigation 제안 → Recovery 검증 → 학습 |
| `reliability-improvement` | SLO/Error Budget Baseline → 개선 → 재측정 → 학습 |
| `delivery-improvement` | Delivery Baseline → Bottleneck → 개선 → 재측정 → 학습 |
| `finops-optimization` | Inform → Optimize → Track/Operate → 실제 가치 측정 → 학습 |
| `change-validation` | Precheck → 독립 승인 → 외부 실행 → Post Verification → Regression Check |

Loop의 핵심:

1. **External State** — 실행 상태를 Model 대화와 분리합니다.
2. **Independent Verification** — `verified_by: agent`를 허용하지 않습니다.
3. **Bounded Execution** — Iteration, Duration, No-progress Budget을 둡니다.
4. **Regression Obligation** — 이전 단계에서 확보한 Reliability/Security/Data Integrity 등을 계속 검증합니다.

Agent가 스스로 `done`을 인증할 수 없습니다.

## Agent 지원

### Codex

Root `AGENTS.md`가 Cross-agent Operating Contract입니다.

### Kiro

`AGENTS.md`와 `.kiro/steering/infrastructure-harness.md`를 사용할 수 있습니다.

### Claude Code

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

주요 Local Skill:

```text
/infra-harness:incident-analysis
/infra-harness:architecture-review
/infra-harness:change-review
/infra-harness:sre-review
/infra-harness:delivery-review
/infra-harness:finops-review
/infra-harness:security-review
/infra-harness:capability-routing
/infra-harness:ticketing
/infra-harness:loop-engineering
```

## 사용 방식

### A. Embedded Context

```text
service-repository/
├── AGENTS.md
└── .infra-context/
    ├── service-catalog.yaml
    ├── architecture/
    ├── adr/
    ├── incidents/
    ├── policies/
    ├── runbooks/
    └── domains/
        ├── sre.yaml
        ├── devops.yaml
        ├── finops.yaml
        └── security.yaml
```

### B. Central Harness / Platform Workspace

서비스 Repository를 수정하지 않고 중앙 Harness에서 여러 서비스의 Context와 Capability를 관리할 수 있습니다.

```text
harness-workspace/
├── AGENTS.md
├── contexts/
│   ├── payment-platform/
│   ├── identity-platform/
│   └── shared-network/
├── capabilities/
└── read-only sources
    ├── service repositories
    ├── runtime / observability
    ├── deployment systems
    └── cost / business data
```

## Machine-readable Contract

`schemas/`에는 Service Catalog, Incident, ADR, Policy, Evidence, Change Proposal, Ticketing, Capability Registry, Domain Profile, Loop Contract가 있습니다.

```text
capability-registry.schema.json  Capability Source Trust / Routing
security-profile.schema.json     Trust / Identity / Security Context
loop-spec.schema.json            Loop Goal / Step / Terminal / Budget
loop-state.schema.json           External Execution State
loop-result.schema.json          Terminal Outcome / Learning
loop-eval-suite.schema.json      Long-horizon Regression Scenario
```

검증:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/validate_capability_registry.py capabilities/registry.yaml
python scripts/check_domain_eval.py \
  evals/domains/security.json \
  mcp-write-boundary \
  examples/eval-output/domain-security-mcp-boundary.json
python scripts/check_loop_eval.py \
  evals/loops/standard.json \
  incident-recovered \
  examples/eval-output/loop-incident-recovered.json
python -m unittest discover -s tests
```

## Live Evidence Adapter는 선택 사항

Prometheus, OpenTelemetry, Datadog, Cloud-native Monitoring, Runtime API, Source Control, Deployment History, SLO Tool, Cost/Usage System, Business Metric 등을 사용할 수 있습니다. **Datadog은 필수가 아닙니다.** Tool 결과는 `schemas/evidence.schema.json`으로 Normalize한 뒤 Fact로 사용합니다.

## MCP 기반 Jira / Linear 자동화

Ticket 생성은 Remote MCP를 Workflow Action으로 사용합니다. Security Lens는 Workflow Write 권한과 Production Mutation 권한을 분리합니다.

```text
Incident / Review / Loop
          ↓
     Ticket Request
          ↓
 Policy + Deduplication
          ↓
    Remote MCP Server
          ↓
 Search → Create/Update
```

## Eval

현재 Eval은 다음을 확인합니다.

- 30개 Provider-neutral Incident Scenario
- Infrastructure / SRE / DevOps / FinOps / Security Domain Eval
- Capability Registry Trust / Supply-chain Unit Test
- Loop Terminal / Iteration Budget / Required & Prohibited Event / Writeback / Regression Obligation
- Agent Self-verification 거부와 No-progress Budget

평가는 **“Agent가 정답을 말했는가?”**뿐 아니라 **“적절한 구현 지식을 선택했는가, Trust Boundary를 지켰는가, 안전한 과정으로 실제 검증 가능한 결과에 도달했는가?”**까지 봅니다.

## Terraform/IaC는 필수가 아닙니다

```text
IaC 환경        Proposal → Code/Config → Plan → PR → Approval
Non-IaC 환경    Proposal → Change Ticket → Console/API Procedure → Approval
운영 절차       Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid          Proposal → Script/Config/API → Controlled Pipeline/Operator
```

Capability는 이 실행 방식에 필요한 구현 지식을 제공하고, Loop는 실행 후 결과를 검증합니다.

## Safety Model

- Read-only Evidence 수집이 기본 출발점입니다.
- Third-party Skill은 검토·관리되기 전까지 Reference입니다.
- External Script/Command를 Capability Routing에서 자동 실행하지 않습니다.
- Agent Hook은 Defense-in-depth이지 Security Boundary가 아닙니다.
- Production Mutation, Destructive Action, Authorization Expansion, Financial Commitment는 독립적으로 승인합니다.
- Loop를 반복해 Human Gate를 우회할 수 없습니다.
- Ticket 생성 권한과 Production 변경 권한을 분리합니다.
- Model은 Truth, Completion, Authorization, Production Control Plane의 소유자가 아닙니다.

## 빠른 시작

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/validate_capability_registry.py capabilities/registry.yaml
python -m unittest discover -s tests
```

## License

MIT
