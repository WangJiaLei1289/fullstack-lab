---
name: sr:save
description: "SRS 工作流第 9 阶段。把全部项目上下文保存到 _context/ 文件，让后续的 Claude 会话无需重读整份 SRS 就能接着工作。"
user-invocable: true
metadata:
  input:  All projects/{slug}/ files
  output: projects/{slug}/_context/*.md (6 context files)
---

# sr:save

目标：把整个项目提炼成紧凑、可重新加载的上下文文件。
未来的会话应当只加载 `_context/` 就能完整理解项目。

---

## 第 0 步 — 识别项目

```
AskUserQuestion: "Which project to save context for? (slug)"
```

读取 `projects/{slug}/` 下所有可用文件。
运行 `python scripts/srs_validator.py --dir projects/{slug}/srs/ --stats`，并用它的计数填写下面的 quality_standards.md / session-notes.md，而不是手工重数。

---

## 第 1 步 — 写上下文文件

在 `projects/{slug}/_context/` 下写入全部文件：

### vision.md

```markdown
# Vision — {Project Name}

## Problem Statement
{what problem does this system solve? 2–3 sentences from spec §1}

## Solution Summary
{what the system does, for whom, and the core value proposition}

## Success Metrics
{how we measure success — from spec §1 or brainstorm}

## Constraints
{top 3 hard constraints — tech, timeline, compliance}
```

### features.md

```markdown
# Features — {Project Name}

## IN Scope (v1.0)
| Feature | Priority | Key FRs | Notes |
|---------|----------|---------|-------|
{every confirmed in-scope feature, one row each}

## OUT of Scope (v1.0 — Deferred)
| Feature | Reason | Target version |
|---------|--------|---------------|
{every explicitly excluded feature}
```

### tech_stack.md

```markdown
# Tech Stack — {Project Name}

## Confirmed Stack
| Layer | Technology | Constraint type |
|-------|-----------|----------------|
{language, framework, DB, cloud, CI/CD — from spec §5}

## Integration Points
| System | Protocol | Direction | Auth |
|--------|----------|-----------|------|
{every external system — from SRS §3.1.3}

## Compliance Requirements
{applicable regulations + specific technical obligations}
```

### glossary.md

```markdown
# Glossary — {Project Name}

Copy of Appendix A from the SRS. Every term, acronym, abbreviation.
Include: domain terms | project-specific terms | role names | system names
```

### quality_standards.md

```markdown
# Quality Standards — {Project Name}

## Confirmed NFR Targets
| ID | Characteristic | Target | Status |
|----|---------------|--------|--------|
{all NFRs from SRS §3.3 — confirmed targets and [TBD] items}

## Validation Status
Validator verdict: {COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT}
Open warnings: {count}
```

### session-notes.md

```markdown
# Session Notes — {Project Name}

## Key Decisions Made
{numbered list — every explicit scope, tech, or design decision from brainstorm}

## Assumptions
{numbered list — from spec §8, with invalidation risk level}

## Open Items
{all [TBD] items — copied from appendix-b-open-issues.md}

## Next Steps
1. Resolve open items in appendix-b (see quality_standards.md for owners)
2. Dev team walkthrough of SRS §3.2 (functional requirements)
3. QA team review of GWT acceptance criteria
4. Architecture review of NFR targets before sprint planning

## SRS Location
projects/{slug}/srs/ — {N} section files
Master index: projects/{slug}/srs/00-master-index.md
```

---

## 第 2 步 — 最终汇总

输出完整的工作流完成汇总：

```
╔══════════════════════════════════════════════════╗
║           SRS Workflow Complete                  ║
╠══════════════════════════════════════════════════╣
║ Project:     {name}                              ║
║ Slug:        {slug}                              ║
║ Location:    projects/{slug}/                    ║
╠══════════════════════════════════════════════════╣
║ Brainstorm:  projects/{slug}/brainstorm.md       ║
║ Spec:        projects/{slug}/spec.md             ║
║ Plan:        projects/{slug}/plan/ (12 files)    ║
║ SRS:         projects/{slug}/srs/  (11 files)    ║
║ Improvement: projects/{slug}/improvement-report.md ║
║ Context:     projects/{slug}/_context/ (6 files) ║
╠══════════════════════════════════════════════════╣
║ FRs:         {total} ({E} Essential / {C} Cond / {O} Opt) ║
║ NFRs:        {total} ({confirmed} confirmed / {TBD} TBD)  ║
║ Verdict:     {COMPLIANT | PARTIALLY COMPLIANT}   ║
║ Open items:  {count}                             ║
╚══════════════════════════════════════════════════╝

Share with your team:
  SRS  → projects/{slug}/srs/00-master-index.md
  Risks→ projects/{slug}/improvement-report.md
```
