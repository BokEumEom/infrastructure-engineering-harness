# Infrastructure Engineering Harness

[English](README.md) | **한국어**

Infrastructure Knowledge와 현재 Evidence를 구조화해 **검토 가능한 인프라 엔지니어링 판단**으로 연결하는 Provider-neutral, Cross-agent Harness입니다.

> **Infrastructure Knowledge → Context → Agent → Code/Proposal → Human Review → Infrastructure**

Claude Code 하나만을 위한 프로젝트가 아니라 **Codex, Kiro, Claude Code 및 `AGENTS.md` 기반 Agent**에서 재사용할 수 있도록 구성합니다. 핵심은 Terraform을 더 빨리 작성하는 것이 아니라 코드 앞단의 Architecture, Decision, 운영 이력, Policy, Evidence, Eval, Change Control을 Agent가 사용할 수 있는 형태로 만드는 것입니다.

## 왜 필요한가

Agent는 이미 IaC, Manifest, Script, Configuration을 빠르게 생성할 수 있습니다. 더 어려운 문제는 다음 질문에 답할 Context를 제공하는 것입니다.

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
                  Validation / Eval / PR
                             ▼
                       Human Approval
                             ▼
                      Infrastructure
```

자세한 구조는 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), Production 적용 단계는 [docs/PRODUCTION-READINESS.md](docs/PRODUCTION-READINESS.md)를 참고하세요.

## Agent 지원

### Codex

Repository root의 `AGENTS.md`를 기본 Operating Contract로 사용합니다. `AGENTS.md`에 모든 지식을 넣지 않고 `.infra-context/`의 구조화된 지식으로 안내하는 Map 역할을 하도록 설계했습니다.

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

## Provider-neutral Context Contract

각 프로젝트가 자신의 Knowledge를 관리합니다.

```text
.infra-context/
├── service-catalog.yaml
├── architecture/
├── adr/
├── incidents/
├── policies/
└── runbooks/
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

## Production Change Workflow

기본 Harness는 Production을 직접 변경하지 않고 Review 가능한 Proposal에서 멈춥니다.

```text
Evidence → Recommendation → Change Proposal → Plan/Validation → PR → Human Approval → Deployment
```

`schemas/change-proposal.schema.json`은 Evidence Reference, Risk, Blast Radius, Validation, Rollback, Approval을 요구합니다. [workflows/change-proposal.md](workflows/change-proposal.md)에 Workflow를 정의했습니다.

## Safety Model

Agent Hook은 Defense-in-depth이지 **Security Boundary가 아닙니다**. 실제 Production Enforcement는 Least-privilege IAM/RBAC, CI/CD Approval, Protected Branch, Policy-as-Code, Audit Log, Deployment Authorization처럼 모델 외부에서 강제해야 합니다.

Production Pilot은 Read-only 권한부터 시작하는 것을 권장합니다.

## 빠른 시작

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
python -m pip install -r requirements.txt
python scripts/validate_context.py examples/.infra-context
```

다른 Repository에 적용할 때는 `examples/.infra-context`를 복사한 뒤 해당 시스템에 맞게 수정합니다. Secret이나 민감한 Payload는 Context에 넣지 않습니다.

## Design Principles

1. Evidence before action
2. 전체 Knowledge를 한 번에 넣지 않는 Progressive Disclosure
3. ADR과 Incident History를 First-class Context로 관리
4. Cloud/Observability Vendor는 Core가 아니라 Adapter
5. Recommendation에 Provenance 포함
6. Production Change는 Reviewable하고 Reversible하게 설계
7. 실제 Authorization은 Agent 외부에서 독립적으로 강제
8. Agent의 판단을 Provider-neutral Eval로 Regression Test

## License

MIT
