#!/usr/bin/env node
/**
 * Regenerate the project-root README.md skill index from .dsh/skills/&lt;name&gt;/SKILL.md.
 *
 *   node .dsh/generate-skills-readme.js
 *
 * Descriptions come from each skill's own frontmatter, so the index cannot drift
 * from what DSH actually shows the model. Usage:
 *   node .dsh/generate-skills-readme.js     (writes README.md at repo root)
 */
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..');
const DEST = path.join(REPO, '.dsh', 'skills');
const DOCS = path.join(REPO, 'docs');

const PM_PLUGINS = [
  ['pm-product-discovery', '产品发现', '构思、实验、假设验证、优先级排序、访谈综合'],
  ['pm-product-strategy', '产品战略', '愿景、战略/精益/商业模式画布、SWOT、PESTLE、安索夫、波特五力、变现'],
  ['pm-execution', '执行', 'PRD、OKR、路线图、冲刺、事前验尸、利益相关方、用户故事、红队评审'],
  ['pm-market-research', '市场研究', '用户画像、用户细分、情感分析、竞品分析、市场规模测算'],
  ['pm-data-analytics', '数据分析', 'SQL 查询生成、同期群与留存分析、A/B 实验解读'],
  ['pm-go-to-market', '上市', 'GTM 战略、增长循环、GTM 打法、滩头细分、ICP'],
  ['pm-marketing-growth', '营销增长', '营销创意、价值主张陈述、北极星指标、命名、定位'],
  ['pm-toolkit', '工具箱', '简历评审、NDA 起草、隐私政策、语法与行文检查'],
  ['pm-ai-shipping', 'AI 交付', '为 vibe-coded 应用写文档、测试覆盖映射、安全/性能审计、交付包汇编'],
];

// Minimal frontmatter reader: the skill sets use only top-level keys plus folded
// scalars (`description: >`), which is all this index needs to resolve.
function frontmatter(file) {
  const raw = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return {};
  const data = {};
  const lines = m[1].split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (!kv) continue;
    const [, key, rest] = kv;
    if (rest === '>' || rest === '|' || /^[>|][-+]?$/.test(rest)) {
      const buf = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || lines[i + 1].trim() === '')) {
        buf.push(lines[++i].trim());
      }
      data[key] = buf.join(rest.startsWith('|') ? '\n' : ' ').replace(/\s+/g, ' ').trim();
      continue;
    }
    data[key] = rest.replace(/^["']|["']$/g, '').trim();
  }
  return data;
}

function shortDescription(text, max = 165) {
  let flat = String(text).replace(/\s+/g, ' ').trim();
  // srs descriptions open with a phase label that the table already carries separately
  flat = flat.replace(/^Phase \d+ of the SRS workflow\.\s*/i, '');
  const sentence = flat.match(/^(.{10,}?[.!?])(?:\s|$)/);
  let out = sentence ? sentence[1] : flat;
  if (out.length > max) {
    const cut = out.slice(0, max);
    const space = cut.lastIndexOf(' ');
    out = (space > 60 ? cut.slice(0, space) : cut).replace(/[,;:\s]+$/, '') + '…';
  }
  return out.replace(/\|/g, '\\|');
}

// plugin membership comes from the vendored source layout
const pmOf = new Map();
const pmRoot = path.join(DOCS, 'pm-skills-2.2.0');
for (const plugin of fs.readdirSync(pmRoot)) {
  const skillsDir = path.join(pmRoot, plugin, 'skills');
  if (!/^pm-/.test(plugin) || !fs.existsSync(skillsDir)) continue;
  for (const name of fs.readdirSync(skillsDir)) pmOf.set(name, plugin);
}
const superpowers = new Set(fs.readdirSync(path.join(DOCS, 'superpowers-7.0.1', 'skills')));
const srs = new Set(fs.readdirSync(path.join(DOCS, 'srs-skills', 'skills')));

const skills = [];
for (const name of fs.readdirSync(DEST).sort()) {
  const dir = path.join(DEST, name);
  if (!fs.statSync(dir).isDirectory()) continue;
  const fm = frontmatter(path.join(dir, 'SKILL.md'));
  const family = pmOf.has(name) ? 'pm' : superpowers.has(name) ? 'superpowers' : srs.has(name) ? 'srs' : 'other';
  skills.push({
    name,
    family,
    plugin: pmOf.get(name),
    description: fm.description,
    userInvocable: fm['user-invocable'],
    modelInvocable: fm['disable-model-invocation'] === true ? false : undefined,
    hasWhenToUse: fm.whenToUse !== undefined,
  });
}

const rows = (list) => list.map(s => `| \`${s.name}\` | ${shortDescription(s.description)} |`).join('\n');
const table = (list) => ['| 技能 | 用途 |', '|---|---|', rows(list)].join('\n');

const out = [];
out.push('# fullstack-lab');
out.push('');
out.push('全栈代码开发空间。本项目在 `.dsh/skills/` 下内置了 **93 个项目级 agent skill**，覆盖产品管理、软件开发方法论、需求规格三条线。');
out.push('');
out.push('## 目录');
out.push('');
out.push('- [这是什么](#这是什么)');
out.push('- [技能怎么被加载](#技能怎么被加载)');
out.push('- [一、PM Skills（69 个）](#一pm-skills69-个)');
out.push('- [二、Superpowers（15 个）](#二superpowers15-个)');
out.push('- [三、srs-skills（9 个）](#三srs-skills9-个)');
out.push('- [怎么用](#怎么用)');
out.push('- [场景速查](#场景速查)');
out.push('- [维护](#维护)');
out.push('');
out.push('## 这是什么');
out.push('');
out.push('技能（skill）是一段按需加载的任务指令：模型平时只看到「名字 + 一句话用途」，遇到匹配的任务时才加载完整正文，因此不会一次性占满上下文。本仓库把三套上游技能包（英文原版）拷进项目，做成项目级技能，本项目的每个会话都会自动获得这 93 个技能，无需再安装。');
out.push('');
out.push('| 来源 | 上游 | 数量 | 定位 |');
out.push('|---|---|---|---|');
out.push('| PM Skills 2.2.0 | `phuryn/pm-skills`（9 个插件） | 69 | 产品经理工作流：发现 → 战略 → 执行 → 上市 → 增长 → AI 交付 |');
out.push('| Superpowers 7.0.1 | `obra/superpowers` | 15 | 编码 agent 的开发方法论：头脑风暴、写计划、TDD、系统化调试、并行子代理、代码评审 |');
out.push('| srs-skills | 上游 README 为越南语、附英文版 | 9 | 从一句想法生成完整软件需求规格说明书（SRS）的九阶段流水线 |');
out.push('');
out.push('原始副本（含中文翻译版、README、CHANGELOG、测试等完整仓库内容）保留在 `docs/` 下，`.dsh/skills/` 里是可用于加载的精简副本。');
out.push('');
out.push('## 技能怎么被加载');
out.push('');
out.push('DSH 的项目级技能根目录是 `<项目根>/.dsh/skills/<name>/SKILL.md`（项目根 = 最近一个含 `.git` 的祖先目录）：');
out.push('');
out.push('- **只扫一层**：`<name>/SKILL.md`。嵌套的 `**/SKILL.md` 不会被发现，所以三套技能都已扁平化到 `.dsh/skills/` 下。');
out.push('- **frontmatter 必填** `name` + `description`，且 `name` 必须是 kebab-case；不合法的技能会被静默跳过。');
out.push('- 目录被监听，增删改技能会自动刷新下一个会话步骤的技能目录，**改完不需要重启**。');
out.push('- 优先级：`.dsh/skills`（项目）> `.agents/skills` > 自定义目录 > `~/.dsh/skills`（用户）；同名时项目级胜出。');
out.push('');

out.push('## 一、PM Skills（69 个）');
out.push('');
out.push('按上游的 9 个插件分组。技能是「名词/概念」，由模型按话题自动加载；上游同名的 42 条命令（`/write-prd` 等）未导入。');
out.push('');
for (const [plugin, label, focus] of PM_PLUGINS) {
  const list = skills.filter(s => s.plugin === plugin);
  out.push(`### ${label} · \`${plugin}\`（${list.length} 个）`);
  out.push('');
  out.push(`覆盖：${focus}。`);
  out.push('');
  out.push(table(list));
  out.push('');
}

out.push('## 二、Superpowers（15 个）');
out.push('');
out.push('一套相互引用的开发方法论。典型路径：`brainstorming` → `writing-plans` → `executing-plans` 或 `subagent-driven-development` → `verification-before-completion` → `requesting-code-review` / `finishing-a-development-branch`；出问题走 `systematic-debugging`，写/改技能走 `writing-skills`。技能之间的 `../<相邻技能>/...` 相对引用在扁平布局下依然有效。');
out.push('');
out.push(table(skills.filter(s => s.family === 'superpowers')));
out.push('');

out.push('## 三、srs-skills（9 个）');
out.push('');
out.push('九阶段 SRS 流水线，串起来用可直接走完整流程：');
out.push('');
out.push('```text');
out.push('sr-brainstorm → sr-spec → sr-plan → (人工评审) → sr-generate → sr-validate → sr-improve → sr-save');
out.push('                        └────────────── srs-workflow 一次编排全程 ──────────────┘');
out.push('已有原始需求、跳过头脑风暴时：srs-generator');
out.push('```');
out.push('');
out.push('| 技能 | 阶段 | 用途 |');
out.push('|---|---|---|');
const stageOf = (d) => {
  const m = String(d).match(/Phase (\d+)/);
  return m ? `第 ${m[1]} 阶段` : '入口';
};
for (const s of skills.filter(x => x.family === 'srs')) {
  out.push(`| \`${s.name}\` | ${stageOf(s.description)} | ${shortDescription(s.description)} |`);
}
out.push('');
out.push('> 上游这几个技能的 frontmatter 写的是 `name: sr:brainstorm`、`cl:srs` 这类带冒号的别名，DSH 不接受，导入时已统一改成 kebab-case（正文里的 `/sr:spec` 等调用提示同步改成 `/sr-spec`），跨 bundle 的 `skills/<bundle>/references/...` 路径改成 `../<bundle>/references/...`。');
out.push('');

out.push('## 怎么用');
out.push('');
out.push('模型侧：技能会以「名字 + 一句话用途」出现在会话的技能目录里，模型判断任务匹配后调用 `skill` 工具加载完整正文——不需要你手动指定。');
out.push('');
out.push('用户侧：所有技能都允许直接以 `/名字` 触发，例如：');
out.push('');
out.push('```text');
out.push('/brainstorming        任何创造性工作开工前的需求澄清');
out.push('/writing-plans        有了需求，先写实施计划再动代码');
out.push('/test-driven-development   实现任何功能或修 bug 之前');
out.push('/systematic-debugging 遇到 bug / 测试失败 / 异常行为');
out.push('/create-prd           写 PRD');
out.push('/pre-mortem           上线前做风险预演');
out.push('/srs-workflow         从一个项目想法生成完整 SRS');
out.push('/code-review          审查改动、找 bug');
out.push('```');
out.push('');
out.push('也可以直接用自然语言描述任务，让模型自己挑技能，例如「帮我把这份需求整理成 PRD」「这个 bug 查一下根因再修」。');
out.push('');
out.push('### 场景速查');
out.push('');
out.push('| 你要做的事 | 对应技能 |');
out.push('|---|---|');
out.push('| 有新想法 / 要加新功能，先想清楚要什么 | `brainstorming` |');
out.push('| 把需求写成 PRD | `create-prd` |');
out.push('| 给一堆需求排优先级 | `prioritize-features`、`prioritization-frameworks` |');
out.push('| 上线前压测计划/策略的风险 | `pre-mortem`、`strategy-red-team` |');
out.push('| 竞品分析、市场测算、用户画像 | `competitor-analysis`、`market-sizing`、`user-personas` |');
out.push('| 定价 / 变现模式 | `pricing-strategy`、`monetization-strategy` |');
out.push('| 准备并整理客户访谈 | `interview-script`、`summarize-interview` |');
out.push('| 动手写代码前先出实施方案 | `writing-plans` |');
out.push('| 实现功能 / 修 bug（先写测试） | `test-driven-development` |');
out.push('| 排查 bug 根因 | `systematic-debugging` |');
out.push('| 审查改动、找缺陷 | `requesting-code-review`、`code-review` |');
out.push('| 声称"做完了"之前自检 | `verification-before-completion` |');
out.push('| 把任务并行拆出去 | `dispatching-parallel-agents`、`subagent-driven-development` |');
out.push('| 生成软件需求规格说明书 | `srs-workflow`（全流程）、`srs-generator`（已有需求） |');
out.push('| A/B 实验、留存、写 SQL | `ab-test-analysis`、`cohort-analysis`、`sql-queries` |');
out.push('| 简历 / NDA / 隐私政策 / 校对 | `review-resume`、`draft-nda`、`privacy-policy`、`grammar-check` |');
out.push('| 给项目新增或改造技能 | `writing-skills` |');
out.push('');

out.push('## 维护');
out.push('');
out.push('```powershell');
out.push('# 重新导入 / 刷新技能（幂等，先删后拷）');
out.push('node .dsh/import-skills.js');
out.push('');
out.push('# 技能索引：本 README 由技能 frontmatter 生成，导入变化后重跑');
out.push('node .dsh/generate-skills-readme.js');
out.push('');
out.push('# 核对数量');
out.push('(Get-ChildItem .dsh/skills -Directory).Count   # 93');
out.push('');
out.push('# 卸载某一套（按前缀）');
out.push('Remove-Item .dsh/skills/sr-*,.dsh/skills/srs-* -Recurse -Force');
out.push('```');
out.push('');
out.push('注意事项：');
out.push('');
out.push('- **上下文成本**：93 条描述会进入每轮会话的技能目录（每条上限 500 字符）。如果觉得重，删掉不常用的技能目录即可，`docs/` 里有原始副本随时可恢复。');
out.push('- **中文版**：`docs/` 下另有 `pm-skills-2.2.0-zh`、`superpowers-7.0.1-zh`、`superpowers-7.0.1-zh-full`、`srs-skills-zh`。它们与英文版技能名完全重名，不能同时导入；要换语言，把 `import-skills.js` 里的来源目录换成 `-zh` 版本（superpowers 用 `-zh-full`），删掉 `.dsh/skills` 后重跑。');
out.push('- **上游内容未被修改**：`docs/` 是原样保留的仓库副本；只有 `.dsh/skills/` 里的副本做过名称与路径规范化（详见 `.dsh/README.md`）。');
out.push('- **上游贡献规则**：`docs/` 内各仓库自带 `AGENTS.md` / `CLAUDE.md`，其中 superpowers 对 agent 提交 PR 有严格限制，如果要在这些上游仓库里改东西，先读那一份。');
out.push('');

fs.writeFileSync(path.join(REPO, 'README.md'), out.join('\n'));
console.log(`README.md written: ${skills.length} skills (${skills.filter(s => s.family === 'pm').length} pm, ${skills.filter(s => s.family === 'superpowers').length} superpowers, ${skills.filter(s => s.family === 'srs').length} srs)`);
