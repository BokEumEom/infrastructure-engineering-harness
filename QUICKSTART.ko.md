# 5분 Quickstart

[English](QUICKSTART.md) | **한국어** | [日本語](QUICKSTART.ja.md) | [简体中文](QUICKSTART.zh-CN.md)

Cloud Credential이나 Production 환경 없이 Infrastructure Engineering Agent를 실행할 수 있습니다. Python 명령을 직접 작성하거나 기억할 필요도 없습니다.

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

`setup`은 Research Preview dependency를 설치합니다. `demo`는 Repository의 fixture만 사용하며 Cloud account, Kubernetes cluster, Observability system, Production 환경에는 연결하지 않습니다.

## `demo`가 하는 일

```text
Infrastructure Engineering Agent
        ↓
Reference Context Validation
        ↓
Resource Graph + Evidence Fixture
        ↓
Scenario Contract Validation
        ↓
DEMO PASS / FAIL
```

`demo` 성공은 deterministic contract와 fixture wiring이 일관된다는 뜻입니다. Live model을 실행하거나 live Agent 성능을 검증하는 명령은 아닙니다.

## Scenario로 Reference Agent 실행하기

```bash
./agent scenario evals/scenarios/sre-dependency-saturation.json
```

이제 기본 `scenario` 명령은 파일 구조만 검사하고 끝나지 않습니다. Reference Agent Orchestrator를 실제로 통과합니다.

```text
Scenario
   ↓
Context + Resource Graph
   ↓
Deterministic Fixture Model
   ↓
evidence.list
   ↓
evidence.read
   ↓
Assessment
   ↓
Independent Verification
   ↓
Scenario Scorer
   ↓
Fixture Runtime Recording
```

`ground_truth`, `required_evidence`, `success_conditions` 같은 evaluator 전용 정보는 Model-visible Context에 넣지 않습니다. Fixture model은 먼저 `evidence.list`로 사용 가능한 증거를 발견하고, `evidence.read`로 읽은 결과를 기반으로 assessment를 생성합니다.

단, 이것은 여전히 **credential-free deterministic fixture run**입니다. 실제 Claude/OpenAI 모델이나 AWS/Kubernetes 운영 환경의 성능 검증을 의미하지 않습니다.

## Scenario 명령

```text
./agent scenario <path>
    Reference Orchestrator로 Scenario를 실행하고 결과를 평가

./agent scenario run <path>
    위 기본 실행을 명시적으로 수행

./agent scenario eval <path>
    실행 후 scorer의 세부 판정까지 출력

./agent scenario check <path>
    Scenario/fixture 참조 무결성만 검사. Agent Turn은 실행하지 않음
```

## 주요 명령

```text
./agent demo
    Credential 없는 빠른 contract demo

./agent validate
    Contributor용 전체 deterministic validation

./agent scenario evals/scenarios/sre-dependency-saturation.json
    Fixture Scenario를 Reference Agent Orchestrator로 실행

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

Fixture recording은 `source: fixture`를 사용합니다. 실제 Agent 실행은 이후 `source: live` 검증 단계에서 별도로 다루며, fixture 결과를 live Agent benchmark로 표현하지 않습니다.

기존 `./harness`와 `harness.cmd`는 내부 Harness 호환 진입점으로 Research Preview 동안 유지합니다.
