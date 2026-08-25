# Infrastructure Engineering Harness

[English](README.md) | **한국어**

인프라 지식을 재사용 가능한 Agent Context로 구조화해, 더 안전한 인프라 분석과 변경 제안을 돕는 오픈소스 Claude Code Plugin입니다.

> **Infrastructure Knowledge → Context → Agent → Code → Infrastructure**

이 프로젝트의 목표는 Agent가 Terraform을 더 빠르게 작성하도록 만드는 것이 아닙니다. 중요한 것은 Agent가 **왜 특정 인프라 변경이 필요한지**, 어떤 제약이 있는지, 변경 전에 어떤 근거를 확인해야 하는지를 이해할 수 있도록 충분한 Context를 제공하는 것입니다.

## 이 저장소가 제공하는 것

- **Incident analysis Skill** — Architecture, Incident History, Runbook, Policy를 기반으로 증상을 분석하고, 근거를 확인한 뒤 Remediation을 제안합니다.
- **Terraform review Skill** — 서비스 중요도, Architecture Decision, Production Policy, 유지보수성을 기준으로 IaC 변경을 검토합니다.
- **Architecture review Skill** — 제안된 설계를 기존 Architecture Principle과 ADR에 맞춰 검토합니다.
- **Production guard Hook** — 일반적인 파괴적 인프라 명령을 차단하고 명시적인 Human Workflow를 요구합니다.
- **예제 `.infra-context/`** — Service Catalog, Architecture, ADR, Incident, Policy를 담을 수 있는 재사용 가능한 Context 구조를 제공합니다.
- **Eval fixture** — Agent의 판단 결과를 검증할 수 있도록 Machine-readable Incident Case를 제공합니다.

이 저장소는 조직별 Infrastructure Knowledge를 **Plugin 내부에 넣지 않습니다**. Plugin은 *어떻게 판단할 것인가*를 정의하고, 각 프로젝트는 `.infra-context/`에서 Agent가 판단에 사용할 Knowledge를 관리합니다.

## Architecture

```text
Infrastructure Knowledge
        │
        ├── Service catalog
        ├── Architecture
        ├── ADRs
        ├── Incident history
        └── Policies / runbooks
        │
        ▼
  .infra-context/
        │
        ▼
Claude Code Skills
        │
        ├── incident-analysis
        ├── terraform-review
        └── architecture-review
        │
        ▼
 Evidence + judgment
        │
        ▼
 Change proposal / Terraform
        │
        ▼
    Human review
        │
        ▼
 Infrastructure
```

## 빠른 시작

### 1. 저장소 Clone

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
```

### 2. 예제 Context를 프로젝트에 복사

```bash
cp -R examples/.infra-context /path/to/your-project/.infra-context
```

샘플 내용을 실제 환경에 맞는, 공개 가능한 Architecture Knowledge로 교체합니다.

### 3. Plugin 로컬 테스트

이 저장소의 상위 디렉터리에서 실행합니다.

```bash
claude --plugin-dir ./infrastructure-engineering-harness
```

Claude Code는 Plugin Manifest, Skills, Agent, Hooks를 자동으로 탐색합니다. Claude Code 공식 문서에서도 로컬 Plugin 테스트에 `--plugin-dir` 사용을 권장합니다.

### 4. Skills 사용

```text
/infra-harness:incident-analysis API latency가 증가했습니다. Production 변경을 제안하기 전에 원인을 분석하세요.

/infra-harness:terraform-review 현재 Terraform 변경을 Reliability, Security, Maintainability 관점에서 검토하세요.

/infra-harness:architecture-review 현재 Architecture Context와 ADR을 기준으로 Runtime Migration 제안을 검토하세요.
```

Skill description이 현재 작업과 일치하면 모델이 자동으로 Skill을 사용할 수도 있습니다.

## Context Contract

Harness를 사용하는 프로젝트는 Infrastructure Knowledge를 다음 구조로 관리하는 것을 권장합니다.

```text
.infra-context/
├── service-catalog.yaml
├── architecture/
│   └── <service>.md
├── adr/
│   └── ADR-<n>-<decision>.md
├── incidents/
│   └── INC-<n>-<incident>.md
├── policies/
│   └── production.md
└── runbooks/
    └── <scenario>.md
```

Skills는 **Progressive Context Loading** 방식을 사용합니다. 모든 문서를 처음부터 읽지 않고 Service Catalog에서 시작해 현재 작업에 필요한 Architecture, Incident, Policy, Runbook, ADR만 선택적으로 로드합니다.

## Knowledge와 Context를 분리하는 이유

사람이 가진 Knowledge는 이런 형태일 수 있습니다.

> "과거 Production Database에서 Burstable Instance의 CPU Credit이 고갈되면서 DB Latency가 증가한 장애가 있었다."

이를 Agent가 활용할 수 있는 Context로 만들면 다음과 같이 지속적으로 검색하고 재사용할 수 있는 정보가 됩니다.

```yaml
service: orders-api
criticality: high
known_incidents:
  - type: cpu-credit-exhaustion
    component: aurora-primary
policy:
  production_burstable_instances: avoid
```

중요한 것은 YAML 자체가 아닙니다. 미래의 Agent가 **현재 증거 + Architecture + 과거 Decision + Policy**를 함께 보고 변경을 제안할 수 있다는 점입니다.

## Guardrails

포함된 `PreToolUse` Hook은 다음과 같은 일반적인 파괴적 명령을 차단합니다.

- `terraform apply`
- `terraform destroy`
- `aws ... delete-*`
- 파괴적인 `kubectl delete`
- 명백한 Recursive Filesystem Delete

이 Guard는 의도적으로 보수적으로 구성되어 있으며 **Security Boundary가 아닙니다**. 실제 Production Control은 IAM, CI/CD Approval, Protected Branch, Policy-as-Code, Cloud Native Authorization 같은 계층에서 별도로 강제해야 합니다.

## Evaluation

`evals/incident/aurora-saturation.json`에는 기대하는 결론과 금지해야 하는 Recommendation을 포함한 최소 Incident Fixture가 있습니다.

표준 라이브러리만 사용하는 간단한 Checker도 포함되어 있습니다.

```bash
python scripts/check_eval_output.py \
  evals/incident/aurora-saturation.json \
  examples/eval-output/aurora-saturation-output.json
```

이 구조는 의도적으로 단순합니다. 핵심은 Infrastructure Agent를 단순히 **유효한 코드를 생성했는가**가 아니라 **올바른 판단을 했는가**로 평가해야 한다는 것입니다.

## Design Principles

1. **Evidence before action** — 충분한 근거 없이 Production 변경을 먼저 제안하지 않습니다.
2. **Progressive disclosure** — 현재 판단에 필요한 Context만 로드합니다.
3. **Decisions are first-class data** — ADR과 Incident History가 이후의 Recommendation에 영향을 주어야 합니다.
4. **Human approval for production** — Agent는 제안하고, Production Control은 사람이 명시적으로 승인합니다.
5. **Structured where useful, narrative where necessary** — Service Metadata는 YAML이 적합하지만 Architecture Reasoning은 Markdown이 더 적합할 수 있습니다.
6. **Context stays with the project** — 재사용 가능한 Reasoning은 Plugin에, 조직별 Knowledge는 Infrastructure Repository에 둡니다.

## 현재 범위

이 프로젝트는 완전한 Autonomous Infrastructure Platform이 아니라 **최소한으로 사용할 수 있는 Harness Foundation**을 목표로 합니다.

AWS, Datadog, GitHub Credential이나 MCP Server를 기본으로 포함하지 않습니다. 실제 Integration은 각 조직의 Access Model에 맞게 추가하는 것을 전제로 합니다.

향후 확장 방향으로는 Provider-neutral Schema, 더 풍부한 Eval Runner, MCP Integration Example, Policy-as-Code Adapter, Cost Review 및 Change-risk Analysis Skill 등을 고려할 수 있습니다.

## Compatibility

현재 Claude Code Plugin Layout을 따릅니다.

```text
.claude-plugin/plugin.json
skills/<name>/SKILL.md
agents/
hooks/hooks.json
```

참고 문서:

- Claude Code Plugins: https://code.claude.com/docs/en/plugins
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Agent Skills specification: https://agentskills.io/

## License

MIT
