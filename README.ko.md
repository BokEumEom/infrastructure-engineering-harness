# Infrastructure Engineering Harness

[English](README.md) | **한국어**

Infrastructure Knowledge와 현재 Evidence를 구조화해 **Infrastructure Engineering, SRE, DevOps, FinOps의 검토 가능한 Engineering Decision**으로 연결하는 Provider-neutral, Cross-agent Harness입니다.

> **Infrastructure Knowledge → Context → Skill → Loop → Verified Outcome → Learning → Next Loop**

**Codex, Kiro, Claude Code 및 Repository-aware Agent**에서 사용할 수 있으며 특정 Cloud, Runtime, IaC Tool, Observability, CI/CD, Cost 또는 Ticketing Platform을 전제로 하지 않습니다.

## 왜 필요한가

Agent는 이미 IaC, Configuration, Script, Runbook, 운영 절차를 빠르게 생성할 수 있습니다. 더 어려운 문제는 **무엇을 왜 바꿔야 하는지, 어떤 Evidence가 있는지, 어떤 제약을 지켜야 하는지, 실제 결과가 기대한 상태가 되었는지 어떻게 검증할지**입니다.

이 Harness는 Architecture, ADR, Incident, Policy, Reliability Objective, Delivery Rule, Cost Ownership과 현재 Evidence를 Agent가 사용할 수 있는 Context로 만듭니다. 여기에 Loop Engineering을 추가해 한 번의 답변으로 끝내기 어려운 작업을 Observe → Decide → Verify → Reconcile → Learn 구조로 반복하되, 모델이 스스로 Truth나 완료 여부를 정의하지 못하도록 설계합니다.

## 구조

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Domain Skill(s)
                    ↓
          Loop Engineering Control
      Observe → Decide → Act/Propose → Verify
         ↑                         ↓
         └──── Reconcile / Learn ──┘
                    ↓
        done / escalated / failed
                    ↓
 Incident / Runbook / ADR·Policy Candidate / Eval
                    ↓
                 Next Loop
```

자세한 내용은 [Architecture](docs/ARCHITECTURE.md), [Loop Engineering](loops/README.md), [Reference Models](docs/REFERENCE-MODELS.md), [Production Readiness](docs/PRODUCTION-READINESS.md)를 참고하세요.

## Domain Packs

| Pack | 주요 용도 | 추가 Context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | Architecture, Capacity, Migration, Dependency, Change Risk | Architecture, ADR, Runtime/Capacity Evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, Error Budget, Incident, Reliability, Toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | Build/Release/Deployment, Rollback, Delivery Performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | Allocation, Usage Efficiency, Commitment, Unit Economics | `domains/finops.yaml` |

역할을 구분하면 다음과 같습니다.

```text
Domain → 어떤 질문을 봐야 하는가
Skill  → 지금 무엇을 할 수 있는가
Loop   → 언제 반복하고, 무엇을 검증하며, 언제 멈추고 학습할 것인가
```

## Loop Engineering

Loop Engineering은 기존 Skill 위에 있는 실행 제어 계층입니다. 한 번의 분석으로 끝나지 않고 **상태 변화와 결과 검증이 필요한 작업**에서 사용합니다.

기본 Loop:

| Loop | 목적 |
| --- | --- |
| `incident-response` | 장애 분석 → 가설 검증 → Mitigation 제안 → Recovery 검증 → 학습 |
| `reliability-improvement` | SLO/Error Budget Baseline → 개선 우선순위 → 추적 → 재측정 → 학습 |
| `delivery-improvement` | Delivery Baseline → Bottleneck 확인 → 개선 → 재측정 → 학습 |
| `finops-optimization` | Inform → Optimize → Track/Operate → 실제 가치 측정 → 학습 |
| `change-validation` | Precheck → 독립 승인 → 외부 실행 → Post Verification → Regression Check |

Loop가 추가하는 핵심은 네 가지입니다.

1. **External State** — 실행 상태를 Model의 대화 내용과 분리해 명시적으로 관리합니다.
2. **Independent Verification** — `verified_by: agent`는 허용하지 않습니다. Environment, Tool, Human, Test Evidence만 Verified Fact가 됩니다.
3. **Bounded Execution** — Iteration, Duration, No-progress Budget을 정의합니다.
4. **Regression Obligation** — 앞 단계에서 확보한 안정성·보안·데이터 무결성 등의 조건을 다음 Iteration에서도 계속 검증합니다.

Agent가 “해결된 것 같다”고 말하는 것만으로 `done`이 되지 않습니다. Success Criteria가 독립적으로 검증되고, Regression Obligation이 통과하고, 필요한 Human Gate가 모두 해소되어야 합니다.

### Incident Loop 예시

```text
Alert / 사용자 제보
       ↓
incident-analysis
       ↓
Leading Hypothesis
       ↓
Independent Verification
       ↓
Change 필요?
   ┌───┴──────────┐
   No             Yes
   ↓               ↓
Recovery 검증    Change Proposal
                  ↓
             Human Approval
                  ↓
          External Execution
                  ↓
             Recovery 검증
                  ↓
            Regression Check
                  ↓
       Incident + Eval Writeback
```

Claude Code에서는:

```text
/infra-harness:loop-engineering
payment-api에 incident-response loop를 실행해줘.
Recovery는 스스로 완료 처리하지 말고 현재 Evidence로 검증하고, Production 변경 승인이 필요하면 그 단계에서 멈춰.
```

Codex와 Kiro도 `AGENTS.md`를 통해 같은 Loop Spec을 사용합니다.

## Agent 지원

### Codex

Root `AGENTS.md`가 Cross-agent Operating Contract입니다. 단일 분석은 Domain Skill로, 반복 검증이 필요한 작업은 Loop로 Routing합니다.

### Kiro

`AGENTS.md`와 `.kiro/steering/infrastructure-harness.md`를 사용할 수 있습니다.

### Claude Code

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

제공 Skill:

```text
/infra-harness:incident-analysis
/infra-harness:architecture-review
/infra-harness:change-review
/infra-harness:sre-review
/infra-harness:delivery-review
/infra-harness:finops-review
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
        └── finops.yaml
```

### B. Central Harness / Platform Workspace

서비스 Repository를 수정하지 않고 중앙 Harness에서 Context를 관리할 수 있습니다.

```text
harness-workspace/
├── AGENTS.md
├── contexts/
│   ├── payment-platform/
│   ├── identity-platform/
│   └── shared-network/
└── read-only sources
    ├── service repositories
    ├── runtime / observability
    ├── deployment systems
    └── cost / business data
```

[Central Context Example](examples/central-context/README.md)을 참고하세요.

## Machine-readable Contract

`schemas/`에는 Service Catalog, Incident, ADR, Policy, Evidence, Change Proposal, Ticketing, Domain Profile, Loop Engineering Contract가 있습니다.

Loop Contract:

```text
loop-spec.schema.json       Loop의 Goal/Step/Terminal/Budget 정의
loop-state.schema.json      외부에서 유지하는 실행 State
loop-result.schema.json     Terminal Outcome과 Learning
loop-eval-suite.schema.json Long-horizon Regression Scenario
```

검증:

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python scripts/check_loop_eval.py \
  evals/loops/standard.json \
  incident-recovered \
  examples/eval-output/loop-incident-recovered.json
python -m unittest discover -s tests
```

## Live Evidence Adapter는 선택 사항

Prometheus, OpenTelemetry, Datadog, Cloud-native Monitoring, Runtime API, Source Control, Deployment History, SLO Tool, Cost/Usage System, Business Metric 등을 사용할 수 있습니다. **Datadog은 필수가 아닙니다.** Tool 결과는 `schemas/evidence.schema.json`으로 Normalize한 뒤 Fact로 사용합니다.

## MCP 기반 Jira / Linear 자동화

Ticket 생성은 Harness에 Jira REST/Linear GraphQL 코드를 넣지 않고 Remote MCP를 Workflow Action으로 사용합니다.

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

Harness는 Ticket Request, Ticket Policy, Evidence Reference, Search-before-create를 담당하고 Provider MCP가 Authentication/Permission/Tool Call을 담당합니다.

[MCP 연결](mcp/README.md), [Ticketing Workflow](workflows/ticketing.md)를 참고하세요.

## Eval

현재 Eval은 단일 Agent 답변뿐 아니라 Loop 과정도 검사합니다.

- 30개 Provider-neutral Incident Scenario
- Infrastructure / SRE / DevOps / FinOps Domain Eval
- Loop Terminal Status / Iteration Budget / Required & Prohibited Event / Writeback / Regression Obligation
- Agent Self-verification 거부와 No-progress Budget을 확인하는 Deterministic Unit Test

평가 질문은 이제 단순히 **“Agent가 정답을 말했는가?”**가 아니라 **“안전하고 제한된 과정으로 실제 검증 가능한 결과에 도달했고, 이전에 확보한 조건을 깨뜨리지 않았는가?”**까지 포함합니다.

## Terraform/IaC는 필수가 아닙니다

```text
IaC 환경        Proposal → Code/Config → Plan → PR → Approval
Non-IaC 환경    Proposal → Change Ticket → Console/API Procedure → Approval
운영 절차       Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid          Proposal → Script/Config/API → Controlled Pipeline/Operator
```

Loop Engineering은 이 실행 방식보다 상위 계층입니다. 공통으로 필요한 것은 Evidence, Risk, Blast Radius, Verification, Recovery, Independent Approval입니다.

## Safety Model

- 기본 출발점은 Read-only Evidence 수집입니다.
- Agent Hook은 Defense-in-depth이지 Security Boundary가 아닙니다.
- Production Mutation, Destructive Action, Authorization Expansion, Financial Commitment는 독립적으로 승인합니다.
- Loop를 반복한다고 Human Gate를 우회할 수 없습니다.
- Ticket 생성 권한과 Production 변경 권한을 분리합니다.
- Model은 Truth, Completion, Authorization, Production Control Plane의 소유자가 아닙니다.

## Reference Models

이 설계는 성숙한 Infrastructure Control Loop와 최근 Agent Loop 연구를 함께 사용합니다. 각 모델이 Repository 구조에 어떻게 반영됐는지는 [Reference Models](docs/REFERENCE-MODELS.md)에 정리했습니다.

| Reference Model | Harness에 반영한 부분 |
| --- | --- |
| IBM Loop Engineering | Goal/Action/Observation/Adjustment와 명시적 종료 기준 |
| LongHorizon-Harness | External State, Independently Verified Fact, Manage/Execute/Audit 분리 |
| LoopsBench | Long-horizon Eval과 Regression Obligation |
| Kubernetes Controllers | Desired vs Actual State Reconciliation |
| OpenGitOps | Declarative/Versioned State와 Continuous Reconciliation |
| Google SRE | SLI/SLO, Error Budget, Reliability Policy, Escalation |
| DORA | Baseline → Constraint → Improve → Check Progress → Repeat |
| FinOps Framework | Inform → Optimize → Operate → Measure → Repeat |
| MCP | Provider-neutral Evidence/Workflow Tool Boundary |
| Independent Approval | 고영향 작업의 Authorization Boundary |

주요 참고:

- IBM Loop Engineering: https://www.ibm.com/think/topics/loop-engineering
- LongHorizon-Harness: https://arxiv.org/abs/2608.01964
- LoopsBench: https://arxiv.org/abs/2608.00267
- Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/
- OpenGitOps: https://opengitops.dev/
- Google SRE: https://sre.google/sre-book/service-level-objectives/ , https://sre.google/workbook/error-budget-policy/
- DORA: https://dora.dev/guides/dora-metrics/
- FinOps: https://www.finops.org/framework/phases/
- Atlassian Rovo MCP: https://support.atlassian.com/atlassian-ai-gateway/docs/set-up-clients/
- Linear MCP: https://linear.app/docs/mcp

## 빠른 시작

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python -m unittest discover -s tests
```

## License

MIT
