# 贡献指南

PM Skills Marketplace 由 [Paweł Huryn](https://www.productcompass.pm)（pawel@productcompass.pm）维护。欢迎贡献——无论是修 bug、改错别字，还是提出新技能的想法。

## 如何贡献

- **Bug 与小修复** —— 直接提 PR。
- **新技能、新命令或较大改动** —— 先开 issue，方便我们一起讨论方案。

## 约定

- PR 保持聚焦——一个 PR 只做一件事。
- 沿用现有模式：技能是名词（领域知识），命令是动词（工作流）。
- 每个技能都需要带 `name` 和 `description` 的 frontmatter。每个命令都需要 `description` 和 `argument-hint`。
- 技能的 `name` 必须与所在目录名一致。
- 命令中不得跨插件引用。后续动作只用自然语言建议。
- 每位贡献者都会被公开列出（见下文「变更日志与贡献者署名」）。
- 提交前请运行检查：`python3 validate_plugins.py` 和 `python3 -m unittest discover -s tests`。

## 变更日志与贡献者署名

每一项面向用户的改动都会在 [CHANGELOG.md](CHANGELOG.md) 中记一条。提 PR 时，把这条记在顶部的 `## Unreleased` 标题下（没有就新建一个），并在条目末尾署上自己——`(#123, thanks @your-handle)`。署名会原样出现在 GitHub Release 说明中，并永久保留在变更日志里。

## 发布（维护者）

`CHANGELOG.md` 是事实来源；tag 与 GitHub Release 都是它的确定性投影（`.github/workflows/tag-on-merge.yml`）：

1. 把 `## Unreleased` 改名为 `## vX.Y.Z — YYYY-MM-DD`。语义化版本：破坏性改动 = major，新增技能/命令或行为变化 = minor，修复与文档 = patch。
2. 在 `.claude-plugin/marketplace.json` 和每个插件的 `plugin.json` 里设置同一版本号——全仓库版本保持一致（测试套件会强制检查）。
3. 推送到 `main`。CI 会校验版本同步、运行校验器与测试套件，然后打上 `vX.Y.Z` 标签，并以变更日志对应章节作为说明发布 GitHub Release。没有新标题 → 不发布；普通推送不受影响。

## 许可证

提交贡献即表示你同意你的贡献按 [MIT License](LICENSE) 授权。
