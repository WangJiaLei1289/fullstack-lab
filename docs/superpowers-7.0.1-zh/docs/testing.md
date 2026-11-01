# 测试 Superpowers

Superpowers 有两类截然不同的测试，各自放在独立的目录里：

- **`tests/`** —— 插件的非 LLM 代码能不能正常工作？针对 brainstorm-server 的 JS、OpenCode 插件加载、codex-plugin 同步和分析工具的 bash + node + python 集成测试。
- **`evals/`** —— 代理在真实的 LLM 会话里行为是否正确？用 Python 测试框架驱动 Claude Code / Codex / Gemini CLI 的真实 tmux 会话，由 LLM 演员与验证者判定技能遵循情况。

## 插件测试

位于 `tests/`。目前包括：

- `tests/brainstorm-server/` —— brainstorm server JS 代码的 node 测试套件。
- `tests/opencode/` —— OpenCode 插件加载、bootstrap 缓存与工具注册的 bash 测试。
- `tests/codex-plugin-sync/` —— bash 同步校验。
- `tests/kimi/` —— Kimi 插件清单接线的 bash/Python 检查。
- `tests/claude-code/test-helpers.sh`、`analyze-token-usage.py` —— 其余 bash 测试用到的工具。
- `tests/claude-code/test-subagent-driven-development.sh` —— 代理能否描述 SDD 的测试（quorum 里没有对应项；它测的是描述回忆，不是行为）。
- `tests/claude-code/test-subagent-driven-development-integration.sh` —— 带 token 分析的扩展 SDD 集成测试（quorum 覆盖 YAGNI 子集；bash 还额外断言提交数、Claude Code 的任务追踪和 token 遥测）。
- `tests/claude-code/test-worktree-native-preference.sh` —— worktree 技能的 RED-GREEN-REFACTOR 验证（quorum 覆盖 PRESSURE 阶段；bash 还覆盖 RED/GREEN 基线）。
- `tests/explicit-skill-requests/` —— Haiku 专用、多轮、以及由技能名提示触发的测试，quorum 未覆盖。
- `tests/diagnosing-superpowers/test-skill-structure.sh` —— diagnosing-superpowers 技能的结构检查（frontmatter、被引用的文件、泄漏扫描、字数预算）；行为场景的评测记录由维护者保存在仓库之外。

用相关目录里的 `run-*.sh` 或 `npm test` 来跑插件测试。

## 技能行为评测

位于 `evals/`（即 [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/) 评测实验室，原名 Drill）。Quorum 是宿主环境 CLI——系统的一部分：它通过一个 Gauntlet QA 代理驱动真实的编程代理 CLI，依据每个场景的验收标准加上确定性的后置检查来打分。场景位于 `evals/scenarios/<name>/`。安装、容器运行时与安全模型见 `evals/README.md`。快速开始（本地应急运行）：

```bash
cd evals
bun install
export SUPERPOWERS_ROOT=/path/to/superpowers
bun run quorum run scenarios/triggering-test-driven-development --coding-agent claude
bun run quorum show <run-dir>
```

Quorum 场景很慢（每个 3–30 分钟以上），并且以宽松模式运行真实的 LLM 会话——请先读 `evals/README.md` 里的 Live Eval Risk 一节。只有静态门禁（`bun run check`、`bun run quorum check`）对公共 CI 是安全的；自然的下一步仍然是分层模型（PR 上跑静态门禁，夜间与按需跑真实会话扫描）。
