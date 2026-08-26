# 5 分钟 Quickstart

[English](QUICKSTART.md) | [한국어](QUICKSTART.ko.md) | [日本語](QUICKSTART.ja.md) | **简体中文**

无需 Cloud credential 或 Production environment 即可体验 Harness，也不需要直接记忆或执行 Python 脚本路径。

> **当前 Research Preview runtime：** 内部实现仍使用 Python 3，但对用户暴露的稳定入口是 `harness` command。

## macOS / Linux

```bash
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
./harness setup
./harness demo
```

## Windows

```powershell
git clone https://github.com/BokEumEom/infrastructure-engineering-harness.git
cd infrastructure-engineering-harness
harness.cmd setup
harness.cmd demo
```

`setup` 安装当前 Research Preview dependency。`demo` 只使用仓库内 fixture，不会连接 Cloud account、Kubernetes cluster、Observability system 或 Production environment。

## `demo` 做什么

```text
Infrastructure Engineering Harness
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

成功的 demo 只证明 deterministic Harness contract 与 scenario wiring 一致，并不证明 live AI Agent 的性能提升。

## 常用命令

```text
./harness demo
    无 credential 的快速体验

./harness validate
    Contributor 使用的 deterministic validation

./harness scenario evals/scenarios/sre-dependency-saturation.json
    验证一个 Scenario 及其引用 fixture

./harness doctor
    查看 local runtime / dependency 状态

./harness setup
    安装 Research Preview dependency
```

Windows 使用 `harness.cmd` 替代 `./harness`。

## PR 前验证

```bash
./harness validate
```

## 下一步

- 添加真实 Incident pattern：`contrib/scenarios/README.md`
- 提交可复现 Agent run：`validation-reports/README.md`
- 添加 Evidence / Discovery Adapter：`CONTRIBUTING.md`
- 阅读 Architecture：`docs/ARCHITECTURE.md`

当前 `demo` 有意保持 deterministic。Live Agent execution 应使用 `source: live` Validation Report 单独记录，不能把 fixture result 当作 live benchmark。
