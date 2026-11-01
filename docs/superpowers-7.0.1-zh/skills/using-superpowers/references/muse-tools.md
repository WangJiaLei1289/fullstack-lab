# Muse 工具映射

技能用动作说话（「派发一个子代理」「建一个待办」「读一个文件」）。在 Muse 上，这些动作对应下面这些工具。

| 技能要求的动作 | Muse 的对应做法 |
|----------------------|----------------|
| 读取一个文件 | `read_file` |
| 读取多个文件 | `read_file`（调用多次）或 `search` |
| 新建一个文件 | `write_file` |
| 编辑一个文件 | `edit_file` |
| 运行 shell 命令 | `bash` |
| 搜索文件内容 | `search` |
| 按文件名查找文件 | `search` 配 `glob` |
| 抓取 URL | `web_fetch` |
| 搜索网页 | `web_search` |
| 调用技能 | 用 `read_file` 读 `skills/<name>/SKILL.md`，或用原生的技能工具 |
| 派发一个子代理（`Subagent (general-purpose):` 模板） | `subagent_spawn`，并填好提示词 |
| 任务跟踪（「建一个待办」「标记为完成」） | `write_todos` 或 `bash` 任务文件 |
| 向用户提问 | `request_user_input` |

## 指令文件

当技能提到「你的指令文件」时，在 Muse 上指的是项目根目录的 **`CLAUDE.md`** 或 **`AGENTS.md`**。在配置了的情况下，Muse 会按层级加载它们。

## 技能调用

Muse 通过 `muse skills` 提供原生技能支持。要调用某个 Superpowers 技能，读它的 `SKILL.md` 并照说明执行。引导（bootstrap，`using-superpowers`）会通过插件钩子在 `SessionStart` 时自动注入——你已经在遵循它了，不要再加载一遍。

## 子代理派发

用 `subagent_spawn` 把工作委托给隔离的子代理。派发之前先填好提示词模板（例如 `implementer-prompt.md`、`task-reviewer-prompt.md`）。如果没有可用的子代理工具，就自己内联把活干了，不要编造工具调用。

## 任务跟踪

用 `write_todos` 跟踪检查清单。为该技能的每个检查清单项建一个待办，过程中标记 in_progress/completed。如果 `write_todos` 不可用，就用 `write_file`/`edit_file` 维护一份 markdown 任务文件。
