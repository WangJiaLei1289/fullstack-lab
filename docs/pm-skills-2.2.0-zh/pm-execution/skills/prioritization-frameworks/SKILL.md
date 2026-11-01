---
name: prioritization-frameworks
description: "9 个优先级排序框架的参考指南，包含公式、适用场景说明与模板——RICE、ICE、Kano、MoSCoW、机会分数等。适用于选择排序方法、对比 RICE 与 ICE 等框架，或了解不同优先级排序方法如何运作。"
---

## 优先级排序框架参考

一份参考指南，帮助你为自身情境选择并应用合适的优先级排序框架。

### 核心原则

绝不要让客户来设计方案。优先级要打在**问题（机会点）**上，而不是功能上。

### 机会分数（Dan Olsen，《The Lean Product Playbook》）

推荐用于给客户问题排优先级的框架。

就每项需求的**重要性（Importance）**与**满意度（Satisfaction）**调研客户（归一化到 0–1 刻度）。

三个相关公式：
- **当前价值** = 重要性 × 满意度
- **机会分数** = 重要性 × (1 − 满意度)
- **创造的客户价值** = 重要性 × (S2 − S1)，其中 S1 = 之前的满意度，S2 = 之后的满意度

高重要性 + 低满意度 = 最高的机会分数 = 最佳机会点。把它画在重要性 vs 满意度图上——左上象限是最佳区间。它排序的是客户问题，而不是解决方案。

### ICE 框架

适用于对举措和想法排优先级。它不仅考虑价值，还考虑风险与经济因素。

- **I**（影响）= 机会分数 × 受影响的客户数
- **C**（信心）= 我们有多大把握？（1-10）。考虑风险。
- **E**（容易度）= 实施起来有多容易？（1-10）。考虑经济因素。

**分数** = I × C × E。越高越优先。

### RICE 框架

把 ICE 中的影响拆成两个独立因子。适合需要更细颗粒度的大型团队。

- **R**（触达）= 受影响的客户数
- **I**（影响）= 机会分数（每位客户的价值）
- **C**（信心）= 我们有多大把握？（0-100%）
- **E**（投入）= 实施需要多少投入？（人月）

**分数** = (R × I × C) / E

### 9 个框架概览

| 框架 | 最适合 | 关键洞察 |
|-----------|----------|-------------|
| 艾森豪威尔矩阵 | 个人任务 | 紧急 vs 重要——用于产品经理个人的任务管理 |
| 影响 vs 投入 | 任务/举措 | 简单的 2×2——快速分级，不适合严谨的战略决策 |
| 风险 vs 回报 | 举措 | 类似影响 vs 投入，但考虑了不确定性 |
| **机会分数** | 客户问题 | **推荐。** 重要性 × (1 − 满意度)。归一化到 0–1。 |
| Kano 模型 | 理解期望 | 必备型、绩效型、魅力型、无差异型、反向型。用于理解，而非排优先级。 |
| 加权决策矩阵 | 多因素决策 | 给标准分配权重，为每个选项打分。适合争取利益相关方认同。 |
| **ICE** | 想法/举措 | 影响 × 信心 × 容易度。推荐用于快速排序。 |
| **RICE** | 规模化场景下的想法 | (触达 × 影响 × 信心) / 投入。在 ICE 基础上加入触达。 |
| MoSCoW | 需求 | Must/Should/Could/Won't。注意：源自项目管理。 |

### 模板

- [机会分数入门（PDF）](https://drive.google.com/file/d/1ENbYPmk1i1AKO7UnfyTuULL5GucTVufW/view)
- [重要性 vs 满意度模板——Dan Olsen（Google 幻灯片）](https://docs.google.com/presentation/d/1jg-LuF_3QHsf6f1nE1f98i4C0aulnRNMOO1jftgti8M/edit#slide=id.g796641d975_0_3)
- [ICE 模板（Google 表格）](https://docs.google.com/spreadsheets/d/1LUfnsPolhZgm7X2oij-7EUe0CJT-Dwr-/edit?usp=share_link&ouid=111307342557889008106&rtpof=true&sd=true)
- [RICE 模板（Google 表格）](https://docs.google.com/spreadsheets/d/1S-6QpyOz5MCrV7B67LUWdZkAzn38Eahv/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### 延伸阅读

- [产品管理框架汇编 + 模板](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Kano 模型：如何取悦客户又不变身功能工厂](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [持续产品发现大师课（CPDM）](https://www.productcompass.pm/p/cpdm)（视频课程）
