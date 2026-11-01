---
name: sr:plan
description: "SRS 工作流第 4 阶段。读取 spec.md，为每个 SRS 章节（§1–§3 + 附录）写一个详细的 plan 文件。每个文件都是对应 SRS 章节的完整蓝图。不限字数。"
user-invocable: true
metadata:
  input:  projects/{slug}/spec.md (from /sr:spec)
  output: projects/{slug}/plan/*.md (12 files)
  next:   /sr:generate  (after user review and approval)
  references:
    - skills/srs-workflow/references/plan-structure-guide.md
---

# sr:plan

目标：产出 12 个 plan 文件——每个 SRS 章节一个——作为生成 SRS 时无歧义的蓝图。不要摘要，不要截断。

---

## 第 0 步 — 识别项目

```
AskUserQuestion: "Which project to plan? (slug)"
```

读取 `projects/{slug}/spec.md`。如果不存在，告诉用户先运行 `/sr:spec`。
加载 `skills/srs-workflow/references/plan-structure-guide.md`。

---

## 第 1 步 — 写 plan 文件

在 `projects/{slug}/plan/` 下创建全部文件。每个文件都要遵循 `plan-structure-guide.md` 中关于必须包含哪些内容的详细规格。

按这个顺序写（写完一个再写下一个）：

1. `00-overview.md`         — 总览地图、FR/NFR 计数总计、参与者表、假设
2. `01-introduction.md`     — §1.1 目的、§1.2 范围（IN/OUT 表）、§1.3 定义、§1.4 参考、§1.5 概览
3. `02-overall-description.md` — §2.1 视角、§2.2 功能、§2.3 用户特征、§2.4 约束、§2.5 假设、§2.6 分配
4. `03-01-external-interfaces.md` — UI 界面、硬件、软件 API、通信协议
5. `03-02-functional-requirements.md` — 全部 FR，含 shall 存根 + GWT 存根 + 优先级
6. `03-03-performance.md`   — 全部 NFR，含数值型响应度量或 [TBD]
7. `03-04-database.md`      — 实体、保留策略、数据量、PII 字段
8. `03-05-design-constraints.md` — 强加的技术栈、合规驱动的约束
9. `03-06-system-attributes.md` — 可靠性、可用性、安全、可维护性、可移植性、易用性
10. `03-07-other-requirements.md` — i18n、法务、运营、迁移过渡、培训
11. `appendix-a-glossary.md`    — 所有需要精确定义的领域术语
12. `appendix-b-open-issues.md` — 所有 plan 文件中的 [NEEDS USER INPUT]，含负责人 + 解决期限

**FR 编号规则（在所有 plan 文件中强制执行）：**
- 连续编号：FR-01、FR-02、FR-03……章节之间不得重置
- 格式：`FR-NN [Essential|Conditional|Optional]`
- 每个 FR 都必须有：Requirement（shall 子句）+ Given/When/Then 存根
- 给不清楚的条目打标签：`[NEEDS USER INPUT: {specific question}]`

---

## 第 2 步 — 汇总表

12 个文件都写完后，运行：
```bash
python scripts/plan_validator.py --dir projects/{slug}/plan/ --stats
```

使用它的计数（不要手工重算——大型 plan 手工数会漂移）。

输出：
```
| File | Section | FRs | NFRs | Open items |
|------|---------|-----|------|-----------|
| 00-overview.md | Master map | — | — | {n} |
| 03-02-functional-requirements.md | §3.2 FR | {n} | — | {n} |
...

Total: {FR count} FRs ({Essential}/{Conditional}/{Optional})
       {NFR count} NFRs ({confirmed} confirmed / {TBD} [TBD])
       {open} open items → see appendix-b-open-issues.md
```

---

## 第 3 步 — 用户评审门禁

```
AskUserQuestion:
"Plan is ready. What would you like to do?
 A) Approve → proceed to /sr:generate
 B) Modify a section → which file(s)?
 C) Show a plan file → which one?
 D) Add features → run /sr:brainstorm again to extend"
```

若选 B：更新相关文件，然后回到第 3 步。
若选 C：展示该文件内容，然后回到第 3 步。
若选 D：让用户运行 `/sr:brainstorm` 并更新 spec，然后从第 0 步重新开始。
若选 A：继续。

---

## 第 4 步 — 交接

plan 获批后输出：
```
Plan approved.

Files: projects/{slug}/plan/ (12 files)
FRs planned: {total} ({Essential} Essential / {Conditional} Conditional / {Optional} Optional)
NFRs planned: {total}
Open items: {count}

Next: /sr:generate → generates full SRS from this plan (no word limit)
```
