---
name: sr:brainstorm
description: "SRS 工作流第 1 阶段。用户给出一个项目主题 → AI 执行一次深入、分类的头脑风暴（5 个强制轮次），在写任何内容之前完整理解参与者、功能、范围边界、技术约束与业务规则。"
user-invocable: true
metadata:
  input:  A project topic (1 sentence to 1 paragraph)
  output: Collected brainstorm answers saved to projects/{slug}/brainstorm.md
  next:   /sr:spec
  references:
    - skills/srs-workflow/references/brainstorm-guide.md
---

# sr:brainstorm

目标：在写下规格的第一个字之前，完整理解这个项目。
不要在本会话中写 spec、plan 或 SRS。

---

## 第 0 步 — 主题接收

从用户那里接收主题。先不要提问。

识别：
- 领域（e-commerce | healthcare | fintech | SaaS | internal tool | mobile | other）
- 规模信号（MVP | startup | enterprise | unknown）
- 已经提到的任何约束

回显：
```
Topic:   {topic}
Domain:  {domain}
Scale:   {scale}
Slug:    {kebab-case name for projects/{slug}/}
```

在继续之前，与用户确认 slug。如果主题太模糊、无法形成 slug，就提问。

---

## 第 1 步 — 加载领域问题

加载 `skills/srs-workflow/references/brainstorm-guide.md`。
选择与识别出的领域相匹配的问题库。

---

## 第 2 步 — 第 1 轮：参与者与用户

使用 `AskUserQuestion` 给出具体的角色选项（不要开放式提问）。

询问：
- 主要最终用户（用该领域的例子）
- 次要用户 / 支持角色
- 管理员 / 后台角色
- 外部系统 / 第三方集成

等待回答。把每个确认的参与者记录为：
```
[ACTOR] {name}: {description} | access level: {read/write/admin}
```

---

## 第 3 步 — 第 2 轮：核心功能

使用 `AskUserQuestion`。给出一个由领域 + 主题推导出的功能检查清单。

对每个功能簇给出子选项。以电商为例：
- 身份认证：(A) 邮箱 + 密码 (B) OAuth (C) 两者都要 (D) 企业 SSO
- 商品目录：(A) 简单商品 (B) 可配置 SKU (C) 组合包 (D) 订阅

把每个选择标记为 [CONFIRMED]。推断可能遗漏的功能——请用户确认或否决。

等待回答。

---

## 第 4 步 — 第 3 轮：范围边界

使用 `AskUserQuestion`。呈现一个两列表格：

| IN 范围（提议） | OUT 范围（提议） |
|---------------------|----------------------|
| {feature A}         | {feature X}          |

请用户在列之间移动条目，或添加新条目。

**硬性阻塞（HARD BLOCK）：** 在用户明确确认 IN/OUT 边界之前，不要继续。

等待回答。

---

## 第 5 步 — 第 4 轮：技术约束

使用 `AskUserQuestion`。询问：
- 技术栈（给出该领域的常见选项）
- 托管方式（云厂商 / 本地部署 / 混合）
- 需要集成的现有系统（带是/否选项）
- 安全与合规（GDPR | HIPAA | PCI-DSS | SOC2 | none）
- 性能目标（给出数值示例：< 200ms | < 500ms | < 1s）
- 时间线 / 预算信号

等待回答。

---

## 第 6 步 — 第 5 轮：业务规则与边界情况

使用 `AskUserQuestion`。询问：
- 角色与权限模型（RBAC | ABAC | 简单的所有者/成员 | 自定义）
- 数据所有权与保留规则
- 系统必须优雅处理的关键故障场景
- 定价 / 计费逻辑（如适用）
- 已记录内容之外的监管要求

等待回答。

---

## 第 7 步 — 完整性检查

第 5 轮之后，对照这份清单自检。任何缺口 = 现在就补一个追问：

- [ ] 每个参与者都有名称 + 描述 + 访问级别
- [ ] IN 范围内的每个功能都已确认（不只是推断）
- [ ] OUT 范围清单是明确的（至少 3 项）
- [ ] 性能 / 可用性 / 安全 三项各至少有一个数值型 NFR 目标
- [ ] 每个功能簇至少有一条业务规则
- [ ] 合规要求已说明（即便为「none」）
- [ ] 集成点已列出（即便为「none」）

只要有任何一个框没勾：先补一轮有针对性的追问，再继续。

---

## 第 8 步 — 保存头脑风暴输出

写入 `projects/{slug}/brainstorm.md`：

```markdown
# Brainstorm: {project name}
Date: {date}

## Topic
{user's original topic verbatim}

## Domain / Scale
{domain} / {scale}

## Actors
{list with [ACTOR] entries}

## Confirmed Features (IN Scope)
{confirmed list}

## OUT of Scope
{explicit list}

## Technical Constraints
{answers from Round 4}

## Business Rules
{answers from Round 5}

## NFR Baselines
{confirmed numeric targets, or [TBD] with context}

## Open Items
{anything still unresolved — will become [TBD] tags in spec}
```

---

## 第 9 步 — 交接

输出：
```
Brainstorm complete.

Project: {name}   Slug: {slug}
Actors:  {count}
Features confirmed (IN scope): {count}
OUT scope items: {count}
Open items: {count}

Saved: projects/{slug}/brainstorm.md

Next: /sr:spec → writes the full spec from this brainstorm
```
