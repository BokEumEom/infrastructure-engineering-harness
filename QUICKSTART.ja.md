# 5分 Quickstart

[English](QUICKSTART.md) | [한국어](QUICKSTART.ko.md) | **日本語** | [简体中文](QUICKSTART.zh-CN.md)

Cloud credential や Production environment がなくても Infrastructure Engineering Agent を試せます。Python コマンドを直接覚える必要もありません。

> **Current Research Preview runtime:** 内部実装は Python 3 を使用しますが、ユーザー向け interface は `agent` command を基本にします。

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

`setup` は Research Preview dependency をインストールします。`demo` は repository に含まれる fixture のみを使用し、Cloud account、Kubernetes cluster、Observability system、Production environment には接続しません。

## `demo` の内容

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

成功した demo は deterministic Agent / Runtime contract と scenario wiring の整合性を確認するものです。Live AI Agent の性能向上を証明するものではありません。

## 主なコマンド

```text
./agent demo
    credential-free の最短体験

./agent validate
    contributor 向け deterministic validation

./agent scenario evals/scenarios/sre-dependency-saturation.json
    1つの Scenario と参照 fixture を検証

./agent doctor
    local runtime / dependency 状態を表示

./agent setup
    Research Preview dependency をインストール
```

Windows では `./agent` の代わりに `agent.cmd` を使用します。

## PR 前の検証

```bash
./agent validate
```

## 次のステップ

- Incident pattern の追加: `contrib/scenarios/README.md`
- 再現可能な Agent run の提出: `validation-reports/README.md`
- Evidence / Discovery Adapter の追加: `CONTRIBUTING.md`
- Architecture: `docs/ARCHITECTURE.md`

現在の `demo` は意図的に deterministic です。Live Agent execution は `source: live` Validation Report として別に記録し、fixture result を live benchmark として扱いません。
\nLegacy compatibility として `./harness` / `harness.cmd` も Research Preview 中は維持します。\n