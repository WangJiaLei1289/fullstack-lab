# fullstack-lab

全栈代码开发空间。本项目在 `.dsh/skills/` 下内置了 **93 个项目级 agent skill**，覆盖产品管理、软件开发方法论、需求规格三条线。

## 目录

- [这是什么](#这是什么)
- [技能怎么被加载](#技能怎么被加载)
- [一、PM Skills（69 个）](#一pm-skills69-个)
- [二、Superpowers（15 个）](#二superpowers15-个)
- [三、srs-skills（9 个）](#三srs-skills9-个)
- [怎么用](#怎么用)
- [场景速查](#场景速查)
- [维护](#维护)

## 这是什么

技能（skill）是一段按需加载的任务指令：模型平时只看到「名字 + 一句话用途」，遇到匹配的任务时才加载完整正文，因此不会一次性占满上下文。本仓库把三套上游技能包（英文原版）拷进项目，做成项目级技能，本项目的每个会话都会自动获得这 93 个技能，无需再安装。

| 来源 | 上游 | 数量 | 定位 |
|---|---|---|---|
| PM Skills 2.2.0 | `phuryn/pm-skills`（9 个插件） | 69 | 产品经理工作流：发现 → 战略 → 执行 → 上市 → 增长 → AI 交付 |
| Superpowers 7.0.1 | `obra/superpowers` | 15 | 编码 agent 的开发方法论：头脑风暴、写计划、TDD、系统化调试、并行子代理、代码评审 |
| srs-skills | 上游 README 为越南语、附英文版 | 9 | 从一句想法生成完整软件需求规格说明书（SRS）的九阶段流水线 |

原始副本（含中文翻译版、README、CHANGELOG、测试等完整仓库内容）保留在 `docs/` 下，`.dsh/skills/` 里是可用于加载的精简副本。

## 技能怎么被加载

DSH 的项目级技能根目录是 `<项目根>/.dsh/skills/<name>/SKILL.md`（项目根 = 最近一个含 `.git` 的祖先目录）：

- **只扫一层**：`<name>/SKILL.md`。嵌套的 `**/SKILL.md` 不会被发现，所以三套技能都已扁平化到 `.dsh/skills/` 下。
- **frontmatter 必填** `name` + `description`，且 `name` 必须是 kebab-case；不合法的技能会被静默跳过。
- 目录被监听，增删改技能会自动刷新下一个会话步骤的技能目录，**改完不需要重启**。
- 优先级：`.dsh/skills`（项目）> `.agents/skills` > 自定义目录 > `~/.dsh/skills`（用户）；同名时项目级胜出。

## 一、PM Skills（69 个）

按上游的 9 个插件分组。技能是「名词/概念」，由模型按话题自动加载；上游同名的 42 条命令（`/write-prd` 等）未导入。

### 产品发现 · `pm-product-discovery`（13 个）

覆盖：构思、实验、假设验证、优先级排序、访谈综合。

| 技能 | 用途 |
|---|---|
| `analyze-feature-requests` | Analyze and prioritize a list of feature requests by theme, strategic alignment, impact, effort, and risk. |
| `brainstorm-experiments-existing` | Design experiments to test assumptions for an existing product — prototypes, A/B tests, spikes, and other low-effort validation methods. |
| `brainstorm-experiments-new` | Design lean startup experiments (pretotypes) for a new product. |
| `brainstorm-ideas-existing` | Brainstorm product ideas for an existing product using multi-perspective ideation from PM, Designer, and Engineer viewpoints. |
| `brainstorm-ideas-new` | Brainstorm feature ideas for a new product in initial discovery from PM, Designer, and Engineer perspectives. |
| `identify-assumptions-existing` | Identify risky assumptions for a feature idea in an existing product across Value, Usability, Viability, and Feasibility. |
| `identify-assumptions-new` | Identify risky assumptions for a new product idea across 8 risk categories including Go-to-Market, Strategy, and Team. |
| `interview-script` | Create a structured customer interview script with JTBD probing questions, warm-up, core exploration, and wrap-up sections. |
| `metrics-dashboard` | Define and design a product metrics dashboard with key metrics, data sources, visualization types, and alert thresholds. |
| `opportunity-solution-tree` | Build an Opportunity Solution Tree (OST) to structure product discovery — map a desired outcome to opportunities, solutions, and experiments. |
| `prioritize-assumptions` | Prioritize assumptions using an Impact × Risk matrix and suggest experiments for each. |
| `prioritize-features` | Prioritize a backlog of feature ideas based on impact, effort, risk, and strategic alignment with top 5 recommendations. |
| `summarize-interview` | Summarize a customer interview transcript into a structured template with JTBD, satisfaction signals, and action items. |

### 产品战略 · `pm-product-strategy`（12 个）

覆盖：愿景、战略/精益/商业模式画布、SWOT、PESTLE、安索夫、波特五力、变现。

| 技能 | 用途 |
|---|---|
| `ansoff-matrix` | Generate an Ansoff Matrix analysis mapping growth strategies across market penetration, market development, product development, and diversification. |
| `business-model` | Generate a Business Model Canvas with all 9 building blocks. |
| `lean-canvas` | Generate a Lean Canvas with problem, solution, metrics, cost structure, UVP, unfair advantage, channels, segments, and revenue. |
| `monetization-strategy` | Brainstorm 3-5 monetization strategies with audience fit, risks, and validation experiments. |
| `pestle-analysis` | Perform a PESTLE analysis covering Political, Economic, Social, Technological, Legal, and Environmental factors. |
| `porters-five-forces` | Perform Porter's Five Forces analysis — competitive rivalry, supplier power, buyer power, threat of substitutes, and threat of new entrants. |
| `pricing-strategy` | Analyze and design pricing strategies including pricing models, competitive pricing analysis, willingness-to-pay estimation, and price elasticity. |
| `product-strategy` | Create a comprehensive product strategy using the 9-section Product Strategy Canvas — vision, segments, costs, value propositions, trade-offs, metrics, growth… |
| `product-vision` | Brainstorm an inspiring, achievable, and emotional product vision that motivates teams and aligns stakeholders. |
| `startup-canvas` | Generate a Startup Canvas combining Product Strategy (9 sections) and Business Model (costs + revenue) for a new product. |
| `swot-analysis` | Perform a detailed SWOT analysis — strengths, weaknesses, opportunities, and threats with actionable recommendations. |
| `value-proposition` | Design a detailed value proposition using a 6-part JTBD template — Who, Why, What before, How, What after, Alternatives. |

### 执行 · `pm-execution`（16 个）

覆盖：PRD、OKR、路线图、冲刺、事前验尸、利益相关方、用户故事、红队评审。

| 技能 | 用途 |
|---|---|
| `brainstorm-okrs` | Brainstorm team-level OKRs aligned with company objectives — qualitative objectives with measurable key results. |
| `create-prd` | Create a lean, decision-ready Product Requirements Document with an 8-section template: summary, contacts, background, objective, market segments, value… |
| `dummy-dataset` | Generate realistic dummy datasets for testing with customizable columns, constraints, and output formats (CSV, JSON, SQL, Python script). |
| `job-stories` | Create job stories using the 'When [situation], I want to [motivation], so I can [outcome]' format with detailed acceptance criteria. |
| `outcome-roadmap` | Transform an output-focused roadmap into an outcome-focused one that communicates strategic intent. |
| `pre-mortem` | Run a pre-mortem risk analysis on a PRD or launch plan. |
| `prioritization-frameworks` | Reference guide to 9 prioritization frameworks with formulas, when-to-use guidance, and templates — RICE, ICE, Kano, MoSCoW, Opportunity Score, and more. |
| `release-notes` | Generate user-facing release notes from tickets, PRDs, or changelogs. |
| `retro` | Facilitate a structured sprint retrospective — what went well, what didn't, and prioritized action items with owners and deadlines. |
| `sprint-plan` | Plan a sprint with capacity estimation, story selection, dependency mapping, and risk identification. |
| `stakeholder-map` | Build a stakeholder map using a power/interest grid, identify communication strategies per quadrant, and generate a communication plan. |
| `strategy-red-team` | Red-team a PRD, roadmap, or strategy by attacking its load-bearing assumptions before reality does. |
| `summarize-meeting` | Summarize a meeting transcript into structured notes with date, participants, topic, key decisions, summary points, and action items. |
| `test-scenarios` | Create comprehensive test scenarios from user stories with test objectives, starting conditions, user roles, step-by-step actions, and expected outcomes. |
| `user-stories` | Create user stories following the 3 C's (Card, Conversation, Confirmation) and INVEST criteria with descriptions, design links, and acceptance criteria. |
| `wwas` | Create product backlog items in Why-What-Acceptance format — independent, valuable, testable items with strategic context. |

### 市场研究 · `pm-market-research`（7 个）

覆盖：用户画像、用户细分、情感分析、竞品分析、市场规模测算。

| 技能 | 用途 |
|---|---|
| `competitor-analysis` | Analyze competitors with strengths, weaknesses, and differentiation opportunities. |
| `customer-journey-map` | Create an end-to-end customer journey map with stages, touchpoints, emotions, pain points, and opportunities. |
| `market-segments` | Identify 3-5 potential customer segments with demographics, JTBD, and product fit analysis. |
| `market-sizing` | Estimate market size using TAM, SAM, and SOM with top-down and bottom-up approaches. |
| `sentiment-analysis` | Analyze user feedback data to identify segments with sentiment scores, JTBD, and product satisfaction insights. |
| `user-personas` | Create refined user personas from research data — 3 personas with JTBD, pains, gains, and unexpected insights. |
| `user-segmentation` | Segment users from feedback data based on behavior, JTBD, and needs. |

### 数据分析 · `pm-data-analytics`（3 个）

覆盖：SQL 查询生成、同期群与留存分析、A/B 实验解读。

| 技能 | 用途 |
|---|---|
| `ab-test-analysis` | Analyze A/B test results with statistical significance, sample size validation, confidence intervals, and ship/extend/stop recommendations. |
| `cohort-analysis` | Perform cohort analysis on user engagement data — retention curves, feature adoption trends, and segment-level insights. |
| `sql-queries` | Generate SQL queries from natural language descriptions. |

### 上市 · `pm-go-to-market`（6 个）

覆盖：GTM 战略、增长循环、GTM 打法、滩头细分、ICP。

| 技能 | 用途 |
|---|---|
| `beachhead-segment` | Identify the first beachhead market segment for a product launch. |
| `competitive-battlecard` | Create sales-ready competitive battlecards comparing your product against a specific competitor — positioning, feature comparison, objection handling, and win/loss… |
| `growth-loops` | Identify growth loops (flywheels) for sustainable traction. |
| `gtm-motions` | Identify the best GTM motions and tools across 7 motion types: Inbound, Outbound, Paid Digital, Community, Partners, ABM, and PLG. |
| `gtm-strategy` | Create a go-to-market strategy covering marketing channels, messaging, success metrics, and launch timeline. |
| `ideal-customer-profile` | Identify the Ideal Customer Profile (ICP) from research data with demographics, behaviors, JTBD, and needs. |

### 营销增长 · `pm-marketing-growth`（5 个）

覆盖：营销创意、价值主张陈述、北极星指标、命名、定位。

| 技能 | 用途 |
|---|---|
| `marketing-ideas` | Generate 5 creative, cost-effective marketing ideas with channels, messaging, and engagement rationale. |
| `north-star-metric` | Define a North Star Metric and 3-5 supporting input metrics that form a metrics constellation. |
| `positioning-ideas` | Brainstorm product positioning ideas differentiated from competitors. |
| `product-name` | Brainstorm 5 unique, memorable product names with rationale aligned to brand values and target audience. |
| `value-prop-statements` | Generate value proposition statements for marketing, sales, and onboarding from existing value propositions. |

### 工具箱 · `pm-toolkit`（4 个）

覆盖：简历评审、NDA 起草、隐私政策、语法与行文检查。

| 技能 | 用途 |
|---|---|
| `draft-nda` | Draft a detailed Non-Disclosure Agreement between two parties covering information types, jurisdiction, and clauses needing legal review. |
| `grammar-check` | Identify grammar, logical, and flow errors in text and suggest targeted fixes without rewriting the entire text. |
| `privacy-policy` | Draft a detailed privacy policy covering data types, jurisdiction, GDPR and compliance considerations, and clauses needing legal review. |
| `review-resume` | Comprehensive PM resume review and tailoring against 10 best practices including XYZ+S formula, keyword optimization, job-specific tailoring, and structure. |

### AI 交付 · `pm-ai-shipping`（3 个）

覆盖：为 vibe-coded 应用写文档、测试覆盖映射、安全/性能审计、交付包汇编。

| 技能 | 用途 |
|---|---|
| `code-review` | Review code for actionable defects. |
| `intended-vs-implemented` | The method for finding the gap between what a system is supposed to do and what the code actually does — the class of bug generic scanners miss because they have no… |
| `shipping-artifacts` | The durable documentation set that makes an AI-built (vibe-coded) app reviewable before shipping. |

## 二、Superpowers（15 个）

一套相互引用的开发方法论。典型路径：`brainstorming` → `writing-plans` → `executing-plans` 或 `subagent-driven-development` → `verification-before-completion` → `requesting-code-review` / `finishing-a-development-branch`；出问题走 `systematic-debugging`，写/改技能走 `writing-skills`。技能之间的 `../<相邻技能>/...` 相对引用在扁平布局下依然有效。

| 技能 | 用途 |
|---|---|
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software… |
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire… |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is… |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical… |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via… |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before… |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

## 三、srs-skills（9 个）

九阶段 SRS 流水线，串起来用可直接走完整流程：

```text
sr-brainstorm → sr-spec → sr-plan → (人工评审) → sr-generate → sr-validate → sr-improve → sr-save
                        └────────────── srs-workflow 一次编排全程 ──────────────┘
已有原始需求、跳过头脑风暴时：srs-generator
```

| 技能 | 阶段 | 用途 |
|---|---|---|
| `sr-brainstorm` | 第 1 阶段 | User gives a project topic → AI runs a deep, categorized brainstorm (5 mandatory rounds) to fully understand actors, features, scope boundary, tech constraints, and… |
| `sr-generate` | 第 6 阶段 | Reads approved plan files and generates a complete IEEE 830-compliant SRS — one file per section, no word limit. |
| `sr-improve` | 第 8 阶段 | Generates an improvement report covering deferred features, technical risks, validation warnings, and next-version candidates. |
| `sr-plan` | 第 4 阶段 | Reads spec.md and writes one detailed plan file per SRS section (§1–§3 + Appendices). |
| `sr-save` | 第 9 阶段 | Saves all project context to _context/ files so future Claude sessions can resume without re-reading the full SRS. |
| `sr-spec` | 第 2 阶段 | Reads projects/{slug}/brainstorm.md and writes a comprehensive spec.md. |
| `sr-validate` | 第 7 阶段 | Runs srs_validator.py --dir on the generated SRS files, reports errors and warnings, auto-fixes ERRORs, and outputs a COMPLIANT / PARTIALLY COMPLIANT /… |
| `srs-generator` | 入口 | Generate IEEE 830 SRS from raw requirements. |
| `srs-workflow` | 入口 | Full SRS workflow: Brainstorm → Spec → Plan (per-section files) → User Review → SRS Generation → Validation → Improvement Report → Context Save. |

> 上游这几个技能的 frontmatter 写的是 `name: sr:brainstorm`、`cl:srs` 这类带冒号的别名，DSH 不接受，导入时已统一改成 kebab-case（正文里的 `/sr:spec` 等调用提示同步改成 `/sr-spec`），跨 bundle 的 `skills/<bundle>/references/...` 路径改成 `../<bundle>/references/...`。

## 怎么用

模型侧：技能会以「名字 + 一句话用途」出现在会话的技能目录里，模型判断任务匹配后调用 `skill` 工具加载完整正文——不需要你手动指定。

用户侧：所有技能都允许直接以 `/名字` 触发，例如：

```text
/brainstorming        任何创造性工作开工前的需求澄清
/writing-plans        有了需求，先写实施计划再动代码
/test-driven-development   实现任何功能或修 bug 之前
/systematic-debugging 遇到 bug / 测试失败 / 异常行为
/create-prd           写 PRD
/pre-mortem           上线前做风险预演
/srs-workflow         从一个项目想法生成完整 SRS
/code-review          审查改动、找 bug
```

也可以直接用自然语言描述任务，让模型自己挑技能，例如「帮我把这份需求整理成 PRD」「这个 bug 查一下根因再修」。

### 场景速查

| 你要做的事 | 对应技能 |
|---|---|
| 有新想法 / 要加新功能，先想清楚要什么 | `brainstorming` |
| 把需求写成 PRD | `create-prd` |
| 给一堆需求排优先级 | `prioritize-features`、`prioritization-frameworks` |
| 上线前压测计划/策略的风险 | `pre-mortem`、`strategy-red-team` |
| 竞品分析、市场测算、用户画像 | `competitor-analysis`、`market-sizing`、`user-personas` |
| 定价 / 变现模式 | `pricing-strategy`、`monetization-strategy` |
| 准备并整理客户访谈 | `interview-script`、`summarize-interview` |
| 动手写代码前先出实施方案 | `writing-plans` |
| 实现功能 / 修 bug（先写测试） | `test-driven-development` |
| 排查 bug 根因 | `systematic-debugging` |
| 审查改动、找缺陷 | `requesting-code-review`、`code-review` |
| 声称"做完了"之前自检 | `verification-before-completion` |
| 把任务并行拆出去 | `dispatching-parallel-agents`、`subagent-driven-development` |
| 生成软件需求规格说明书 | `srs-workflow`（全流程）、`srs-generator`（已有需求） |
| A/B 实验、留存、写 SQL | `ab-test-analysis`、`cohort-analysis`、`sql-queries` |
| 简历 / NDA / 隐私政策 / 校对 | `review-resume`、`draft-nda`、`privacy-policy`、`grammar-check` |
| 给项目新增或改造技能 | `writing-skills` |

## 维护

```powershell
# 重新导入 / 刷新技能（幂等，先删后拷）
node .dsh/import-skills.js

# 技能索引：本 README 由技能 frontmatter 生成，导入变化后重跑
node .dsh/generate-skills-readme.js

# 核对数量
(Get-ChildItem .dsh/skills -Directory).Count   # 93

# 卸载某一套（按前缀）
Remove-Item .dsh/skills/sr-*,.dsh/skills/srs-* -Recurse -Force
```

注意事项：

- **上下文成本**：93 条描述会进入每轮会话的技能目录（每条上限 500 字符）。如果觉得重，删掉不常用的技能目录即可，`docs/` 里有原始副本随时可恢复。
- **中文版**：`docs/` 下另有 `pm-skills-2.2.0-zh`、`superpowers-7.0.1-zh`、`superpowers-7.0.1-zh-full`、`srs-skills-zh`。它们与英文版技能名完全重名，不能同时导入；要换语言，把 `import-skills.js` 里的来源目录换成 `-zh` 版本（superpowers 用 `-zh-full`），删掉 `.dsh/skills` 后重跑。
- **上游内容未被修改**：`docs/` 是原样保留的仓库副本；只有 `.dsh/skills/` 里的副本做过名称与路径规范化（详见 `.dsh/README.md`）。
- **上游贡献规则**：`docs/` 内各仓库自带 `AGENTS.md` / `CLAUDE.md`，其中 superpowers 对 agent 提交 PR 有严格限制，如果要在这些上游仓库里改东西，先读那一份。
