---
name: requesting-code-review
description: "在完成任务、实现重大功能之后，或在合并之前，用来验证工作是否满足需求时使用"
---

# 请求代码评审

分派一个代码评审者子代理，在问题级联之前抓住它们。评审者拿到的是精心准备的上下文，用于评估——绝不是你这个会话的历史记录。

**核心原则：** 尽早评审，经常评审。

## 何时请求评审

**强制：**
- 子代理驱动开发中每个任务完成后
- 完成重大功能后
- 合并到 main 之前

**可选但值得：**
- 卡住的时候（换个新鲜视角）
- 重构之前（基线检查）
- 修复复杂 bug 之后

## 如何请求

**1. 获取 git 的 SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or: git merge-base origin/main HEAD
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 分派代码评审者子代理：**

分派一个 `general-purpose` 子代理，填写 [code-reviewer.md](code-reviewer.md) 中的模板

**占位符：**
- `{DESCRIPTION}` —— 你构建了什么的简要概述
- `{PLAN_OR_REQUIREMENTS}` —— 它应该做什么
- `{BASE_SHA}` —— 起始提交
- `{HEAD_SHA}` —— 结束提交

**3. 根据反馈行动：**
- 立刻修复 Critical 问题
- 在继续之前修复 Important 问题
- 记录 Minor 问题，留待以后
- 如果评审者错了，就反驳（并给出理由）

## 示例

```
[Just completed Task 2: Add verification function]（刚完成任务 2：添加验证函数）

你：先请求代码评审，再继续。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | cut -d' ' -f1)
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]（分派代码评审者子代理）
  DESCRIPTION：新增 verifyIndex() 和 repairIndex()，覆盖 4 类问题
  PLAN_OR_REQUIREMENTS：来自 docs/superpowers/plans/deployment-plan.md 的任务 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]（子代理返回如下）：
  Strengths：架构干净，测试真实
  Issues：
    Important：缺少进度提示
    Minor：上报间隔用了魔法数字（100）
  Assessment：可以继续

你：[Fix progress indicators]（修复进度提示）
[Continue to Task 3]（继续任务 3）
```

## 常见的自我合理化

| 借口 | 现实 |
|--------|---------|
| 「我干脆自己看 diff，不分派评审者」 | 你是协调者——自己就地看 diff 会烧掉你继续推进工作所需的上下文窗口。分派一个评审者子代理：diff 和评估都留在它的上下文里，只有发现回传给你。 |
| 「评审者需要我的整个会话历史才能理解这个改动」 | 交给它精心准备的上下文，绝不是你会话的历史记录。这样评审者盯住的是工作产物，而不是你的思路过程。 |

## 危险信号

**绝不：**
- 因为「这很简单」就跳过评审
- 忽视 Critical 问题
- 带着未修复的 Important 问题继续推进
- 与有效的技术反馈争论

**如果评审者错了：**
- 用技术理由反驳
- 展示能证明它有效的代码/测试
- 请求澄清

见模板：[code-reviewer.md](code-reviewer.md)
