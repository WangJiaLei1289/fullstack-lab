"""文档与清单的一致性检查，在每次 PR、推送和发布时运行。

锁定以下内容：
- marketplace.json 列出的插件与磁盘上的插件目录完全一致；
- 全仓库只有一个版本号：CHANGELOG 最新标题 == marketplace.json == 每个 plugin.json
  （CLAUDE.md 规则：每个插件不单独设置版本号）；
- CHANGELOG 标题格式规范、带日期、不重复，并按从新到旧排列；
- README 中的计数（首屏、各插件摘要、插件 README 章节标题）与实际磁盘上的技能、命令数量一致；
- 插件 README 中每个 /plugin:command 引用都能对应到真实的命令文件。
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CHANGELOG = ROOT / "CHANGELOG.md"
README = ROOT / "README.md"


def plugin_dirs():
    return sorted(
        p
        for p in ROOT.iterdir()
        if p.is_dir() and (p / ".claude-plugin" / "plugin.json").is_file()
    )


def skill_count(plugin: Path) -> int:
    skills = plugin / "skills"
    if not skills.is_dir():
        return 0
    return sum(1 for s in skills.iterdir() if s.is_dir())


def command_count(plugin: Path) -> int:
    cmds = plugin / "commands"
    if not cmds.is_dir():
        return 0
    return len(list(cmds.glob("*.md")))


def marketplace() -> dict:
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


def latest_changelog_version() -> str:
    for line in CHANGELOG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## v(\d+\.\d+\.\d+)\b", line)
        if m:
            return m.group(1)
    raise AssertionError("CHANGELOG.md 中找不到 ## vX.Y.Z 标题")


class TestMarketplaceList(unittest.TestCase):
    def test_marketplace_lists_exactly_the_plugins_on_disk(self):
        listed = {p["name"] for p in marketplace()["plugins"]}
        on_disk = {p.name for p in plugin_dirs()}
        self.assertEqual(
            listed,
            on_disk,
            f"marketplace.json 与磁盘不一致 —— 只在清单里：{sorted(listed - on_disk)}，"
            f"只在磁盘上：{sorted(on_disk - listed)}",
        )

    def test_sources_point_at_matching_directories(self):
        for p in marketplace()["plugins"]:
            self.assertEqual(
                p["source"],
                f"./{p['name']}",
                f"插件 {p['name']} 的 source 是 {p['source']}",
            )


class TestVersionSync(unittest.TestCase):
    """全仓库只有一个版本号；CHANGELOG 最新标题就是已发布的版本。"""

    def test_all_versions_identical_and_match_changelog(self):
        want = latest_changelog_version()
        mismatches = []
        mp_version = marketplace()["version"]
        if mp_version != want:
            mismatches.append(f"marketplace.json={mp_version}")
        for p in plugin_dirs():
            manifest = p / ".claude-plugin" / "plugin.json"
            v = json.loads(manifest.read_text(encoding="utf-8"))["version"]
            if v != want:
                mismatches.append(f"{p.name}={v}")
        self.assertEqual(
            mismatches,
            [],
            f"CHANGELOG 写的是 v{want}；以下位置未同步：{mismatches}",
        )


class TestChangelogFormat(unittest.TestCase):
    def test_headings_well_formed_dated_unique_descending(self):
        text = CHANGELOG.read_text(encoding="utf-8")
        headings = [l for l in text.splitlines() if l.startswith("## ")]
        self.assertTrue(headings, "CHANGELOG.md 中没有任何 ## 标题")

        versions = []
        for h in headings:
            if h.strip() == "## Unreleased":
                continue
            m = re.match(r"^## v(\d+\.\d+\.\d+) — \d{4}-\d{2}-\d{2}$", h)
            self.assertIsNotNone(
                m,
                f"CHANGELOG 标题格式错误 {h!r} —— 期望形如 '## vX.Y.Z — YYYY-MM-DD'",
            )
            versions.append(tuple(int(x) for x in m.group(1).split(".")))

        self.assertEqual(
            len(versions), len(set(versions)), "存在重复的版本号标题"
        )
        self.assertEqual(
            versions,
            sorted(versions, reverse=True),
            "版本标题未按从新到旧排列",
        )


class TestReadmeCounts(unittest.TestCase):
    def _totals(self):
        plugins = plugin_dirs()
        return (
            sum(map(skill_count, plugins)),
            sum(map(command_count, plugins)),
            len(plugins),
        )

    def test_root_readme_headline_counts(self):
        skills, commands, plugins = self._totals()
        text = README.read_text(encoding="utf-8")
        m = re.search(
            r"(\d+) PM skills and (\d+) chained workflows across (\d+) plugins", text
        )
        self.assertIsNotNone(m, "README.md 中找不到首屏计数句")
        self.assertEqual(
            (int(m.group(1)), int(m.group(2)), int(m.group(3))),
            (skills, commands, plugins),
            "README.md 首屏计数与磁盘上的实际数量不一致",
        )

    def test_marketplace_description_counts(self):
        skills, commands, plugins = self._totals()
        desc = marketplace()["description"]
        m = re.search(
            r"(\d+) domain-specific skills and (\d+) chained workflows across (\d+) PM plugins",
            desc,
        )
        self.assertIsNotNone(
            m, "marketplace.json 的 description 中找不到计数句"
        )
        self.assertEqual(
            (int(m.group(1)), int(m.group(2)), int(m.group(3))),
            (skills, commands, plugins),
            "marketplace.json 的 description 计数与磁盘上的实际数量不一致",
        )

    def test_root_readme_per_plugin_counts(self):
        text = README.read_text(encoding="utf-8")
        found = {}
        for m in re.finditer(
            r"<strong>\d+\.\s*(pm-[\w-]+)</strong>[^)]*\((\d+) skills?, (\d+) commands?\)",
            text,
        ):
            found[m.group(1)] = (int(m.group(2)), int(m.group(3)))
        for p in plugin_dirs():
            self.assertIn(
                p.name,
                found,
                f"README.md 中找不到 {p.name} 的 '(N skills, M commands)' 摘要行",
            )
            self.assertEqual(
                found[p.name],
                (skill_count(p), command_count(p)),
                f"README.md 中 {p.name} 的计数不正确",
            )

    def test_plugin_readme_section_counts(self):
        for p in plugin_dirs():
            readme = p / "README.md"
            if not readme.is_file():
                continue
            text = readme.read_text(encoding="utf-8")
            m = re.search(r"^## Skills \((\d+)\)", text, re.M)
            if m:
                self.assertEqual(
                    int(m.group(1)),
                    skill_count(p),
                    f"{p.name}/README.md 的 '## Skills (N)' 标题计数错误",
                )
            m = re.search(r"^## Commands \((\d+)\)", text, re.M)
            if m:
                self.assertEqual(
                    int(m.group(1)),
                    command_count(p),
                    f"{p.name}/README.md 的 '## Commands (N)' 标题计数错误",
                )


class TestCommandReferences(unittest.TestCase):
    """插件 README 中提到的每个 /plugin:command 都必须在磁盘上存在。"""

    def test_plugin_readme_command_refs_exist(self):
        for p in plugin_dirs():
            readme = p / "README.md"
            if not readme.is_file():
                continue
            text = readme.read_text(encoding="utf-8")
            for m in re.finditer(rf"/{re.escape(p.name)}:([\w-]+)", text):
                cmd = p / "commands" / f"{m.group(1)}.md"
                self.assertTrue(
                    cmd.is_file(),
                    f"{p.name}/README.md 引用了 /{p.name}:{m.group(1)}，"
                    f"但 commands/{m.group(1)}.md 不存在",
                )


if __name__ == "__main__":
    unittest.main()
