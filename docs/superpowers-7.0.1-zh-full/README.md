# Superpowers

Superpowers 是一套完整的软件开发方法论，为你的编程代理而造，建立在一组可组合的技能之上，外加一些初始指令，确保你的代理真的会用到它们。

## 目录

- [工作原理](#how-it-works)
- [商业服务](#commercial-services)
- [快速开始](#installation)
  - [Claude Code](#claude-code)
  - [Antigravity](#antigravity)
  - [Codex App](#codex-app)
  - [Codex CLI](#codex-cli)
  - [Cursor](#cursor)
  - [Devin CLI](#devin-cli)
  - [Factory Droid](#factory-droid)
  - [Gemini CLI](#gemini-cli)
  - [GitHub Copilot CLI](#github-copilot-cli)
  - [Grok Build CLI](#grok-build-cli)
  - [Kimi Code](#kimi-code)
  - [OpenCode](#opencode)
  - [Pi](#pi)
  - [Qwen Code](#qwen-code)
  - [Hermes Agent](#hermes-agent)
  - [Muse](#muse)
- [基本工作流](#the-basic-workflow)
- [出问题时怎么办](#when-something-goes-wrong)
- [社区](#community)
- [里面有什么](#whats-inside)
- [理念](#philosophy)
- [贡献](#contributing)
- [更新](#updating)
- [许可证](#license)
- [视觉伴侣遥测](#visual-companion-telemetry)

## 工作原理

它从你启动编程代理的那一刻就开始了。只要它看出你在构建某个东西，它*不会*径直扑向写代码。相反，它退后一步，问你真正想做的是什么。

等它从对话里梳理出一份规格，会以足够短、能真正读完并消化的段落展示给你。

在你确认设计之后，你的代理会整理出一份实施计划，清晰到足以让一个热情但品味糟糕、没有判断力、没有项目背景、还讨厌测试的初级工程师照着做。它强调真正的红/绿 TDD、YAGNI（You Aren't Gonna Need It）和 DRY。

接下来，等你说「开始」，它就会启动 *subagent-driven-development* 流程，让各个代理逐项完成工程任务，检查并评审它们的工作，然后继续推进。你的代理一次自主工作几个小时、不偏离你们共同制定的计划，这并不罕见。

细节还有很多，但上面就是这个系统的核心。而且因为技能会自动触发，你不需要做任何特别的事。你的编程代理只是有了 Superpowers。

## 商业服务

如果你在企业中使用 Superpowers，并且希望获得商业支持、额外工具或托管支出方面的帮助，欢迎随时写信到 sales@primeradiant.com。

## 安装

安装方式因宿主环境而异。如果你用不止一个，请为每个分别安装 Superpowers。

### Claude Code

Superpowers 可通过[官方 Claude 插件市场](https://claude.com/plugins/superpowers)获取

#### 官方插件市场

- 从 Anthropic 官方插件市场安装插件：

  ```bash
  /plugin install superpowers@claude-plugins-official
  ```

#### Superpowers 插件市场

Superpowers 插件市场提供 Superpowers 以及一些其他相关的 Claude Code 插件。

- 注册插件市场：

  ```bash
  /plugin marketplace add obra/superpowers-marketplace
  ```

- 从这个插件市场安装插件：

  ```bash
  /plugin install superpowers@superpowers-marketplace
  ```

### Antigravity

从本仓库把 Superpowers 作为插件安装：

```bash
agy plugin install https://github.com/obra/superpowers
```

Antigravity 会列出每个已安装技能的描述，而
`using-superpowers` 技能的描述会促使模型在对话开始时加载该技能。用同一条命令重装即可更新。

### Codex App

Superpowers 可通过[官方 Codex 插件市场](https://github.com/openai/plugins)获取。

- 在 Codex 应用里，点击侧边栏的 Plugins。
- 你应该能在 Coding 一栏看到 `Superpowers`。
- 点 Superpowers 旁边的 `+`，然后按提示操作。

### Codex CLI

Superpowers 可通过[官方 Codex 插件市场](https://github.com/openai/plugins)获取。

- 打开插件搜索界面：

  ```bash
  /plugins
  ```

- 搜索 Superpowers：

  ```bash
  superpowers
  ```

- 选择 `Install Plugin`。

### Cursor

- 在 Cursor Agent 聊天里，从插件市场安装：

  ```text
  /add-plugin superpowers
  ```

- 或者在插件市场里搜索 "superpowers"。

### Devin CLI

- 从本仓库安装插件：

  ```bash
  devin plugins install obra/superpowers
  ```

- 用下面的命令更新到最新版本：

  ```bash
  devin plugins update superpowers
  ```

### Factory Droid

- 注册插件市场：

  ```bash
  droid plugin marketplace add https://github.com/obra/superpowers
  ```

- 安装插件：

  ```bash
  droid plugin install superpowers@superpowers
  ```

### Gemini CLI

- 安装扩展：

  ```bash
  gemini extensions install https://github.com/obra/superpowers
  ```

- 之后更新：

  ```bash
  gemini extensions update superpowers
  ```

### GitHub Copilot CLI

- 注册插件市场：

  ```bash
  copilot plugin marketplace add obra/superpowers-marketplace
  ```

- 安装插件：

  ```bash
  copilot plugin install superpowers@superpowers-marketplace
  ```

### Grok Build CLI

Superpowers 可通过[官方 Grok 插件市场](https://github.com/xai-org/plugin-marketplace)获取。

- 从 xAI 的官方插件市场安装插件：

  ```bash
  grok plugin install superpowers@xai-official --trust
  ```

- 或者在 TUI 里打开插件市场，搜索 Superpowers 并安装：

  ```text
  /marketplace
  ```

### Kimi Code

Superpowers 已在 Kimi Code 的插件市场中提供。

- 打开 Kimi Code 的插件管理器：

  ```text
  /plugins
  ```

- 进入 `Marketplace` > `Superpowers` 并安装。

- 或者直接从本仓库安装：

  ```text
  /plugins install https://github.com/obra/superpowers
  ```

- 详细文档：[docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

OpenCode 使用自己的插件安装方式；即使你已经在别的宿主环境里用过 Superpowers，也要为它
单独安装。

- 告诉 OpenCode：

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- 详细文档：[docs/README.opencode.md](docs/README.opencode.md)

### Pi

从本仓库把 Superpowers 作为 Pi 包安装：

```bash
pi install git:github.com/obra/superpowers
```

本地开发时，用这个检出作为临时包来运行 Pi：

```bash
pi -e /path/to/superpowers
```

Pi 包会加载 Superpowers 技能，以及一个小扩展：它在会话启动时注入 `using-superpowers` bootstrap，并在压缩之后再次注入。Pi 有原生技能，因此不需要兼容用的 `Skill` 工具。子代理和任务列表工具仍是可选的 Pi 配套包。

### Qwen Code

Qwen Code 直接从 Claude Code 插件市场安装插件。

- 从本仓库安装插件，提示时选择 `superpowers`：

  ```bash
  qwen extensions install obra/superpowers
  ```

- 之后更新：

  ```bash
  qwen extensions update superpowers
  ```

### Hermes Agent

从本仓库把 Superpowers 作为 Hermes 插件安装：

```bash
hermes plugins install obra/superpowers --enable
```

安装后重启所有活跃的 Hermes 会话。注意：Hermes 没有
压缩后的钩子，所以一个非常长的会话如果在第一轮之后发生压缩，就会丢掉 bootstrap——如果技能不再触发，就开一个新会话。

### Muse

Superpowers 可作为原生 Muse 插件使用——同一个仓库、同一套技能、所有宿主环境。`using-superpowers` bootstrap 通过原生 `SessionStart` 钩子注入，与 Claude Code、Codex、Cursor、Gemini、Pi 等一致——不需要按会话选择启用。

- 从本地检出安装：

  ```bash
  muse plugins install ./
  muse plugins approve superpowers
  ```

  或者克隆后安装：

  ```bash
  git clone https://github.com/obra/superpowers.git
  muse plugins install ./superpowers
  muse plugins approve superpowers
  ```

- 之后更新：

  ```bash
  muse plugins update superpowers
  ```

安装后重启活跃的 Muse 会话，好让 `SessionStart` 钩子生效——技能立即生效，钩子需要首次安装时批准。要验证，开一个新会话并发送 `Let's make a react todo list`——装好的环境会在写任何代码之前自动触发 `brainstorming`。版本记录在 `.version-bump.json` 中，因此 `scripts/bump-version.sh` 能让它保持同步。

## 基本工作流

1. **brainstorming** - 动手构建任何东西之前激活。用提问把你真正想要的东西以及原因引出来，让你自己把它讲清楚，然后复述它的理解供你纠正。小改动在聊天里谈定；项目则会产出一份写下来的设计文档，让实施者可以据此规划。

2. **using-git-worktrees** - 设计获批后激活。在新分支上创建隔离工作区，运行项目初始化，验证干净的测试基线。

3. **writing-plans** - 拿到已批准的设计后激活。把工作拆成小块任务（每个 2-5 分钟）。每个任务都有确切的文件路径、完整代码和验证步骤。

4. **subagent-driven-development** 或 **executing-plans** - 拿到计划后激活。要么为每个任务分派一个全新的子代理，并在每个任务之后评审（最彻底）；要么在当前会话里逐个内联实现所有任务，最后对整个分支做一次全新评审（最省）。

5. **test-driven-development** - 实现过程中激活。强制执行 RED-GREEN-REFACTOR：写一个会失败的测试，看它失败，写最少量的代码，看它通过，提交。删掉在测试之前写下的代码。

6. **requesting-code-review** - 任务之间激活。对照计划做评审，按严重程度报告问题。关键问题会阻塞进度。

7. **finishing-a-development-branch** - 任务完成时激活。验证测试，给出选项（合并/PR/保留/丢弃），清理工作树。

**代理在任何任务之前都会检查相关技能。** 这些是强制工作流，不是建议。

## 出问题时怎么办

有时会话会出毛病：技能在不该触发时触发了，该出声时却沉默，或者代理无视计划、重复劳动、比你预期烧掉更多 token。让你的编程代理去「figure out what went wrong with superpowers in this session」（查清这次会话里 superpowers 出了什么问题），它就会调用 **diagnosing-superpowers** 技能。如果要检查更早的会话，就点名它：「figure out what went wrong with superpowers in session `<id>`」。

该技能会读取会话记录，用行级证据报告发生了什么；如果你需要，还会打包一份已脱敏的压缩包用于提 bug。

## 社区

Superpowers 由 [Jesse Vincent](https://blog.fsck.com) 以及 [Prime Radiant](https://primeradiant.com) 的伙伴们共同打造。

- **Discord**：[加入我们](https://discord.gg/35wsABTejz)，获取社区支持、提问、分享你用 Superpowers 在构建什么
- **Issues**：https://github.com/obra/superpowers/issues
- **发布公告**：[订阅](https://primeradiant.com/superpowers/)以获取新版本通知

## 里面有什么

### 技能库

**测试**
- **test-driven-development** - RED-GREEN-REFACTOR 循环（含测试反模式参考）

**调试**
- **systematic-debugging** - 4 阶段根因流程（含根因追踪、纵深防御、基于条件的等待等技巧）
- **verification-before-completion** - 确保问题真的修好了
- **diagnosing-superpowers** - 查明一次会话里出了什么问题，并附上证据；导出脱敏压缩包或提交 issue

**协作**
- **brainstorming** - 动手之前先把意图梳理出来
- **writing-plans** - 详细的实施计划
- **executing-plans** - 内联执行计划：一个上下文，一次最终评审
- **dispatching-parallel-agents** - 并发的子代理工作流
- **requesting-code-review** - 评审前的检查清单
- **receiving-code-review** - 回应反馈
- **using-git-worktrees** - 并行开发分支
- **finishing-a-development-branch** - 合并/PR 决策工作流
- **subagent-driven-development** - 两阶段评审的快速迭代（先规格符合性，再代码质量）

**元技能**
- **writing-skills** - 按最佳实践创建新技能（含测试方法论）
- **using-superpowers** - 技能系统简介

## 理念

- **测试驱动开发** - 永远先写测试
- **系统化胜于临时应付** - 流程胜于猜测
- **降低复杂度** - 以简单为首要目标
- **证据胜于断言** - 宣布成功之前先验证

阅读[最初的发布公告](https://blog.fsck.com/2025/10/09/superpowers/)。

## 贡献

Superpowers 的一般贡献流程如下。请记住，我们通常不接受新增技能的贡献，而且对技能的任何更新都必须在所有我们支持的编程代理上都能用。我们也不接受代理写的、去修别人提的 issue 的 PR，除非维护者要求这么做，即使你碰到了同样的问题也不例外；请把报告加到已有的 issue 里。

1. Fork 这个仓库
2. 切换到 'dev' 分支
3. 为你的工作创建一个分支
4. 按照 `writing-skills` 技能来创建和测试新增或修改的技能
5. 提交 PR，填满拉取请求模板的每一个小节，包括由人用自己的话写的摘要。

技能行为测试使用 [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/) 的 drill 评测宿主环境，克隆到 `evals/`——安装说明见 `evals/README.md`。插件基础设施测试位于 `tests/`，通过相关的 `run-*.sh` 或 `npm test` 运行。

完整指南见 `skills/writing-skills/SKILL.md`。

## 更新

Superpowers 的更新方式多少取决于编程代理，但通常是自动的。

## 许可证

MIT License——详见 LICENSE 文件

## 视觉伴侣遥测

因为技能和插件不会给创作者任何反馈，我们完全不知道你们有多少人在用 Superpowers。默认情况下，brainstorming 可选「视觉伴侣」功能里的 Prime Radiant 徽标是从我们网站加载的。它包含正在使用的 Superpowers 版本，不包含任何关于你的项目、提示词或编程代理的细节。我们看不到你的点击，也看不到你在构建什么。这有助于我们大致了解有多少人在用 Superpowers、用的是哪个版本。它 100% 可选。要关闭它，把环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设为任意真值。Superpowers 也尊重 Claude Code 的 `DISABLE_TELEMETRY` 与 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 退出选项。
