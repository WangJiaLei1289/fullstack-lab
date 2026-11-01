# Antigravity CLI（`agy`）工具映射

技能用动作说话（「派发一个子代理」「建一个待办」「读一个文件」）。在 Antigravity CLI（`agy`）上，这些动作对应下面这些工具。

| 技能要求的动作 | Antigravity CLI 的对应工具 |
|----------------------|----------------------|
| 派发一个子代理（`Subagent (general-purpose):` 模板） | 用带内置 `TypeName` 的 `invoke_subagent`——`self` 用于全能力工作，`research` 用于只读 |
| 任务跟踪（「建一个待办」「标记为完成」） | 一份**任务产物（task artifact）**——`write_to_file` 配 `IsArtifact: true` 和 `ArtifactType: "task"`（见[任务跟踪](#task-tracking)）。**不是** `manage_task`，那个工具管的是后台进程。 |

## 任务跟踪

Antigravity **没有待办工具**（`manage_task` 管的是后台进程——`list`/`kill`/`status`/`send_input`——它*不是*检查清单）。当某个技能要求建待办列表或跟踪任务时，就维护一份**任务产物**：用 `write_to_file` 保存的 markdown 检查清单（`IsArtifact: true`、`ArtifactMetadata.ArtifactType: "task"`），过程中用 `replace_file_content` / `multi_replace_file_content` 修改它。

任何多步任务开始时，先创建任务产物，列出你计划里的每一步。每完成一步，就修改产物把它标记为完成（`- [x]`）。计划有变就更新检查清单。保持它是最新的——它是你判断还剩什么的事实来源；对话变长之后，在开始每一步之前重读一遍。
