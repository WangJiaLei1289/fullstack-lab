# pm-ai-shipping — AI 交付套件（AI Shipping Kit）

面向对 AI 生成的代码负责的产品经理和创始人。为 vibe-coded（用自然语言让 AI 直接写出代码）应用编写文档，评审其在正确性、安全和性能方面的缺陷，并产出一份可供评审者直接使用的交付包。

## 概览

AI agent 写代码很快，但不留下任何关于 *意图* 的记录——系统应该做什么、谁能做什么、密钥存放在哪里。没有这份记录，无论是人还是审计 agent 都无法判断代码是否可以安全发布。这套工具恢复了可评审性：先为系统建立文档，再审计文档所述与代码实际行为之间的差距——这正是通用扫描器会漏掉的一类 bug，因为它们没有意图模型。

完整流程请从 `/ship-check` 开始，也可以只用专家命令运行其中单个阶段。

文件夹和文件名都是默认值。这套工具优先沿用仓库自身的设置——它的 agent 指令、它的文档文件夹，以及它已有的文档和测试覆盖文件——只有在仓库没有时才回退到 `documentation/`、`documentation/tests.md` 和 `reports/`，并在输出中说明这一点。

两个静态审计都接受一个 git 范围（`<base>..<head>`，例如某次发布中尚未发布的提交）或 `changes`（未提交的工作区），然后只审计变更部分：变更的文件，以及变更新近触达或新近造成错误的地方。一次发布通常只审计其变更；首次发布或大规模重构之后，才审计整个仓库。

对于以手工维护文档和覆盖图来承载意图的仓库，`/document-app check` 和 `/derive-tests check` 是发布时使用的形式：它们不写任何文件，把每一处不一致连同两侧的 `file:line` 列出来，由负责人判断是代码错还是文档错，最后给出一行可被发布检查清单引用的总结。

## 安装

从 [pm-skills 插件市场](https://github.com/phuryn/pm-skills) 安装并启用 `pm-ai-shipping` 插件。每个命令都可以用 `/pm-ai-shipping:<command>` 或其简写 `/<command>` 触发；技能会在主题匹配时自动加载。

## Skills (3) 技能

- **shipping-artifacts** — 让 AI 构建的应用可被评审的那套持久文档：每个应用都需要的核心部分（架构、用户/权限流程、权限、变量/密钥、测试覆盖图），加上仅在适用时才补充的条件文档（邮件、cron、SEO、内嵌 agent/自动化）。它定义了每份文档必须承载什么，以及评审者如何使用它。
- **code-review** — 顶层评审技能。正确性是它的核心；**性能和安全是同一套引擎的可选子情形**。它以跨越边界的双方所达成的约定为立足点——那些逐文件看不出、因为单看每一侧都合理的缺陷——强制构造一次违反约定的执行，并在报告前逐一反驳候选项。
- **intended-vs-implemented** — 找出系统文档所述行为与代码实际行为之间差距的方法，两侧都给出引用证据，不要含糊其辞的发现。

## Commands (5) 命令

- `/pm-ai-shipping:ship-check` — 把一个 vibe-coded 仓库变成可供评审者直接使用的交付包：编写文档、接好 agent 上下文、运行正确性、安全和性能评审、增加一轮由第二个模型独立进行且不受引导的评审、映射测试覆盖，并汇总结果。
- `/pm-ai-shipping:document-app` — 逆向解析代码库，产出评审者和审计者需要的系统文档——核心文档集（架构、流程、权限、变量）加上适用时的条件文档（邮件、cron、SEO、自动化）。`/document-app check` 不写任何文件，只报告现有文档与代码不一致的地方。
- `/pm-ai-shipping:derive-tests` — 把文档化的意图转换为测试覆盖图：盘点当前已有的测试，将其与建议的测试和未经核实的空白区分开，为每个用例标记 unit / guarded-live / manual，并推荐一个遵循仓库既定门禁策略的门禁（仓库未说明时，使用合并前必须先通过的 CI 门禁）。`/derive-tests check` 不写任何文件，只报告覆盖图相对于文档和测试套件已过时的地方。
- `/pm-ai-shipping:security-audit-static` — 静态安全审计：梳理信任边界，交叉引用文档化的意图，自我反驳每一条发现，只报告有证据支撑的风险。`/security-audit-static <base>..<head>` 或 `changes` 只审计变更。
- `/pm-ai-shipping:performance-audit-static` — 静态性能审计：找出 N+1 查询和请求瀑布、过度获取、缺失索引以及缓存机会，按投入和影响排序。`/performance-audit-static <base>..<head>` 或 `changes` 只审计变更。

## 作者

Paweł Huryn — [The Product Compass 通讯](https://www.productcompass.pm)

## 许可证

MIT
