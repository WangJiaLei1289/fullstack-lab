# Hermes Agent 工具映射

技能用动作说话（「派发一个子代理」「建一个待办」「读一个文件」）。在 Hermes Agent 上，这些动作对应下面这些工具。

## 工具

| 技能要求的动作 | Hermes 工具 |
|---|---|
| 读取一个文件 | `read_file` |
| 新建一个文件 | `write_file` |
| 编辑一个文件（定向补丁） | `patch` |
| 运行 shell 命令 | `terminal` |
| 搜索文件内容 | `search_files` |
| 按文件名查找文件 | `terminal` 配 `find` |
| 抓取 URL / 读取网页 | `web_extract(urls=[...])` |
| 搜索网页 | `web_search(query=...)` |
| 派发一个子代理 | `delegate_task(goal=..., context=..., toolsets=[...], role="leaf")` |
| 任务跟踪 | `todo` 工具 |
| 调用技能 | `skill_view("skill-name")` |

## 指令文件

当技能提到「你的指令文件」时，在 Hermes Agent 上指的是项目目录里的 **`AGENTS.md`**，或全局的 **`SOUL.md`**（位于 `~/.hermes/SOUL.md`）。

## 调用技能

Hermes Agent 有一套 `skills` 工具集，里面有 `skill_view` 和 `skills_list` 两个工具。
要调用某个 superpowers 技能，用：

```
skill_view("brainstorming")  # 查看 brainstorming 技能
skill_view("test-driven-development")  # 查看 test-driven-development 技能
```

如果 `skill_view` 找不到某个 superpowers 技能（在插件完全注册之前，它可能不在目录里），就退回到直接读 SKILL.md：

```
read_file(path="~/.hermes/plugins/superpowers/skills/<skill-name>/SKILL.md")  # 退回到直接读取技能文件
```

在没有原生技能加载能力的其它宿主环境上，用的也是这同一个回退办法。

## 子代理派发

用 `delegate_task` 派生隔离的子代理，来处理并行或串行的工作流：

```
delegate_task(goal="...", context="...", toolsets=[...], role="leaf")  # 派发叶子角色子代理
```

如果 `delegate_task` 不可用，就自己内联把活干了，不要编造工具调用。

## 任务跟踪

会话内的任务跟踪用 `todo` 工具。多代理任务板则用 `hermes kanban` CLI（如果有的话）。遇到旧文档里的 `TodoWrite` 引用，就按上面这个任务跟踪动作来处理。
