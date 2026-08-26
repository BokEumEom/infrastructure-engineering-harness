# Infrastructure Engineering Harness

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Infrastructure Knowledge와 현재 Evidence를 **Infrastructure Engineering / SRE / DevOps / FinOps / Security**의 검토 가능한 Engineering Decision과 통제된 구현으로 연결하는 provider-neutral, cross-agent Harness입니다.

> **Knowledge → Context → Decision Skill → Capability → Loop → Verified Outcome → Learning → Next Loop**

> **상태: Research Preview.** Core contract, deterministic scenario, evaluation plumbing, Harness CLI는 현재 사용할 수 있습니다. Live adapter, persistent runtime, controlled execution은 아직 experimental 단계입니다.

## 먼저 실행해보기

전체 Architecture를 먼저 이해할 필요는 없습니다.

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./harness setup
./harness demo
```

Windows:

```powershell
harness.cmd setup
harness.cmd demo
```

자세한 내용: [한국어 Quickstart](QUICKSTART.ko.md)

`demo`는 Repository에 포함된 fixture만 사용합니다. Cloud account, Kubernetes cluster, production environment에는 연결하지 않습니다. `DEMO PASS`는 Harness contract와 scenario wiring이 일관된다는 의미이며, live AI Agent의 성능 향상을 증명하는 결과는 아닙니다.

## 무엇을 해결하는가

Agent는 이미 IaC, Configuration, Script, Pipeline, Runbook을 생성할 수 있습니다. 더 어려운 문제는 다음입니다.

- 무엇을 왜 변경해야 하는가
- 어떤 Evidence가 판단을 충분히 뒷받침하는가
- 어떤 Constraint / Trust Boundary를 지켜야 하는가
- 어떤 Skill / Capability를 선택해야 하는가
- 실행 후 실제 결과를 어떻게 독립적으로 검증할 것인가

```text
Organizational Knowledge + Live Environment
                    ↓
              Resource Graph
                    ↓
             Context Resolution
                    ↓
                Domain Lens
                    ↓
              Decision Skill
                    ↓
             Capability Routing
                    ↓
              Bound Capability
                    ↓
               Runtime Kernel
                    ↓
        Authorized External Execution
                    ↓
           Independent Verification
                    ↓
            Engineering Loop + Learn
```

## 핵심 구성

- **Domain** — Infrastructure / SRE / DevOps / FinOps / Security 관점
- **Decision Skill** — 무엇을 왜 해야 하는지 판단
- **Capability** — 어떻게 구현하거나 검증할지 선택
- **Resource Graph** — 실제 Resource와 Dependency를 provider-neutral 구조로 표현
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Session/Event Log, Tool Pipeline, Guard, Approval, Sandbox의 reference runtime
- **Engineering Loop** — Observe → Decide → Act/Propose → Verify → Learn
- **Skill Lift / Context Lift** — paired evaluation으로 Skill과 Context의 실제 기여 측정
- **Artifact Reflex** — Paperthin-inspired artifact hygiene, SSOT, eval integrity

## Safety 원칙

- Read-only Evidence 수집을 기본값으로 둡니다.
- Tool output을 자동으로 verified fact로 승격하지 않습니다.
- `verified_by: agent`를 허용하지 않습니다.
- Third-party `reference_only` Skill은 execution authority를 얻지 않습니다.
- Production mutation / destructive action / permission expansion / financial commitment는 독립적인 승인이 필요합니다.
- Fixture validation과 live Agent effectiveness를 명확히 구분합니다.

## 참여 방법

Framework 코드를 수정하지 않아도 기여할 수 있습니다.

- 실제 운영 경험을 비식별화해 [Scenario](contrib/scenarios/README.md)로 추가
- Agent를 실행하고 [Validation Report](validation-reports/README.md) 제출
- Kubernetes / Prometheus 같은 read-only Adapter 구현
- Skill Eval / negative case 추가
- Reference Model 제안

자세한 내용: [CONTRIBUTING.md](CONTRIBUTING.md)

## 언어 정책

English를 technical contract의 canonical source로 유지합니다. 한국어·일본어·중국어 README와 Quickstart는 first-class entry documentation으로 관리하고, CI에서 핵심 marker와 링크의 drift를 검사합니다.

[Localization policy](docs/LOCALIZATION.md)

## License

MIT
