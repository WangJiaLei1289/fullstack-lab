---
name: sr:validate
description: "SRS 工作流第 7 阶段。对已生成的 SRS 文件运行 srs_validator.py --dir，报告错误与警告，自动修复 ERROR，并输出 COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT 判定。"
user-invocable: true
metadata:
  input:  projects/{slug}/srs/ directory (from /sr:generate)
  output: validation verdict + fixes applied inline
  next:   /sr:improve
---

# sr:validate

目标：对照 IEEE 830-1998 校验已生成的 SRS。
报告之前先修掉所有 ERROR。WARN 会被记录进改进报告。

---

## 第 0 步 — 识别项目

```
AskUserQuestion: "Which project to validate? (slug)"
```

检查 `projects/{slug}/srs/` 是否存在并包含 .md 文件。
如果缺失：告诉用户先运行 `/sr:generate`。

---

## 第 1 步 — 运行校验器

执行：
```bash
python scripts/srs_validator.py --dir projects/{slug}/srs/
```

捕获 stdout。展示完整的校验表。

---

## 第 2 步 — 立即修复 ERROR

对每一条 ERROR 发现项：
1. 找出受影响的 SRS 章节文件
2. 按 IEEE 830 规则修复问题：
   - `missing-section`：以正确的标题格式补上该章节
   - `fr-no-shall`：用显式的 shall 子句重写 Requirement 行
   - `fr-numbering-gap`：给 FR 重新编号以填补断档（同步更新所有引用）
3. 说明修了什么：`FIXED [ERROR] fr-no-shall in FR-07 → added "shall" clause`

修完所有 ERROR 后：重新运行校验器，确认没有新的 ERROR。

---

## 第 3 步 — 收集 WARN

列出全部 WARN 发现项，但不要在这里修——它们会进入改进报告。

格式：
```
WARN: unresolved-tag — 3 [TBD] tags remain (NFR-03, NFR-07, §1.3)
WARN: fr-incomplete-gwt — FR-12: missing "Then:" field
WARN: nfr-no-numeric — NFR-05 Response Measure has no numeric threshold
```

---

## 第 4 步 — 判定

输出：
```
## Validation Result

Verdict: COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT
File:    projects/{slug}/srs/ ({N} files)

ERRORs fixed:  {count}
WARNings open: {count} → captured in /sr:improve report

Next: /sr:improve → improvement report + warning resolution guide
```
