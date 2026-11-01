# 技能编写最佳实践

> 学习如何写出有效的技能，让代理能发现并成功使用它们。

好的技能简洁、结构清晰，并经过真实使用的检验。本指南给出实用的编写决策，帮你写出代理能发现并有效使用的技能。

关于技能如何运作的概念背景，见 [技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 是一种公共资源。你的技能要与代理需要知道的其他一切共享这个上下文窗口，包括：

* 系统提示词
* 对话历史
* 其它技能的元数据
* 你真正的请求

你的技能里不是每个 token 都有直接成本。启动时，只会预加载所有技能的元数据（name 与 description）。代理只在技能变得相关时才读 SKILL.md，并且只在需要时读额外文件。不过，保持 SKILL.md 简洁仍然重要：一旦代理加载它，每个 token 都在与对话历史和其他上下文竞争。

**默认假设**：代理已经非常聪明

只补充代理还没有的上下文。对每条信息都要质疑：

* 「代理真的需要这段解释吗？」
* 「我可以假设代理已经知道这个吗？」
* 「这一段值得它花掉的 token 吗？」

**好例子：简洁**（约 50 个 token）：

````markdown  theme={null}
## 提取 PDF 文本

用 pdfplumber 提取文本：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**坏例子：过于啰嗦**（约 150 个 token）：

```markdown  theme={null}
## 提取 PDF 文本

PDF（Portable Document Format）是一种常见的文件格式，其中包含
文本、图片和其他内容。要从 PDF 中提取文本，你需要使用一个库。
可用的 PDF 处理库很多，但我们推荐 pdfplumber，因为它易用，
而且能很好地处理大多数情况。
首先你需要用 pip 安装它，然后就可以使用下面的代码……
```

简洁版假设代理知道 PDF 是什么、库是怎么工作的。

### 设定合适的自由度

让具体程度与任务的脆弱性和可变性相匹配。

**高自由度**（基于文本的指令）：

适用于：

* 多种做法都成立
* 决策取决于上下文
* 靠启发式方法引导做法

示例：

```markdown  theme={null}
## 代码评审流程

1. 分析代码结构与组织方式
2. 检查潜在的 bug 与边界情况
3. 提出可读性与可维护性方面的改进
4. 验证是否符合项目约定
```

**中等自由度**（伪代码或带参数的脚本）：

适用于：

* 已有偏好的模式
* 允许一定变化
* 配置会影响行为

示例：

````markdown  theme={null}
## 生成报告

使用这个模板，并按需定制：

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**低自由度**（具体脚本，参数很少或没有）：

适用于：

* 操作脆弱且容易出错
* 一致性至关重要
* 必须遵循特定顺序

示例：

````markdown  theme={null}
## 数据库迁移

严格按这个脚本执行：

```bash
python scripts/migrate.py --verify --backup
```

不要修改这条命令，也不要添加额外参数。
````

**类比**：把代理想象成一个正在探路的机器人：

* **两侧是悬崖的窄桥**：只有一条安全的前进路线。要给出具体的护栏和精确指令（低自由度）。示例：必须按精确顺序执行的数据库迁移。
* **没有危险的旷野**：很多路径都能成功。给出大致方向，信任代理自己找到最佳路线（高自由度）。示例：代码评审，由上下文决定最佳做法。

### 在你打算使用的所有模型上测试

技能是对模型的补充，所以效果取决于底层模型。要在你打算搭配使用的所有模型上测试你的技能。

**按模型区分的测试考量**：

* **Claude Haiku**（快、便宜）：技能给出的指引够不够？
* **Claude Sonnet**（均衡）：技能是否清晰、高效？
* **Claude Opus**（推理强）：技能是否避免了过度解释？

对 Opus 恰到好处的内容，对 Haiku 可能需要更详细。如果你打算在多个模型上使用技能，就要追求让它们都好用的指令。

## 技能结构

<Note>
  **YAML frontmatter**：SKILL.md 的 frontmatter 需要两个字段：

  * `name` —— 技能的人类可读名称（最多 64 个字符）
  * `description` —— 一行描述，说明技能做什么、何时使用（最多 1024 个字符）

  完整的技能结构细节见 [技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 命名约定

使用一致的命名模式，让技能更容易被引用和讨论。我们建议技能名用**动名词形式**（动词 + -ing），这样能清楚描述技能提供的活动或能力。

**好的命名示例（动名词形式）**：

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**可接受的替代形式**：

* 名词短语：“PDF Processing”、“Spreadsheet Analysis”
* 动作导向：“Process PDFs”、“Analyze Spreadsheets”

**避免**：

* 含糊的名字：“Helper”、“Utils”、“Tools”
* 过于泛化：“Documents”、“Data”、“Files”
* 你的技能集合内部模式不一致

一致的命名让以下事情更容易：

* 在文档和对话中引用技能
* 一眼看懂一个技能做什么
* 组织并检索多个技能
* 维护一个专业、连贯的技能库

### 编写有效的 description

`description` 字段决定技能能否被发现，应当同时写清技能做什么、何时使用。

<Warning>
  **始终用第三人称写**。description 会被注入系统提示词，人称不一致会导致发现失败。

  * **好**：“Processes Excel files and generates reports”
  * **避免**：“I can help you process Excel files”
  * **避免**：“You can use this to process Excel files”
</Warning>

**要具体，并包含关键术语**。既写清技能做什么，也写清使用它的具体触发条件／场景。

每个技能有且只有一个 description 字段。description 对技能选择至关重要：代理要从可能 100 多个可用技能中挑出正确的那一个。你的 description 必须给足细节，让代理知道何时该选这个技能，而 SKILL.md 的其余部分提供实现细节。

有效示例：

**PDF Processing 技能：**

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel Analysis 技能：**

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git Commit Helper 技能：**

```yaml  theme={null}
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避免下面这种含糊的描述：

```yaml  theme={null}
description: Helps with documents
```

```yaml  theme={null}
description: Processes data
```

```yaml  theme={null}
description: Does stuff with files
```

### 渐进式披露模式

SKILL.md 是一份概览，就像上手指南里的目录那样，在需要时把代理指向详细材料。关于渐进式披露如何运作的解释，见概览里的 [技能如何工作](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

**实用指引：**

* 为获得最佳表现，把 SKILL.md 正文控制在 500 行以内
* 接近这个上限时，把内容拆到独立文件
* 用下面的模式来有效组织指令、代码和资源

#### 可视化概览：从简单到复杂

一个基础技能只需要一个 SKILL.md 文件，里面包含元数据和指令：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="Simple SKILL.md file showing YAML frontmatter and markdown body" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

随着技能成长，你可以把额外内容打包进去，让代理只在需要时加载：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="Bundling additional reference files like reference.md and forms.md." data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

完整的技能目录结构可能长这样：

```
pdf/
├── SKILL.md              # 主要指令（触发时加载）
├── FORMS.md              # 表单填写指南（按需加载）
├── reference.md          # API 参考（按需加载）
├── examples.md           # 用法示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 工具脚本（执行，不加载）
    ├── fill_form.py      # 表单填写脚本
    └── validate.py       # 校验脚本
```

#### 模式 1：带引用文件的概览式指南

````markdown  theme={null}
---
name: PDF Processing
description: 从 PDF 文件中提取文本和表格、填写表单、合并文档。适用于处理 PDF 文件，或用户提到表单与文档提取时。
---

# PDF 处理

## 快速开始

用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 进阶功能

**表单填写**：完整指南见 [FORMS.md](FORMS.md)
**API 参考**：所有方法见 [REFERENCE.md](REFERENCE.md)
**示例**：常见模式见 [EXAMPLES.md](EXAMPLES.md)
````

代理只在需要时才加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

#### 模式 2：按领域组织

对于跨多个领域的技能，按领域组织内容，避免加载无关上下文。当用户问的是销售指标，代理只需要读销售相关的表结构，不需要财务或营销数据。这样 token 用量低、上下文集中。

```
bigquery-skill/
├── SKILL.md（概览与导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（商机、销售管道）
    ├── product.md（API 使用情况、功能）
    └── marketing.md（营销活动、归因）
```

````markdown SKILL.md theme={null}
# BigQuery 数据分析

## 可用的数据集

**财务**：收入、ARR、计费 → 见 [reference/finance.md](reference/finance.md)
**销售**：商机、销售管道、客户账户 → 见 [reference/sales.md](reference/sales.md)
**产品**：API 使用情况、功能、采用情况 → 见 [reference/product.md](reference/product.md)
**营销**：营销活动、归因、邮件 → 见 [reference/marketing.md](reference/marketing.md)

## 快速搜索

用 grep 查找特定指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### 模式 3：条件式细节

给出基础内容，链接到进阶内容：

```markdown  theme={null}
# DOCX 处理

## 创建文档

新文档请用 docx-js。见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

简单编辑可直接修改 XML。

**修订模式**：见 [REDLINING.md](REDLINING.md)
**OOXML 细节**：见 [OOXML.md](OOXML.md)
```

代理只在用户需要那些功能时才读 REDLINING.md 或 OOXML.md。

### 避免深层的嵌套引用

当文件是通过别的被引用文件再被引用时，代理可能只读到文件的一部分。遇到嵌套引用时，代理可能会用 `head -100` 这类命令预览内容，而不是读完整文件，结果信息不完整。

**所有引用都只离 SKILL.md 一层**。所有参考文件都应当直接从 SKILL.md 链接过去，确保代理在需要时读到完整文件。

**坏例子：层级太深**：

```markdown  theme={null}
# SKILL.md
见 [advanced.md](advanced.md)……

# advanced.md
见 [details.md](details.md)……

# details.md
这里才是真正的信息……
```

**好例子：只有一层**：

```markdown  theme={null}
# SKILL.md

**基本用法**：[instructions in SKILL.md]
**进阶功能**：见 [advanced.md](advanced.md)
**API 参考**：见 [reference.md](reference.md)
**示例**：见 [examples.md](examples.md)
```

### 给较长的参考文件加上目录

参考文件超过 100 行时，在开头放一个目录。这样即使代理只是部分预览，也能看到可用信息的完整范围。

**示例**：

```markdown  theme={null}
# API 参考

## 目录
- 身份认证与初始化
- 核心方法（创建、读取、更新、删除）
- 进阶功能（批量操作、webhook）
- 错误处理模式
- 代码示例

## 身份认证与初始化
...

## 核心方法
...
```

这样代理就可以读完整文件，或按需跳到特定章节。

关于这种基于文件系统的架构如何实现渐进式披露，见下文「高级」部分的 [运行时环境](#runtime-environment) 一节。

## 工作流与反馈闭环

### 复杂任务用工作流

把复杂操作拆成清晰、有先后顺序的步骤。对特别复杂的工作流，给一份检查清单，让代理可以复制进自己的回复，边做边勾。

**示例 1：研究综合工作流**（适用于不含代码的技能）：

````markdown  theme={null}
## 研究综合工作流

复制这份检查清单，跟踪你的进度：

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**第 1 步：阅读所有源文档**

逐一阅读 `sources/` 目录下的每份文档，记下主要论点与支撑证据。

**第 2 步：找出关键主题**

在各来源之间找规律。哪些主题反复出现？各来源在哪里一致、在哪里冲突？

**第 3 步：交叉核对论断**

对每个主要论断，核实它确实出现在源材料中，并记下每条论断由哪个来源支撑。

**第 4 步：创建结构化摘要**

按主题组织发现，包含：
- 主要论断
- 来自各来源的支撑证据
- 相互冲突的观点（如果有）

**第 5 步：核对引用**

检查每条论断是否都指向了正确的源文档。如果引用不完整，回到第 3 步。
````

这个例子说明工作流如何用于不需要代码的分析任务。检查清单这个模式适用于任何复杂、多步骤的流程。

**示例 2：PDF 表单填写工作流**（适用于含代码的技能）：

````markdown  theme={null}
## PDF 表单填写工作流

复制这份检查清单，完成一项就勾掉一项：

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**第 1 步：分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这会提取表单字段及其位置，并保存到 `fields.json`。

**第 2 步：创建字段映射**

编辑 `fields.json`，为每个字段填入值。

**第 3 步：校验映射**

运行：`python scripts/validate_fields.py fields.json`

继续之前，先修复所有校验错误。

**第 4 步：填写表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**第 5 步：验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，回到第 2 步。
````

清晰的步骤能防止代理跳过关键校验。检查清单帮你和代理一起跟踪多步骤工作流的进度。

### 实现反馈闭环

**常见模式**：运行校验器 → 修复错误 → 重复

这个模式能大幅提升产出质量。

**示例 1：遵循风格指南**（适用于不含代码的技能）：

```markdown  theme={null}
## 内容评审流程

1. 按 STYLE_GUIDE.md 中的指南起草内容
2. 对照检查清单逐项自查：
   - 检查术语是否一致
   - 确认示例符合标准格式
   - 确认所有必需小节都已包含
3. 如果发现问题：
   - 逐条记录问题，并指明对应小节
   - 修改内容
   - 再对照一遍检查清单
4. 只有所有要求都满足才继续
5. 定稿并保存文档
```

这里展示的是用参考文档而不是脚本实现的校验闭环。这个「校验器」就是 STYLE\_GUIDE.md，代理通过阅读和比对来完成检查。

**示例 2：文档编辑流程**（适用于含代码的技能）：

```markdown  theme={null}
## 文档编辑流程

1. 对 `word/document.xml` 做修改
2. **立即校验**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果校验失败：
   - 仔细阅读错误信息
   - 在 XML 中修复问题
   - 再次运行校验
4. **只有校验通过才继续**
5. 重新打包：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试输出文档
```

校验闭环能尽早发现错误。

## 内容准则

### 避免时效性信息

不要写会过时的信息：

**坏例子：时效性内容**（会变得不正确）：

```markdown  theme={null}
如果你在 2025 年 8 月之前做这件事，就用旧 API。
2025 年 8 月之后，用新 API。
```

**好例子**（用「旧模式」小节）：

```markdown  theme={null}
## 当前做法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（已于 2025-08 弃用）</summary>

v1 API 用的是：`api.example.com/v1/messages`

该端点已不再支持。
</details>
```

「旧模式」小节提供了历史背景，又不弄乱主体内容。

### 术语保持一致

选定一个术语，在整个技能里统一使用：

**好——一致**：

* 始终用 “API endpoint”
* 始终用 “field”
* 始终用 “extract”

**坏——不一致**：

* 混用 “API endpoint”、“URL”、“API route”、“path”
* 混用 “field”、“box”、“element”、“control”
* 混用 “extract”、“pull”、“get”、“retrieve”

一致性能帮代理理解和遵循指令。

## 常用模式

### 模板模式

为输出格式提供模板。按需要决定严格程度。

**严格需求**（如 API 响应或数据格式）：

````markdown  theme={null}
## 报告结构

必须始终（ALWAYS）使用这个确切的模板结构：

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**灵活指引**（在需要适配时有用）：

````markdown  theme={null}
## 报告结构

下面是一个合理的默认格式，但请根据分析内容自行判断：

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

按具体分析类型按需调整小节。
````

### 示例模式

如果技能的输出质量取决于是否看过示例，就像常规提示那样给出输入／输出对照：

````markdown  theme={null}
## 提交信息格式

按这些示例生成提交信息：

**示例 1：**
输入：新增基于 JWT token 的用户身份认证
输出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**示例 2：**
输入：修复报告中日期显示不正确的问题
输出：
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**示例 3：**
输入：更新依赖并重构错误处理
输出：
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

遵循这个风格：type(scope)：简要描述，然后是详细说明。
````

比起只给描述，示例能更清楚地让代理理解想要的风格和细节程度。

### 条件式工作流模式

引导代理走过各个决策点：

```markdown  theme={null}
## 文档修改工作流

1. 判断修改类型：

   **是创建新内容吗？** → 走下面的「创建流程」
   **是在编辑现有内容吗？** → 走下面的「编辑流程」

2. 创建流程：
   - 使用 docx-js 库
   - 从零构建文档
   - 导出为 .docx 格式

3. 编辑流程：
   - 解包现有文档
   - 直接修改 XML
   - 每次改动后都校验
   - 完成后重新打包
```

<Tip>
  如果工作流变得很大、步骤很多，考虑把它们放进独立文件，并告诉代理根据手头任务读对应的文件。
</Tip>

## 评测与迭代

### 先建立评测

**在写大量文档之前先创建评测。** 这能确保你的技能解决的是真实问题，而不是把想象出来的问题写成文档。

**评测驱动开发：**

1. **找出缺口**：让代理在没有技能的情况下跑代表性任务。记录具体的失败或缺失的上下文
2. **创建评测**：构造三个场景来检验这些缺口
3. **建立基线**：测量代理在没有技能时的表现
4. **写最小指令**：只写足够解决这些缺口、并通过评测的内容
5. **迭代**：执行评测，与基线对比，然后改进

这个做法确保你在解决真实问题，而不是去预判可能永远不会出现的需求。

**评测结构**：

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  这个例子演示了一个带简单测试评分表的数据驱动评测。我们目前没有提供运行这些评测的内置方式。用户可以自建评测体系。评测是你衡量技能有效性的唯一事实来源。
</Note>

### 和代理一起迭代开发技能

最有效的技能开发流程要拉上代理本身。和一个实例（「代理 A」）一起创建技能，再把技能交给其他实例（「代理 B」）使用。代理 A 帮你设计和改进指令，代理 B 在真实任务里测试它们。之所以有效，是因为底层模型既懂怎么写有效的代理指令，也知道代理需要什么信息。

**创建一个新技能：**

1. **先在没有技能的情况下完成一个任务**：用常规提示和代理 A 一起解决一个问题。过程中你会自然地提供上下文、解释偏好、分享流程知识。留意你反复提供了哪些信息。

2. **找出可复用的模式**：完成任务后，找出你提供的哪些上下文对将来类似的任务有用。

   **示例**：如果你做的是一次 BigQuery 分析，你可能提供过表名、字段定义、过滤规则（比如「总是排除测试账号」）以及常见查询模式。

3. **让代理 A 创建技能**：「创建一个技能，把刚才这套 BigQuery 分析模式固化下来。包含表结构、命名约定，以及过滤测试账号的规则。」

   <Tip>
     现代代理天生理解技能的格式和结构。你不需要特殊的系统提示词，也不需要「writing skills」技能来帮你创建技能。直接让代理创建一个技能，它就会生成结构正确的 SKILL.md 内容，frontmatter 和正文都会合适。
   </Tip>

4. **审查简洁性**：检查代理 A 是否加了不必要的解释。问它：「把解释什么是赢单率的那段删掉——代理已经知道了。」

5. **改进信息架构**：让代理 A 更有效地组织内容。例如：「把表结构整理到单独的参考文件里，我们之后可能还会加更多表。」

6. **在类似任务上测试**：让代理 B（加载了技能的新实例）在相关场景里使用这个技能。观察代理 B 能否找到正确的信息、正确应用规则、顺利完成任务。

7. **根据观察迭代**：如果代理 B 卡住或漏了什么，带着具体细节回到代理 A：「代理用这个技能时，忘了按 Q4 过滤日期。我们要不要加一节讲日期过滤的常见做法？」

**迭代已有技能：**

改进技能时，同样是这种分层模式在继续。你在以下几件事之间交替：

* **和代理 A 一起工作**（帮你打磨技能的专家）
* **用代理 B 测试**（拿技能做真实工作的代理）
* **观察代理 B 的行为**，把洞察带回给代理 A

1. **在真实工作流里使用技能**：交给代理 B（已加载技能）真实任务，而不是测试场景

2. **观察代理 B 的行为**：记下它在哪些地方卡住、成功，或做出意料之外的选择

   **观察示例**：「我让代理 B 出一份区域销售报告时，它写了查询，却忘了过滤掉测试账号，尽管技能里提到了这条规则。」

3. **回到代理 A 做改进**：把当前的 SKILL.md 给它，并描述你观察到的现象。问它：「我注意到代理 B 在我要求区域报告时忘了过滤测试账号。技能里提到了过滤，但也许不够显眼？」

4. **审查代理 A 的建议**：代理 A 可能会建议重新组织内容让规则更显眼，用更强的措辞（比如用「必须过滤」而不是「始终过滤」），或者重构工作流那一节。

5. **应用改动并测试**：按代理 A 的改进更新技能，再让代理 B 在类似请求上测一遍

6. **按使用情况重复**：遇到新场景就继续这个「观察—改进—测试」的循环。每一轮迭代都是基于代理的真实行为，而不是凭假设。

**收集团队反馈：**

1. 把技能分享给队友，观察他们怎么用
2. 问：技能是否在预期时触发？指令清楚吗？缺了什么？
3. 吸收反馈，补上你自己使用模式里的盲区

**为什么这套做法有效**：代理 A 懂代理需要什么，你提供领域专长，代理 B 通过真实使用暴露缺口，而迭代改进让技能基于观察到的行为、而不是假设来变好。

### 观察代理如何在技能中穿行

迭代技能时，留意代理在实践中实际是怎么用它们的。注意这些现象：

* **意料之外的探索路径**：代理读文件的顺序和你预想的不一样？这可能说明你的结构没有你想的那么直观
* **漏掉的连接**：代理没有顺着引用去读重要文件？你的链接可能需要更明确、更显眼
* **过度依赖某些小节**：如果代理反复读同一个文件，考虑那部分内容是不是该放进主 SKILL.md
* **被忽略的内容**：如果代理从不访问某个打包文件，它可能没必要，或者在主指令里提示得不够

根据这些观察来迭代，而不是凭假设。技能元数据里的 'name' 和 'description' 尤其关键。代理在判断是否针对当前任务触发技能时，用的就是它们。务必让它们清楚说明技能做什么、什么时候该用。

## 要避免的反模式

### 避免 Windows 风格路径

文件路径一律用正斜杠，即使在 Windows 上也是如此：

* ✓ **好**：`scripts/helper.py`、`reference/guide.md`
* ✗ **避免**：`scripts\helper.py`、`reference\guide.md`

Unix 风格路径在所有平台都能用，而 Windows 风格路径在 Unix 系统上会报错。

### 避免给太多选项

除非必要，不要摆出多种做法：

````markdown  theme={null}
**坏例子：选项太多**（令人困惑）：
"你可以用 pypdf，或者 pdfplumber，或者 PyMuPDF，或者 pdf2image，或者……"

**好例子：给出默认值**（并留出逃生口）：
"用 pdfplumber 提取文本：
```python
import pdfplumber
```

需要 OCR 的扫描版文件，改用 pdf2image 配 pytesseract。"
````

## 高级：带可执行代码的技能

下面几节讲的是包含可执行脚本的技能。如果你的技能只用 markdown 指令，直接跳到 [有效技能检查清单](#checklist-for-effective-skills)。

### 自己解决，不要推给代理

给技能写脚本时，要处理错误情况，而不是把问题推给代理。

**好例子：显式处理错误**：

```python  theme={null}
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```

**坏例子：推给代理**：

```python  theme={null}
def process_file(path):
    # Just fail and let the agent figure it out
    return open(path).read()
```

配置参数也要有理由并写进文档，避免「巫毒常量」（Ousterhout 定律）。如果你都不知道正确的值，代理又怎么能确定？

**好例子：自解释**：

```python  theme={null}
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**坏例子：魔法数字**：

```python  theme={null}
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### 提供工具脚本

即使你的代理自己也能写脚本，预先做好的脚本仍有优势：

**工具脚本的好处**：

* 比生成的代码更可靠
* 省 token（不需要把代码放进上下文）
* 省时间（不需要生成代码）
* 保证不同使用之间的一致性

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="Bundling executable scripts alongside instruction files" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

上图展示了可执行脚本如何与指令文件配合。指令文件（forms.md）引用脚本，代理可以直接执行它，而不必把脚本内容加载进上下文。

**一个重要区别**：在指令里说清楚代理应该：

* **执行脚本**（最常见）：「运行 `analyze_form.py` 来提取字段」
* **当作参考来读**（用于复杂逻辑）：「字段提取算法见 `analyze_form.py`」

对多数工具脚本来说，执行是首选，因为它更可靠、更高效。脚本执行如何运作，见下面的 [运行时环境](#runtime-environment) 一节。

**示例**：

````markdown  theme={null}
## 工具脚本

**analyze_form.py**：提取 PDF 中的所有表单字段

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

输出格式：
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**：检查互相重叠的边界框

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**：把字段值写入 PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### 使用视觉分析

当输入可以渲染成图片时，让代理去分析它们：

````markdown  theme={null}
## 表单布局分析

1. 把 PDF 转成图片：
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. 分析每一页图片，识别表单字段
3. 代理可以直观地看到字段位置与类型
````

<Note>
  在这个例子里，你需要自己写 `pdf_to_images.py` 脚本。
</Note>

代理的视觉能力有助于理解布局和结构。

### 创建可校验的中间产物

代理执行复杂、开放式任务时会犯错。「计划—校验—执行」模式让代理先用结构化格式做出计划，再用脚本校验这个计划，然后才执行，从而尽早发现错误。

**示例**：假设你让代理根据一张表格去更新 PDF 里的 50 个表单字段。没有校验的话，它可能引用不存在的字段、造出互相冲突的值、漏掉必填字段，或者把更新应用错。

**解决方案**：用上面展示的工作流模式（PDF 表单填写），但增加一个中间的 `changes.json` 文件，在应用改动前先校验它。工作流变成：分析 → **创建计划文件** → **校验计划** → 执行 → 验证。

**为什么这个模式有效：**

* **尽早发现错误**：校验在改动应用之前就找出问题
* **机器可校验**：脚本给出客观的验证
* **计划可回退**：代理可以在不碰原始文件的情况下反复改计划
* **调试清晰**：错误信息直接指向具体问题

**何时使用**：批量操作、破坏性改动、复杂校验规则、高风险操作。

**实现提示**：让校验脚本的输出更详细，给出具体的错误信息，比如「Field 'signature\_date' not found. Available fields: customer\_name, order\_total, signature\_date\_signed」，帮助代理修正问题。

### 打包依赖

技能运行在代码执行环境里，并受平台特有的限制：

* **claude.ai**：可以从 npm 和 PyPI 安装包，也能从 GitHub 仓库拉取
* **Anthropic API**：没有网络访问，也不能在运行时安装包

在 SKILL.md 里列出需要的包，并到 [代码执行工具文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) 确认它们可用。

### 运行时环境

技能运行在一个具备文件系统访问、bash 命令和代码执行能力的代码执行环境中。关于这套架构的概念解释，见概览里的 [技能架构](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#the-skills-architecture)。

**这对你的编写有什么影响：**

**代理如何访问技能：**

1. **元数据预加载**：启动时，所有技能 YAML frontmatter 里的 name 和 description 会被加载进系统提示词
2. **文件按需读取**：代理在需要时用读文件工具从文件系统访问 SKILL.md 和其他文件
3. **脚本高效执行**：工具脚本可以通过 bash 执行，不必把全部内容加载进上下文。只有脚本的输出消耗 token
4. **大文件不占上下文**：参考文件、数据或文档在实际被读取之前不消耗上下文 token

* **文件路径很重要**：代理会像浏览文件系统一样浏览你的技能目录。用正斜杠（`reference/guide.md`），不要用反斜杠
* **用有描述性的文件名**：用能说明内容的名字：`form_validation_rules.md`，而不是 `doc2.md`
* **为便于发现而组织**：按领域或功能组织目录
  * 好：`reference/finance.md`、`reference/sales.md`
  * 坏：`docs/file1.md`、`docs/file2.md`
* **打包完整的资源**：放入完整的 API 文档、大量示例、大数据集；在被访问之前不占上下文
* **确定性操作优先用脚本**：写 `validate_form.py`，而不是让代理生成校验代码
* **把执行意图说清楚**：
  * 「运行 `analyze_form.py` 来提取字段」（执行）
  * 「提取算法见 `analyze_form.py`」（当作参考来读）
* **测试文件访问路径**：用真实请求测试，验证代理能浏览你的目录结构

**示例：**

```
bigquery-skill/
├── SKILL.md（概览，指向参考文件）
└── reference/
    ├── finance.md（收入指标）
    ├── sales.md（销售管道数据）
    └── product.md（使用分析）
```

当用户问收入相关的问题时，代理读 SKILL.md，看到指向 `reference/finance.md` 的引用，然后调用 bash 只读那个文件。sales.md 和 product.md 留在文件系统上，在需要之前不消耗任何上下文 token。正是这种基于文件系统的模型让渐进式披露成为可能。代理可以按每个任务的实际需要去浏览并选择性地加载。

关于技术架构的完整细节，见技能概览里的 [技能如何工作](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

### 引用 MCP 工具

如果你的技能用到 MCP（Model Context Protocol）工具，要始终使用完全限定的工具名，避免「工具找不到」的错误。

**格式**：`ServerName:tool_name`

**示例**：

```markdown  theme={null}
使用 BigQuery:bigquery_schema 工具获取表结构。
使用 GitHub:create_issue 工具创建 issue。
```

其中：

* `BigQuery` 和 `GitHub` 是 MCP 服务器名
* `bigquery_schema` 和 `create_issue` 是这些服务器里的工具名

不带服务器前缀时，代理可能定位不到工具，尤其是在有多个 MCP 服务器可用的情况下。

### 避免假设工具已经装好

不要假设包已经可用：

````markdown  theme={null}
**坏例子：假设已经装好**：
"用 pdf 库处理这个文件。"

**好例子：明确说明依赖**：
"安装所需的包：`pip install pypdf`

然后这样用它：
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## 技术备注

### YAML frontmatter 要求

SKILL.md 的 frontmatter 需要 `name`（最多 64 个字符）和 `description`（最多 1024 个字符）两个字段。完整结构细节见 [技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。

### token 预算

为获得最佳表现，把 SKILL.md 正文控制在 500 行以内。如果内容超过这个量，就用前面讲的渐进式披露模式把它拆到独立文件里。架构细节见 [技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

## 有效技能检查清单

分享技能之前，先确认：

### 核心质量

* [ ] description 具体且包含关键术语
* [ ] description 同时写清技能做什么、何时使用
* [ ] SKILL.md 正文在 500 行以内
* [ ] 额外细节放在独立文件里（如需要）
* [ ] 没有时效性信息（或已放进「旧模式」小节）
* [ ] 全篇术语一致
* [ ] 示例具体，不抽象
* [ ] 文件引用只隔一层
* [ ] 恰当使用了渐进式披露
* [ ] 工作流步骤清晰

### 代码与脚本

* [ ] 脚本自己解决问题，而不是推给代理
* [ ] 错误处理显式且有帮助
* [ ] 没有「巫毒常量」（所有取值都有理由）
* [ ] 所需包已在指令中列出，并确认可用
* [ ] 脚本有清晰的文档
* [ ] 没有 Windows 风格路径（全部用正斜杠）
* [ ] 关键操作有校验／验证步骤
* [ ] 质量关键任务包含反馈闭环

### 测试

* [ ] 至少创建了三个评测
* [ ] 在 Haiku、Sonnet 和 Opus 上测试过
* [ ] 用真实使用场景测试过
* [ ] 已吸收团队反馈（如适用）

## 下一步

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    创建你的第一个技能
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    在 Claude Code 里创建和管理技能
  </Card>

  <Card title="Use Skills with the API" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    以编程方式上传并使用技能
  </Card>
</CardGroup>
