---
name: using-git-worktrees
description: "在开始需要与当前工作区隔离的功能开发时，或在执行实现计划之前使用——确保通过原生工具或 git 工作树兜底创建出隔离的工作区"
---

# 使用 Git 工作树

## 概览

确保工作在隔离的工作区里进行。优先使用你所在平台原生的工作树（worktree）工具。只有在没有原生工具可用时，才退回到手工 git 工作树。

**核心原则：** 先检测已有的隔离。然后使用原生工具。最后退回 git。绝不要跟宿主环境对着干。

**开始时宣告：**「I'm using the using-git-worktrees skill to set up an isolated workspace.」（我正在使用 using-git-worktrees 技能来搭建隔离的工作区。）

## 第 0 步：检测已有的隔离

**在创建任何东西之前，先检查你是否已经身处隔离的工作区。**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**子模块防护：** `GIT_DIR != GIT_COMMON` 在 git 子模块内部同样成立。在得出「已经在工作树里」的结论之前，先确认你不在子模块里：

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**如果 `GIT_DIR != GIT_COMMON`（且不是子模块）：** 你已经在一个链接的工作树里。跳到第 2 步（项目初始化）。不要再创建另一个工作树。

报告并说明分支状态：
- 在分支上：「Already in isolated workspace at `<path>` on branch `<name>`.」
- 分离 HEAD：「Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time.」

**如果 `GIT_DIR == GIT_COMMON`（或身处子模块）：** 你处于一个普通的仓库检出。

用户是否已在你的指令中表明过工作树偏好？如果没有，在创建工作树之前先征求同意：

> 「需要我搭建一个隔离的工作树吗？它能保护你当前的分支不被改动。」

如果已有明确声明的偏好，就照做，不要问。如果用户拒绝同意，就原地工作，跳到第 2 步。

## 第 1 步：创建隔离的工作区

**你有两种机制。按这个顺序尝试。**

### 1a. 原生工作树工具（首选）

用户已经要求隔离的工作区（第 0 步的同意）。你是否已经有创建工作树的方式？它可能是名为 `EnterWorktree`、`WorktreeCreate` 的工具，一个 `/worktree` 命令，或一个 `--worktree` 开关。如果有，就用它，跳到第 2 步。

原生工具会自动处理目录位置、分支创建与清理。在有原生工具的情况下使用 `git worktree add`，会制造出你的宿主环境看不见也管不了的幻影状态。

只有在没有原生工作树工具可用时，才继续到第 1b 步。

### 1b. Git 工作树兜底

**仅在第 1a 步不适用时使用**——你没有可用的原生工作树工具。用 git 手工创建工作树。

#### 目录选择

按这个优先级顺序。用户明确表达的偏好永远优先于观察到的文件系统状态。

1. **检查你的指令中是否声明了工作树目录偏好。** 如果用户已经指定，就用它，不要问。

2. **检查是否已有项目本地的工作树目录：**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   如果找到了，就用它。如果两者都存在，`.worktrees` 胜出。

3. **如果没有其他指引可用**，默认使用项目根目录下的 `.worktrees/`。

#### 安全检查（仅限项目本地目录）

**在创建工作树之前必须验证目录已被忽略：**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果没有被忽略：** 加到 .gitignore，提交这次改动，然后再继续。

**为什么关键：** 防止不小心把工作树的内容提交进仓库。

#### 创建工作树

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**沙箱兜底：** 如果 `git worktree add` 因权限错误失败（沙箱拒绝），告诉用户沙箱阻止了工作树创建，你改为在当前目录工作。然后原地运行初始化和基线测试。

## 第 2 步：项目初始化

自动检测并运行相应的初始化：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 第 3 步：验证干净的基线

运行测试，确保工作区从干净状态开始：

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：** 报告失败，询问是继续还是调查。

**如果测试通过：** 报告就绪。

### 报告

```
工作树已就绪：<full-path>
测试通过（<N> 个测试，0 失败）
可以开始实现 <feature-name> 了
```

## 快速参考

| 情况 | 动作 |
|-----------|--------|
| 已经在链接的工作树里 | 跳过创建（第 0 步） |
| 身处子模块 | 按普通仓库处理（第 0 步防护） |
| 有原生工作树工具 | 使用它（第 1a 步） |
| 没有原生工具 | git 工作树兜底（第 1b 步） |
| `.worktrees/` 存在 | 使用它（验证已被忽略） |
| `worktrees/` 存在 | 使用它（验证已被忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 两者都不存在 | 检查指令文件，然后默认 `.worktrees/` |
| 目录未被忽略 | 加到 .gitignore + 提交 |
| 创建时权限错误 | 沙箱兜底，原地工作 |
| 基线测试失败 | 报告失败 + 询问 |
| 没有 package.json/Cargo.toml | 跳过依赖安装 |

## 常见的自我合理化

| 借口 | 现实 |
|--------|---------|
| 「我显然不在工作树里——不用检查」 | 跑第 0 步。宿主环境创建的隔离和子模块都能骗过肉眼；检测命令才能定论。 |
| 「`git worktree add` 比找原生工具快」 | 原生工具（例如 `EnterWorktree`）管着位置、分支和清理。绕过它就是头号错误——它会制造出你的宿主环境看不见也管不了的幻影状态。 |
| 「工作树目录肯定已经被忽略了」 | 跑 `git check-ignore`。未被忽略的工作树目录会把整棵树提交进仓库。 |
| 「随便什么目录名都行」 | 明确的指令优先于已有的项目本地目录，后者又优先于 `.worktrees/` 默认值。 |
| 「工作区是新的——基线测试可以等等」 | 脏的基线会让之后每一次失败都变得有歧义。现在就跑测试；是否带着失败继续推进，要由你的搭档来决定。 |
