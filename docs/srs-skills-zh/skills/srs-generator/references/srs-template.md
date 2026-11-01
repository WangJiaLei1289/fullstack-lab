# 软件需求规格说明书
*符合 IEEE 830-1998*

| 字段 | 值 |
|-------|-------|
| 项目 | {project name} |
| 版本 | v0.1 —— 草稿 |
| 日期 | {YYYY-MM-DD} |
| 编写人 | {author / role} |
| 状态 | 草稿 |

> **记号约定：** "shall" 表示强制义务。"should" 表示期望但可选。
> 质量属性遵循 ISO/IEC 25010。NFR 度量遵循 ISO/IEC 25023 质量属性场景。

---

## 1. 引言

### 1.1 目的
{本文档面向谁（开发团队、QA、利益相关方），以及它规定的是哪个系统。1–2 句。}

### 1.2 范围

**系统名称：** {name}

{一段话描述产品做什么及其主要目标。}

**范围内 / 范围外：**

| 功能领域 | 范围内 | 范围外 |
|--------------|----------|--------------|
| {area 1} | ✓ | |
| {area 2} | | ✓ |

> 如果无法从输入填充该表，使用 `[CONTEXT-GAP: out-of-scope boundary not defined]`。
> §3.2 中的每个功能领域都必须出现在这张表里。

### 1.3 定义、缩略语与缩写
完整术语表见附录 A。本文档使用的标准缩写：

| 缩写 | 定义 |
|-------------|------------|
| SRS | 软件需求规格说明书（Software Requirements Specification） |
| FR | 功能需求（Functional Requirement） |
| NFR | 非功能需求（Non-Functional Requirement） |
| GWT | Given / When / Then |
| TBD | 待定（To Be Determined） |

### 1.4 引用
| # | 文档 | 类型 | 日期 |
|---|----------|------|------|
| 1 | {原始输入文档的标题或描述} | 源输入 | {date} |
| 2 | IEEE 830-1998 | 标准 | 1998 |
| 3 | ISO/IEC 25010:2011 | 质量模型 | 2011 |
| 4 | ISO/IEC 25023:2016 | 质量度量 | 2016 |

### 1.5 概览
第 2 节描述产品总体上下文、用户特征与约束。第 3 节给出可追溯到源输入的具体功能与非功能需求。附录 A 是术语表；附录 B 列出开发批准前必须解决的未决问题。

---

## 2. 总体描述

### 2.1 产品视角
{系统如何嵌入更大的上下文：独立产品、套件的一部分、替换既有系统，或是新能力。如适用，附上上下文图或外部系统清单。}

外部系统 / 接口：
- {External system 1} — {relationship}
- {External system 2} — {relationship}

### 2.2 产品功能
主要能力的高层摘要（细节见 §3.2）：

- {Capability 1}
- {Capability 2}
- {Capability 3}

### 2.3 用户特征

| 参与者 | 技术水平 | 访问权限 | 备注 |
|-------|----------------|---------------|-------|
| {actor 1} | {beginner / intermediate / expert} | {permissions} | |
| {actor 2} | | | |

> 任何缺少正式定义的角色，都标记 `[GLOSSARY-GAP: {actor}]`。

### 2.4 约束
{从输入中提取的监管、技术、资源和平台约束。使用编号列表。}

1. {约束 1——来自输入的原文或转述}
2. {Constraint 2}

> 如果输入中找不到约束，使用 `[CONTEXT-GAP: no constraints identified]`。

### 2.5 假设与依赖
{本规格成立所必须满足的条件。}

1. {假设 1——若不成立，本规格会改变}
2. {假设 2——第三方服务、数据迁移、技术栈等}

### 2.6 需求分配
*（可选——IEEE 830 §5.2.6）* 明确推迟到未来版本的功能：

- {Deferred feature 1} — 推迟原因
- 如果没有：「当前没有推迟的需求。」

---

## 3. 具体需求

### 3.1 外部接口需求

#### 3.1.1 用户界面
{屏幕/页面清单、导航约束、无障碍标准（例如 WCAG 2.1 AA）。}

#### 3.1.2 硬件接口
{设备目标、传感器、外设。}
`[TBD: hardware interfaces not specified | owner: {role} | resolve-by: sprint planning]`

#### 3.1.3 软件接口

| 外部系统 | 接口类型 | 协议 | 认证方式 | 备注 |
|-----------------|---------------|----------|-------------|-------|
| {system 1} | REST API / SDK / DB | HTTPS / WebSocket | OAuth 2.0 / API Key | |

#### 3.1.4 通信接口
{网络协议、数据格式、加密要求。}

---

### 3.2 功能（功能需求）

<!-- SKILL: repeat the block below for each FR. One "shall" per block. Exactly one "When" per GWT. -->
<!-- Priority: Essential = MVP must-ship | Conditional = nice-to-have | Optional = future release -->

#### FR-01 [Essential]
**需求：** 系统应 {verb} {object}，触发条件为 {condition}。
**参与者：** {执行该动作的角色}
**前置条件：** {本 FR 适用前必须成立的系统状态}
**Given:** {初始上下文 / 状态}
**When:** {触发条件或用户动作——只能有一个}
**Then:** {可从外部观察的结果}
**来源：** [{在输入或澄清轮次中的原文位置}]

> ⚠️ 如果「Then」无法从外部观察 → 标记 `[VERIFIABILITY-FAIL: FR-01]` 并加入附录 B。

---

#### FR-02 [Essential]
**需求：** 系统应 {verb} {object}，触发条件为 {condition}。
**参与者：** {role}
**前置条件：** {state}
**Given:** {context}
**When:** {trigger}
**Then:** {observable outcome}
**来源：** [{location}]

---

<!-- Continue FR-03, FR-04… in sequence. No gaps in numbering. -->

---

### 3.3 性能需求

<!-- SKILL: one block per performance NFR. Response Measure must be numeric — no adjectives. -->

#### NFR-01 [性能 — ISO/IEC 25010：时间特性]
| 属性 | 值 |
|-----------|-------|
| 来源 | {谁/什么触发了该关注点} |
| 刺激 | {事件或负载条件——例如「1,000 名用户同时提交表单」} |
| 环境 | {正常 / 峰值 / 降级} |
| 制品 | {系统组件或端点} |
| 响应 | {系统如何响应} |
| 响应度量 | {数字阈值——例如「p95 延迟 < 500 ms」} |

> ⚠️ 不允许使用模糊修饰语（fast、quick、responsive）。
> 未解决时：`[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`

---

### 3.4 逻辑数据库需求
{数据实体、关系、保留期、访问约束。}

| 实体 | 关键属性 | 关系 | 保留期 |
|--------|---------------|---------------|-----------|
| {Entity 1} | {id, name, …} | {属于实体 2} | {N years} |

> 如果未提及数据库，使用 `[TBD: database schema not specified | owner: tech lead | resolve-by: sprint planning]`。

---

### 3.5 设计约束
{强制遵守的标准、被强制的技术选型、§2.4 中的硬件限制。}

1. {例如「系统应按既有技术栈使用 {language/framework} 实现」}
2. {例如「所有静态数据都应使用 AES-256 加密」}

---

### 3.6 软件系统属性

<!-- One QA Scenario block per characteristic. ISO/IEC 25010 characteristics: -->
<!-- Reliability | Availability | Security | Maintainability | Portability -->

#### NFR-{NN} [安全 — ISO/IEC 25010：安全]
| 属性 | 值 |
|-----------|-------|
| 来源 | 未授权用户 |
| 刺激 | 在没有有效凭证的情况下尝试访问受保护资源 |
| 环境 | 生产环境 |
| 制品 | 认证层 |
| 响应 | 系统拒绝请求并记录该次尝试 |
| 响应度量 | 100% 的未授权请求被拒绝；500 毫秒内创建审计日志条目 |

> 如果系统有用户角色，要包含 RBAC 需求。如果系统是 Web 系统，参考 OWASP Top 10。

#### NFR-{NN} [可用性 — ISO/IEC 25010：可用性]
| 属性 | 值 |
|-----------|-------|
| 来源 | 终端用户 |
| 刺激 | 在计划运营时段内发起访问请求 |
| 环境 | 正常 |
| 制品 | 整个系统 |
| 响应 | 系统接受并处理请求 |
| 响应度量 | {例如「按月统计 99.5% 正常运行时间，不含计划内维护」} |

---

### 3.7 其他需求
{国际化、本地化、法律、许可、监管要求。}

- 如果没有：「目前未识别出额外需求。」

---

## 附录 A：术语表

| 术语 | 定义 |
|------|------------|
| {domain term 1} | {一句话定义} |
| {domain term 2} | {one-sentence definition} |
| {domain term 3} | {one-sentence definition} |

> 要得到 COMPLIANT 判定，§1–§3 中所有 `[GLOSSARY-GAP: {term}]` 标签都必须在这里解决。

---

## 附录 B：待解决问题

| # | 章节 | 缺口类型 | 描述 | 优先级 | 状态 |
|---|---------|----------|-------------|----------|--------|
| 1 | §{N.N} | [CONTEXT-GAP / GLOSSARY-GAP / VERIFIABILITY-FAIL / TBD] | {description} | P{1/2/3} | Open |

> 在文档获批进入开发之前，本附录必须为空（或所有条目均为 Resolved）。

---

## 修订历史

| 版本 | 日期 | 作者 | 变更 |
|---------|------|--------|--------|
| v0.1 | {YYYY-MM-DD} | {author} | 初稿 |
