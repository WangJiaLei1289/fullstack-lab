#!/usr/bin/env python3
"""
插件集合校验器
==============
按 Claude Code 插件规范校验集合中的全部插件：
- plugin.json 清单：必填字段、作者信息、关键词
- 技能：YAML frontmatter（name 必须与目录名一致，description 必填）
- 命令：YAML frontmatter（description 与 argument-hint 必填）
- 交叉引用：命令引用的技能必须存在于同一插件中
- README：存在且包含预期章节

参考：
- Anthropic plugin-dev README（https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev）
- agentskills.io 规范
- Claude Code 插件参考文档（https://code.claude.com/docs/en/plugins-reference）

作者：Paweł Huryn —— The Product Compass Newsletter（https://www.productcompass.pm）
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


# ─── 配置 ─────────────────────────────────────────────────────────────────────

# 规范要求的 plugin.json 必填字段
REQUIRED_MANIFEST_FIELDS = ["name", "version", "description"]
RECOMMENDED_MANIFEST_FIELDS = ["author", "keywords", "homepage", "license"]
REQUIRED_AUTHOR_FIELDS = ["name", "email"]
RECOMMENDED_AUTHOR_FIELDS = ["url"]

# 技能 frontmatter 必填字段
REQUIRED_SKILL_FIELDS = ["name", "description"]

# 命令 frontmatter 必填字段
REQUIRED_COMMAND_FIELDS = ["description"]
RECOMMENDED_COMMAND_FIELDS = ["argument-hint"]

# README 预期包含的章节（大小写不敏感的包含匹配）
EXPECTED_README_SECTIONS = ["overview", "install", "skill", "command"]


# ─── ANSI 颜色 ────────────────────────────────────────────────────────────────

class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


# ─── 辅助函数 ─────────────────────────────────────────────────────────────────

def parse_yaml_frontmatter(content: str) -> Optional[dict]:
    """从 Markdown 文件中提取 YAML frontmatter（位于 --- 标记之间的内容）。"""
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    fm_text = content[3:end].strip()
    # 简易 YAML 解析器，只处理扁平的键值对
    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r'^(\S+):\s*(.+)$', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip().strip('"').strip("'")
            result[key] = value
    return result


def count_words(content: str) -> int:
    """统计 Markdown 正文的词数（不含 frontmatter）。"""
    # 去掉 frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:]
    return len(content.split())


# ─── 校验器 ───────────────────────────────────────────────────────────────────

class ValidationResult:
    def __init__(self):
        self.errors: list[str] = []      # 必须修复
        self.warnings: list[str] = []    # 建议修复
        self.info: list[str] = []        # 仅供参考

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def note(self, msg: str):
        self.info.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def validate_manifest(plugin_dir: str) -> ValidationResult:
    """校验插件清单 plugin.json。"""
    result = ValidationResult()
    pj_path = os.path.join(plugin_dir, ".claude-plugin", "plugin.json")

    if not os.path.isfile(pj_path):
        result.error("缺少 .claude-plugin/plugin.json")
        return result

    try:
        with open(pj_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.error(f"plugin.json 不是合法 JSON：{e}")
        return result

    # 必填字段
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in data or not data[field]:
            result.error(f"缺少必填字段：{field}")

    # name 必须与目录名一致
    dir_name = os.path.basename(plugin_dir)
    if data.get("name") and data["name"] != dir_name:
        result.error(f"名称不一致：plugin.json 写的是 '{data['name']}'，但目录名是 '{dir_name}'")

    # 版本号格式
    version = data.get("version", "")
    if version and not re.match(r'^\d+\.\d+\.\d+$', version):
        result.warn(f"版本号 '{version}' 不符合语义化版本格式（x.y.z）")

    # 推荐字段
    for field in RECOMMENDED_MANIFEST_FIELDS:
        if field not in data:
            result.warn(f"缺少推荐字段：{field}")

    # 作者校验
    author = data.get("author")
    if isinstance(author, dict):
        for field in REQUIRED_AUTHOR_FIELDS:
            if field not in author or not author[field]:
                result.warn(f"缺少 author.{field}")
        for field in RECOMMENDED_AUTHOR_FIELDS:
            if field not in author:
                result.note(f"缺少 author.{field}")
    elif author is not None:
        result.warn("author 应为包含 name、email、url 字段的对象")

    # 关键词校验
    keywords = data.get("keywords", [])
    if not keywords:
        result.warn("未定义关键词")
    elif not isinstance(keywords, list):
        result.error("keywords 必须是数组")

    # description 长度检查
    desc = data.get("description", "")
    if desc and len(desc) < 20:
        result.warn(f"description 过短（{len(desc)} 个字符）")

    result.note(f"版本：{version}")
    result.note(f"关键词：{len(keywords) if isinstance(keywords, list) else 0} 个")

    return result


def validate_skill(skill_dir: str) -> ValidationResult:
    """校验单个技能目录。"""
    result = ValidationResult()
    skill_name = os.path.basename(skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md):
        result.error("缺少 SKILL.md")
        return result

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # frontmatter 检查
    fm = parse_yaml_frontmatter(content)
    if fm is None:
        result.error("缺少 YAML frontmatter（文件必须以 --- 开头）")
        return result

    # 必填字段
    for field in REQUIRED_SKILL_FIELDS:
        if field not in fm or not fm[field]:
            result.error(f"缺少必填 frontmatter 字段：{field}")

    # name 必须与目录名一致（agentskills.io 规范）
    if fm.get("name") and fm["name"] != skill_name:
        result.error(f"名称不一致：frontmatter 写的是 '{fm['name']}'，但目录名是 '{skill_name}'")

    # description 质量
    desc = fm.get("description", "")
    if desc:
        if len(desc) < 30:
            result.warn(f"description 过短（{len(desc)} 个字符）")
        # 建议包含触发短语
        trigger_keywords = ["trigger", "use when", "use for"]
        has_triggers = any(kw in desc.lower() for kw in trigger_keywords)
        if not has_triggers:
            result.note("description 缺少显式触发短语（例如 'Triggers: ...'）")

    # 词数统计
    word_count = count_words(content)
    result.note(f"词数：{word_count}")
    if word_count > 3000:
        result.warn(f"技能篇幅偏长（{word_count} 词）。建议用 references/ 做渐进式披露")
    elif word_count < 50:
        result.warn(f"技能篇幅过短（{word_count} 词），可能需要补充内容。")

    return result


def validate_command(cmd_path: str) -> ValidationResult:
    """校验单个命令文件。"""
    result = ValidationResult()

    with open(cmd_path, "r", encoding="utf-8") as f:
        content = f.read()

    # frontmatter 检查
    fm = parse_yaml_frontmatter(content)
    if fm is None:
        result.error("缺少 YAML frontmatter（文件必须以 --- 开头）")
        return result

    # 必填字段
    for field in REQUIRED_COMMAND_FIELDS:
        if field not in fm or not fm[field]:
            result.error(f"缺少必填 frontmatter 字段：{field}")

    # 推荐字段
    for field in RECOMMENDED_COMMAND_FIELDS:
        if field not in fm or not fm[field]:
            result.warn(f"缺少推荐 frontmatter 字段：{field}")

    # description 质量
    desc = fm.get("description", "")
    if desc and len(desc) < 10:
        result.warn(f"description 过短（{len(desc)} 个字符）")

    # 命令是否引用技能（仅作信息提示）
    skill_refs = re.findall(r'\*\*(\w[\w-]+)\*\*\s+skill', content)
    if skill_refs:
        result.note(f"引用的技能：{', '.join(skill_refs)}")

    return result


def validate_readme(plugin_dir: str) -> ValidationResult:
    """校验插件 README.md。"""
    result = ValidationResult()
    readme_path = os.path.join(plugin_dir, "README.md")

    if not os.path.isfile(readme_path):
        result.warn("缺少 README.md")
        return result

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # 检查预期章节
    for section in EXPECTED_README_SECTIONS:
        if section not in content:
            result.note(f"README 可能缺少 '{section}' 章节")

    result.note(f"README：{count_words(content)} 词")
    return result


def validate_cross_references(plugin_dir: str, skill_names: list[str]) -> ValidationResult:
    """检查命令引用的技能是否确实存在于本插件。"""
    result = ValidationResult()
    cmds_dir = os.path.join(plugin_dir, "commands")

    if not os.path.isdir(cmds_dir):
        return result

    for cmd_file in sorted(os.listdir(cmds_dir)):
        if not cmd_file.endswith(".md"):
            continue
        cmd_path = os.path.join(cmds_dir, cmd_file)
        with open(cmd_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 查找形如 **skill-name** skill 的技能引用
        refs = re.findall(r'\*\*(\w[\w-]+)\*\*\s+skill', content)
        for ref in refs:
            if ref not in skill_names:
                result.warn(f"命令 {cmd_file} 引用的技能 '{ref}' 不在本插件中")

    return result


# ─── 主校验流程 ───────────────────────────────────────────────────────────────

def validate_plugin(plugin_dir: str) -> dict:
    """对单个插件执行全部校验。"""
    plugin_name = os.path.basename(plugin_dir)
    results = {"name": plugin_name, "sections": {}}

    # 1. 插件清单
    results["sections"]["manifest"] = validate_manifest(plugin_dir)

    # 2. 技能
    skills_dir = os.path.join(plugin_dir, "skills")
    skill_names = []
    skill_results = {}
    if os.path.isdir(skills_dir):
        for skill_name in sorted(os.listdir(skills_dir)):
            skill_path = os.path.join(skills_dir, skill_name)
            if os.path.isdir(skill_path):
                skill_names.append(skill_name)
                skill_results[skill_name] = validate_skill(skill_path)
    results["sections"]["skills"] = skill_results
    results["skill_count"] = len(skill_names)

    # 3. 命令
    cmds_dir = os.path.join(plugin_dir, "commands")
    cmd_results = {}
    if os.path.isdir(cmds_dir):
        for cmd_file in sorted(os.listdir(cmds_dir)):
            if cmd_file.endswith(".md"):
                cmd_path = os.path.join(cmds_dir, cmd_file)
                cmd_results[cmd_file] = validate_command(cmd_path)
    results["sections"]["commands"] = cmd_results
    results["command_count"] = len(cmd_results)

    # 4. README
    results["sections"]["readme"] = validate_readme(plugin_dir)

    # 5. 交叉引用
    results["sections"]["cross-refs"] = validate_cross_references(plugin_dir, skill_names)

    return results


def print_validation_result(label: str, vr: ValidationResult, indent: int = 4):
    """打印单条校验结果。"""
    prefix = " " * indent
    if vr.errors:
        for e in vr.errors:
            print(f"{prefix}{C.RED}✗ 错误：{C.RESET} {e}")
    if vr.warnings:
        for w in vr.warnings:
            print(f"{prefix}{C.YELLOW}⚠ 警告：{C.RESET}  {w}")
    if vr.info:
        for i in vr.info:
            print(f"{prefix}{C.DIM}ℹ {i}{C.RESET}")


def print_report(all_results: list[dict]):
    """打印完整校验报告。"""
    total_errors = 0
    total_warnings = 0
    total_skills = 0
    total_commands = 0

    print(f"\n{C.BOLD}{'='*70}")
    print(f" 插件集合校验器 —— 校验报告")
    print(f"{'='*70}{C.RESET}\n")

    for plugin in all_results:
        name = plugin["name"]
        sc = plugin["skill_count"]
        cc = plugin["command_count"]
        total_skills += sc
        total_commands += cc

        # 统计该插件的错误/警告数量
        p_errors = 0
        p_warnings = 0
        for key, section in plugin["sections"].items():
            if isinstance(section, ValidationResult):
                p_errors += len(section.errors)
                p_warnings += len(section.warnings)
            elif isinstance(section, dict):
                for vr in section.values():
                    p_errors += len(vr.errors)
                    p_warnings += len(vr.warnings)

        total_errors += p_errors
        total_warnings += p_warnings

        # 插件标题
        status = f"{C.GREEN}✓ 通过{C.RESET}" if p_errors == 0 else f"{C.RED}✗ 未通过{C.RESET}"
        warn_str = f" {C.YELLOW}（{p_warnings} 条警告）{C.RESET}" if p_warnings > 0 else ""
        print(f"{C.BOLD}{C.CYAN}┌─ {name}{C.RESET}  [{sc} 个技能，{cc} 个命令]  {status}{warn_str}")

        # 插件清单
        manifest = plugin["sections"]["manifest"]
        if manifest.errors or manifest.warnings:
            print(f"  {C.BOLD}插件清单：{C.RESET}")
            print_validation_result("manifest", manifest)

        # 有问题的技能
        skill_results = plugin["sections"]["skills"]
        skills_with_issues = {k: v for k, v in skill_results.items() if v.errors or v.warnings}
        if skills_with_issues:
            print(f"  {C.BOLD}有问题的技能：{C.RESET}")
            for sname, vr in skills_with_issues.items():
                print(f"    {sname}:")
                print_validation_result(sname, vr, indent=6)

        # 有问题的命令
        cmd_results = plugin["sections"]["commands"]
        cmds_with_issues = {k: v for k, v in cmd_results.items() if v.errors or v.warnings}
        if cmds_with_issues:
            print(f"  {C.BOLD}有问题的命令：{C.RESET}")
            for cname, vr in cmds_with_issues.items():
                print(f"    {cname}:")
                print_validation_result(cname, vr, indent=6)

        # README
        readme = plugin["sections"]["readme"]
        if readme.errors or readme.warnings:
            print(f"  {C.BOLD}README：{C.RESET}")
            print_validation_result("readme", readme)

        # 交叉引用
        xrefs = plugin["sections"]["cross-refs"]
        if xrefs.errors or xrefs.warnings:
            print(f"  {C.BOLD}交叉引用：{C.RESET}")
            print_validation_result("cross-refs", xrefs)

        print(f"{C.CYAN}└{'─'*69}{C.RESET}\n")

    # 汇总
    print(f"{C.BOLD}{'='*70}")
    print(f" 汇总")
    print(f"{'='*70}{C.RESET}")
    print(f"  插件：   {len(all_results)} 个")
    print(f"  技能：   {total_skills} 个")
    print(f"  命令：   {total_commands} 个")
    print(f"  合计：   {total_skills + total_commands} 个组件")
    print()
    if total_errors == 0:
        print(f"  {C.GREEN}{C.BOLD}✓ 全部检查通过{C.RESET}（{total_warnings} 条警告）")
    else:
        print(f"  {C.RED}{C.BOLD}✗ {total_errors} 个错误{C.RESET}，{total_warnings} 条警告")
    print()

    return total_errors


def main():
    """查找并校验集合中的所有插件。"""
    # 确保 Windows 下输出使用 UTF-8
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 确定根路径
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(base_path):
        print(f"错误：{base_path} 不是目录")
        sys.exit(1)

    # 查找所有插件目录（即包含 .claude-plugin/ 的目录）
    plugin_dirs = []
    for entry in sorted(os.listdir(base_path)):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path) and os.path.isdir(os.path.join(full_path, ".claude-plugin")):
            plugin_dirs.append(full_path)

    if not plugin_dirs:
        print(f"在 {base_path} 中没有找到任何插件")
        print("（查找的是包含 .claude-plugin/ 的目录）")
        sys.exit(1)

    print(f"在 {base_path} 中找到 {len(plugin_dirs)} 个插件\n")

    # 逐个校验
    all_results = []
    for pd in plugin_dirs:
        all_results.append(validate_plugin(pd))

    # 打印报告
    errors = print_report(all_results)

    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
