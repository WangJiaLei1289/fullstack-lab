# 项目级技能（DSH skills）

本目录是 **DeepSeek Harness 的项目级 skill 根目录**：`.dsh/skills/<name>/SKILL.md`。

DSH 的发现规则（来自 `@deepseek-ai/dsh-skill-filesystem`）：

- 项目根 = 当前工作目录向上找到的**最近一个含 `.git` 的目录**（本仓库根即 `fullstack-lab/`，因此本目录生效）。
- 优先级：`<projectRoot>/.dsh/skills` (rank 100) > `<projectRoot>/.agents/skills` (200) > 自定义目录 (300) > `~/.dsh/skills` (400)。
- **只扫一层**：`<root>/<name>/SKILL.md` 或 `<root>/<name>.md`；`**/SKILL.md` 这种嵌套结构不会被发现。
- frontmatter 必填 `name` + `description`；`name` 必须是 kebab-case（`^[a-z0-9]+(?:-[a-z0-9]+)*$`），否则**静默跳过**。
- 目录被监听，增删改名/改 frontmatter 会实时刷新会话 skill 目录，无需重启。

## 已导入的三套（英文原版）

| 来源 | 仓库位置（保留原始副本） | skill 数 |
|---|---|---|
| PM Skills 2.2.0（product management，9 插件） | `docs/pm-skills-2.2.0/pm-*/skills/` | 69 |
| Superpowers 7.0.1（开发方法论） | `docs/superpowers-7.0.1/skills/` | 15 |
| srs-skills（IEEE 830 SRS 流水线） | `docs/srs-skills/skills/` | 9 |
| **合计** | | **93** |

`docs/` 下另有 `pm-skills-2.2.0-zh`、`superpowers-7.0.1-zh`、`superpowers-7.0.1-zh-full`、`srs-skills-zh`
四份中文副本，本次未导入（与英文版 skill 名完全重名，同时导入会冲突）。要换成中文版见文末。

## 导入时做的规范化（只改副本，`docs/` 原文件未动）

1. **srs-skills 名称改写**：原 frontmatter 用 `name: sr:brainstorm`、`cl:srs`、`cl:srs-flow`，含冒号不是合法 skill 名，
   会被 DSH 直接跳过。已改为目录名形式的 kebab-case（`sr-brainstorm`、`srs-generator`、`srs-workflow` …），
   正文中的 `/sr:spec` 等调用提示同步改为 `/sr-spec`。
2. **srs-skills 引用路径改写**：正文里 `skills/<bundle>/references/...` 改为 `../<bundle>/references/...`。
   9 个 bundle 现在都是 `.dsh/skills/` 的兄弟目录，跨 bundle 引用照旧可用（与 superpowers 的相对引用风格一致）。
3. **pm-skills 命令占位符**：这些 skill 原本是 Claude Code 命令模板，正文里的 `$ARGUMENTS` 占位符
   改为 `the user's request` / `Provide the following as input:`，`/pm-ai-shipping:code-review` 改为 `/code-review`。
4. **superpowers 未改**：其 `../<sibling-skill>/...` 相对引用在扁平布局下天然成立。

## 验证 / 使用 / 卸载

```powershell
# 重新导入（幂等，会先删后拷每个目标目录）
node .dsh/import-skills.js

# 重新生成根目录 README.md 的技能索引（读各技能 frontmatter）
node .dsh/generate-skills-readme.js

# 核对数量
(Get-ChildItem .dsh/skills -Directory).Count      # 93

# 卸载某套（按前缀）
Remove-Item .dsh/skills/sr-*,.dsh/skills/srs-* -Recurse -Force   # srs-skills
```

会话中如何用：

- 模型侧：skill 会以 name+description 形式出现在技能目录里，按需调用 `skill` 工具加载正文。
- 用户侧：`user-invocable` 的 skill 可直接输入 `/name` 触发（如 `/srs-workflow`、`/pre-mortem`）。

## 注意事项

- **93 个 skill 会全部进入每轮会话的技能目录**，每条 description 最长 500 字符。上下文开销明显变大；
  如果只想保留常用的，删掉对应目录即可（`docs/` 里有原始副本，随时可重新导入）。
- 三套的 42 条 `commands/*.md`（PM Skills 的命令层）**没有导入**——DSH 的项目级根目录只认 skill，
  命令层是 Claude Code 的概念；这些命令对应的能力已由其 skill 覆盖。
- 语言副本切换：想用中文版时，把 `import-skills.js` 里的 `pm-skills-2.2.0` / `superpowers-7.0.1` / `srs-skills`
  换成 `-zh` 目录（superpowers 用 `-zh-full`），删掉 `.dsh/skills` 后重跑即可。
