# Infrastructure Engineering Agent

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

Infrastructure / Operations / DevOps / SRE / FinOps / Security の業務を調査・レビュー・計画・検証する provider-neutral な **Infrastructure Engineering Agent** です。Harness は製品名ではなく、Agent 内部の Runtime / Control Plane を指します。

> **Agent の判断は自由にし、authority と truth は Runtime boundary で制約する。**

> **Status: Research Preview.** Core contracts、deterministic scenarios、evaluation plumbing、Agent CLI は利用できます。Live adapters、persistent runtime、controlled execution はまだ experimental です。

## まず試す

アーキテクチャ全体を理解する必要はありません。

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

Windows:

```powershell
agent.cmd setup
agent.cmd demo
```

詳細: [日本語 Quickstart](QUICKSTART.ja.md)

`demo` は checked-in fixture のみを使用し、Cloud account / Kubernetes cluster / production environment には接続しません。`DEMO PASS` は Harness contract の整合性を示すだけで、live AI agent の性能向上を証明するものではありません。

## 何を解決するか

Agent はすでに IaC、設定、script、pipeline、runbook を生成できます。難しいのは次の部分です。

- 何を、なぜ変更するべきか
- どの Evidence が判断を支えるか
- どの制約・trust boundary を守るか
- どの Skill / Capability を使うか
- 実行結果をどう独立検証するか

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

## 主要コンポーネント

- **Agent Contract** — Agent の role / authority / backend / completion boundary\n- **Domain** — Infrastructure / Operations / SRE / DevOps / FinOps / Security の lens
- **Decision Skill** — 何をなぜ行うべきかを判断
- **Capability** — 実装・検証方法を選択
- **Resource Graph** — 実環境の resource / dependency を provider-neutral に表現
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Session/Event Log、Tool Pipeline、Guard、Approval、Sandbox の reference runtime
- **Engineering Loop** — Observe → Decide → Act/Propose → Verify → Learn
- **Skill Lift / Context Lift** — Skill と Context の実際の寄与を paired evaluation で測定
- **Artifact Reflex** — Paperthin-inspired artifact hygiene、SSOT、eval integrity

## Safety の原則

- read-only evidence collection をデフォルトにする
- tool output を自動的に verified fact としない
- `verified_by: agent` を認めない
- third-party `reference_only` Skill に execution authority を与えない
- production mutation / destructive action / permission expansion / financial commitment は独立した承認を必要とする
- fixture validation と live agent effectiveness を区別する

## 参加方法

Framework code を変更しなくても参加できます。

- 実運用経験を匿名化した [Scenario](contrib/scenarios/README.md) として追加
- Agent を実行して [Validation Report](validation-reports/README.md) を提出
- Kubernetes / Prometheus などの read-only Adapter を実装
- Skill Eval / Harness Lift / negative case を追加
- Reference Model を提案

詳細: [CONTRIBUTING.md](CONTRIBUTING.md)

## 言語ポリシー

English は technical contract の canonical source です。日本語・韓国語・简体中文では README と Quickstart を first-class entry documentation として維持し、CI で主要な marker と link の drift を検出します。

[Localization policy](docs/LOCALIZATION.md)

## License

MIT
\nLegacy compatibility として `./harness` / `harness.cmd` も Research Preview 中は維持します。\n