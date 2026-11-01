# GitHub issue

当 `gh` 已安装并通过认证时就用它；它负责认证、速率限制和 JSON。退路是改用 curl 调公开 API，再不行就给一个由你的搭档自己打开的 URL。

## 搜索

```bash
gh search issues --repo obra/superpowers --limit 10 "<terms>" \
  --json number,state,title --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'
```

没有 `gh` 时（未认证，每分钟 10 次请求）：

```bash
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/issues?q=repo:obra/superpowers+is:issue+<url-encoded terms>&per_page=10" \
  | jq -r '.items[] | "\(.number)\t\(.state)\t\(.title)"'
```

连 curl 也没有时，把 `https://github.com/obra/superpowers/issues?q=<terms>` 交给对方。

## 提交

把填写好的 `templates/issue.md` 写入工作区，并展示确切文本。获得批准后：

```bash
gh issue create --repo obra/superpowers --title "<title>" --body-file <path> \
  --label bug --label automated-issue-report
```

当提交者没有 push 权限时，GitHub 会静默丢弃标签，所以这些标签只有协作者提交时才会生效；模板页脚仍会把该 issue 标记为由技能提交。`gh` 无法附加文件：在 issue 创建后，把交付包路径给你的搭档，让对方通过浏览器附加。

没有 `gh` 时，给一个基于 `bug_report.md` 模板的预填链接，任何提交者用它都会自动打上 `bug` 标签：

```
https://github.com/obra/superpowers/issues/new?template=bug_report.md&title=<url-encoded title>&body=<url-encoded body>
```

GitHub 会拒绝大约超过 8,000 个字符的 URL；超过这个长度时，只带标题发送链接，并让你的搭档从文件里粘贴正文。