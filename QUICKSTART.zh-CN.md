# 5 分钟 Quickstart

[English](QUICKSTART.md) | [한국어](QUICKSTART.ko.md) | [日本語](QUICKSTART.ja.md) | **简体中文**

无需 Cloud credential 或 Production environment 即可体验 Infrastructure Engineering Agent，也不需要直接记忆或执行 Python 脚本路径。

> **当前 Research Preview runtime：** 内部实现仍使用 Python 3，但对用户暴露的默认入口是 `agent` command。

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

`setup` 安装当前 Research Preview dependency。`demo` 只使用仓库内 fixture，不会连接 Cloud account、Kubernetes cluster、Observability system 或 Production environment。

## `demo` 做什么

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

成功的 demo 只证明 deterministic Agent / Runtime contract 与 scenario wiring 一致，并不证明 live AI Agent 的性能提升。

## 常用命令

```text
./agent demo
    无 credential 的快速体验

./agent validate
    Contributor 使用的 deterministic validation

./agent scenario evals/scenarios/sre-dependency-saturation.json
    验证一个 Scenario 及其引用 fixture

./agent doctor
    查看 local runtime / dependency 状态

./agent setup
    安装 Research Preview dependency
```

Windows 使用 `harness.cmd` 替代 `./harness`。

## PR 前验证

```bash
./agent validate
```

## 下一步

- 添加真实 Incident pattern：`contrib/scenarios/README.md`
- 提交可复现 Agent run：`validation-reports/README.md`
- 添加 Evidence / Discovery Adapter：`CONTRIBUTING.md`
- 阅读 Architecture：`docs/ARCHITECTURE.md`

当前 `demo` 有意保持 deterministic。Live Agent execution 应使用 `source: live` Validation Report 单独记录，不能把 fixture result 当作 live benchmark。
\n兼容入口 `./harness` / `harness.cmd` 在 Research Preview 期间继续保留。\n