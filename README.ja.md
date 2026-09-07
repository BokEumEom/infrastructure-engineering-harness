# Infrastructure Engineering Agent

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

Infrastructure / Operations / DevOps / SRE / FinOps / Security の業務を調査・レビュー・計画・検証する provider-neutral な **Infrastructure Engineering Agent** です。

> **Agent の判断は自由にし、実行フローは Orchestrator が調整し、authority と truth は Harness / Control Plane で制約する。**

> **Status: Research Preview.** Agent contract、reference Turn Runtime、Skills、Resource Graph、deterministic scenarios、evaluation plumbing、Agent CLI は利用できます。Live adapters、persistent production runtime、controlled execution は experimental です。

## まず試す

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

`demo` は fixture のみを使用し、Cloud account / Kubernetes cluster / production environment には接続しません。`DEMO PASS` は deterministic contract plumbing の整合性を示すだけで、live Agent の有効性を証明しません。

## Architecture

```text
CLI / Web / Slack / GitHub / MCP / API
                    ↓
          Agent Orchestrator / Turn Runtime
                    ↓
          Context + Memory + Skills + Tools
                    ↓
       Infrastructure Engineering Agent
                    ↓
              Model Judgment
                    ↓
               Tool Executor
                    ↓
          Harness / Control Plane
 Provenance · Scope · Guard · Approval · Audit
          Change Control · Recording
                    ↓
            Capability Backends
                    ↓
 AWS / K8s / CI/CD / Observability / Cost / Security
                    ↓
          Independent Verification
             ↙              ↘
           done       reconcile if needed
                           ↓
                    Engineering Loop
```

- Agent は reasoning と next-action judgment を担当します。
- Orchestrator は Turn lifecycle と model/tool flow を担当します。
- Harness / Control Plane は provenance、permission、approval、change safety を担当します。
- Independent Verification が outcome を確認します。

Orchestrator は truth や production authority を所有しません。

## Model-visible surface

モデルが基本的に見るのは次の 3 つです。

```text
Context
Skills
Tools
```

Domain / Capability / Binding / Workflow / Loop は内部 metadata です。固定の routing chain を必須にしません。

## 主要コンポーネント

- **Agent Orchestrator / Turn Runtime** — すべての channel を一つの Turn lifecycle に統合
- **Context Pack** — provenance / freshness / gap を含む bounded context
- **Skills / Tools** — progressive に公開される guidance / action
- **Capability Registry** — source / trust / risk / availability metadata
- **Resource Graph** — provider-neutral な resource / dependency / discovery provenance
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Event Log / Tool Pipeline / Guard / Approval / State の reference primitives
- **Harness / Control Plane** — provenance / scope / approval / change control / audit / recording
- **Engineering Loop** — repeated external-state reconciliation が必要な場合だけ利用
- **Skill Lift / Context Lift / Harness Lift** — Agent guidance の効果を評価
- **Artifact Reflex** — Paperthin-inspired artifact hygiene / SSOT / eval integrity

## Runtime Event Log

```text
Runtime Event Log
  ├─ Trace / Span
  ├─ Latency / Cache Metrics
  ├─ Recording
  └─ Evaluation
```

append-only Runtime Event Log が execution SSOT です。Trace、Metrics、Recording は別の truth store ではなく、同じ runtime history に関連付けます。

## Safety

- read-only discovery / evidence collection が default authority
- mutation target は trusted Resource Provenance と bound scope が必要
- tool output は自動的に Verified Fact にならない
- `verified_by: agent` は無効
- chat text / Orchestrator state / channel / delegate は production authorization ではない
- approval は exact staged revision に binding され、apply 前に revalidate される
- destructive / privilege-expanding / financial / production-impacting action は independent authorization が必要

## Reference Models

Primary references:

- Anthropic Commerce Agents — Agent product / model-tool loop / Backend / runtime safety
- Anthropic Context Engineering — minimal context / progressive disclosure / unhobbling
- Samsung Account AgentCore AIOps — observability / channel convergence / task evaluation / scale-out
- Kubernetes Controllers + LongHorizon-Harness — reconciliation / external task state
- NVIDIA ACES / SkillEvaluator — artifact/effect evaluation

Supporting references include DeepSeek Harness、GBrain、Backpass、Paperthin、LoopsBench、MCP/OpenGitOps。Google SRE / DORA / FinOps は engineering domain truth の基準です。

> **Reference widely, expose narrowly.**

詳細: [docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md)

## 参加

- 実運用経験を匿名化した [Scenario](contrib/scenarios/README.md) を追加
- Agent を実行して [Validation Report](validation-reports/README.md) を提出
- read-only Adapter を実装
- Skill Eval / Harness Lift / negative case を追加
- Reference Model を提案

詳細: [CONTRIBUTING.md](CONTRIBUTING.md)

## 言語ポリシー

English が machine-readable technical contract の canonical source です。日本語・韓国語・简体中文 README / Quickstart は first-class entry documentation として維持します。

[Localization policy](docs/LOCALIZATION.md)

## License

MIT
