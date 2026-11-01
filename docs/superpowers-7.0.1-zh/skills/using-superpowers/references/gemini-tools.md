# Gemini CLI 工具映射

技能用动作说话（「派发一个子代理」「建一个待办」「读一个文件」）。在 Gemini CLI 上，这些动作对应下面这些工具。

| 技能要求的动作 | Gemini CLI 的对应工具 |
|----------------------|----------------------|
| 读取一个文件 | `read_file` |
| 一次读取多个文件 | `read_many_files` |
| 新建一个文件 | `write_file` |
| 编辑一个文件 | `replace` |
| 运行 shell 命令 | `run_shell_command` |
| 搜索文件内容 | `grep_search` |
| 按文件名查找文件 | `glob` |
| 列出文件与子目录 | `list_directory` |
| 抓取一个 URL | `web_fetch` |
| 搜索网页 | `google_web_search` |
| 调用技能 | `activate_skill` |
| 派发一个子代理（`Subagent (general-purpose):` 模板） | `invoke_agent` 配 `agent_name: "generalist"`（可用 `@generalist` 聊天语法调用——见[子代理支持](#subagent-support)） |
| 多个并行派发 | 在同一个回复里发起多个 `invoke_agent` 调用 |
| 任务跟踪（「建一个待办」「标记为完成」） | `write_todos`（状态：pending、in_progress、completed、cancelled、blocked） |

## 指令文件

当技能提到「你的指令文件」时，在 Gemini CLI 上指的是 **`GEMINI.md`**。Gemini CLI 按层级加载 `GEMINI.md`：全局的在 `~/.gemini/GEMINI.md`，项目级的是工作区目录及其各级父目录里的文件，另外还有子目录里的 `GEMINI.md`——当某个工具访问那些目录中的文件时会加载。

## 个人技能目录

用户级技能放在 **`~/.gemini/skills/`**，另有 **`~/.agents/skills/`** 作为跨运行时的别名（与 Codex 和 Copilot CLI 共用）。同一层级下两个目录都存在时，`.agents/skills/` 优先。每个技能是一个子目录，里面有一个 `SKILL.md`（带 `name` 和 `description` frontmatter）。

## 子代理支持

Gemini CLI 通过 `invoke_agent` 工具派发子代理，该工具接受 `agent_name` 和 `prompt` 参数。同一次派发也暴露为聊天语法快捷方式：输入 `@generalist <prompt>` 等价于调用 `invoke_agent` 并传 `agent_name: "generalist"`。内置代理名包括 `generalist`、`cli_help`、`codebase_investigator`，以及（启用浏览器工具时）`browser_agent`。

技能用 `Subagent (general-purpose):` 来派发，并且要么引用一个提示词模板文件（例如 `superpowers:subagent-driven-development` 的 `./implementer-prompt.md`），要么直接给出内联提示词。在 Gemini CLI 上：

| 技能的派发形式 | Gemini CLI 的对应做法 |
|---------------------|---------------------|
| 引用 `*-prompt.md` 模板（实现者、任务评审者、代码评审者等） | 填好模板，然后用 `invoke_agent` 配 `agent_name: "generalist"` 和填好的提示词 |
| 引用 `superpowers:requesting-code-review` 的 `./code-reviewer.md` | `invoke_agent` 配 `agent_name: "generalist"` 和填好的评审模板 |
| 内联提示词（不引用模板） | `invoke_agent` 配 `agent_name: "generalist"` 和你写的内联提示词 |

### 提示词填充

技能提供带占位符的提示词模板，例如 `{WHAT_WAS_IMPLEMENTED}` 或 `[FULL TEXT of task]`。把完整提示词交给 `invoke_agent` 之前，先填好所有占位符。提示词模板本身包含代理的角色、评审标准和预期输出格式——子代理会照着执行。

### 并行派发

Gemini CLI 支持并行派发子代理。在同一个回复里发起多个 `invoke_agent` 调用（或在一条提示词里多次调用 `@generalist`），就能并行跑相互独立的子代理工作。相互依赖的任务要保持串行，但不要为了保留一份更简单的历史记录，就把独立的子代理任务也串起来。

## Gemini CLI 的其它工具

这些工具是 Gemini CLI 独有的：

| 工具 | 用途 |
|------|---------|
| `save_memory`（旧版） | 当 `experimental.memoryV2 = false` 时，跨会话保存事实 |
| `get_internal_docs` | 查阅 Gemini CLI 自带的文档 |
| `ask_user` | 向用户提结构化问题（文本 / 单选 / 多选） |
| `enter_plan_mode` / `exit_plan_mode` | 进入和退出只读的计划模式 |
| `update_topic` | 更新当前会话的主题 / 战略意图元数据 |
| `complete_task` | 表示某个 Gemini 子代理已完成，并把结果返回给父代理 |
| `tracker_create_task`、`tracker_update_task`、`tracker_get_task`、`tracker_list_tasks`、`tracker_add_dependency`、`tracker_visualize` | 功能丰富的任务跟踪器，支持依赖关系与可视化 |
| `read_mcp_resource`、`list_mcp_resources` | 访问 MCP 资源 |
