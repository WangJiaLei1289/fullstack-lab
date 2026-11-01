# Superpowers for Kimi Code

配合 [Kimi Code](https://github.com/MoonshotAI/kimi-code) 使用 Superpowers 的完整指南。

## 安装

Superpowers 已收录在 Kimi Code 的插件市场中。

打开插件管理器：

```text
/plugins
```

进入 `Marketplace` > `Superpowers` 并安装。

你也可以从本仓库安装：

```text
/plugins install https://github.com/obra/superpowers
```

如果要在 `dev` 上验证尚未发布的版本，请显式指定分支：

```text
/plugins install https://github.com/obra/superpowers/tree/dev
```

Kimi Code 会把插件变更应用到新会话。安装、更新、启用、禁用或重新加载插件之后，请用 `/new` 开一个全新会话。

## 工作原理

Kimi 插件清单位于 `.kimi-plugin/plugin.json`。

该清单做三件事：

1. 把 Kimi Code 指向现有的 `skills/` 目录。
2. 通过 `sessionStart.skill` 在会话开始时加载 `using-superpowers`。
3. 通过 `skillInstructions` 提供 Kimi 专用的工具映射。

Kimi Code 直接从本仓库读取 Superpowers 技能。没有复制技能文件，没有符号链接，没有钩子，也没有额外的运行时依赖。

## 工具映射

技能用动作来描述，而不是写死某个运行时的工具名。在 Kimi Code 上，这些动作对应到：

- "Ask the user" / "ask clarifying questions"（询问用户 / 提出澄清问题）-> `AskUserQuestion`
- "Create a todo" / "mark complete in todo list"（创建待办 / 在待办列表中标记完成）-> `TodoList`
- "Dispatch a subagent"（分派子代理）-> `Agent`
- "Invoke a skill"（调用技能）-> Kimi Code 原生的 `Skill` 工具
- "Read a file" / "write a file" / "edit a file"（读文件 / 写文件 / 改文件）-> `Read`、`Write`、`Edit`
- "Run a shell command"（运行 shell 命令）-> `Bash`
- "Search file contents"（搜索文件内容）-> `Grep`
- "Find files by path or pattern"（按路径或模式查找文件）-> `Glob`
- "Fetch a URL"（抓取 URL）-> `FetchURL`
- "Search the web"（搜索网络）-> `WebSearch`

## 更新

使用 Kimi Code 的插件管理器：

```text
/plugins
```

选择 Superpowers 并在那里更新。更新后用 `/new` 开一个全新会话。

## 排障

### 插件没有加载

1. 运行 `/plugins info superpowers`，检查诊断信息。
2. 确认插件已启用。
3. 安装或更新之后，用 `/new` 开一个全新会话。

### 直接用 GitHub 安装却装到了旧版本

当仓库 URL 是裸地址且存在最新 GitHub release 时，Kimi Code 会安装最新的 GitHub release。要在下一个 Superpowers 版本发布前测试未发布的改动，请显式安装该分支：

```text
/plugins install https://github.com/obra/superpowers/tree/dev
```

### 技能没有触发

1. 确认 `/plugins info superpowers` 显示插件已启用。
2. 用 `/new` 开一个全新会话。
3. 试试验收提示词：`Let's make a react todo list`。装好的环境应该在写代码之前加载 `brainstorming`。
