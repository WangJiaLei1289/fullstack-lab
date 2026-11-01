---
name: sr:improve
description: "SRS 工作流第 8 阶段。生成一份改进报告，覆盖延后实现的功能、技术风险、校验警告，以及下一版本候选。不限字数。"
user-invocable: true
metadata:
  input:  projects/{slug}/srs/ + projects/{slug}/plan/ + validation output
  output: projects/{slug}/improvement-report.md
  next:   /sr:save
---

# sr:improve

目标：产出一份坦诚的改进报告——哪些被延后、哪些带风险、哪些应该在开发开始前解决。引用具体的 FR/NFR ID。

---

## 第 0 步 — 识别项目

```
AskUserQuestion: "Which project? (slug)"
```

从 `projects/{slug}/` 读取：
- `spec.md`（用于延后实现的功能和待解决项）
- `srs/appendix-b-open-issues.md`（用于全部 [TBD] 项）
- `srs/03-03-performance.md`（用于 [TBD] 的 NFR）
- 校验器输出（如果有）（来自 `/sr:validate` 的 WARN）

---

## 第 1 步 — 写 improvement-report.md

写入 `projects/{slug}/improvement-report.md`。不限字数。

### §1 — 延后实现的功能（下一版本候选）

列出 spec.md 中每个被标记为 OUT 范围、用户提到过但被延后的功能。
对每一项：
- 功能名称
- 为何延后（用户给出的原因，若头脑风暴中说过）
- 预估工作量等级（low | medium | high）——仅 AI 估计，不是承诺
- 建议版本：v1.1 | v2.0 | unknown

### §2 — 技术风险

对 NFR 中每个未解决的 [TBD]：
- NFR-ID + 描述
- 需要什么数据才能定出目标
- 若不解决的风险：(A) 无法写测试 (B) 无法对 SLA 作出承诺 (C) 架构决策被阻塞
- 建议负责人 + 解决里程碑

对 §3.1 中的每个外部集成：
- 集成名称 + 系统
- 风险：依赖第三方可用性 / API 版本管理 / 速率限制
- 缓解建议

### §3 — FR 细化建议

找出符合以下情况的 FR：
- 过于宽泛（把多个本应独立成 FR 的行为合在一起）
- 缺少反面情形（它失败时会发生什么？）
- 缺少参与者变体（同一动作、不同权限级别）

逐条列出，并给出建议的拆分或补充。

### §4 — NFR 缺口

响应度量为 [TBD] 的 NFR → 列出：哪种基准测试能产出真实数字。
响应度量只有形容词的 NFR（本应被校验器抓到）→ 给出改写建议。

### §5 — 校验警告

逐条枚举来自 `/sr:validate` 的每个 WARN，并写明：
- 警告文本
- 它指向哪个文件/FR/NFR
- 建议的解决方式（具体动作，而不是「复查一下」）
- 紧迫度：开发前必须解决 | QA 前应该解决 | 可以延后

### §6 — 流程建议

关于需求流程本身的观察：
- 用户输入含糊的那几轮 → 记下需要后续工作坊的主题领域
- 失效风险很高的假设 → 标出来，请利益相关方签字确认
- 缺少领域专家输入（例如「没有安全架构师评审过 NFR-02」）

---

## 第 2 步 — 交接

输出：
```
Improvement report: projects/{slug}/improvement-report.md

Deferred features:      {count}
Technical risks:        {count}
FR refinement items:    {count}
NFR gaps:               {count}
Validation warnings:    {count}
Process recommendations:{count}

Next: /sr:save → saves project context files for future sessions
```
