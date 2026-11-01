# 让技能抵御自我合理化

属于 superpowers:writing-skills 的一部分。当基线失败属于纪律性失败时使用：
代理明明知道规则，却在压力下跳过它。

## 让技能抵御自我合理化

强制纪律的技能（如 TDD）必须能抵御自我合理化。代理很聪明，在压力下一定会去找漏洞。

**范围：** 这套工具针对的是纪律性失败——代理知道规则，却在压力下跳过它。对于产出形态不对或漏掉要素的情况，基于禁止的做法反而会适得其反；请改用「让表达形式匹配失败类型」一节里给出的那些形式。

**心理学备注：** 理解说服技巧为什么有效，能帮你系统地运用它们。研究基础见本目录下的 persuasion-principles.md（Cialdini, 2021; Meincke et al., 2025），涉及权威、承诺、稀缺、社会认同与统一性原则。

### 把每个漏洞都明确堵死

不要只陈述规则——要禁止具体的变通做法：

<Bad>
```markdown
Write code before test? Delete it.
```
</Bad>

<Good>
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```
</Good>

### 回应「精神 vs 字面」的争论

把根本性原则早早放进去：

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

这能一次性切断「我是在遵循精神」这一整类自我合理化。

### 建立自我合理化对照表

从基线测试中收集自我合理化（见下文「测试」一节）。代理提出的每一个借口都要进表：

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

### 建立危险信号清单

让代理在自我合理化时容易自查：

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

### 为违规症状更新 SDO

在 description 里补上：你即将违规时的症状：

```yaml
description: use when implementing any feature or bugfix, before writing implementation code
```
