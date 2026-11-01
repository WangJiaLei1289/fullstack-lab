# CLAUDE.md

本文件为在本仓库工作的 AI 代理（Claude Code、Cowork 等）提供指引。它是本项目「如何组织、如何维护」的唯一事实来源。

## 项目概览

**PM Skills**（`phuryn/pm-skills`）——一个包含 **9 个独立插件**（68 个技能、42 个命令）的插件市场，把结构化的产品管理工作流带给 AI 编程助手。为 Claude Code 与 Claude Cowork 打造；其中的技能也兼容其他代理（Gemini CLI、Cursor、Codex CLI）。

所有者：Paweł Huryn — pawel@productcompass.pm — https://www.productcompass.pm

## 仓库结构

```
pm-skills/                           <- 仓库根目录
├── .claude-plugin/marketplace.json  <- 根插件市场清单（列出全部 9 个插件）
├── .docs/images/                    <- README 使用的图片（webp、gif）
├── .gitattributes
├── .gitignore
├── .github/workflows/               <- CI：tests.yml（每次 PR/推送）、tag-on-merge.yml（自动发布）
├── CHANGELOG.md                     <- 发布的事实来源（main 上出现新的 ## vX.Y.Z 标题 = 发布）
├── CLAUDE.md                        <- 本文件（代理指引，唯一事实来源）
├── AGENTS.md                        <- 指向 CLAUDE.md（供非 Claude 代理使用）
├── CONTRIBUTING.md                  <- 贡献者指南
├── README.md                        <- 公开文档（GitHub）
├── LICENSE                          <- MIT
├── validate_plugins.py              <- 插件校验器
├── tests/                           <- 单元测试 + 文档一致性测试（unittest）
└── pm-{name}/                       <- 9 个插件目录
    ├── .claude-plugin/plugin.json   <- 每个插件的清单
    ├── skills/{skill}/SKILL.md      <- 每个技能一个目录
    ├── commands/{command}.md        <- 每个命令一个文件
    └── README.md                    <- 每个插件的文档
```

### 9 个插件

| 插件 | 关注点 |
|--------|-------|
| `pm-product-discovery` | 构思、实验、假设验证、优先级排序、访谈综合 |
| `pm-product-strategy` | 愿景、战略/精益/商业模式画布、SWOT、PESTLE、安索夫矩阵、波特五力、变现 |
| `pm-execution` | PRD、OKR、路线图、冲刺、事前验尸、利益相关方地图、用户故事、红队评审 |
| `pm-market-research` | 用户画像、用户细分、情感分析、竞品分析、市场规模测算 |
| `pm-data-analytics` | SQL 查询生成、同期群与留存分析 |
| `pm-go-to-market` | GTM 战略、增长循环、GTM 打法、滩头细分市场、ICP |
| `pm-marketing-growth` | 营销创意、价值主张陈述、北极星指标、命名、定位 |
| `pm-toolkit` | 简历评审、NDA 起草、隐私政策、语法与行文检查 |
| `pm-ai-shipping` | AI Shipping Kit：为 vibe-coded 应用写文档、梳理测试覆盖、按预期行为审计安全与性能，并汇编交付包 |

## 关键设计规则

- **技能 = 名词/概念。** 框架与分析知识，话题匹配时由 Claude 自动加载（`lean-canvas`、`pre-mortem`、`market-sizing`）。
- **命令 = 动词。** 由用户触发的工作流，串起一个或多个技能（`/write-prd`、`/discover`、`/plan-launch`）。
- **不跨插件引用。** 命令只用自然语言建议后续动作（「要我帮你设计增长循环吗？」）。绝不硬引用其他插件的命令——插件各自独立安装，硬引用可能导致损坏。
- **插件内部的「Uses」引用没问题** —— 同一插件里的技能与命令总是一起发布。
- 命令只用一个 `$ARGUMENTS` 占位符。技能不需要占位符（它们从对话中读取上下文）。
- **必须提供 frontmatter：** 技能需要 `name` + `description`；命令需要 `description` + `argument-hint`。
- 技能的 `name` **必须与所在目录名一致**。
- 技能可以通过 `/plugin-name:skill-name` 或 `/skill-name` 强制加载。
- 保持 frontmatter 精简（它总会被加载）；把细节放进 SKILL.md 正文（触发时才加载）——渐进式披露。

## 什么内容在哪里可见

| 位置 | 可见于 | 说明 |
|----------|-----------|-------|
| `marketplace.json` → `description` | Cowork 插件市场浏览器、Claude Code | 整个插件市场的一句话简介 |
| `plugin.json` → `description` | Cowork 插件列表、Claude Code | 每个插件的摘要；简洁、实用 |
| `SKILL.md` frontmatter → `description` | Cowork 技能列表、Claude 自动加载 | 写上触发词，让 Claude 在合适时机加载技能 |
| 命令 frontmatter → `description` + `argument-hint` | Cowork 与 Claude Code（输入 `/` 时） | 简短、可直接执行 |
| `README.md`（仓库根目录） | 仅 GitHub | 完整文档；Claude 运行时不会加载 |

`plugin.json` 与仓库 `README.md` 中的描述应保持一致（文字相同）。

## 版本与发布

- **`CHANGELOG.md` 是事实来源。** 最新的 `## vX.Y.Z — YYYY-MM-DD` 标题就是已发布版本。向 `main` 推送一个新增标题的提交后，CI（`.github/workflows/tag-on-merge.yml`）会校验版本同步与测试套件、打上 `vX.Y.Z` 标签，并以该章节作为说明发布 GitHub Release。
- **所有版本保持同步。** `marketplace.json`、全部 9 个 `plugin.json` 以及最新的 CHANGELOG 标题始终携带同一版本号（由 `tests/test_consistency.py` 强制检查）。不存在按插件独立编号这回事。
- 每一项面向用户的改动都要在 `## Unreleased` 下加一条 CHANGELOG 条目；贡献者在条目内就地署名（`#PR, thanks @handle`）。完整流程见 CONTRIBUTING.md 的「发布」一节。
- 语义化版本：破坏性改动 = major；新增技能/命令或行为变化 = minor；修复与文档 = patch。

## 技能中的文章链接（延伸阅读）

- 已映射的技能以 `### Further Reading` 一节结尾，链接到相关的 Product Compass 文章。
- **语气必须保持中性** —— 不用推广性措辞、不用 CTA、不出现「subscribe」「check out」之类的引导。只给文章标题和 URL。
- Claude 根据对话相关性来展示这些链接，而不是每次回复都带上。
- 标题中含「Masterclass」或「Course」的文章是视频课程——请标注 `(video course)`。

## 操作流程

### 改动任何技能/命令之后
1. 在仓库根目录运行 `python3 validate_plugins.py` 和 `python3 -m unittest discover -s tests`。
2. 如果新增或删除了技能/命令，更新 `README.md` 中的计数（首屏 + 每个插件摘要 + 插件 README 的章节标题——三处测试都会检查）。
3. 如果总数发生变化，更新 `marketplace.json` 描述里的计数。
4. 任何面向用户的改动都要在 `## Unreleased` 下加一条 `CHANGELOG.md` 条目。
5. 发布时把所有清单中的版本号一起提升（见「版本与发布」）。

### 改动描述之后
- `plugin.json` 的描述改了 → 检查 `README.md` 是否需要做同样的修改（两者保持一致）。
- `SKILL.md` 的描述改了 → 无需其他同步（它是该技能的唯一来源）。

## 校验

`validate_plugins.py` 检查：`plugin.json` 的必填字段 / name 匹配 / semver / author / keywords；技能 frontmatter 以及 name 是否与目录匹配；命令 frontmatter（`description` + `argument-hint`）；README 是否存在；以及插件内部的命令→技能引用。

`tests/` 补上一致性这一层：README 计数与磁盘对比、marketplace 插件列表与目录对比、所有清单 + CHANGELOG 的版本同步、CHANGELOG 标题格式，以及插件 README 中的 `/plugin:command` 引用。两者都在每次 PR 与推送到 `main` 时于 CI 中运行，并为发布把关。

```
python3 validate_plugins.py
python3 -m unittest discover -s tests
```

## 完成工作后可以建议什么

主动提供相关的后续动作：
- 结构性改动之后：「要我跑一下校验器吗？」
- 新增/删除技能或命令之后：「需要我更新 README.md 与 marketplace.json 里的计数吗？」
- 改过描述之后：「要把这次修改同步到 README.md / plugin.json 吗？」
- 任何仓库改动之后：「需要我提升版本号吗？」
