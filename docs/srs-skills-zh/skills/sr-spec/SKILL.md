---
name: sr:spec
description: "SRS 工作流第 2 阶段。读取 projects/{slug}/brainstorm.md，写出一份全面的 spec.md。不限字数。"
user-invocable: true
metadata:
  input:  projects/{slug}/brainstorm.md (from /sr:brainstorm)
  output: projects/{slug}/spec.md
  next:   /sr:plan
---

# sr:spec

目标：把头脑风暴的输出变成一份结构化、全面的 spec。
不限字数——每一节都必须写全。

---

## 第 0 步 — 识别项目

询问用户项目 slug（或从上下文推断）：

```
AskUserQuestion: "Which project to write spec for? (slug name or path to brainstorm.md)"
```

读取 `projects/{slug}/brainstorm.md`。如果不存在，告诉用户先运行 `/sr:brainstorm`。

---

## 第 1 步 — 写 spec.md

写入 `projects/{slug}/spec.md`。不限字数。每个小节都写全。

### §1 — 项目概览
- 系统名称（在头脑风暴中确认）
- 问题陈述（这解决了什么问题？）
- 方案摘要（系统做什么、给谁做、怎么做）
- 主要成功指标（我们怎么知道它在起作用？）

### §2 — 参与者
每个确认的参与者一个完整条目：
- 名称与角色
- 技术熟练度（non-technical | basic | intermediate | expert）
- 领域知识水平
- 使用频率与渠道（web | mobile | API | all）
- 无障碍需求（如有）
- 数据访问范围（read | write | admin）

### §3 — 功能（IN 范围）
对每个确认的功能：
- 功能名称 + 功能簇
- 用用户自己的话描述（逐字取自头脑风暴）
- AI 展开的细节（这暗示了哪些子能力？）
- 使用它的参与者
- 优先级层级：Essential | Conditional | Optional

### §4 — OUT 范围
表格：功能 | 排除原因 | 计划在哪个版本
头脑风暴 OUT 范围清单中的每一项。

### §5 — 技术约束
- 技术栈：语言、框架、运行时
- 托管 / 部署模式
- 需要集成的现有系统（名称、协议、方向）
- 安全标准（认证模型、加密要求）
- 合规：适用法规 + 具体义务

### §6 — 业务规则
编号列表。每条规则：精确、可测试的陈述。
示例：「BR-01：若用户账户余额低于订单总额，用户不能下单。」
覆盖头脑风暴第 5 轮浮现的每一条规则。

### §7 — NFR 基线
表格格式：

| ID | 特性 | 目标 | 状态 |
|----|---------------|--------|--------|
| NFR-01 | 响应时间 | < 500ms at p95 | 已确认 |
| NFR-02 | 可用性 | 99.9% uptime | 已确认 |
| NFR-03 | 数据保留 | 7 年 | [TBD: legal to confirm \| owner: PM \| resolve-by: Sprint 1] |

### §8 — 假设
编号列表。每条假设：假设了什么 + 如果假设不成立会发生什么。

### §9 — 待解决项
头脑风暴「待解决项」一节中的每一个 [TBD]，附：
- 未知的是什么
- 需要谁来回答
- 若不解决的后果

---

## 第 2 步 — 完成前确认

写完之后，做一次自检：
- 每个确认的参与者是否至少出现在一个功能条目里？
- 每个确认的功能是否都有优先级层级？
- brainstorm.md 里的每个 [TBD] 是否都出现在 §9 中？
- 每条业务规则是否都有编号且可测试？

输出交接消息之前，修好任何缺口。

---

## 第 3 步 — 交接

输出：
```
Spec written: projects/{slug}/spec.md

Actors:         {count}
Features (IN):  {count}
OUT scope:      {count}
Business rules: {count}
NFR baselines:  {count confirmed} confirmed, {count TBD} [TBD]
Open items:     {count}

Next: /sr:plan → breaks this spec into per-section SRS plan files
```
