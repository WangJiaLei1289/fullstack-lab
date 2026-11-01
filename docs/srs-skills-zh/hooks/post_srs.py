#!/usr/bin/env python3
"""
钩子：PostToolUse (Write)
在 Claude 写完一个文件之后触发。

如果写入的文件位于 'plan/' 目录下，就自动运行 plan_validator.py
（第 4 阶段就绪门禁）。如果它看起来像 SRS（路径包含 'srs' 且以 .md 结尾），
就自动运行 srs_validator.py。无论哪种情况，判定结果都会作为
additionalContext 注入。
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"


def is_plan_file(file_path: str) -> bool:
    p = Path(file_path)
    return p.suffix == ".md" and p.parent.name.lower() == "plan"


def is_srs_file(file_path: str) -> bool:
    p = Path(file_path)
    if p.suffix != ".md":
        return False
    # 匹配：文件名为 srs-*.md，或位于名为 'srs' 的路径层级内
    path_str = str(p).lower().replace("\\", "/")
    return "srs" in p.name.lower() or "/srs/" in path_str


def run_script(script_name: str, args: list[str]) -> str | None:
    script = SCRIPTS_DIR / script_name
    if not script.exists():
        return None
    try:
        result = subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True, text=True, timeout=25, encoding="utf-8"
        )
        return result.stdout.strip()
    except Exception:
        return None


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = event.get("tool_name", "")
    if tool_name != "Write":
        sys.exit(0)

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    if is_plan_file(file_path):
        plan_dir = str(Path(file_path).parent)
        validation = run_script("plan_validator.py", ["--dir", plan_dir])
        if not validation:
            sys.exit(0)
        output = {
            "additionalContext": (
                f"## Post-save: Plan Validation\n\n"
                f"{validation}\n\n"
                "> Fix ERROR findings before running /sr:generate — they will block the gate. "
                "WARNs (e.g. open [NEEDS USER INPUT] items) should be tracked in appendix-b-open-issues.md."
            )
        }
        print(json.dumps(output))
        return

    if not is_srs_file(file_path):
        sys.exit(0)

    p = Path(file_path)
    # 如果文件位于名为 'srs' 的目录内，就校验整个目录
    if p.parent.name.lower() == "srs":
        validation = run_script("srs_validator.py", ["--dir", str(p.parent)])
    else:
        validation = run_script("srs_validator.py", [file_path])
    if not validation:
        sys.exit(0)

    output = {
        "additionalContext": (
            f"## Post-save: SRS Validation\n\n"
            f"{validation}\n\n"
            "> Fix any ERROR findings before marking the SRS as ready for review. "
            "WARN items should be resolved or explicitly acknowledged."
        )
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
