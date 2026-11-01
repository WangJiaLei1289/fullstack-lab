# 从已有的进度账本恢复

属于 superpowers:subagent-driven-development 技能的一部分。本计划的工作区里已经有进度账本，位于 `<workspace>/progress.md`。

如果账本第一行写的计划文件就是你这份，那么带有 `Task <N>:
complete` 行的任务都已完成——不要重新分派它们；从第一个没有该行的任务继续。若某个任务最后一行是修复轮次，说明它停在循环中间：
从下一轮继续该循环。若账本第一行写的是另一个计划文件——或者在旧的扁平路径
`.superpowers/sdd/progress.md` ——是别的计划的进度：原样留在那里，自己从零开始一个新的。
