# Superpowers for OpenCode

配合 [OpenCode.ai](https://opencode.ai) 使用 Superpowers 的完整指南。

## 安装

OpenCode V2 需要 2.0.4 或更高版本。

### OpenCode V1

沿用现有的 V1 插件配置：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

### OpenCode V2（2.0.4 或更高）

使用 V2 插件配置：

```json
{
  "plugins": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

本地 V2 安装时，请配置为包含 `index.js` 的那个仓库目录。OpenCode 2.0.4 与 2.0.7
会拒绝配置成直接的 JavaScript 文件路径。被发现到的插件符号链接仍然受支持。

重启 OpenCode。V2 使用 `opencode` 命令；`opencode2` 可能作为别名提供。插件通过 OpenCode 的插件管理器
安装，并注册全部技能。

验证方式：问它："Tell me about your superpowers"

### 从旧的基于符号链接的安装方式迁移（V1）

如果你以前用 `git clone` 加符号链接安装过 superpowers，先清掉旧的那套：

```bash
# Remove old symlinks
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers

# Optionally remove the cloned repo
rm -rf ~/.config/opencode/superpowers

# Remove skills.paths from opencode.json if you added one for superpowers
```

然后按上面的安装步骤操作。

## 用法

### 查找技能

用 OpenCode 原生的 `skill` 工具列出所有可用技能：

```
use skill tool to list skills
```

### 加载技能

```
use skill tool to load brainstorming
```

### 个人技能

在 `~/.config/opencode/skills/` 里创建你自己的技能：

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

创建 `~/.config/opencode/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: Use when [condition] - [what it does]
---

# My Skill

[Your skill content here]
```

### 项目技能

在项目内的 `.opencode/skills/` 中创建项目专用技能。

**V2 技能优先级：** 项目技能 > 个人技能 > Superpowers 技能。在测试过的 V1 1.18.31 上，
当个人技能或项目技能与内置的 Superpowers 技能同名时，Superpowers 技能优先；请给个人技能和项目技能
用不同的名字。迁移不会改变这一行为。

## 更新

OpenCode 通过一个基于 git 的包规格安装 Superpowers。某些 OpenCode 与 Bun 版本会把解析后的 git 依赖
固定在锁文件或缓存里，所以重启可能拿不到最新的 Superpowers 提交。如果更新不出现，
清除 OpenCode 的包缓存，或重新安装插件。

要固定到某个特定版本，在规格里加上 tag 或 commit（V1 的 `plugin` 键与 V2 的 `plugins` 键写法相同）：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v7.0.1"]
}
```

在 V2 上，请固定到 `v6.4.1` 或更高版本；`v6.3.0` 及更早的发布只能在 V1 上加载。

## 工作原理

插件做两件事，用的是各宿主变体自己的 API：

1. **注册技能目录**，让 OpenCode 无需符号链接或手工配置就能发现全部 superpowers 技能。
    - **V1：** 通过 `config` 钩子，注入到 `config.skills.paths`
    - **V2：** 通过 `setup()` 函数，使用 `ctx.skill.transform()`（V2 原生 API，运行时确认生效）
2. **注入 bootstrap 上下文**，并附带宿主变体专用的工具映射：V1 会话得到下面这套 V1 工具名，V2 会话得到 V2 的名字。
    - **V1：** 通过 `experimental.chat.messages.transform` 钩子
    - **V2：** 通过 `ctx.session.hook("context")` —— V2 的等价物（运行时确认生效）

控制会话（controller）会在临时的模型上下文中收到 using-superpowers bootstrap。被委派的子会话
仍能访问原生技能，但不会收到控制会话的 bootstrap。没有父会话的手工 fork 仍保持控制会话
行为。当 V2 的原生压缩保留了更早的用户消息时（默认的
`compaction.keep.tokens` 预算），bootstrap 会进入检查点之前的第一条被保留的用户消息，
与未压缩会话中的情形相同。当压缩移除所有用户消息时，插件会在
检查点之后追加一条临时 bootstrap 消息。无论哪种情况，已保存的历史都不变。

如果会话查找失败，插件会为该次请求保留 bootstrap，并在下一次请求时重试。
查找失败不会被缓存为控制会话决策。

### 工具映射

技能用动作来说话，而不是点名某个运行时的工具。bootstrap 会把它们映射到你所用 OpenCode 变体实际暴露的工具。

**V1（`opencode` 1.x）：**

- "Create a todo" / "mark complete in todo list"（创建待办 / 在待办列表中标记完成）→ `todowrite`
- `Subagent (general-purpose):` 模板 → OpenCode 的 `task` 工具，带 `subagent_type: "general"`（代码库探索用 `"explore"`）
- "Invoke a skill"（调用技能）→ OpenCode 原生的 `skill` 工具
- "Read a file"（读文件）→ `read`
- "Create a file" / "edit a file" / "delete a file"（建文件 / 改文件 / 删文件）→ `apply_patch`
- "Run a shell command"（运行 shell 命令）→ `bash`
- "Search file contents" / "find files by name"（搜索文件内容 / 按名字查找文件）→ `grep`、`glob`
- "Fetch a URL"（抓取 URL）→ `webfetch`

**V2（`opencode` 2.0.4 或更高；`opencode2` 可能作为别名提供）：**

- "Create a todo"（创建待办）→ V2 完全没有待办类工具；映射会告诉模型改用 markdown 文件（或宿主环境的计划功能）来跟踪计划
- `Subagent (general-purpose):` 模板 → OpenCode 的 `subagent` 工具，带 `agent: "general"`（探索用 `"explore"`）；传 `sessionID` 以继续之前的子代理
- "Invoke a skill"（调用技能）→ OpenCode 原生的 `skill` 工具
- "Read a file"（读文件）→ `read`
- "Create, edit, or delete files"（建、改、删文件）→ 可用时用 `patch` 加 `patchText`；否则用 `write` 创建或覆盖文件、用 `edit` 做定点修改、用 `shell` 删除
- "Run a shell command"（运行 shell 命令）→ `shell`（`command`、`workdir`、`timeout`、`background`）
- "Search file contents" / "find files by name"（搜索文件内容 / 按名字查找文件）→ `grep`、`glob`
- "Fetch a URL"（抓取 URL）→ `webfetch`
- "Search the web"（搜索网络）→ `websearch`

简言之，V2 把 `task` 改名为 `subagent`（代理名从 `subagent_type` 移到 `agent`，
继续之前的工作要靠带 `sessionID` 重新调用），把 `apply_patch` 改名为 `patch`，
把 `bash` 改名为 `shell`，并彻底去掉了待办工具。可用的修改类工具取决于所选模型：
`patch` 对选定的 GPT 模型 ID 可用，其他模型则用 `write` 与 `edit`。

（V1 清单依据已安装的 OpenCode 1.18.x CLI 的工具清单核对；V2 清单依据 OpenCode 2.0.4 与 2.0.7 的宿主契约核对。）

## 排障

### 插件没有加载

**V1：** 查看 OpenCode 日志：

```
opencode run --print-logs "hello" 2>&1 | grep -i superpowers
```

**V2：** 插件在后台服务器中加载，`--print-logs` 只有在加 `--standalone` 时才会显示它的日志：

```
opencode run --standalone --print-logs "hello" 2>&1 | grep -i superpowers
```

或者查看 `~/.local/share/opencode/log/opencode.log`，过滤 `role=server`。

同时确认 `opencode.json` 里的插件路径正确，并且你运行的是较新版本的 OpenCode。

### Windows 安装问题

有些 Windows 上的 OpenCode 构建在基于 git 的插件规格上存在上游安装器问题，包括
`git+https` URL 的缓存路径，以及 Bun 即使在普通终端里也能用、却找不到
`git.exe`。如果 OpenCode 装不上插件，可以试试用系统 npm 安装，再让 OpenCode 指向本地
包：

```powershell
npm install superpowers@git+https://github.com/obra/superpowers.git --prefix "$HOME\.config\opencode"
```

然后在 `opencode.json` 里用已安装包的绝对路径（按你的 OpenCode 版本）。OpenCode 不会展开
`~`；`~/...` 这样的条目会被当作包名，而不是本地目录。

**V1：**

```json
{
  "plugin": ["C:\\Users\\<you>\\.config\\opencode\\node_modules\\superpowers"]
}
```

**V2（2.0.4 或更高）：**

```json
{
  "plugins": ["C:\\Users\\<you>\\.config\\opencode\\node_modules\\superpowers"]
}
```

### 找不到技能

1. 用 OpenCode 的 `skill` 工具列出可用技能
2. 检查插件是否正在加载（见上文）
3. 每个技能都需要一个带合法 YAML frontmatter 的 `SKILL.md` 文件

### bootstrap 没有出现

- **V1：** 检查 OpenCode 版本是否支持 `experimental.chat.messages.transform` 钩子。配置变更后重启 OpenCode。
- **V2：** 插件用 `ctx.session.hook("context")` 注入 bootstrap。用 `opencode api get /api/plugin` 确认插件已加载。配置变更后用 `opencode service restart` 重启。`opencode2` 命令可能作为别名提供。

## 获取帮助

- 报告问题：https://github.com/obra/superpowers/issues
- 主文档：https://github.com/obra/superpowers
- OpenCode V2 文档：https://opencode.ai/v2/docs/
- OpenCode V1 文档：https://opencode.ai/docs/
