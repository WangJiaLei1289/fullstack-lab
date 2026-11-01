# pm-execution

执行与产品管理技能：PRD、OKR、路线图、冲刺、事前验尸、利益相关方地图、用户故事、优先级排序框架等。

## Skills (16) 技能

- **brainstorm-okrs** — 头脑风暴与公司目标对齐的团队级 OKR。
- **create-prd** — 创建精简、可直接用于决策的产品需求文档（PRD），使用 8 段式模板，涵盖摘要、背景、目标、细分市场、价值主张、解决方案细节和发布计划。默认保持精简（约一到两页），需要时可提供更完整的规格说明。
- **dummy-dataset** — 生成逼真的测试用假数据集，支持自定义列、约束条件和输出格式（CSV、JSON、SQL、Python 脚本）。
- **job-stories** — 使用「When [situation], I want to [motivation], so I can [outcome]」格式创建任务故事（Job Story），并附详细的验收标准。
- **outcome-roadmap** — 将产出导向的路线图转化为结果导向的路线图。
- **pre-mortem** — 对 PRD 进行事前验尸（pre-mortem）分析。
- **prioritization-frameworks** — 9 种优先级排序框架的参考指南，含公式、适用场景指引和模板。
- **release-notes** — 根据工单、PRD 或变更日志生成面向用户的发布说明。
- **retro** — 引导一场结构化的冲刺复盘。
- **sprint-plan** — 规划冲刺：产能估算、故事选取、依赖关系梳理和风险识别。
- **stakeholder-map** — 使用权力/兴趣矩阵绘制利益相关方地图，识别每个象限的沟通策略，并生成沟通计划。
- **strategy-red-team** — 对 PRD、路线图或战略做红队评审，攻击其承重假设；对失效模式排序，并为每种模式给出成本最低的测试和终止判据。
- **summarize-meeting** — 将会议逐字稿总结为结构化模板，包含日期、参会人、主题、要点和行动项。
- **test-scenarios** — 根据用户故事创建完整的测试场景，包含测试目标、起始条件、用户角色、分步操作和预期结果。
- **user-stories** — 按 3C 原则（Card、Conversation、Confirmation）和 INVEST 准则创建用户故事，包含描述、设计链接和验收标准。
- **wwas** — 以 Why-What-Acceptance 格式创建产品待办项。

## Commands (11) 命令

- `/pm-execution:generate-data` — 生成逼真的测试用假数据集 — CSV、JSON、SQL 插入语句或 Python 脚本。
- `/pm-execution:meeting-notes` — 将会议逐字稿总结为结构化纪要，包含决议、行动项和后续动作。
- `/pm-execution:plan-okrs` — 头脑风暴与公司目标对齐的团队级 OKR — 定性的目标配可量化的关键结果。
- `/pm-execution:pre-mortem` — 对 PRD、发布计划或功能做事前验尸风险分析 — 在问题发生前识别可能出问题的地方。
- `/pm-execution:red-team-prd` — 对 PRD、路线图或战略做红队评审 — 攻击其承重假设，并在投入前为每个假设给出成本最低的测试。
- `/pm-execution:sprint` — 冲刺生命周期 — 规划冲刺、进行复盘或生成发布说明。
- `/pm-execution:stakeholder-map` — 在权力 × 兴趣矩阵上标注利益相关方，并制定有针对性的沟通计划。
- `/pm-execution:test-scenarios` — 根据用户故事或功能规格生成完整的测试场景 — 正常路径、边界情况和错误处理。
- `/pm-execution:transform-roadmap` — 将基于功能的路线图转换为传达战略意图的结果导向路线图。
- `/pm-execution:write-prd` — 根据功能想法或问题陈述创建精简的产品需求文档，需要时可提供更完整的规格说明。
- `/pm-execution:write-stories` — 将功能拆解为待办项 — 用户故事、任务故事或 WWA 格式，并附验收标准。

## 作者

Paweł Huryn — [The Product Compass 通讯](https://www.productcompass.pm)

## 许可证

MIT
