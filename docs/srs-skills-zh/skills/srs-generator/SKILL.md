---
name: cl:srs
description: "从原始需求生成 IEEE 830 SRS。当用户说「写 SRS」「生成需求文档」「分析需求」「我这里有客户给的原始需求」，或者粘贴客户邮件/聊天记录/PRD 时使用。"
user-invocable: true
metadata:
  use_when: 用户提供客户的原始需求（邮件、聊天、要点列表、不完整的 PRD），需要整理成 IEEE 830 SRS
  do_not_use_when: 需求已是完整的 SRS 格式；或有更专门的技能负责该任务
  quality_standards: 所有 FR 使用「shall」子句；所有 NFR 使用数字阈值；不得虚构用户未提供的内容
  anti_patterns: >
    不要把输入中不存在的需求凭空造出来——标记为 [CONTEXT-GAP: {desc}]。
    不要在 FR/NFR 中使用模糊形容词（快、简单、很多）——标记为 [VERIFIABILITY-FAIL: {FR-NN}]。
    不要跳过澄清轮次。没有用户明确确认，不要保存文件。
  outputs: IEEE 830 SRS，位于 docs/srs-{slug}-{YYYYMMDD}.md + 合规判定
  references: skills/srs-generator/references/srs-template.md, skills/srs-generator/references/gap-detection-guide.md
---

# cl:srs — 从原始需求生成 IEEE 830 SRS

流水线：**头脑风暴** → 接收 → 提取 → 缺口扫描 → 澄清（P1 → P2 → P3）→ 生成 → 评审门禁 → 保存

参考文件（开始前加载）：
- `skills/srs-generator/references/srs-template.md`
- `skills/srs-generator/references/gap-detection-guide.md`

**上下文文件（存在时加载——由 `scripts/init_project.py` 创建）：**
- `projects/{name}/_context/vision.md` → 预填 §1.2 范围与 §2.1
- `projects/{name}/_context/features.md` → 预填 §2.2 与 IN/OUT 表
- `projects/{name}/_context/tech_stack.md` → 预填 §3.5 设计约束
- `projects/{name}/_context/glossary.md` → 预填附录 A
- `projects/{name}/_context/quality_standards.md` → 预填 §3.3–§3.6 NFR

如果上下文文件存在：跳过其中已给出答案的头脑风暴门禁问题。

---

### 头脑风暴门禁 — 先理解上下文

先不要索取原始需求。先理解项目上下文。

用一个 `AskUserQuestion` 批次提出这 3 个问题：

1. **系统类型：** Web 应用 / 移动应用 / API / 内部工具 / SaaS / 桌面端 / 其他？
2. **主要用户：** 谁会使用这个系统？（终端客户、内部员工、管理员、B2B 客户等）
3. **核心问题：** 这个系统解决什么问题？（1–2 句）

等待回答。用回答来预填 §2.1 产品视角、§2.3 用户特征和 §1.2 范围。

收到回答后，提示：
```
Context noted. Now paste your raw requirements — any format works:
client email, bullet list, chat transcript, PRD draft.
```

等待原始输入，然后进入第 0 步。

---

### 第 0 步 — 接收输入

静默通读全部输入。输出：
```
Input received: ~{N} words | type: [email prose | bullet list | partial PRD | mixed]
```

---

### 第 1 步 — 提取与分类

输出结构化区块：
- **参与者**——明确提及和隐含的利益相关方。未定义的打标签：`[GLOSSARY-GAP: {actor}]`
- **功能**——FR-01、FR-02……采用「主体可以做 X」的形式。记录表述策略：散文 / 列表 / PRD
- **约束**——只记录原文片段（技术栈、期限、合规、预算）
- **范围外信号**——明确排除的内容。如果没有：`[CONTEXT-GAP: no out-of-scope boundary stated]`

为每个条目追加 `[Source: {location}]`。

---

### 第 2 步 — 缺口扫描

加载 `skills/srs-generator/references/gap-detection-guide.md`。运行全部 7 种模式。输出：

| # | Priority | Pattern | Verbatim fragment / missing element |
|---|----------|---------|-------------------------------------|

零缺口 → 明确说明，跳到 **SRS 生成**。

---

### 第 3 步 — 第 1 轮澄清（P1——阻塞项）

如果存在 P1 缺口，发出带 ≤7 个问题的 `AskUserQuestion`。标签：
```
Round 1 of 3 — Scope & Actors (P1 — must resolve before writing SRS)
```

收到后：整合答案，标记已解决的缺口。未回答的 P1 → `[CONTEXT-GAP: {desc}]` → 附录 B。
只有在参与者和范围都仍然为零时才阻塞。然后进入第 2 轮。

---

### 第 4 步 — 第 2 轮澄清（P2——功能细节）

如果仍有 P2 缺口，发出带 ≤7 个问题的 `AskUserQuestion`。标签：
```
Round 2 of 3 — Functional Details (P2)
```

未回答 → 在 SRS 与附录 B 中记录所假设的默认值。然后进入第 3 轮。

---

### 第 5 步 — 第 3 轮澄清（P3——可选）

发出带 ≤7 个问题的 `AskUserQuestion`。标签：
```
Round 3 of 3 — Non-Functional & Secondary Details (P3 — optional)
Reply 'skip' to use [TBD] placeholders.
```

收到「skip」时：把所有 P3 缺口标记为 `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`。
进入 **SRS 生成**。

---

### SRS 生成

用收集到的全部信息填充 `skills/srs-generator/references/srs-template.md`。

**§1.2 范围**——每个功能领域都必须有 IN / OUT 表。

**§3.2 功能需求**——每个 FR 区块：
```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor:        {role}
Precondition: {state}
Given:        {context}
When:         {trigger — exactly one}
Then:         {externally observable outcome}
Source:       [{location}]
```
不可观察的「Then」→ `[VERIFIABILITY-FAIL: FR-NN]` → 附录 B

**§3.3–§3.6 NFR**——质量属性场景（ISO/IEC 25023）：
```
NFR-NN [{ISO/IEC 25010 characteristic}]
Source / Stimulus / Environment / Artifact / Response / Response Measure: {numeric}
```

填充完成后，运行 `gap-detection-guide.md` 中的 IEEE 830 质量检查清单。输出判定：
- `COMPLIANT`——所有章节齐全，附录 B 为空
- `PARTIALLY COMPLIANT`——章节齐全，但附录 B 有未决项
- `NON-COMPLIANT`——缺少必需章节

---

### 人工评审门禁

```
Review complete. SRS is {verdict}.
Open issues: {count} (see Appendix B).
Proceed to save? [Y / n]
```

在写入任何文件之前，等待明确确认。

---

### 保存与报告

1. 从 §1.2 的产品名称推导 slug（小写、连字符）。无法推导时：询问用户。
2. 路径：`docs/srs-{slug}-{YYYYMMDD}.md`
3. 回显绝对路径，等待确认。
4. 如 `docs/` 不存在则创建，写入文件，确认：`"Saved ✓ {absolute_path}"`
