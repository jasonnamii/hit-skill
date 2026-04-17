#!/usr/bin/env python3
"""
hit-skill self-check — evals/cases.json 기반 구조·트리거·스포크 정합성 검증.

실행:
    python scripts/validate.py ./
출력:
    JSON {pass: [...], warn: [...], fail: [...], grade: "GREEN|ORANGE|RED"}
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "## ⛔ 절대 규칙",
    "## §1. 모드 자동 판별",
    "## §2. 1차 스크리닝",
    "## §2.5. 도메인 어댑터 라우팅",
    "## §3. 상세 로딩",
    "## §4. 모드별 실행",
    "## §4.5. 리포트 변환",
]

REQUIRED_FILES = [
    "SKILL.md",
    "references/layer1-mechanism.md",
    "references/layer2-formulas.md",
    "references/layer3-propagation.md",
    "references/domain-routing.md",
    "references/execution-guide.md",
    "references/report-template.md",
    "references/screening-tables.md",
    "evals/cases.json",
]


def check_structure(skill_dir: Path) -> dict:
    """필수 파일·섹션 존재 확인."""
    report = {"pass": [], "fail": []}

    for rel in REQUIRED_FILES:
        fpath = skill_dir / rel
        if fpath.exists():
            report["pass"].append(f"file_exists:{rel}")
        else:
            report["fail"].append(f"missing_file:{rel}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section in text:
                report["pass"].append(f"section:{section.strip()}")
            else:
                report["fail"].append(f"missing_section:{section.strip()}")

        size = len(text.encode("utf-8"))
        if size <= 10_000:
            report["pass"].append(f"size_ok:{size}B")
        else:
            report["fail"].append(f"size_over_10KB:{size}B")

    return report


def check_triggers(skill_dir: Path) -> dict:
    """description 블록의 P1/P2/P3/NOT 최소 기준 확인."""
    report = {"pass": [], "warn": []}
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return report

    text = skill_md.read_text(encoding="utf-8")
    fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
    if not fm_match:
        report["warn"].append("no_frontmatter")
        return report

    fm = fm_match.group(1)
    for tier, minimum in [("P1", 5), ("P2", 2), ("P3", 2)]:
        m = re.search(rf"{tier}:\s*(.+)", fm)
        if not m:
            report["warn"].append(f"missing_tier:{tier}")
            continue
        count = len([x for x in re.split(r"[,\uff0c]", m.group(1)) if x.strip()])
        if count >= minimum:
            report["pass"].append(f"tier_ok:{tier}={count}")
        else:
            report["warn"].append(f"tier_low:{tier}={count}/<{minimum}")

    if "NOT:" in fm:
        report["pass"].append("not_section_exists")
    else:
        report["warn"].append("missing_not_section")

    return report


def check_evals(skill_dir: Path) -> dict:
    """evals/cases.json 구조 확인."""
    report = {"pass": [], "fail": []}
    cases_path = skill_dir / "evals" / "cases.json"
    if not cases_path.exists():
        report["fail"].append("evals/cases.json_missing")
        return report

    try:
        data = json.loads(cases_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report["fail"].append(f"cases_json_invalid:{e}")
        return report

    cases = data.get("cases", [])
    if len(cases) >= 3:
        report["pass"].append(f"cases_count:{len(cases)}")
    else:
        report["fail"].append(f"cases_too_few:{len(cases)}/<3")

    modes_seen = set()
    for case in cases:
        mode = case.get("expected", {}).get("mode")
        if mode:
            modes_seen.add(mode)
    if modes_seen >= {"진단", "설계", "변환"}:
        report["pass"].append("all_3_modes_covered")
    else:
        report["fail"].append(f"modes_missing:{sorted({'진단','설계','변환'}-modes_seen)}")

    return report


def grade(all_pass: int, all_warn: int, all_fail: int) -> str:
    total = all_pass + all_warn + all_fail
    if total == 0:
        return "RED"
    score = (all_pass + 0.5 * all_warn) / total * 100
    if all_fail > 0:
        return "RED" if score < 60 else "ORANGE"
    return "GREEN" if score >= 80 else "ORANGE"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate.py <skill_dir>", file=sys.stderr)
        return 2

    skill_dir = Path(sys.argv[1]).resolve()
    if not (skill_dir / "SKILL.md").exists():
        print(f"ERROR: {skill_dir}/SKILL.md not found", file=sys.stderr)
        return 2

    struct = check_structure(skill_dir)
    triggers = check_triggers(skill_dir)
    evals = check_evals(skill_dir)

    passed = struct["pass"] + triggers["pass"] + evals["pass"]
    warned = triggers.get("warn", [])
    failed = struct["fail"] + evals["fail"]

    result = {
        "target": skill_dir.name,
        "pass": passed,
        "warn": warned,
        "fail": failed,
        "grade": grade(len(passed), len(warned), len(failed)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["grade"] != "RED" else 1


if __name__ == "__main__":
    sys.exit(main())
