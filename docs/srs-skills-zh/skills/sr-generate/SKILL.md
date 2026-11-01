---
name: sr:generate
description: "SRS 工作流第 6 阶段。读取已批准的 plan 文件，生成一份完整的、符合 IEEE 830 的 SRS——每个章节一个文件，不限字数。完整的 SRS 在所有文件合计可能达到 300+ 页。"
user-invocable: true
metadata:
  input:  projects/{slug}/plan/*.md (approved by user via /sr:plan)
  output: projects/{slug}/srs/*.md (11 section files + master index)
  next:   /sr:validate
  references:
    - skills/srs-generator/references/srs-template.md
---

# sr:generate

目标：产出一份完整、可直接发布的 IEEE 830 SRS。
不限字数。每个章节文件都必须写全——不要占位符、不要摘要、不要「详见 plan」。

---

## 第 0 步 — 识别项目与门禁

```
AskUserQuestion: "Which project to generate SRS for? (slug)"
```

读取 `projects/{slug}/plan/` 下的所有文件。
如果 plan 文件不存在或不完整：告诉用户先运行 `/sr:plan`。

在写任何内容之前，先运行就绪门禁：
```bash
python scripts/plan_validator.py --dir projects/{slug}/plan/
```

- **BLOCKED**（发现 ERROR，例如缺文件、FR 编号断档、缺少 shall 子句、优先级标签错误）：就此停下。列出这些 ERROR，并告诉用户先通过 `/sr:plan` 修好，再重试 `/sr:generate`。
- **READY WITH WARNINGS**（例如未解决的 `[NEEDS USER INPUT]` 还没有记入 appendix-b-open-issues.md）：展示这些警告，请用户确认是否仍然继续，或者回到 `/sr:plan` 把它们解决掉。
- **READY**：进入第 1 步。

加载 `skills/srs-generator/references/srs-template.md`。

---

## 第 1 步 — 生成章节文件

在 `projects/{slug}/srs/` 下创建文件。每写完一个文件再写下一个。每个章节都遵循 `srs-template.md` 的格式。

**文件顺序：**

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

---

## FR 格式（03-02 中每个 FR 都必须照此）

```markdown
#### FR-NN [Essential|Conditional|Optional]

**Requirement:** The system shall {precise verb} {object} when {condition}.

| Field | Value |
|-------|-------|
| Actor | {who triggers this} |
| Precondition | {system state before} |
| Trigger | {what causes it} |
| Source | {brainstorm round / business rule / regulatory} |

**Acceptance Criteria (GWT):**
- **Given** {system state}
- **When** {actor action or event}
- **Then** {expected system response — measurable}
- **And** {additional assertions if needed}
```

规则：
- FR-ID 在整个文件内连续编号——不得重置
- 每个 FR 都必须有：shall 子句 + 全部表格字段 + 完整的 GWT
- Requirement 行里不要出现 TBD——如果某项需求还不清楚，它就不该出现在 SRS 里（改为在 appendix-b-open-issues.md 里列出）

---

## NFR 格式（03-03 和 03-06 中每个 NFR 都必须照此）

ISO/IEC 25023 质量属性场景格式：

```markdown
#### NFR-NN — {ISO 25010 Characteristic}: {Sub-characteristic}

| Field | Value |
|-------|-------|
| Source of Stimulus | {who/what triggers the scenario} |
| Stimulus | {the event} |
| Environment | {system state at time of event} |
| Artifact | {which part of the system} |
| Response | {what the system does} |
| Response Measure | {numeric threshold — e.g., ≤ 500ms at 95th percentile} |
```

**规则：** 响应度量必须是数值。不要形容词（fast、good、acceptable）。
如果确实未知：`[TBD: {what data is needed} | owner: {role} | resolve-by: {milestone}]`

---

## 第 2 步 — 生成主索引

写入 `projects/{slug}/srs/00-master-index.md`：

```markdown
# SRS Master Index — {Project Name}
Version: 1.0   Date: {date}   Status: DRAFT

## Document Map
| File | Section | Description | Word count (est.) |
|------|---------|-------------|-----------------|
...

## FR Summary
Total FRs: {n}
- Essential: {n}
- Conditional: {n}
- Optional: {n}

## NFR Summary
Total NFRs: {n} ({n} confirmed / {n} [TBD])

## Open Items
{count} items in appendix-b-open-issues.md requiring resolution before FINAL status.
```

---

## 第 3 步 — 交接

运行 `python scripts/srs_validator.py --dir projects/{slug}/srs/ --stats`，并使用下面给出的计数（不要手工重数一份 300+ 页的文档）。

输出：
```
SRS generation complete.

Location: projects/{slug}/srs/
Files: 11 section files + 00-master-index.md
FRs:  {total} ({Essential}/{Conditional}/{Optional})
NFRs: {total} ({confirmed} confirmed / {TBD} [TBD])

Next: /sr:validate → validates SRS against IEEE 830-1998
```
