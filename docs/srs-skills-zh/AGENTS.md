# 集成指南 —— srs-skills

本包提供的技能与具体代理无关。SKILL.md 文件使用纯 markdown 指令，
任何 LLM 都能读懂；遵循这些指令不需要任何工具专有语法。

---

## Claude Code

在 Claude Code 中直接打开 `srs-skills/`——技能与钩子会从 `settings.json` 自动发现：

```
srs-skills/
  skills/srs-generator/SKILL.md   ← /cl:srs  (quick SRS from existing reqs)
  skills/srs-workflow/SKILL.md    ← /cl:srs-flow  (full pipeline: brainstorm → SRS)
  skills/srs-generator/references/  ← shared references (srs-template, gap-guide)
  skills/srs-workflow/references/   ← workflow references (brainstorm-guide, plan-structure)
```

| 技能 | 调用方式 | 适用场景 |
|-------|--------|----------|
| `cl:srs` | `/cl:srs` | 用户已经有原始需求文本 |
| `cl:srs-flow` | `/cl:srs-flow` | 用户只有主题/想法——需要完整的头脑风暴 → SRS 流水线 |

复制到另一个项目：

```bash
# Quick SRS skill only
cp -r srs-skills/skills/srs-generator <your-project>/skills/srs-generator/

# Full workflow skill (includes above references)
cp -r srs-skills/skills/srs-workflow <your-project>/skills/srs-workflow/

# Automation scripts
cp -r srs-skills/scripts <your-project>/
cp -r srs-skills/hooks <your-project>/hooks/
cp srs-skills/settings.json <your-project>/settings.json
```

---

## Gemini CLI

```bash
cp -r srs-skills/skills/srs-generator .gemini/skills/
cp -r srs-skills/skills/srs-workflow .gemini/skills/
```

在 `.gemini/system.md` 中：
```
When the user types @srs: follow .gemini/skills/srs-generator/SKILL.md
When the user types @srs-flow: follow .gemini/skills/srs-workflow/SKILL.md
```

---

## GitHub Copilot（工作区指令）

在 `.github/copilot-instructions.md` 中：
```
For quick SRS from existing requirements, follow: srs-skills/skills/srs-generator/SKILL.md
For full brainstorm-to-SRS pipeline, follow: srs-skills/skills/srs-workflow/SKILL.md
```

---

## 任何其他 LLM / 代理

把对应的 SKILL.md 加载进代理的系统提示词：

| 目标 | 要加载的文件 |
|------|--------------|
| 从已有需求快速生成 SRS | `skills/srs-generator/SKILL.md` + `references/srs-template.md` + `references/gap-detection-guide.md` |
| 从主题走完整流水线 | `skills/srs-workflow/SKILL.md` + 两个参考目录 |

这些技能是自包含的——不需要任何外部 API。Python 脚本是可选增强
（gap_scanner.py、srs_validator.py），可以从 Claude 钩子调用，也可以在 CLI 手动运行。

---

## 关键字 / 别名约定

| 工具 | 技能 | 别名 |
|------|-------|-------|
| Claude Code | cl:srs | `/cl:srs` |
| Claude Code | cl:srs-flow | `/cl:srs-flow` |
| Gemini CLI | srs-generator | `@srs` |
| Gemini CLI | srs-workflow | `@srs-flow` |
| GitHub Copilot | srs-generator | `#srs` |
| GitHub Copilot | srs-workflow | `#srs-flow` |
| 自定义代理 | 两者皆可 | `!srs` / `!srs-flow` |
