# 5분 Quickstart

[English](QUICKSTART.md) | **한국어** | [日本語](QUICKSTART.ja.md) | [简体中文](QUICKSTART.zh-CN.md)

Cloud Credential이나 Production 환경 없이 Infrastructure Engineering Agent를 바로 실행할 수 있습니다. Python 명령을 직접 작성하거나 기억할 필요도 없습니다.

> **현재 Research Preview Runtime:** 내부 구현은 Python 3를 사용하지만, 사용자 인터페이스는 `agent` 명령을 기본으로 합니다.

## macOS / Linux

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

## Windows

```powershell
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
agent.cmd setup
agent.cmd demo
```

`setup`은 현재 Research Preview dependency를 설치합니다. `demo`는 Repository에 포함된 fixture만 사용하며 Cloud account, Kubernetes cluster, Observability system, Production 환경에 연결하지 않습니다.

## `demo`가 하는 일

```text
Infrastructure Engineering Agent
        ↓
Reference Context Validation
        ↓
Resource Graph + Evidence Fixture
        ↓
SRE Dependency Saturation Scenario
        ↓
Safety / Consistency Check
        ↓
DEMO PASS / FAIL
```

성공한 demo는 deterministic Agent/Runtime contract와 scenario wiring이 일관된다는 의미입니다. Live AI Agent의 성능 향상을 증명하지 않습니다.

## 주요 명령

```text
./agent demo
    Credential 없는 빠른 체험

./agent validate
    Contributor용 전체 deterministic validation

./agent scenario evals/scenarios/sre-dependency-saturation.json
    특정 Scenario와 참조 fixture 검증

./agent doctor
    Local runtime/dependency 상태 확인

./agent setup
    Research Preview dependency 설치
```

Windows에서는 `./agent` 대신 `agent.cmd`를 사용합니다.

## PR 전 검증

```bash
./agent validate
```

## 다음 단계

- 실제 Incident Pattern 추가: `contrib/scenarios/README.md`
- 재현 가능한 Agent Run 제출: `validation-reports/README.md`
- Evidence/Discovery Adapter 추가: `CONTRIBUTING.md`
- Architecture 읽기: `docs/ARCHITECTURE.md`

현재 `demo`는 의도적으로 deterministic합니다. Live Agent 실행은 `source: live` Validation Report로 별도 기록하며, fixture 결과를 live Agent benchmark로 표현하지 않습니다.
\n기존 `./harness`와 `harness.cmd`는 내부 Harness 호환 진입점으로 Research Preview 동안 유지합니다.\n