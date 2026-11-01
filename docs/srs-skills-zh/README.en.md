# srs-skills

[Tiếng Việt](./README.md) · [English](./README.en.md)

AI 技能包：从一句原始想法出发，生成完整、结构化并通过校验的**软件需求规格说明书（IEEE 830-1998）**。

开箱即可用于 Claude Code。兼容 Gemini CLI、GitHub Copilot，以及任何能遵循 markdown 指令文件的 LLM。

## 技能索引

| 技能 | 作用 |
|---|---|
| [srs-workflow](./skills/srs-workflow/) | 编排从想法到交接的完整流水线 |
| [srs-generator](./skills/srs-generator/) | 从已有需求快速生成 SRS |
| [sr-brainstorm](./skills/sr-brainstorm/) | 通过 5 轮提问获取需求 |
| [sr-spec](./skills/sr-spec/) | 把头脑风暴结果汇总成规格 |
| [sr-plan](./skills/sr-plan/) | 为每个 SRS 章节制定蓝图 |
| [sr-generate](./skills/sr-generate/) | 生成 IEEE 830 文档集 |
| [sr-validate](./skills/sr-validate/) | 校验结构并修复错误 |
| [sr-improve](./skills/sr-improve/) | 建立改进待办列表 |
| [sr-save](./skills/sr-save/) | 保存上下文，供后续会话继续 |

---

## 它做什么

把一个想法或主题变成符合标准的 SRS，而需求本身一个字都不用你亲手写。流水线负责结构化需求获取、规格撰写、计划生成、SRS 生成、IEEE 830 校验以及改进建议。

```
Idea / Topic → Brainstorm → Spec → Plan → SRS (multi-file) → Validate → Improve → Save
```

或者，如果你已经有现成的需求文本：

```
Existing requirements text → /cl:srs → IEEE 830 SRS
```

---

## 前置条件

- 已安装并配置好 **Claude Code CLI**，并持有有效的 Anthropic API key
- **Python 3.8+** 在 `PATH` 中（校验脚本与可选的 CLI 工具需要）

除 Anthropic API 之外，不需要任何外部服务。

---

## 安装

**最快的方式——直接打开这个文件夹：**

把 `srs-skills/` 作为你的 Claude Code 工作区打开。所有技能与脚本立刻可用。

**复制到已有项目：**

```bash
# Quick SRS skill only
cp -r srs-skills/skills/srs-generator <your-project>/skills/srs-generator/

# Full pipeline skill
cp -r srs-skills/skills/srs-workflow <your-project>/skills/srs-workflow/

# Automation scripts (optional)
cp -r srs-skills/scripts <your-project>/
cp -r srs-skills/hooks <your-project>/hooks/
cp srs-skills/settings.json <your-project>/settings.json
```

---

## 选择你的工作流

| 情况 | 命令 |
|---|---|
| 你只有一个主题或想法，还没有写需求 | 使用下面的完整流水线（`/sr:*`） |
| 你已经有需求文本 | `/cl:srs` —— 直接跳到 SRS 生成 |

---

## 完整流水线：`/sr:*` 命令

按顺序执行各个步骤。每一步都会读取上一步的输出。

### 第 1 步 —— `/sr:brainstorm`

**目的：** 通过 5 轮有针对性的问题，做结构化的需求获取。

从你的主题开始。AI 会分 5 轮提出带可选项的问题：

| 轮次 | 关注点 |
|---|---|
| 1 | 参与者与用户——谁使用系统、怎么使用 |
| 2 | 核心功能——系统必须做什么 |
| 3 | 范围——什么在范围内、什么明确排除在外 |
| 4 | 技术约束 + NFR 目标——性能、安全、平台 |
| 5 | 业务规则与边界情况——约束和异常流程 |

AI **绝不猜测**——只要有不明确的地方就提出澄清问题。只有当没有遗留待办项时，这一轮才结束。

**输出：** `projects/{slug}/brainstorm.md`

---

### 第 2 步 —— `/sr:spec`

**目的：** 把头脑风暴的产出转成结构化的叙述式规格。

读取 `brainstorm.md`，写出完整规格，覆盖：参与者、功能清单、业务规则、NFR 基线、假设以及待办项。不限字数——所有已捕获的细节都保留。

**输出：** `projects/{slug}/spec.md`

---

### 第 3 步 —— `/sr:plan`

**目的：** 在生成 SRS 之前，先为每个 SRS 章节生成详细计划。

读取 `spec.md`，创建 **12 个独立的计划文件**——每个 SRS 章节一份蓝图（§1 到 §3、附录 A 和 B）。每份蓝图包含 FR 桩、NFR 目标，以及驱动后续生成的结构性决策。

在这一步结束时，AI 会把计划交给你审阅，并在进入生成之前征求批准。

**输出：** `projects/{slug}/plan/`（12 个文件）

---

### 第 4 步 —— `/sr:generate`

**目的：** 根据已批准的计划生成完整的 SRS 文档。

读取已批准的计划文件，产出一份完整的、符合 IEEE 830 的 SRS，不限字数——复杂系统可达 300 多页。为便于管理，每个章节都是独立文件。

**生成期间强制执行的规则：**

- 每条功能需求都使用 `The system shall ...` 句式
- 每条 FR 都有 Given / When / Then 验收标准
- 每条非功能需求都有数值化的响应度量（不要用「fast」「secure」这类含糊形容词）

**输出：** `projects/{slug}/srs/`（11 个章节文件 + 总索引）

---

### 第 5 步 —— `/sr:validate`

**目的：** 自动化的 IEEE 830 合规检查。

对整个 `srs/` 目录运行 `srs_validator.py`，检查：

| 检查项 | 校验内容 |
|---|---|
| 必需章节 | IEEE 830 的所有必需章节都已存在 |
| FR 编号 | FR 编号序列没有缺口 |
| shall 子句 | 每条 FR 都包含 shall 句式 |
| GWT 覆盖 | 每条 FR 都有 Given / When / Then 标准 |
| NFR 目标 | 所有 NFR 都有数值化的响应度量 |
| 未解决标记 | 没有遗留的 `[TBD]` 或 `[CONTEXT-GAP]` 标记 |

**行为：**
- **ERRORs** —— 在当前会话中立即修复
- **WARNs** —— 传递给下一步供其考虑

**判定：** `COMPLIANT` / `PARTIALLY COMPLIANT` / `NON-COMPLIANT`

---

### 第 6 步 —— `/sr:improve`

**目的：** 生成结构化的改进报告。

产出一份按优先级排序的改进报告，覆盖：被推迟的功能及其原因、规格中发现的技术风险、NFR 缺口（设定了目标但可能不现实的领域）、应当拆分成更小需求的 FR，以及校验步骤带过来的所有警告。

**输出：** `projects/{slug}/improvement-report.md`

---

### 第 7 步 —— `/sr:save`

**目的：** 保存一份精简的项目上下文快照，供后续 Claude Code 会话使用。

把整条流水线的关键决策持久化到 6 个小文件里，这样新会话无需重读整份 SRS 就能重新加载项目上下文。

**输出：** `projects/{slug}/_context/` —— 6 个文件：
- `vision.md` —— 项目目标与参与者
- `features.md` —— 功能清单及优先级
- `tech-stack.md` —— 已确认的技术决策
- `glossary.md` —— 领域术语与定义
- `quality-standards.md` —— NFR 目标与合规说明
- `session-notes.md` —— 待办项与已做的决策

---

## 快速 SRS：`/cl:srs`

当你已经有需求文本、想直接得到一份 IEEE 830 的 SRS 时，用这个。

**工作原理：**

1. 粘贴你的需求文本（或提供文件引用）
2. AI 扫描 7 类歧义：含糊的量词、未定义的参与者、缺失的错误流程、相互矛盾、无依据的断言、范围蔓延信号，以及可测试性缺口
3. 澄清问题按优先级提出——P1 阻塞项优先
4. 生成一份单文件的、符合 IEEE 830 的 SRS

**什么时候用 `/cl:srs`，什么时候用完整流水线：**

| 使用 `/cl:srs` | 使用 `/sr:*` 流水线 |
|---|---|
| 你已经有写好的需求文档或需求简报 | 你只有一个主题，要从零开始 |
| 时间紧，想要快速产出 | 你想要充分的需求获取和多文件的 SRS |
| 内部工具、范围较小 | 面向客户、学术或生产级系统 |

---

## CLI 脚本（可选）

`scripts/` 目录里是可直接运行的独立 Python 工具：

```bash
# Scan a requirements text file for gaps before feeding it to the AI
python scripts/gap_scanner.py requirements.txt

# Validate an SRS directory against IEEE 830
python scripts/srs_validator.py --dir projects/{slug}/srs/

# Strict mode — treat WARNs as ERRORs
python scripts/srs_validator.py --dir projects/{slug}/srs/ --strict

# Output as JSON (for CI integration or downstream tooling)
python scripts/srs_validator.py --dir projects/{slug}/srs/ --format json

# Initialize the project scaffold for a new project
python scripts/init_project.py {slug}
```

---

## 输出结构

```
projects/{slug}/
├── brainstorm.md              ← Step 1 output — structured Q&A results
├── spec.md                    ← Step 2 output — full specification prose
├── plan/                      ← Step 3 output — 12 section blueprints
│   ├── plan-01-introduction.md
│   ├── plan-02-overall-desc.md
│   └── ... (12 files total)
├── srs/                       ← Step 4 output — full IEEE 830 SRS
│   ├── INDEX.md               ← Master index with section links
│   ├── section-1-introduction.md
│   ├── section-2-overall-description.md
│   ├── section-3-requirements.md
│   └── ... (11 files total)
├── improvement-report.md      ← Step 6 output
└── _context/                  ← Step 7 output — compact session-reload snapshots
    ├── vision.md
    ├── features.md
    ├── tech-stack.md
    ├── glossary.md
    ├── quality-standards.md
    └── session-notes.md
```

---

## 与其他工具集成

技能文件就是纯 Markdown——任何能遵循书面指令的 LLM 都能使用。

### Claude Code（内置）

```
skills/srs-generator/SKILL.md  ← /cl:srs
skills/srs-workflow/SKILL.md   ← /cl:srs-flow
```

打开工作区后，技能会自动出现在 Claude Code 的自动补全里。

### Gemini CLI

```bash
cp -r srs-skills/skills/srs-generator .gemini/skills/
cp -r srs-skills/skills/srs-workflow .gemini/skills/
```

添加到 `.gemini/system.md`：
```
When the user types @srs: follow .gemini/skills/srs-generator/SKILL.md
When the user types @srs-flow: follow .gemini/skills/srs-workflow/SKILL.md
```

### GitHub Copilot（工作区指令）

添加到 `.github/copilot-instructions.md`：
```
For quick SRS from existing requirements, follow: srs-skills/skills/srs-generator/SKILL.md
For full brainstorm-to-SRS pipeline, follow: srs-skills/skills/srs-workflow/SKILL.md
```

### 任何其他 LLM 或代理

把技能文件加载进代理的系统提示词：

| 目标 | 需要加载的文件 |
|---|---|
| 从已有需求快速生成 SRS | `skills/srs-generator/SKILL.md` + `references/srs-template.md` + `references/gap-detection-guide.md` |
| 从主题走完整流水线 | `skills/srs-workflow/SKILL.md` + 两个 `references/` 目录 |

不需要任何外部 API。Python 脚本是可选的增强项。

### 各工具的别名约定

| 工具 | 快速 SRS | 完整流水线 |
|---|---|---|
| Claude Code | `/cl:srs` | `/cl:srs-flow` |
| Gemini CLI | `@srs` | `@srs-flow` |
| GitHub Copilot | `#srs` | `#srs-flow` |
| 自定义代理 | `!srs` | `!srs-flow` |

---

## 与 Virtual Team Skill 集成

如果你使用 [Virtual Team Skill](../virtual-team-skill/README.md)，可以把生成的规格直接喂给 BA 代理：

```
/team-ba --project my-app --level mid --spec projects/my-app/spec.md
```

BA 代理会读取 `projects/my-app/spec.md`（如果存在 `brainstorm.md` 也一并读取），而不是让你描述需求。这样整条团队流水线就能以一份精确、经过校验的规格作为起点。

---

## 命令汇总

```
Full pipeline (start from idea):
  /sr:brainstorm → /sr:spec → /sr:plan → /sr:generate → /sr:validate → /sr:improve → /sr:save

  or shorthand full pipeline:  /cl:srs-flow

Quick SRS (start from existing requirements text):
  /cl:srs
```
