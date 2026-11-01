---
name: verification-before-completion
description: "在即将声称工作已完成、已修复或已通过时，在提交或创建 PR 之前使用——要求在做出任何成功声明之前运行验证命令并确认输出；永远先证据后断言"
---

# 完成前验证

## 概览

**核心原则：** 永远先证据后断言。

**违反这条规则的字面要求，就是违反这条规则的精神。**

## 铁律

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

如果你没有在本次消息中运行过验证命令，你就不能声称它通过了。

## 门禁函数

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## 常见失败

| 声明 | 需要 | 还不够 |
|-------|----------|----------------|
| 测试通过 | 测试命令输出：0 失败 | 之前的运行、「应该能过」 |
| Linter 干净 | Linter 输出：0 错误 | 部分检查、外推 |
| 构建成功 | 构建命令：退出码 0 | Linter 通过、日志看起来不错 |
| Bug 已修复 | 测试原始症状：通过 | 改了代码、假定已修复 |
| 回归测试有效 | 已验证红-绿循环 | 测试只通过一次 |
| 代理已完成 | VCS diff 显示改动 | 代理报告「成功」 |
| 需求已满足 | 逐行检查清单 | 测试通过 |

## 危险信号 —— 停下来

- 使用「should」「probably」「seems to」这类词
- 在验证之前就表达满意（「太好了！」「完美！」「完成了！」等）
- 未经验证就要提交/推送/创建 PR
- 相信代理的成功报告
- 依赖部分验证
- 想着「就这一次」
- 累了，想让工作赶紧结束
- **任何在未运行验证的情况下暗示成功的措辞**

## 防止自我合理化

| 借口 | 现实 |
|--------|---------|
| 「现在应该能跑了」 | 去运行验证 |
| 「我有信心」 | 信心 ≠ 证据 |
| 「就这一次」 | 没有例外 |
| 「Linter 通过了」 | Linter ≠ 编译器 |
| 「代理说成功了」 | 独立验证 |
| 「我累了」 | 疲惫 ≠ 借口 |
| 「部分检查就够了」 | 部分证明不了什么 |
| 「换个说法，规则就不适用了」 | 精神重于字面 |

## 关键模式

**测试：**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**回归测试（TDD 红-绿）：**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**构建：**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**需求：**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**代理分派：**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## 何时适用

**始终在以下情况之前：**
- 任何成功/完成声明的变体
- 任何表达满意的说法
- 任何关于工作状态的正面陈述
- 提交、创建 PR、完成任务
- 进入下一个任务
- 分派任务给代理

**规则适用于：**
- 确切的措辞
- 转述与同义词
- 暗示成功
- 任何暗示完成/正确的沟通
