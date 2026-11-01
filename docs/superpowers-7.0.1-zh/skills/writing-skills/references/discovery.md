# 为「被发现」而写 SKILL.md

属于 superpowers:writing-skills：SKILL.md 模板，以及如何为技能命名、写描述、控制篇幅，让代理能找到并阅读它。

## SKILL.md 的结构

**Frontmatter（YAML）：**
- 两个必填字段：`name` 和 `description`（全部支持的字段见 [agentskills.io/specification](https://agentskills.io/specification)）
- 总长度最多 1024 个字符
- `name`：只能用字母、数字和连字符（不能有括号、特殊字符）
- `description`：第三人称，只描述「何时使用」（不是「它做什么」）
  - 以「Use when...」开头，聚焦触发条件
  - 包含具体的症状、场景和上下文
  - **绝不概括技能的过程或工作流程**（原因见下文「技能发现优化」）
  - 尽量控制在 500 个字符以内

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision non-obvious]

Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)
Before/after code comparison

## Quick Reference
Table or bullets for scanning common operations

## Implementation
Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes
What goes wrong + fixes

## Real-World Impact (optional)
Concrete results
```

## 技能发现优化（SDO）

**这对「被发现」至关重要：**未来的代理需要**找到**你的技能

### 1. 信息丰富的 description 字段

**目的：**你的代理会读 description，来决定某个任务该加载哪些技能。要让它能回答：「我现在应该读这个技能吗？」

**格式：**以「Use when...」开头，聚焦触发条件

**关键：description = 何时使用，而不是技能做什么**

description 只应该描述触发条件。**不要**在 description 里概括技能的过程或工作流程。

**为什么这点重要：**测试发现，当 description 概括了技能的工作流程时，代理可能会照着 description 行事，而不去读完整的技能内容。一句写着「任务之间做代码评审」的 description，让一个代理只做了**一次**评审——尽管技能的流程图清楚地显示了**两次**评审（先检查是否符合规格，再检查代码质量）。

当 description 改成「Use when executing implementation plans with independent tasks」（不概括工作流程）之后，代理正确地读了流程图，并遵循了分两阶段的评审流程。

**陷阱：**概括工作流程的 description 会给代理造出一条捷径。技能正文就成了代理跳过的文档。

```yaml
# ❌ BAD: Summarizes workflow - agents may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ❌ BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks in the current session

# ✅ GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

**内容：**
- 使用具体的触发条件、症状和场景，表明这个技能适用
- 描述**问题**（竞态条件、行为不一致），而不是**特定语言的症状**（setTimeout、sleep）
- 除非技能本身就是特定技术的，否则触发词应保持技术无关
- 如果技能是特定技术的，就在触发条件里写明这一点
- 用第三人称写（它会被注入系统提示词）
- **绝不概括技能的过程或工作流程**

```yaml
# ❌ BAD: Too abstract, vague, doesn't include when to use
description: For async testing

# ❌ BAD: First person
description: I can help you with async tests when they're flaky

# ❌ BAD: Mentions technology but skill isn't specific to it
description: Use when tests use setTimeout/sleep and are flaky

# ✅ GOOD: Starts with "Use when", describes problem, no workflow
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently

# ✅ GOOD: Technology-specific skill with explicit trigger
description: Use when using React Router and handling authentication redirects
```

### 2. 关键词覆盖

使用代理会去搜索的词：
- 错误信息：「Hook timed out」「ENOTEMPTY」「race condition」
- 症状：「flaky」「hanging」「zombie」「pollution」
- 同义词：「timeout/hang/freeze」「cleanup/teardown/afterEach」
- 工具：实际命令、库名、文件类型

### 3. 描述性命名

**用主动语态，动词开头：**
- ✅ `creating-skills` 而不是 `skill-creation`
- ✅ `condition-based-waiting` 而不是 `async-test-helpers`

### 4. Token 效率（关键）

**问题：**入门类技能和高频引用的技能会被加载进**每一次**对话。每个 token 都算数。

**目标词数：**
- 入门工作流：每个 <150 词
- 高频加载的技能：总共 <200 词
- 其他技能：<500 词（仍然要保持简洁）

**技巧：**

**把细节挪到工具的 help 里：**
```bash
# ❌ BAD: Document all flags in SKILL.md
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: Reference --help
search-conversations supports multiple modes and filters. Run --help for details.
```

**使用交叉引用：**
```markdown
# ❌ BAD: Repeat workflow details
When searching, dispatch subagent with template...
[20 lines of repeated instructions]

# ✅ GOOD: Reference other skill
Always use subagents (50-100x context savings). REQUIRED: Use [other-skill-name] for workflow.
```

**压缩示例：**
```markdown
# ❌ BAD: Verbose example (42 words)
your human partner: "How did we handle authentication errors in React Router before?"
You: I'll search past conversations for React Router authentication patterns.
[Dispatch subagent with search query: "React Router authentication error handling 401"]

# ✅ GOOD: Minimal example (20 words)
Partner: "How did we handle auth errors in React Router?"
You: Searching...
[Dispatch subagent → synthesis]
```

**消除冗余：**
- 不要重复交叉引用技能里已经有的内容
- 不要解释从命令本身就能明显看出的东西
- 不要包含同一模式的多个示例

**验证：**
```bash
wc -w skills/path/SKILL.md
# getting-started workflows: aim for <150 each
# Other frequently-loaded: aim for <200 total
```

**按你「做什么」或核心洞察来命名：**
- ✅ `condition-based-waiting` > `async-test-helpers`
- ✅ `using-skills` 而不是 `skill-usage`
- ✅ `flatten-with-flags` > `data-structure-refactoring`
- ✅ `root-cause-tracing` > `debugging-techniques`

**动名词（-ing）很适合表示流程：**
- `creating-skills`、`testing-skills`、`debugging-with-logs`
- 主动，描述你正在做的动作

### 5. 交叉引用其他技能

**当你写引用其他技能的文档时：**

只写技能名，并加上明确的要求标记：
- ✅ 好：`**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`
- ✅ 好：`**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging`
- ❌ 差：`See skills/testing/test-driven-development`（不确定是不是必需）
- ❌ 差：`@skills/testing/test-driven-development/SKILL.md`（强制加载，烧上下文）

**为什么不用 @ 链接：**`@` 语法会立即强制加载文件，在你真正需要之前就消耗 200k+ 上下文。
