# Infrastructure Engineering Harness

[English](README.md) | **한국어**

Infrastructure Knowledge와 현재 Evidence를 구조화해 **Infrastructure Engineering, SRE, DevOps, FinOps의 검토 가능한 Engineering Decision**으로 연결하는 Provider-neutral, Cross-agent Harness입니다.

> **Infrastructure Knowledge → Context → Agent → Decision/Proposal → Human Review → Infrastructure**

**Codex, Kiro, Claude Code 및 Repository-aware Agent**에서 사용할 수 있으며 특정 Cloud, Runtime, Terraform, Kubernetes, Datadog, CI/CD, Cost 또는 Ticketing Platform을 전제로 하지 않습니다.

## 왜 필요한가

Agent는 IaC, Configuration, Script, Runbook, 운영 절차를 빠르게 만들 수 있습니다. 더 어려운 문제는 **무엇을 왜 바꿔야 하는지, 어떤 Evidence가 있는지, 어떤 제약을 지켜야 하는지** 판단하는 것입니다.

이 Harness는 Architecture, ADR, Incident, 운영 Policy, Reliability Objective, Delivery Rule, Cost Ownership과 현재 Evidence를 Agent가 사용할 수 있는 Context로 만듭니다.

## 구조

```text
Durable Knowledge + Optional Live Evidence
                    ↓
              Context Resolution
                    ↓
               Harness Core
                    ↓
      ┌─────────────┼─────────────┐
Infrastructure     SRE          DevOps        FinOps
Architecture   Reliability    Delivery      Cost/Value
Capacity       SLO/Budget     Recovery      Allocation
Failure modes  Incident       Stability     Unit Economics
      └─────────────┼─────────────┘
                    ↓
          Evidence-based Decision
                    ↓
              Change Proposal
                    ↓
       Validation / Eval / Review
                    ↓
 PR / Ticket / Runbook / Controlled Procedure
                    ↓
              Human Approval
                    ↓
                Execution
```

자세한 내용은 [Architecture](docs/ARCHITECTURE.md), [Production Readiness](docs/PRODUCTION-READINESS.md)를 참고하세요.

## Domain Packs

공통 Core 위에 네 가지 Engineering Lens를 제공합니다.

| Pack | 주요 용도 | 추가 Context |
| --- | --- | --- |
| [Infrastructure](domains/infrastructure/README.md) | Architecture, Capacity, Migration, Dependency, Change Risk | Architecture, ADR, Runtime/Capacity Evidence |
| [SRE](domains/sre/README.md) | SLI/SLO, Error Budget, Incident, Reliability, Toil | `domains/sre.yaml` |
| [DevOps](domains/devops/README.md) | Build/Release/Deployment, Rollback, Delivery Performance | `domains/devops.yaml` |
| [FinOps](domains/finops/README.md) | Allocation, Usage Efficiency, Commitment, Unit Economics | `domains/finops.yaml` |

여러 영역이 얽힌 결정은 Pack을 함께 사용합니다. 비용 절감안이 SLO를 훼손한다면 이를 하나의 모호한 결론으로 합치지 않고 **FinOps Opportunity와 SRE Constraint를 각각 드러냅니다.**

## Agent 지원

### Codex

Root `AGENTS.md`를 Operating Contract로 사용하며 Task에 맞는 Domain Pack과 Context를 선택합니다.

### Kiro

`AGENTS.md`와 함께 `.kiro/steering/infrastructure-harness.md`를 Workspace Steering Adapter로 제공합니다.

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
```

## 사용 방식

### A. Embedded Context

Service 또는 Infrastructure Repository 안에서 Context를 함께 관리합니다.

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

예시:

```text
.infra-context를 사용해 현재 Latency Incident를 분석해줘.
Infrastructure와 SRE 관점으로 보고 Evidence와 가정을 분리해. Production 변경은 실행하지 마.
```

### B. Central Harness / Platform Workspace

Service Repository를 변경하지 않고 Platform/SRE/Infrastructure 팀이 중앙에서 Context를 운영합니다.

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

예시:

```text
contexts/payment-platform을 사용해 분석해줘.
이번 Capacity 감소안은 Cost와 Reliability에 모두 영향을 주므로 Infrastructure, SRE, FinOps Pack을 사용해.
외부 시스템은 Read-only로 보고 Evidence가 충분한 경우에만 Change Proposal을 작성해.
```

[Central Context Example](examples/central-context/README.md)도 제공합니다.

## 실제 예시: 하나의 변경을 네 관점으로 보기

Traffic은 안정적이고 Capacity Headroom이 크며, 99.9% SLO와 Error Budget은 건강하고, Rollback 가능한 Deployment Path가 있지만 월 비용이 증가했다고 가정합니다.

- **Infrastructure**: 실제 Over-capacity인지, Capacity 감소가 Failure Mode를 바꾸는지 확인
- **SRE**: 감소 후에도 SLO와 Error Budget Policy를 만족할 수 있는지 확인
- **DevOps**: Rollout, Validation, Rollback, Failed Deployment Recovery 검토
- **FinOps**: Unit Cost, Allocation, 예상 절감액, Engineering Effort/Risk 검토

최종 Proposal에는 각 관점의 Evidence와 Trade-off가 함께 남습니다.

## Context Schema와 Validation

Service Catalog, Incident, ADR, Policy, Evidence, Change Proposal, Ticket Request/Policy, Domain Profile, Eval Suite를 Machine-readable Schema로 제공합니다.

```bash
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

## Live Evidence Adapter는 선택 사항

현재 상태가 필요한 경우에만 Read-only Adapter를 붙입니다.

Prometheus, OpenTelemetry Backend, Datadog, Cloud-native Monitoring, Runtime API, Source Control, Deployment History, SLO Tool, Cost/Usage System, Business Metric 등을 사용할 수 있습니다. **Datadog은 필수가 아닙니다.** 결과는 `schemas/evidence.schema.json`으로 Normalize합니다.

## MCP 기반 Jira / Linear 티켓 자동화

Ticket 생성은 Harness 안에 Jira REST API나 Linear GraphQL API 코드를 넣는 방식이 아니라 **공식 Remote MCP Server를 사용하는 Workflow Action**으로 설계했습니다.

```text
Incident / Review / Change Proposal
              ↓
         Ticket Request
              ↓
      Policy + Deduplication
              ↓
      Official Remote MCP Server
        ├─ Atlassian Rovo MCP
        └─ Linear MCP
              ↓
        Search → Create/Update
```

Harness가 담당하는 것은 Provider-neutral 규칙입니다.

- `schemas/ticket-request.schema.json` — 어떤 업무를 Ticket으로 만들 것인지
- `schemas/ticket-policy.schema.json` — `disabled`, `manual`, Policy 기반 `auto_create`
- 안정적인 SHA-256 Fingerprint를 이용한 중복 방지
- 항상 Search-before-create
- 생성 Ticket에 Evidence / Source Reference 포함

실제 인증, 권한, Jira/Linear Tool 호출은 각 Provider의 MCP Server가 담당합니다.

예시 Policy:

```yaml
mode: policy
default_action: manual
rules:
  - id: high-severity-incident
    when:
      kinds: [incident]
      severities: [sev1, sev2]
    action: auto_create
    require_evidence: true
    min_evidence: 2
```

이렇게 하면 충분한 Evidence가 있는 SEV1/SEV2 Incident Follow-up은 자동 생성하면서 FinOps Optimization이나 Architecture 개선안은 Manual로 유지할 수 있습니다.

예제에서 사용하는 공식 MCP Endpoint:

```text
Atlassian Rovo MCP  https://mcp.atlassian.com/v1/mcp/authv2
Linear read/write  https://mcp.linear.app/mcp
Linear read-only   https://mcp.linear.app/mcp/readonly
```

자세한 내용은 [MCP 연결](mcp/README.md), [Ticketing Workflow](workflows/ticketing.md), [Ticketing Adapter](adapters/actions/ticketing/README.md)를 참고하세요.

## Provider-neutral Eval

- `evals/standard/`의 30개 Incident Scenario
- Infrastructure Domain Eval
- SRE Error Budget / Reliability Eval
- DevOps Delivery / Recovery Eval
- FinOps Allocation / Unit Economics Eval

예시:

```bash
python scripts/check_domain_eval.py \
  evals/domains/sre.json \
  error-budget-exhausted \
  examples/eval-output/domain-sre-error-budget.json
```

## Terraform/IaC는 필수가 아닙니다

환경에 따라 Review Artifact가 달라집니다.

```text
IaC 환경        Proposal → Code/Config → Plan → PR → Approval
Non-IaC 환경    Proposal → Change Ticket → Console/API Procedure → Approval
운영 절차       Proposal → Reviewed Runbook → Maintenance Window → Approval
Hybrid          Proposal → Script/Config/API → Controlled Pipeline/Operator
```

공통으로 필요한 것은 Terraform이 아니라 **Evidence, Risk, Blast Radius, Validation, Recovery, Independent Approval**입니다.

## Safety Model

Agent Hook은 Defense-in-depth이며 Security Boundary가 아닙니다. 실제 Production Enforcement는 IAM/RBAC, Deployment/Change Approval, Policy-as-Code, Protected Branch, Audit System 등 모델 외부에서 독립적으로 강제해야 합니다.

Ticket 생성 권한과 Production 변경 권한은 분리합니다. Ticket 자동화를 켰다는 이유로 광범위한 MCP Write Tool을 Auto-approve하지 않습니다.

## 빠른 시작

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
python -m unittest discover -s tests
```

## 참고 모델

- Google SRE — SLO / Error Budget: https://sre.google/sre-book/service-level-objectives/
- DORA Software Delivery Performance: https://dora.dev/insights/dora-metrics-history/
- FinOps Framework: https://www.finops.org/framework/
- Atlassian Rovo MCP: https://support.atlassian.com/atlassian-ai-gateway/docs/set-up-clients/
- Linear MCP: https://linear.app/docs/mcp

## License

MIT
