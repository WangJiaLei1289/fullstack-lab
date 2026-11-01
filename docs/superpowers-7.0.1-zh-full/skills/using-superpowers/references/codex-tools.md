## 派发子代理需要多代理能力

在你的 Codex 配置（`~/.codex/config.toml`）里加上：

```toml
[features]
multi_agent = true
```

这会启用 `dispatching-parallel-agents` 和 `subagent-driven-development` 这类技能所使用的多代理工具。
你能拿到哪些工具，取决于你的模型预设选中哪个多代理版本（当前预设跑 V2，旧预设跑 V1）。
当实际工具清单与任何表格（包括下面这张）冲突时，以实际工具清单为准。

- **派生（spawn）：** 用 `spawn_agent {fork_turns: "none"}` 给孩子一个干净的上下文；默认的 `"all"` 会把你的完整对话记录复制给孩子。
  在 Codex 0.145+ 上，`~/.codex/agents/` 下的角色文件会通过 `agent_type` 挂到隔离分支（isolated fork）上。
  全历史分支接受 `model` 和 `reasoning_effort` 覆盖（那里只有 `agent_type` 会被拒绝）——隔离分支是 SDD 的默认做法，目的是保持上下文干净，而不是因为覆盖需要它。
- **修复轮（fix rounds）：** 用 `followup_task` 恢复实现者——它会送达你的消息、触发一个回合，并透明地重新加载被宿主环境驱逐的孩子。
  绝不要因为「派生的代理没法再收到消息」这种猜测去重新派发一个实现者；在 V2 上它永远可以收到。
- **生命周期（lifecycle）：** V2 没有 `close_agent`。完成的孩子会在需要空位时被自动驱逐；不关闭它们没有成本。
  只有 V1 会话才有 `close_agent`——在那里，评审者返回评审结果后就关闭它们，每个实现者在其任务评审通过后关闭。
- **模型名：** 绝不要把技能、表格或旧会话里的模型名直接抄进 `spawn_agent`，除非先对照你当前的派生允许清单核验过——
  V2 只接受支持 V2 的预设，其余会直接报错。

## 等待孩子返回

`wait_agent` 是事件订阅，不是轮询：长等待会在孩子产生邮箱活动的那一刻醒来，延迟与短等待相同。
短超时轮询毫无收益，每次轮询还要花一次工具调用——以及一次上下文重新计费。在实测会话里，大约三分之二的等待调用都是超时的短轮询。

- 当你还有本地工作要做时，根本不要等待。完成的孩子最终答案会被推送到你的邮箱，并在你的下一个回合送达。
- 当你确实空闲、而孩子还在跑时，按有界的时间段等待：`wait_agent` 配 `timeout_ms` 300000-600000（5-10 分钟）。
  每段结束后——无论是醒来还是超时——发一行状态、运行 `list_agents`，并追问任何已完成却没有汇报的孩子。
  绝不要堆叠短于五分钟的轮询；事件订阅唤醒一个有界时间段的速度和短轮询一样快。
- 完成邮件唤不醒空闲的控制器（它被投递时不触发回合）；覆盖这段空闲窗口正是 `wait_agent` 唯一的职责。
  如果某一段等待超时且毫无活动，那是提示你去做收尾对齐，而不是去缩短下一段的等待时间。

## 派生时的模型路由

你发出的每一次 `spawn_agent`——包括你自己就是被派生出来、正在跑扇出的孩子——都必须按你正在执行的技能的模型选择规则，显式设置 `model` 和 `reasoning_effort`。
只设 `model` 是个陷阱：孩子的推理强度会静默重置为该模型的默认值，而不是你的值。

请你的搭档在 `~/.codex/config.toml` 里加一道机器级兜底，让任何漏掉的派生仍然落到一个刻意选择的层级上，而不是静默继承会话里最贵的模型：

```toml
[agents]
default_subagent_model = "<a mid-tier model from your spawn allowlist>"
default_subagent_reasoning_effort = "medium"
```

## 环境检测

会创建工作树或收尾分支的技能，应当先用只读的 git 命令检测环境，再继续：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → 已经在链接式工作树里（跳过创建）
- `BRANCH` 为空 → detached HEAD（无法从沙箱里建分支/推送/开 PR）

各技能如何使用这些信号，见 `using-git-worktrees` 第 0 步和 `finishing-a-development-branch` 第 1 步。

## Codex App 收尾

当沙箱阻止分支/推送操作时（在外部管理的工作树里处于 detached HEAD），代理应提交全部工作，并告知用户改用 App 的原生控件：

- **"Create branch"** —— 命名分支，然后通过 App 界面提交/推送/开 PR
- **"Hand off to local"** —— 把工作转移到用户本地的检出目录

代理仍可以跑测试、暂存文件，并输出建议的分支名、提交信息和 PR 描述供用户复制。
