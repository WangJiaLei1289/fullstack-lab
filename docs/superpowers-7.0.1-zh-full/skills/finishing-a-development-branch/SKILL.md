---
name: finishing-a-development-branch
description: "当实现已经完成、所有测试都通过，而你需要决定如何整合这些工作时使用"
---

# 收尾开发分支

## 概览

**核心原则：** 验证测试 → 检测环境 → 呈现选项 → 执行选择 → 清理。

**开始时宣告：** "I'm using the finishing-a-development-branch skill to complete this work."（我正在使用 finishing-a-development-branch 技能来完成这项工作。）

## 第 1 步：验证测试

运行项目的完整测试套件（`npm test` / `cargo test` / `pytest` / `go test ./...`）。

**如果测试失败**，报告失败并停下来——菜单要等测试全绿之后才出现：

```
测试失败（<N> 个失败项）。完成之前必须先修好：

[Show failures]（展示失败项）
```

**如果测试通过：** 继续第 2 步。

## 第 2 步：检测环境

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

这决定了要展示哪个菜单，以及清理工作如何进行：

| 状态 | 菜单 | 清理 |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON`（普通仓库） | 标准 3 个选项 | 没有工作树需要清理 |
| `GIT_DIR != GIT_COMMON`，命名分支 | 标准 3 个选项 | 基于来源判定（见第 6 步） |
| `GIT_DIR != GIT_COMMON`，分离头指针（detached HEAD） | 精简为 2 个选项（没有合并） | 由外部管理——保持原样 |

## 第 3 步：确定基础分支

基础分支就是这次工作从它分出来的那个分支——通常在计划、对话或该分支的上游里写明了。如果还不知道，就问：「这个分支是从 <你最好的猜测> 分出来的——对吗？」合并前先确认：合错基础分支，撤销起来很贵。

## 第 4 步：呈现选项

**普通仓库和命名分支的工作树——只呈现这 3 个选项：**

```
实现完成。你想怎么做？

1. 在本地合并回 <base-branch>
2. 推送并创建一个 Pull Request
3. 保持分支原样（我稍后自己处理）

选哪个？
```

**分离头指针——只呈现这 2 个选项：**

```
实现完成。你现在处于分离的 HEAD 状态（由外部管理的工作区）。

1. 作为新分支推送并创建一个 Pull Request
2. 保持原样（我稍后自己处理）

选哪个？
```

完全按写好的内容呈现菜单——简洁，每个选项都来自上面的列表。丢弃这些工作只在你的搭档明确要求时才会发生（见下面「如果你的搭档要求丢弃这些工作」）。等待他们的回答；整合方式由他们决定。

## 第 5 步：执行所选操作

### 选项 1：在本地合并

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

如果合并后的结果测试失败：停下来，把工作树和分支留在原处，然后排查——还没有推送任何东西，所以这次合并是本地的、可恢复的。

一旦合并结果全绿：清理工作树（第 6 步），然后删除分支：

```bash
git branch -d <feature-branch>
```

### 选项 2：推送并创建 PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

然后用代码托管平台（forge）的工具，针对 <base-branch> 创建拉取/合并请求——有 CLI 就用它的 CLI，否则用大多数平台在你推送时会打印出来的创建 URL——如果仓库有 PR 模板和约定，就照它们来，并把 URL 报告给你的搭档。

保留工作树——你的搭档会在那里根据 PR 反馈继续迭代。

### 选项 3：保持原样

报告："Keeping branch <name>. Worktree preserved at <path>."（中文大意：保留分支 <name>，工作树保留在 <path>。）

### 如果你的搭档要求丢弃这些工作

这条路径只在收到「把工作扔掉」的明确请求时才会走。先确认：

```
这会永久删除：
- 分支 <name>
- 所有提交：<commit-list>
- 位于 <path> 的 worktree

输入 'discard' 以确认。
```

等待那个一模一样的确认。它到了之后：

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

然后清理工作树（第 6 步）并强制删除分支：

```bash
git branch -D <feature-branch>
```

## 第 6 步：清理工作区

**对选项 1 和已确认的丢弃执行。** 选项 2 和 3 始终保留工作树。两个调用方都已经把当前目录切到主仓库根目录——移除工作树必须从工作树外面执行——并且使用第 2 步捕获的 `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` 值，那些值是在切目录之前捕获的。

**如果 `GIT_DIR == GIT_COMMON`：** 普通仓库，没有工作树需要清理。到此结束。

**如果 `WORKTREE_PATH` 位于 `.worktrees/` 或 `worktrees/` 下：** superpowers 创建了这个工作树——清理由我们负责：

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**如果移除被拒绝**（`contains modified or untracked files`）：工作树里存着只存在于那里的文件——未提交的计划、笔记或草稿。绝不按自己的主张加 `--force`。给你的搭档看利害所在，然后问：

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
拒绝移除 worktree——这些文件从未提交过：

<file list>

1. 清理之前先把它们提交到 <branch>
2. 把它们移到 <main repo root> 里
3. 删除它们（无法恢复）

选哪个？
```

执行所选的操作，然后移除工作树。

**其他情况：** 宿主环境拥有这个工作区——保持原样。如果你的平台提供了退出工作区的工具，就用它。

## 快速参考

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | 是 | - | - | 是 |
| 2. 创建 PR | - | 是 | 是 | - |
| 3. 保持原样 | - | - | 是 | - |
| 丢弃（仅在明确要求时） | - | - | - | 是（强制） |

## 常见的自我合理化

| 借口 | 现实 |
|--------|---------|
| 「本会话早些时候测试通过了」 | 在你即将整合的那棵代码树上跑一遍套件。一次全绿只证明它跑过的那棵树。 |
| 「他们显然想合并」 | 整合是你搭档的决定。呈现菜单，然后等待。 |
| 「他们看起来已经做完这个功能了——我主动提议丢弃吧」 | 菜单照写好的样子就是完整的。只有你搭档明确说出要丢弃时，才做丢弃。 |
| 「『行，删掉吧』算确认」 | 只有亲手输入的 `discard` 一词才授权删除。 |
| 「PR 已经开出来了，工作树现在就是累赘」 | PR 的反馈要在那个工作树里修。它要一直留到工作落地。 |
| 「这个别的工作树看起来过期了——我顺手也清掉」 | 只清理 `.worktrees/` 或 `worktrees/` 下的工作树。其他都归宿主环境管。 |
| 「移除被拒绝了——`--force` 只是把清理做完」 | 被拒绝意味着有文件只存在于那个工作树里。`--force` 会把它们永久销毁。给你的搭档看，然后询问。 |
| 「合并后的失败大概是偶发」 | 合并结果失败就停下一切。分支和工作树保持不动，直到你排查清楚。 |
| 「基础分支显然是 main」 | 确认分叉点，或者直接问。合错基础分支，撤销起来很贵。 |
| 「推送被拒绝了——强制推送就能解决」 | 推送被拒绝意味着远端已经变了。先排查；只有你搭档明确要求时才强制推送。 |
