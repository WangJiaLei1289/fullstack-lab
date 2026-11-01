---
name: cl:srs-flow
description: "完整 SRS 工作流：头脑风暴 → 规格 → 计划（按章节拆成文件）→ 用户评审 → SRS 生成 → 校验 → 改进报告 → 上下文保存。当用户给出项目主题、希望走完整个需求流水线时使用。"
user-invocable: true
metadata:
  use_when: 用户给出项目主题/想法，希望端到端产出一份完整的 SRS
  do_not_use_when: 用户只想基于已有需求快速生成 SRS（改用 /cl:srs）
  hard_rules: >
    未经用户明确确认，绝不进入下一阶段。
    绝不猜测或假设——不清楚就立刻问。
    绝不截断输出——文件没有字数限制（SRS 可达 300 页以上）。
    所有问题在可能时都必须给出答案选项——绝不只问开放式问题。
  references:
    - skills/srs-workflow/references/brainstorm-guide.md
    - skills/srs-workflow/references/plan-structure-guide.md
    - skills/srs-generator/references/srs-template.md
    - skills/srs-generator/references/gap-detection-guide.md
---

# cl:srs-flow — 完整 SRS 工作流

```
Phase 0  Topic Intake
Phase 1  Deep Brainstorm      ← multi-round, categorized, options-driven
Phase 2  Spec Writing         ← no word limit
Phase 3  Options Gate         ← user chooses next action
Phase 4  Plan Writing         ← 1 .md file per SRS section
Phase 5  User Review          ← iterate until approved
Phase 6  SRS Generation       ← 1 .md file per section, full detail
Phase 7  Auto-Validate        ← scripts/srs_validator.py
Phase 8  Improvement Report
Phase 9  Context Save
```

**输出目录：** `projects/{slug}/`

---

## 第 0 阶段 — 主题接收

接收用户的主题（一句话到一段话均可）。此时不要提问。

识别：
- 领域（电商、医疗、金融科技、内部工具、SaaS 等）
- 规模信号（初创、企业、MVP 等）
- 提到的任何约束

回显一段 3 行摘要：
```
Topic:      {topic}
Domain:     {detected domain}
Scale:      {detected scale or "unknown"}
```

然后说明：「开始深度头脑风暴。我会在动笔之前按类别提问。」
进入第 1 阶段。

---

## 第 1 阶段 — 深度头脑风暴

**硬性规则：在能确信回答以下全部问题之前，AI 不得进入第 2 阶段：**
- 所有参与者是谁（主要 + 次要 + 外部系统）？
- 所有核心功能是什么（不只是提到的——要推断并确认）？
- 明确的系统边界是什么（范围内 / 不在范围内）？
- 技术约束有哪些？
- 业务规则与合规要求有哪些？

加载 `skills/srs-workflow/references/brainstorm-guide.md` 以获取按领域划分的问题集。

### 轮次结构

每轮：用 `AskUserQuestion` 提一个类别的问题。
每轮最多 5 个问题。尽可能给出具体选项——当带「Other」的多选题足以覆盖时，绝不问
开放式问题。

**必做轮次（按顺序）：**

**第 1 轮 — 参与者与用户**
询问：主要用户、次要用户、管理员角色、外部系统/API。
对每一类参与者：给出带描述的角色选项。等待回答。

**第 2 轮 — 核心功能**
给出根据领域 + 主题推导出的功能检查清单。
对每个功能簇：展示子选项（例如认证：邮箱/密码 | OAuth | SSO | 全部）。
把用户的选择标记为 [CONFIRMED]。推断可能未被提及的功能——请用户确认或否决。
等待回答。

**第 3 轮 — 范围边界**
给出两列表格：拟定的 IN scope 与拟定的 OUT scope。
请用户移动条目或新增条目。在范围上硬性拦截：没有明确的范围内/外边界，绝不继续。
等待回答。

**第 4 轮 — 技术约束**
询问：技术栈、托管方式、要集成的既有系统、安全/合规标准、
性能目标（给出数字示例）、时间线/预算信号。
等待回答。

**第 5 轮 — 业务规则与边界情况**
询问：数据所有权、角色/权限模型、定价/计费逻辑（如适用）、
监管要求、系统必须优雅处理的关键故障场景。
等待回答。

**第 5 轮之后：** 运行完整性检查：
- 还有参与者未定义？→ 在继续之前现在就问。
- 有功能范围不清？→ 现在就问。
- 缺少 NFR 基线？→ 现在就问。

**[GATE]** 只有在完整性检查通过、没有任何未决项时，才进入第 2 阶段。
说明：「头脑风暴完成。我现在有足够信息来写规格了。继续。」

---

## 第 2 阶段 — 规格撰写

按规格模板的结构撰写 `projects/{slug}/spec.md`。

**没有字数限制。** 每一节都要写全——不要概括，也不要截断。
- 每个参与者：完整描述、访问权限、经验水平
- 每个功能：用用户的原话 + AI 展开的细节
- 每条约束：原文 + 含义
- 范围内/外表格：详尽
- 业务规则：编号、精确
- NFR 目标：已确认的给数字，未确认的写 [TBD with context]

写完后，输出：
```
Spec written: projects/{slug}/spec.md
Sections: §1 ... §N
Word count: ~{N}
```

进入第 3 阶段。

---

## 第 3 阶段 — 选项门禁

用 `AskUserQuestion` 呈现下面的菜单：

```
Spec is ready. What would you like to do next?

A) Write plan          → break SRS into per-section plan files, then review
B) Re-read spec        → show full spec.md content for review/editing
C) Adjust brainstorm   → return to Phase 1 to add/change requirements
D) Jump to SRS         → skip planning, generate SRS directly (not recommended)
```

等待用户选择，并据此路由。
B → 展示 spec.md，然后回到第 3 阶段。
C → 回到覆盖该缺口的第 1 阶段对应轮次。
D → 跳到第 6 阶段。
A → 进入第 4 阶段。

---

## 第 4 阶段 — 计划撰写

加载 `skills/srs-workflow/references/plan-structure-guide.md`。

在 `projects/{slug}/plan/` 下为每个 SRS 章节创建一个计划文件：

```
plan/
  00-overview.md
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

**对每个文件：**
- 写出该 SRS 章节计划中的完整内容
- 包含：将写什么、每个子项、带「shall」占位子句的 FR 列表、NFR 目标
- 没有字数限制——计划文件是蓝图，必须没有歧义
- 给仍需用户输入的条目打标签：`[NEEDS USER INPUT: {what}]`

所有计划文件写完后，输出一张汇总表：
```
| File | Section | FRs planned | NFRs planned | Open items |
|------|---------|------------|--------------|------------|
```

进入第 5 阶段。

---

## 第 5 阶段 — 用户评审

呈现第 4 阶段的汇总表。然后用 `AskUserQuestion` 询问：

```
Plan is ready for review. What would you like to do?

A) Approve plan → proceed to SRS generation
B) Modify section → specify which section(s) to change
C) Add features → return to Phase 1 Round 2
D) Show full plan file → specify which file to display
```

如果用户修改：更新相关计划文件，然后回到本门禁。
**[GATE]** 只有在用户明确选择「批准计划」（选项 A）后，才进入第 6 阶段。

获批后说明：「计划已批准。开始生成 SRS。」

---

## 第 6 阶段 — SRS 生成

逐节生成 SRS，每一节在 `projects/{slug}/srs/` 下各成一个文件：

```
srs/
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

加载并遵循 `skills/srs-generator/references/srs-template.md` 中每节的格式。

**FR 格式（强制）：**
```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor / Precondition / Given / When / Then / Source
```

**NFR 格式：** ISO/IEC 25023 质量属性场景——只允许数字化的响应度量。

**没有字数限制。** 每个文件都必须完整。所有文件合起来，一份完整的 SRS 可能达到 300 页以上——这是正常且符合预期的。

另外生成 `projects/{slug}/srs/00-master-index.md`，链接所有章节文件并标注字数。

进入第 7 阶段。

---

## 第 7 阶段 — 自动校验

一次性对整个 SRS 目录运行校验器：

```bash
python scripts/srs_validator.py --dir projects/{slug}/srs/
```

输出完整的校验表。然后汇总：

```
## Validation Results
Overall: COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT
Errors:   N   (must fix before proceeding)
Warnings: N   (captured in Phase 8 report)
```

对每个 ERROR：立即修复受影响的 SRS 章节文件，然后重新运行校验器。
不要留下任何未解决的 ERROR。WARN 项不阻塞——在第 8 阶段记录下来。

进入第 8 阶段。

---

## 第 8 阶段 — 改进报告

撰写 `projects/{slug}/improvement-report.md`：

- **被推迟的功能**——标记为不在范围内、但被标为可能未来需要的条目
- **技术风险**——目标为 [TBD] 的 NFR、集成未知项、合规缺口
- **细化建议**——还能进一步拆分的 FR、需要真实负载测试数据的 NFR
- **下一版本候选**——用户提到但被明确推迟的功能
- **校验警告**——第 7 阶段中应在开发前解决的 WARN 项

没有字数限制。要具体——引用确切的 FR/NFR 编号、章节编号，以及头脑风暴中用户的原话。

进入第 9 阶段。

---

## 第 9 阶段 — 上下文保存

撰写 `projects/{slug}/_context/`：

```
_context/
  vision.md           ← project goals, problem statement, success metrics
  features.md         ← confirmed in/out scope feature list
  tech_stack.md       ← confirmed tech constraints
  glossary.md         ← all terms defined in Appendix A
  quality_standards.md← confirmed NFR numeric targets
  session-notes.md    ← key decisions made, open questions, next steps
```

然后输出最终摘要：
```
Workflow complete.

Project:    {name}
Location:   projects/{slug}/
SRS files:  {N} section files
FRs:        {total FR count}
NFRs:       {total NFR count}
Verdict:    {COMPLIANT | PARTIALLY COMPLIANT}
Open items: {count} (see appendix-b-open-issues.md)

Next step: share projects/{slug}/srs/ with your dev team.
```
