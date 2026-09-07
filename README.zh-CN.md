# Infrastructure Engineering Agent

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

这是一个 provider-neutral 的 **Infrastructure Engineering Agent**，用于调查、审查、规划和验证 Infrastructure / Operations / DevOps / SRE / FinOps / Security 工作。

> **让 Agent 自由判断，让 Orchestrator 负责执行流程，并在 Harness / Control Plane 边界约束 authority 与 truth。**

> **状态：Research Preview。** Agent contract、reference Turn Runtime、Skills、Resource Graph、deterministic scenarios、evaluation plumbing 与 Agent CLI 已可使用；live adapters、persistent production runtime 与 controlled execution 仍处于 experimental 阶段。

## 先运行起来

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./agent setup
./agent demo
```

Windows：

```powershell
agent.cmd setup
agent.cmd demo
```

详细说明：[中文 Quickstart](QUICKSTART.zh-CN.md)

`demo` 只使用 fixture，不会连接 Cloud account、Kubernetes cluster 或 production environment。`DEMO PASS` 只证明 deterministic contract plumbing 一致，并不证明 live Agent effectiveness。

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

- Agent 负责 reasoning 与 next-action judgment。
- Orchestrator 负责 Turn lifecycle 与 model/tool flow。
- Harness / Control Plane 负责 provenance、permission、approval、change safety。
- Independent Verification 负责确认 outcome。

Orchestrator 不拥有 truth，也不拥有 production authority。

## Model-visible surface

模型默认只需要理解三个主要概念：

```text
Context
Skills
Tools
```

Domain / Capability / Binding / Workflow / Loop 主要是 runtime 内部 metadata，不是强制 reasoning chain。

## 核心组件

- **Agent Orchestrator / Turn Runtime** — 所有 channel 进入同一个 Turn lifecycle
- **Context Pack** — 带 provenance / freshness / evidence gap 的 bounded context
- **Skills / Tools** — 按需 progressive 暴露的 guidance / action
- **Capability Registry** — source / trust / risk / availability metadata
- **Resource Graph** — provider-neutral 的 resource / dependency / discovery provenance
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Event Log / Tool Pipeline / Guard / Approval / State reference primitives
- **Harness / Control Plane** — provenance / scope / approval / change control / audit / recording
- **Engineering Loop** — 只有在需要 repeated external-state reconciliation 时使用
- **Skill Lift / Context Lift / Harness Lift** — 评估 Agent guidance 的实际贡献
- **Artifact Reflex** — Paperthin-inspired artifact hygiene / SSOT / eval integrity

## Runtime Event Log

```text
Runtime Event Log
  ├─ Trace / Span
  ├─ Latency / Cache Metrics
  ├─ Recording
  └─ Evaluation
```

append-only Runtime Event Log 是 execution SSOT。Trace、Metrics、Recording 不应成为独立 truth store，而应关联或派生自同一份 runtime history。

## Safety

- 默认 authority 是 read-only discovery / evidence collection
- mutation target 需要 trusted Resource Provenance 和 bound scope
- tool output 不会自动成为 Verified Fact
- 不允许 `verified_by: agent`
- chat text / Orchestrator state / channel / delegate 不是 production authorization
- approval 绑定 exact staged revision，并在 apply 前重新验证
- destructive / privilege-expanding / financial / production-impacting action 需要 independent authorization

## Reference Models

Primary references：

- Anthropic Commerce Agents — Agent product / model-tool loop / Backend / runtime safety
- Anthropic Context Engineering — minimal context / progressive disclosure / unhobbling
- Samsung Account AgentCore AIOps — observability / channel convergence / task evaluation / scale-out
- Kubernetes Controllers + LongHorizon-Harness — reconciliation / external task state
- NVIDIA ACES / SkillEvaluator — artifact/effect evaluation

Supporting references 包括 DeepSeek Harness、GBrain、Backpass、Paperthin、LoopsBench、MCP/OpenGitOps。Google SRE / DORA / FinOps 用作 engineering domain truth。

> **Reference widely, expose narrowly.**

详细说明：[docs/REFERENCE-MODELS.md](docs/REFERENCE-MODELS.md)

## 如何参与

- 把真实运维经验匿名化为 [Scenario](contrib/scenarios/README.md)
- 运行 Agent 并提交 [Validation Report](validation-reports/README.md)
- 实现 read-only Adapter
- 增加 Skill Eval / Harness Lift / negative case
- 提议新的 Reference Model

详细说明：[CONTRIBUTING.md](CONTRIBUTING.md)

## 语言策略

English 是 machine-readable technical contract 的 canonical source。中文、韩文和日文 README / Quickstart 作为 first-class entry documentation 维护。

[Localization policy](docs/LOCALIZATION.md)

## License

MIT
