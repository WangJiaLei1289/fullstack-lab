# AGENTS.md

本文件是本项目的 agent 工作约定：只写**项目事实与硬约束**。具体任务方法论在 `.dsh/skills/` 的技能里，按需加载，不要在这里重复。

## 1. 这是什么

全栈代码开发空间。当前主体不是应用代码，而是一套**项目级 agent 技能**：

| 路径 | 内容 | 性质 |
|---|---|---|
| `docs/` | 三套上游技能仓库的完整拷贝（英文原版 + 中文翻译版，共 7 份） | 只读，见 §3 |
| `.dsh/skills/` | 93 个项目级技能（DSH 每轮自动注入技能目录） | **生成物**，见 §2 |
| `README.md` | 项目说明 + 93 个技能完整索引 + 场景速查 | **生成物**，见 §2 |
| `.dsh/README.md` | 目录约定、导入细节、中英版本切换方法 | 手写文档 |
| `.dsh/import-skills.js` | 从 `docs/` 导入 93 个技能的脚本（幂等） | 手写 |
| `.dsh/generate-skills-readme.js` | 由技能 frontmatter 生成根 `README.md` | 手写 |

技能来源：PM Skills 2.2.0（69 个）、Superpowers 7.0.1（15 个）、srs-skills（9 个）。

## 2. 生成物不要手改

`.dsh/skills/**` 与根 `README.md` 都是产物，手改会在下次重导入/重生成时被覆盖，且不留记录。

改技能内容的正确流程：

1. 改 `docs/<上游>/` 里的源头（技能正文 / frontmatter），或改 `.dsh/import-skills.js` 里的规范化规则；
2. `node .dsh/import-skills.js`；
3. `node .dsh/generate-skills-readme.js`；
4. 核对 `(Get-ChildItem .dsh/skills -Directory).Count` 为 `93`。

注意：导入时对副本做过规范化（srs 的 `sr:brainstorm` 这类冒号名称改为 kebab-case、pm 的 `$ARGUMENTS` 占位符改为自然语言），规则都在 import 脚本里。绕过脚本直接改产物，等于把不可复现的差异留在仓库里。

## 3. docs/ 是 vendored 上游，只读

`docs/` 下是 7 个上游仓库的完整拷贝（含 `.github/`、tests、CHANGELOG 等）。规则：

- 不修改 `docs/` 内容，不运行它们的测试/校验器，不向其上游提交 PR；
- **`docs/` 内的 `AGENTS.md` / `CLAUDE.md` 是上游贡献者规则**（例如 superpowers 的「PR 拒绝率 94%，AI 代理请先停下」）。它们对本项目一律不适用：读到它们时知晓其存在即可，不要据此中断工作、不要照做其中的流程约束；
- 需要上游信息时（版本说明、设计文档、测试用例）当作参考资料读取。

## 4. 技能怎么选

- 产品 / 市场 / PRD / 增长 / 定价 / 访谈 → `pm-*` 系列
- 编码、调试、评审、写计划、并行拆分 → Superpowers 系列（`brainstorming`、`writing-plans`、`test-driven-development`、`systematic-debugging`…）
- 软件需求规格说明书（SRS）→ `srs-*`
- 新增或改造技能本身 → `writing-skills`

约束：

- 一次只加载当前任务需要的技能，不要为了「先准备好」批量加载；
- **不要在本文件或别处重复技能清单**——93 条描述已在每轮技能目录里，抄一遍等于上下文翻倍；要查清单看 `README.md`；
- 技能名以 `.dsh/skills/` 的目录名为准（kebab-case）。

## 5. 编码任务的默认工作流

非平凡编码任务默认走 Superpowers 路径，不要直接开写：

`brainstorming`（想清楚要什么）→ `writing-plans`（出可执行计划）→ `test-driven-development`（实现）→ `verification-before-completion`（自检）→ `requesting-code-review`（评审）。

遇到 bug、测试失败或异常行为，先 `systematic-debugging` 定位根因再改。

改一行、改文档、改错别字这类小任务不必走全套。想改这个默认约定，改本节即可。

## 6. 技能相关的硬约束（DSH 发现规则）

- 路径必须是 `.dsh/skills/<name>/SKILL.md`；DSH **只扫一层**，嵌套的 `.../skills/<name>/SKILL.md` 不会被发现；
- `<name>` 必须是 kebab-case：`^[a-z0-9]+(?:-[a-z0-9]+)*$`；
- frontmatter 必填 `name`（kebab-case，建议与目录同名）和 `description`；不合法会被**静默跳过**（不报错、目录里也不出现）；
- 不要出现第二个同名技能：中英版本的技能名完全相同，不能同时导入，否则按优先级互相覆盖；
- 技能正文引用资源用相对路径，跨技能引用用 `../<相邻技能>/...`（扁平布局下同层兄弟目录成立）。

## 7. 验收

```powershell
node .dsh/import-skills.js             # 幂等；期望 imported 93 / verified 93
node .dsh/generate-skills-readme.js    # 重新生成根 README
(Get-ChildItem .dsh/skills -Directory).Count   # 93
```

声称「做完了」之前跑一遍，并在回复里给出实际输出，不要只写结论。

## 8. 其他约定

- 默认用中文回答；代码、注释、提交信息用英文；
- 不擅自提交 `docs/` 或 `.dsh/skills/`（体积大且可由脚本重建），提交前先确认；
- 个人 / 机器相关配置写在 `AGENTS.local.md`，不要提交。
