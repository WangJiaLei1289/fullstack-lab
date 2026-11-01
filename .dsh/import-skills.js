#!/usr/bin/env node
/**
 * Import the three vendored skill sets from docs/ into DSH project-level skills.
 *
 *   node .dsh/import-skills.js
 *
 * Sources (English originals):
 *   docs/pm-skills-2.2.0/{pm-*}/skills/<skill>/   69 skills
 *   docs/superpowers-7.0.1/skills/<skill>/        15 skills
 *   docs/srs-skills/skills/<skill>/                9 skills
 *
 * Destination: .dsh/skills/<skill>/  (DSH project root = nearest ancestor with .git;
 * the provider only scans one level: <root>/<name>/SKILL.md, name must be kebab-case).
 *
 * Normalizations applied to the copies (docs/ stays untouched):
 *   srs-skills: name/alias `sr:x` -> `sr-x`, `cl:srs-flow` -> `srs-workflow`,
 *               `cl:srs` -> `srs-generator`, and shared reference paths
 *               `skills/<bundle>/references/` -> `../<bundle>/references/` so the
 *               sibling-bundle layout keeps working.
 *   pm-skills:  `$ARGUMENTS` command placeholders -> natural-language input wording,
 *               `/pm-ai-shipping:code-review` -> `/code-review`.
 *   superpowers: unchanged (its `../<sibling-skill>/...` refs already resolve).
 */
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..');
const DOCS = path.join(REPO, 'docs');
const DEST = path.join(REPO, '.dsh', 'skills');
const SKILL_NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const SRS_RULES = [
  ['cl:srs-flow', 'srs-workflow'],
  ['cl:srs', 'srs-generator'],
  ['sr:brainstorm', 'sr-brainstorm'],
  ['sr:generate', 'sr-generate'],
  ['sr:improve', 'sr-improve'],
  ['sr:plan', 'sr-plan'],
  ['sr:save', 'sr-save'],
  ['sr:spec', 'sr-spec'],
  ['sr:validate', 'sr-validate'],
  ['skills/srs-workflow/references/', '../srs-workflow/references/'],
  ['skills/srs-generator/references/', '../srs-generator/references/'],
];

const PM_RULES = [
  ['Use $ARGUMENTS to pass:', 'Provide the following as input:'],
  ['**$ARGUMENTS**', "**the user's request**"],
  ['$ARGUMENTS', "the user's request"],
  ['pm-ai-shipping:code-review', 'code-review'],
];

const TEXT_EXT = new Set(['.md', '.txt', '.json', '.yaml', '.yml', '.py', '.sh', '.js', '.cjs', '.mjs']);

function collect() {
  const out = [];
  const add = (dir, family) => {
    if (!fs.existsSync(path.join(dir, 'SKILL.md'))) return;
    out.push({ dir, family });
  };

  const pmRoot = path.join(DOCS, 'pm-skills-2.2.0');
  for (const plugin of fs.readdirSync(pmRoot)) {
    const skillsDir = path.join(pmRoot, plugin, 'skills');
    if (!/^pm-/.test(plugin) || !fs.existsSync(skillsDir)) continue;
    for (const name of fs.readdirSync(skillsDir)) add(path.join(skillsDir, name), 'pm-skills');
  }

  for (const root of [['superpowers-7.0.1', 'superpowers'], ['srs-skills', 'srs-skills']]) {
    const skillsDir = path.join(DOCS, root[0], 'skills');
    for (const name of fs.readdirSync(skillsDir)) add(path.join(skillsDir, name), root[1]);
  }
  return out;
}

function normalizeTree(dir, rules) {
  let changed = 0;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { changed += normalizeTree(p, rules); continue; }
    if (!TEXT_EXT.has(path.extname(e.name))) continue;
    const before = fs.readFileSync(p, 'utf8');
    let after = before;
    for (const [from, to] of rules) after = after.split(from).join(to);
    if (after !== before) { fs.writeFileSync(p, after); changed++; }
  }
  return changed;
}

const sources = collect();
fs.mkdirSync(DEST, { recursive: true });
const imported = [];
for (const { dir, family } of sources) {
  const name = path.basename(dir);
  if (!SKILL_NAME.test(name)) { console.warn(`skip ${dir}: directory name is not kebab-case`); continue; }
  const target = path.join(DEST, name);
  fs.rmSync(target, { recursive: true, force: true });
  fs.cpSync(dir, target, { recursive: true });
  if (family === 'srs-skills') normalizeTree(target, SRS_RULES);
  if (family === 'pm-skills') normalizeTree(target, PM_RULES);
  imported.push({ name, family });
}

const counts = imported.reduce((acc, i) => ({ ...acc, [i.family]: (acc[i.family] || 0) + 1 }), {});
console.log(`imported ${imported.length} skills:`, counts);

const seen = new Set();
for (const name of fs.readdirSync(DEST)) {
  const p = path.join(DEST, name);
  if (!fs.statSync(p).isDirectory()) continue;
  const raw = fs.readFileSync(path.join(p, 'SKILL.md'), 'utf8').replace(/^\uFEFF/, '');
  const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fmName = fm && (fm[1].match(/^name:(.*)$/m) || [])[1];
  const ok = fm && fmName && SKILL_NAME.test(fmName.trim().replace(/^["']|["']$/g, '')) && /^description:/m.test(fm[1]);
  if (!ok) console.warn(`INVALID skill after import: ${name}`);
  if (seen.has(name)) console.warn(`duplicate skill name: ${name}`);
  seen.add(name);
}
console.log(`verified ${seen.size} skills`);
