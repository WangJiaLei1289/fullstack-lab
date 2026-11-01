#!/usr/bin/env python3
"""
gap_scanner.py — 预扫描原始需求文本，找出歧义模式。

在处理输入之前，用正则 + 启发式规则检测模式 1–7。Claude 读取输出，
对其进行校验与扩展，跳过对明显缺口的重复推导 —— 每个会话可省 1–2 轮 LLM 交互。

用法：
    python scripts/gap_scanner.py requirements.txt
    echo "Users should be able to login fast" | python scripts/gap_scanner.py -
    python scripts/gap_scanner.py requirements.txt --format json
    python scripts/gap_scanner.py requirements.txt --min-priority P2
"""

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# 确保在 Windows 上输出 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Gap 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Gap:
    pattern_id: int
    pattern_label: str
    priority: str        # P1 | P2 | P3
    fragment: str        # 触发该标记的原文片段
    context: str = ""    # 便于阅读的上下文句子
    escalation: str = "" # 优先级从默认值上调的原因


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _sentences(text: str) -> list[str]:
    return re.split(r'(?<=[.!?])\s+', text.strip())


def _find_matches(pattern: str, text: str, flags: int = re.IGNORECASE) -> list[re.Match]:
    return list(re.finditer(pattern, text, flags))


def _surrounding_sentence(match: re.Match, text: str) -> str:
    """返回包含该匹配项的句子。"""
    start = text.rfind("\n", 0, match.start())
    start = 0 if start == -1 else start + 1
    end = text.find("\n", match.end())
    end = len(text) if end == -1 else end
    return text[start:end].strip()[:120]


# ---------------------------------------------------------------------------
# 模式检测器
# ---------------------------------------------------------------------------

VAGUE_QUANTIFIERS = (
    r"\b(many|few|some|large|small|fast|slow|soon|quickly|appropriate|"
    r"good|high|low|reasonable|sufficient|minimal|significant|several|"
    r"numerous|better|worse|easy|simple|complex|robust|scalable|reliable|"
    r"secure|performant|efficient|optimal)\b"
)

CORE_FEATURE_SIGNALS = r"\b(login|auth|payment|checkout|search|upload|report|export|dashboard)\b"


def scan_pattern_1(text: str) -> list[Gap]:
    """模糊量词。"""
    gaps = []
    for m in _find_matches(VAGUE_QUANTIFIERS, text):
        word = m.group(0).lower()
        sentence = _surrounding_sentence(m, text)
        # 若模糊词是某个核心功能唯一可度量的信号，则上调为 P2
        escalated = bool(re.search(CORE_FEATURE_SIGNALS, sentence, re.IGNORECASE)
                         and not re.search(r"\d+\s*(ms|s|%|rpm|tps|mb|gb|users?)", sentence, re.IGNORECASE))
        gaps.append(Gap(
            pattern_id=1,
            pattern_label="Vague Quantifier",
            priority="P2" if escalated else "P3",
            fragment=f'"{word}"',
            context=sentence,
            escalation="only measurable signal for core feature" if escalated else "",
        ))
    return gaps


WEAK_MODALS = r"\b(should|might|could|may)\b"
STRONG_OBLIGATION = r"\b(shall|must|will|is required to)\b"


def scan_pattern_2(text: str) -> list[Gap]:
    """弱情态动词。"""
    gaps = []
    for m in _find_matches(WEAK_MODALS, text):
        word = m.group(0).lower()
        sentence = _surrounding_sentence(m, text)
        # 若句子里同时含核心功能信号且没有 shall，则上调为 P1
        has_core = bool(re.search(CORE_FEATURE_SIGNALS, sentence, re.IGNORECASE))
        has_strong = bool(re.search(STRONG_OBLIGATION, sentence, re.IGNORECASE))
        priority = "P1" if (has_core and not has_strong) else "P2"
        gaps.append(Gap(
            pattern_id=2,
            pattern_label="Weak Modality",
            priority=priority,
            fragment=f'"{word}"',
            context=sentence,
            escalation="weak modal on core feature" if priority == "P1" else "",
        ))
    return gaps


UNDEFINED_ACTOR_TOKENS = r"\b(they|them|their|it\b|the user|the admin|the customer|the system|the client)\b"
DEFINED_ACTOR_SIGNALS  = r"\b(is defined as|refers to|means|acting as|role of)\b"


def scan_pattern_3(text: str) -> list[Gap]:
    """未定义的行为主体 / 没有先行词的代词。"""
    gaps = []
    defined_actors: set[str] = set()
    # 收集显式定义的行为主体
    for m in _find_matches(DEFINED_ACTOR_SIGNALS, text):
        window = text[max(0, m.start() - 40):m.start()].lower()
        defined_actors.update(re.findall(r"\b\w+\b", window))

    for m in _find_matches(UNDEFINED_ACTOR_TOKENS, text):
        token = m.group(0).lower()
        if any(t in defined_actors for t in token.split()):
            continue
        sentence = _surrounding_sentence(m, text)
        gaps.append(Gap(
            pattern_id=3,
            pattern_label="Undefined Actor",
            priority="P1",
            fragment=f'"{m.group(0)}"',
            context=sentence,
        ))
    return gaps


ANAPHORIC_TOKENS = r"\b(this|that|these|those|the former|the latter|the above|the same|the following)\b"


def scan_pattern_4(text: str) -> list[Gap]:
    """指代不明的前向引用。"""
    # 仅当句中该代词前面有多个候选名词时才标记
    gaps = []
    for m in _find_matches(ANAPHORIC_TOKENS, text):
        sentence = _surrounding_sentence(m, text)
        # 统计同一句中该词之前出现的不同名词
        before = sentence[: sentence.lower().find(m.group(0).lower())]
        noun_candidates = re.findall(r"\b[A-Z][a-z]+|[a-z]{4,}\b", before)
        if len(set(noun_candidates)) >= 2:
            # 若处在交易/数据/删除语境中，则上调为 P1
            danger_ctx = bool(re.search(r"\b(delete|pay|submit|approve|transfer|own|belong|update)\b", sentence, re.IGNORECASE))
            gaps.append(Gap(
                pattern_id=4,
                pattern_label="Anaphoric Reference",
                priority="P1" if danger_ctx else "P2",
                fragment=f'"{m.group(0)}"',
                context=sentence,
                escalation="ambiguous referent in transaction/data context" if danger_ctx else "",
            ))
    return gaps


def scan_pattern_5(text: str) -> list[Gap]:
    """并列歧义 —— 形如「A and B or C」的结构。"""
    gaps = []
    # 模式：word AND word OR word，或以 and/or 结尾的逗号列表
    coord_pattern = r"\b\w+\s+and\s+\w+\s+or\s+\w+|\b\w+,\s*\w+,?\s+(and|or)\s+\w+"
    for m in _find_matches(coord_pattern, text):
        sentence = _surrounding_sentence(m, text)
        danger_ctx = bool(re.search(r"\b(delete|permission|access|authorize|deny|grant)\b", sentence, re.IGNORECASE))
        gaps.append(Gap(
            pattern_id=5,
            pattern_label="Coordination Ambiguity",
            priority="P1" if danger_ctx else "P2",
            fragment=f'"{m.group(0).strip()}"',
            context=sentence,
            escalation="ambiguity in authorization/deletion rule" if danger_ctx else "",
        ))
    return gaps


# 缺失约束的信号 —— 出现即表示该约束已被处理
CONSTRAINT_SIGNALS = {
    "error_handling":  r"\b(error|fail|timeout|invalid|exception|fallback|retry)\b",
    "concurrency":     r"\b(\d+\s*(users?|concurrent|simultaneous|tps|rpm|requests?))\b",
    "permissions":     r"\b(role|permission|access control|authorize|deny|grant|rbac)\b",
    "rollback":        r"\b(rollback|undo|revert|cancel|void|reverse)\b",
    "nfr_baseline":    r"\b(\d+\s*(ms|s|%|uptime|availability|sla|latency))\b",
}

DESTRUC_OPERATIONS = r"\b(delete|remove|drop|purge|publish|send|pay|transfer|submit)\b"


def scan_pattern_6(text: str) -> list[Gap]:
    """缺失约束 —— 检查必需类别是否缺席。"""
    gaps = []
    lower = text.lower()

    for category, signal in CONSTRAINT_SIGNALS.items():
        if not re.search(signal, text, re.IGNORECASE):
            # 只有存在破坏性操作时，才标记缺少回滚
            if category == "rollback" and not re.search(DESTRUC_OPERATIONS, text, re.IGNORECASE):
                continue
            priority_map = {
                "error_handling": "P1",
                "permissions": "P1",
                "rollback": "P1",
                "concurrency": "P2",
                "nfr_baseline": "P2",
            }
            gaps.append(Gap(
                pattern_id=6,
                pattern_label=f"Missing Constraint ({category.replace('_', ' ')})",
                priority=priority_map[category],
                fragment=f"no {category.replace('_', ' ')} found in document",
                context="",
            ))
    return gaps


SCOPE_IN  = r"\b(in scope|included|will support|must have|shall include)\b"
SCOPE_OUT = r"\b(out of scope|excluded|will not|won't|not included|not supported)\b"
REQUIRED  = r"\b(required|mandatory|must|shall)\b"


def scan_pattern_7(text: str) -> list[Gap]:
    """矛盾 —— 尽力而为的启发式检测。"""
    gaps = []
    sentences = _sentences(text)

    # 启发式 A：同一功能同时被描述为在范围内和不在范围内
    in_scope_nouns:  set[str] = set()
    out_scope_nouns: set[str] = set()

    for s in sentences:
        nouns = set(re.findall(r"\b[A-Z][a-z]{2,}|[a-z]{4,}\b", s))
        if re.search(SCOPE_IN, s, re.IGNORECASE):
            in_scope_nouns.update(nouns)
        if re.search(SCOPE_OUT, s, re.IGNORECASE):
            out_scope_nouns.update(nouns)

    overlap = in_scope_nouns & out_scope_nouns - {"scope", "will", "support", "include"}
    if overlap:
        gaps.append(Gap(
            pattern_id=7,
            pattern_label="Contradiction",
            priority="P1",
            fragment=f"feature(s) appear both in-scope and out-of-scope: {', '.join(sorted(overlap)[:5])}",
            context="",
        ))

    # 启发式 B：高性能目标 + 严重受限的硬件
    has_high_load = bool(re.search(r"\b\d{4,}\s*(users?|concurrent|tps)\b", text, re.IGNORECASE))
    has_low_hw    = bool(re.search(r"\b(1|2|4)\s*gb\s*(ram|memory)\b", text, re.IGNORECASE))
    if has_high_load and has_low_hw:
        gaps.append(Gap(
            pattern_id=7,
            pattern_label="Contradiction",
            priority="P1",
            fragment="high concurrency target vs. low-spec hardware",
            context="",
        ))

    return gaps


# ---------------------------------------------------------------------------
# 编排器
# ---------------------------------------------------------------------------

SCANNERS = [
    scan_pattern_1,
    scan_pattern_2,
    scan_pattern_3,
    scan_pattern_4,
    scan_pattern_5,
    scan_pattern_6,
    scan_pattern_7,
]

PRIORITY_ORDER = {"P1": 0, "P2": 1, "P3": 2}


def scan(text: str, min_priority: str = "P3") -> list[Gap]:
    gaps: list[Gap] = []
    for scanner in SCANNERS:
        gaps.extend(scanner(text))
    # 去重：片段 + 模式组合完全相同的项
    seen: set[tuple] = set()
    unique: list[Gap] = []
    for g in gaps:
        key = (g.pattern_id, g.fragment)
        if key not in seen:
            seen.add(key)
            unique.append(g)
    # 按最低优先级过滤
    threshold = PRIORITY_ORDER[min_priority]
    unique = [g for g in unique if PRIORITY_ORDER[g.priority] <= threshold]
    # 排序：P1 在前，其次按模式 id
    return sorted(unique, key=lambda g: (PRIORITY_ORDER[g.priority], g.pattern_id))


# ---------------------------------------------------------------------------
# 输出格式化器
# ---------------------------------------------------------------------------

def format_markdown(gaps: list[Gap]) -> str:
    if not gaps:
        return "**Gap scan complete — no ambiguity patterns detected.**\n"
    lines = [
        f"**Gap scan: {len(gaps)} issue(s) found**\n",
        "| # | Priority | Pattern | Fragment | Context |",
        "|---|----------|---------|---------|---------|",
    ]
    for i, g in enumerate(gaps, 1):
        escalation = f" ⬆ {g.escalation}" if g.escalation else ""
        ctx = g.context.replace("|", "\\|") if g.context else "—"
        lines.append(
            f"| {i} | **{g.priority}**{escalation} "
            f"| Pattern {g.pattern_id} — {g.pattern_label} "
            f"| {g.fragment} | {ctx} |"
        )
    lines.append(
        "\n> Generated by gap_scanner.py — Claude should validate and extend this list."
    )
    return "\n".join(lines)


def format_json(gaps: list[Gap]) -> str:
    return json.dumps(
        [
            {
                "pattern_id": g.pattern_id,
                "pattern_label": g.pattern_label,
                "priority": g.priority,
                "fragment": g.fragment,
                "context": g.context,
                "escalation": g.escalation,
            }
            for g in gaps
        ],
        indent=2,
        ensure_ascii=False,
    )


# ---------------------------------------------------------------------------
# 命令行接口（CLI）
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pre-scan raw requirements for IEEE 830 ambiguity patterns."
    )
    parser.add_argument(
        "input",
        help="Path to requirements file, or '-' to read from stdin",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--min-priority",
        choices=["P1", "P2", "P3"],
        default="P3",
        help="Minimum priority to report (default: P3 = all)",
    )
    args = parser.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        path = Path(args.input)
        if not path.exists():
            print(f"[!] File not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")

    gaps = scan(text, min_priority=args.min_priority)

    if args.format == "json":
        print(format_json(gaps))
    else:
        print(format_markdown(gaps))


if __name__ == "__main__":
    main()
