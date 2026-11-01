# 最终评审与收尾

属于 superpowers:subagent-driven-development 技能的一部分。计划里的每个任务都已完成。

最终覆盖整个分支的评审也要拿到一个包：运行 `bash scripts/review-package PLAN_FILE MERGE_BASE HEAD`（MERGE_BASE = 分支起步时的那个提交，例如 `git merge-base main HEAD`），并在最终评审的分派里附上它打印出的路径，这样最终评审者只需读一个文件，而不必用 git 命令重新推导分支 diff。用可用的最强模型来分派（见 SKILL.md 的模型选择），并使用 superpowers:requesting-code-review 的
[code-reviewer.md](../../requesting-code-review/code-reviewer.md)。把它指向账本里的「延后次要项」与「搁置」行，好让它甄别哪些必须在合并前修掉。

如果最终的分支级评审返回了发现项，就分派**一个**修复子代理，把完整的发现项清单交给它——而不是每个发现项一个修复者。逐发现项的修复者各自重建上下文、各自重跑测试套件；真实会话里最终评审的修复波次，比它所有任务加起来还贵。然后对这次修复波次只做一次定范围的复审（对修复区间运行 `bash scripts/review-package PLAN_FILE FIX_BASE HEAD`，使用
[re-review-prompt.md](../re-review-prompt.md)）。
对残余发现项的裁定，按修复循环里「断路器」的做法处理
（references/fix-loop.md）：连同裁定一起搁置，或对承重的那些做出裁定并把你的决定记入账本。只有那四件会中止运行中计划的事（见 SKILL.md 开头）才会在这里中止你。没有第二波修复——残余的承重发现项会在 finishing-a-development-branch 呈现选项时浮到你的搭档面前。

### 收尾

在删除任何东西之前，把账本里每一行包含 `Ruling:` 的内容——预检裁定、搁置的发现项、断路器裁定，全部——按你做决定的顺序收进最终消息里的「我做过的裁定」一节，每条都写明如果错了要付出什么代价。这份清单是穷尽的：账本里有一条裁定，清单里就要有它。这份清单是你的搭档得知你替他们做下那些决定的唯一途径——他们读它，然后返工你搞错的部分。一条随工作区一起消失的裁定，就是一桩秘密做出的决定。

当最终的分支级评审干净、且它的修复已合并后，删除本计划的工作区（`rm -rf <workspace>`）——现在，git 历史就是记录。同级目录属于别的计划；不要动它们。

使用 superpowers:finishing-a-development-branch。
