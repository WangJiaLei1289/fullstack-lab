"""validate_plugins.py 的单元测试，以及仓库级校验闸门。"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import validate_plugins as vp


class TestFrontmatterParser(unittest.TestCase):
    def test_parses_flat_keys(self):
        fm = vp.parse_yaml_frontmatter(
            '---\ndescription: Hello world\nargument-hint: "[x]"\n---\nBody'
        )
        self.assertEqual(fm["description"], "Hello world")
        self.assertEqual(fm["argument-hint"], "[x]")

    def test_none_without_frontmatter(self):
        self.assertIsNone(vp.parse_yaml_frontmatter("# Just markdown\n"))

    def test_none_when_unterminated(self):
        self.assertIsNone(vp.parse_yaml_frontmatter("---\ndescription: x\n"))

    def test_strips_quotes(self):
        fm = vp.parse_yaml_frontmatter("---\nname: 'quoted'\n---\n")
        self.assertEqual(fm["name"], "quoted")


class TestCountWords(unittest.TestCase):
    def test_excludes_frontmatter(self):
        self.assertEqual(vp.count_words("---\nname: x\n---\none two three"), 3)


class TestRepoPassesValidation(unittest.TestCase):
    """仓库中的每个插件都必须零错误通过校验器。"""

    def test_all_plugins_valid(self):
        plugin_dirs = sorted(
            str(p)
            for p in ROOT.iterdir()
            if p.is_dir() and (p / ".claude-plugin").is_dir()
        )
        self.assertTrue(plugin_dirs, "仓库根目录下没有找到任何插件")

        failures = []
        for pd in plugin_dirs:
            results = vp.validate_plugin(pd)
            for section, value in results["sections"].items():
                items = value.values() if isinstance(value, dict) else [value]
                for vr in items:
                    for err in vr.errors:
                        failures.append(f"{results['name']}/{section}: {err}")

        self.assertEqual(
            failures, [], "校验器报错：\n" + "\n".join(failures)
        )


if __name__ == "__main__":
    unittest.main()
