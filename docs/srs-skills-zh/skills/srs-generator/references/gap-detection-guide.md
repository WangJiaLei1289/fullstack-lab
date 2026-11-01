# 缺口检测指南
*由 `srs-generator` 的第 2 步（缺口扫描）使用*

该技能标记的每个缺口都必须匹配下面 7 种模式之一。
每个检出的缺口按以下格式输出：
```
[P{1|2|3}] Pattern {N} — {type label}: "{verbatim fragment or description of what is absent}"
```

---

## 标签参考

| 标签 | 含义 | 在 SRS 中的位置 |
|-----|---------|------------------------|
| `[CONTEXT-GAP: {desc}]` | 输入中缺失的信息 | §1–§3、附录 B |
| `[GLOSSARY-GAP: {term}]` | 领域术语未定义 | §1.3 引用、附录 A |
| `[VERIFIABILITY-FAIL: {FR-NN}]` | FR 的结果无法从外部观察 | §3.2、附录 B |
| `[TBD: {condition} \| owner: {role} \| resolve-by: {date}]` | 推迟——必须在批准前解决 | 任何 §3 NFR |

---

## 模式 1：模糊量词

**定义：** 用在可度量属性上的非数字数量形容词或副词。

**触发词：** many、few、some、large、small、fast、slow、soon、quickly、appropriate、good、high、low、reasonable、sufficient、minimal、significant、several、numerous。

**示例：**
- 「系统必须快速响应」→ `[P3] Pattern 1 — Vague Quantifier: "quickly" — no numeric threshold for response time`
- 「我们需要高可用」→ `[P2] Pattern 1 — Vague Quantifier: "high availability" — no percentage or MTBF target stated`

**优先级：** 默认 P3。如果该模糊词是某核心功能唯一的成功标准，则升级为 P2。

---

## 模式 2：弱情态动词

**定义：** 表达可能性或意愿、而非义务的情态动词。

**触发词：** should、might、could、may、can（在需求语境中表示许可时）。
与以下词区分：`shall`、`must`——按 IEEE 830，它们是无歧义的义务。

**示例：**
- 「用户应该能够导出报表」→ `[P2] Pattern 2 — Weak Modality: "should" on core feature — is export required or optional?`
- 「仪表盘可以显示分析数据」→ `[P3] Pattern 2 — Weak Modality: "could" — treat as Conditional/Optional feature`

**优先级：** 默认 P2。如果「should」出现在已声明的核心功能上，则升级为 P1（按 IEEE 830 §4.3.2，这会让该功能无法实现地含糊）。

---

## 模式 3：未定义的参与者

**定义：** 需求中出现、但此前没有定义的角色标签，或没有明确先行角色的代词。

**触发信号：** 「the user」（未定义的用户画像）、「they」、「it」（指代系统）、「admin」（没有访问级别）、「customer」（多画像系统）、「the system」（范围内有多个系统时）。

**示例：**
- 「它应该发送确认邮件」→ `[P1] Pattern 3 — Undefined Actor: "It" — unclear which system/component sends the email`
- 「管理员可以审批订单」→ `[P2] Pattern 3 — Undefined Actor: "Admin" — shop admin, platform admin, or both?`

**优先级：** 主要参与者含糊时（核心流程不可测试）为 P1。次要参与者含糊时为 P2。
**动作：** 每个未定义的参与者在第 1 步提取时也会触发 `[GLOSSARY-GAP: {actor}]`。

---

## 模式 4：回指引用

**定义：** 当同类型的多个实体都在范围内时，指代对象含糊的代词或指示词。与模式 3 不同——这里参与者已经命名，但后文的代词不清楚。

**触发信号：** 「this」、「that」、「these」、「it」、「they」、「the former」、「the latter」、「same」、「the above」。

**示例：**
- "The manager approves the invoice; the supplier reviews it and the accountant signs it."
  → `[P2] Pattern 4 — Anaphoric Reference: both "it" instances could refer to the invoice or the approval record`

**优先级：** 默认 P2。如果含糊代词出现在交易、数据流、所有权或删除相关的陈述中，则升级为 P1。

---

## 模式 5：并列歧义

**定义：** 由「and」/「or」连接、逻辑分组不清楚的复合名词短语或条件。

**典型形式：**
- "A and B or C"——"or" 只作用于 B 和 C，还是整个短语？
- "admins and users with permission"——是用户需要权限，还是只有管理员？
- "create, edit, or delete reports and logs"——delete 是否同时作用于两者？

**示例：**
- "Managers and users with read access can export reports and invoices."
  解释 A：(managers) and (users with read access) can export (reports) and (invoices).
  解释 B：(managers) and (users) with read access can export (reports) and (invoices).
  → `[P2] Pattern 5 — Coordination Ambiguity: "managers and users with read access" — permission scope unclear`

**优先级：** 默认 P2。如果歧义出现在授权、权限或删除规则中，则升级为 P1。

---

## 模式 6：缺失约束

**定义：** 某一类必需约束完全缺失——而不是只写得含糊。检查全部五个子类：

| 子类 | 要检查什么 | 缺失时的优先级 |
|-------------|------------------|--------------------|
| 错误处理 | 功能在失败、超时或无效输入时没有陈述任何行为 | 核心交易为 P1 |
| 并发 / 数据量 | 没有最大并发用户数、TPS 或数据量 | P2 |
| 权限 / 角色 | 功能存在，但没有被授权执行它的角色（或没有拒绝未授权角色） | 任何 CUD 操作为 P1 |
| 回滚 / 撤销 | 破坏性操作（删除、发布、支付）没有回滚或确认要求 | P1 |
| 非功能基线 | 文档中任何地方都没有性能、安全或可用性目标 | P2 |

**示例：**
- 支付失败没有错误行为 → `[P1] Pattern 6 — Missing Constraint: no error handling for payment failure`
- 没有说明并发用户上限 → `[P2] Pattern 6 — Missing Constraint: no concurrency/volume target`

---

## 模式 7：矛盾

**定义：** 两条或多条不能同时成立的陈述，或对同一功能施加互斥条件。

**常见形式：**
- 同一功能在一处是「必需」，在另一处是「不在范围内」
- 某个角色同时被授予和被拒绝同一权限
- 性能目标与已陈述的硬件约束冲突

**示例：**
- "The system must support 10,000 concurrent users." + "The server will be a single shared VM with 2GB RAM."
  → `[P1] Pattern 7 — Contradiction: concurrent user target (10,000) is incompatible with stated hardware (single 2GB VM)`

**检测方法：** 把所有提取出的 FR 陈述相互比较，并分别与已陈述的约束比较，检查逻辑上是否不相容。不要只依赖触发词扫描。

**优先级：** 如果矛盾涉及核心功能、参与者权限或数据完整性规则，则为 P1。如果只是主要功能与次要功能之间的矛盾（其中一个可能本就不在范围内），则为 P2。

---

## 优先级分类参考

| 优先级 | 条件 | 动作 |
|----------|-----------|--------|
| **P1** | 缺口使某项需求无法实现或无法测试 | 在写任何 SRS 章节之前于第 1 轮解决。无法解决则阻塞生成。 |
| **P2** | 缺口带来范围风险，但可以假设一个合理默认值 | 在第 2 轮解决。若未回答：在 SRS 与附录 B 中记录所假设的默认值。 |
| **P3** | 缺口可推迟；实现团队可以自主决定 | 在第 3 轮提出。若跳过：标记 `[TBD: {condition} \| owner: {role} \| resolve-by: sprint planning]`。 |

---

## IEEE 830 质量属性检查清单

在 SRS 生成之后运行这份清单，以确定合规判定。每项未通过的检查都会产出一个标签。

| 属性（IEEE 830 §4.3） | 在生成的 SRS 中验证什么 | 未通过时的标签 |
|--------------------------|-------------------------------------|----------------|
| **正确** | 每个 FR 都有 `[Source: {input location}]`，可追溯到用户提供的内容 | `[CONTEXT-GAP: FR-NN has no source]` |
| **无歧义** | 任何 FR/NFR 陈述中都不再留下模糊修饰语；只可能有一种解释 | 模式 1 或 2 标记 |
| **完整** | 所有参与者都有 ≥1 个 FR；所有 FR 都有 Actor + Precondition + GWT；§1.2 的 IN/OUT 表已填好 | `[CONTEXT-GAP: {what is missing}]` |
| **一致** | 没有两个 FR 互相矛盾；整份文档术语统一 | 模式 7 标记 |
| **有分级** | 每个 FR 都带有 Essential / Conditional / Optional 标签 | `[CONTEXT-GAP: FR-NN ranking missing]` |
| **可验证** | 每项 NFR 都有数字化响应度量；每个 FR 的「Then」都可从外部观察 | `[VERIFIABILITY-FAIL: FR-NN]` |
| **可修改** | 每条需求都是单条原子的「shall」陈述；FR 之间没有冗余 | 结构性备注（不给标签） |
| **可追溯** | 每个 FR 都有唯一的 FR-NN 编号；附录 B 把未决缺口链接到其 SRS 章节 | 结构性备注（不给标签） |

**判定规则：**
- **COMPLIANT**——8 项检查全部通过；附录 B 为空或所有条目均为 Resolved
- **PARTIALLY COMPLIANT**——所有必需章节齐全，但附录 B 有未决项
- **NON-COMPLIANT**——缺少必需章节，或 ≥3 个属性存在普遍性失败

---

## 完整示例

**示例输入（一封真实的客户邮件）：**

> Hi team, we're building an internal invoicing tool for our finance department. Managers should be able to create and send invoices to clients, and clients can view and download them. The system needs to be fast and support many users at the same time. Admins can manage user accounts. We also want notifications when an invoice is approved — the system should send them automatically. We don't need mobile support for now. It should integrate with our existing accounting software. Data needs to be kept safe, and we'll need an audit log for compliance purposes.

**缺口扫描输出：**

| # | 优先级 | 模式 | 原文片段 / 缺失元素 |
|---|----------|---------|-------------------------------------|
| 1 | P2 | 模式 2——弱情态 | 「should be able to create」——发票创建是 Essential 还是 Conditional？ |
| 2 | P3 | 模式 1——模糊量词 | 「fast」——没有数字化的响应时间目标 |
| 3 | P3 | 模式 1——模糊量词 | 「many users at the same time」——没有并发用户数 |
| 4 | P2 | 模式 3——未定义的参与者 | 「Admins」——没有定义管理员角色与经理角色的区别；两者重叠不清 |
| 5 | P2 | 模式 4——回指引用 | 「the system should send them automatically」——「them」可能指发票，也可能指通知 |
| 6 | P1 | 模式 6——缺失约束（权限） | 「clients can view and download」——没有定义角色授权；没有陈述对非客户的限制 |
| 7 | P2 | 模式 6——缺失约束（回滚） | 已发送的发票没有陈述回滚——已发送的发票能撤回吗？ |
| 8 | P1 | 模式 6——缺失约束（错误处理） | 会计软件集成没有陈述失败行为 |

**检出的模式：** 4 种不同类型（模式 1、2、3、4、6）——超过 COMPLIANT 缺口扫描所需的最低 4 种。
