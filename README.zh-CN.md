# Infrastructure Engineering Agent

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

这是一个 provider-neutral 的 **Infrastructure Engineering Agent**，用于调查、审查、规划和验证 Infrastructure / Operations / DevOps / SRE / FinOps / Security 工作。Harness 不再是产品身份，而是 Agent 内部的 Runtime / Control Plane。

> **让 Agent 自由判断，在 Runtime boundary 约束 authority 与 truth。**

> **状态：Research Preview。** Core contracts、deterministic scenarios、evaluation plumbing 与 Agent CLI 已可使用；live adapters、persistent runtime 与 controlled execution 仍处于 experimental 阶段。

## 先运行起来

不需要先理解完整架构。

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

`demo` 只使用仓库内 fixture，不会连接 Cloud account、Kubernetes cluster 或 production environment。`DEMO PASS` 仅说明 Harness contract 与 scenario wiring 一致，并不证明 live AI agent 的性能更好。

## 它解决什么问题

Agent 已经可以生成 IaC、配置、脚本、pipeline 和 runbook。更难的问题是：

- 应该改什么，为什么改
- 哪些 Evidence 足以支持判断
- 必须遵守哪些 constraint / trust boundary
- 应该选择哪个 Skill / Capability
- 执行后如何进行独立验证

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

## 核心组件

- **Agent Contract** — Agent 的角色、权限、Backend 与完成边界\n- **Domain** — Infrastructure / Operations / SRE / DevOps / FinOps / Security 的工程视角
- **Decision Skill** — 判断应该做什么以及为什么
- **Capability** — 选择如何实现或验证
- **Resource Graph** — provider-neutral 的实际资源与依赖关系
- **Bound Capability** — Capability + Resource Scope + Permission Scope + Evidence Source
- **Runtime Kernel** — Session/Event Log、Tool Pipeline、Guard、Approval、Sandbox 的 reference runtime
- **Engineering Loop** — Observe → Decide → Act/Propose → Verify → Learn
- **Skill Lift / Context Lift** — 通过 paired evaluation 衡量 Skill / Context 的实际贡献
- **Artifact Reflex** — Paperthin-inspired artifact hygiene、SSOT 与 eval integrity

## Safety 原则

- 默认从 read-only evidence collection 开始
- tool output 不会自动成为 verified fact
- 不允许 `verified_by: agent`
- third-party `reference_only` Skill 不获得 execution authority
- production mutation / destructive action / permission expansion / financial commitment 需要独立授权
- fixture validation 与 live agent effectiveness 必须明确区分

## 如何参与

不修改 framework code 也可以贡献：

- 把真实运维经验匿名化为 [Scenario](contrib/scenarios/README.md)
- 运行 Agent 并提交 [Validation Report](validation-reports/README.md)
- 实现 Kubernetes / Prometheus 等 read-only Adapter
- 增加 Skill Eval / Harness Lift / negative case
- 提议新的 Reference Model

详细说明：[CONTRIBUTING.md](CONTRIBUTING.md)

## 语言策略

English 是 technical contract 的 canonical source。中文、韩文和日文的 README 与 Quickstart 作为 first-class entry documentation 维护，CI 会检查关键 marker 与链接是否发生 drift。

[Localization policy](docs/LOCALIZATION.md)

## License

MIT
\n兼容入口 `./harness` / `harness.cmd` 在 Research Preview 期间继续保留。\n