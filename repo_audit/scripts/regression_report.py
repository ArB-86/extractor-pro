from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


LONG_QUESTION_THRESHOLD = 500


@dataclass(frozen=True)
class FileStats:
    relative_path: str
    total_questions: int
    total_question_length: int
    average_question_length: float
    duplicate_questions: int
    long_questions: int


@dataclass(frozen=True)
class ComparisonRow:
    relative_path: str
    baseline_questions: int
    current_questions: int
    delta: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare current extraction results against a baseline directory.",
    )
    parser.add_argument(
        "--baseline",
        required=True,
        help="Path to the baseline output/json directory to compare against.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace_root = resolve_workspace_root()
    current_root = resolve_current_root()
    report_path = workspace_root / "output" / "reports" / "regression_report.txt"
    baseline_root = resolve_baseline_root(args.baseline)

    current_stats = collect_stats(current_root)
    baseline_stats = collect_stats(baseline_root)
    comparisons = compare_counts(current_stats, baseline_stats)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        format_report(current_root, baseline_root, current_stats, baseline_stats, comparisons),
        encoding="utf8",
    )

    print(report_path)


def resolve_current_root() -> Path:
    from pathlib import Path

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    OUTER_OUTPUT = PROJECT_ROOT.parent / "output" / "json"
    INNER_OUTPUT = PROJECT_ROOT / "output" / "json"

    if OUTER_OUTPUT.exists() and any(OUTER_OUTPUT.rglob("*.json")):
        return OUTER_OUTPUT
    elif INNER_OUTPUT.exists() and any(INNER_OUTPUT.rglob("*.json")):
        return INNER_OUTPUT
    else:
        raise RuntimeError(
            f"No JSON files found.\n"
            f"Checked:\n"
            f"  {OUTER_OUTPUT}\n"
            f"  {INNER_OUTPUT}"
        )


def resolve_baseline_root(baseline_arg: str) -> Path:
    baseline_root = Path(baseline_arg).expanduser().resolve()

    if not baseline_root.exists():
        raise RuntimeError(
            f"Baseline directory does not exist:\n{baseline_root}"
        )

    if not any(baseline_root.rglob("*.json")):
        raise RuntimeError(
            f"No JSON files found in baseline:\n{baseline_root}"
        )

    return baseline_root


def resolve_workspace_root() -> Path:
    script_root = Path(__file__).resolve().parent.parent
    candidates = [script_root, script_root.parent]

    for candidate in candidates:
        json_root = candidate / "output" / "json"
        if json_root.exists() and any(json_root.rglob("*.json")):
            return candidate

    return script_root


def resolve_input_root(path: Path, workspace_root: Path) -> Path:
    resolved = path.expanduser()
    if not resolved.is_absolute():
        resolved = resolved.resolve()

    if resolved.exists() and any(resolved.rglob("*.json")):
        return resolved

    fallback = (workspace_root / path).resolve()
    if fallback.exists() and any(fallback.rglob("*.json")):
        return fallback

    return resolved


def collect_stats(root: Path) -> dict[str, FileStats]:
    stats: dict[str, FileStats] = {}

    if not root.exists():
        return stats

    for file_path in sorted(root.rglob("*.json")):
        relative_path = str(file_path.relative_to(root))
        payload = load_json(file_path)
        records = extract_records(payload)
        question_texts = [normalize_text(record.get("question_text")) for record in records]
        question_lengths = [len(text) for text in question_texts]

        stats[relative_path] = FileStats(
            relative_path=relative_path,
            total_questions=len(records),
            total_question_length=sum(question_lengths),
            average_question_length=mean(question_lengths) if question_lengths else 0.0,
            duplicate_questions=count_duplicate_questions(question_texts),
            long_questions=sum(1 for length in question_lengths if length > LONG_QUESTION_THRESHOLD),
        )

    return stats


def load_json(file_path: Path) -> Any:
    with file_path.open("r", encoding="utf8") as handle:
        return json.load(handle)


def extract_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        questions = payload.get("questions")
        if isinstance(questions, list):
            return [item for item in questions if isinstance(item, dict)]

        if any(key in payload for key in ("question_text", "question_id", "chapter", "subject")):
            return [payload]

    return []


def normalize_text(value: Any) -> str:
    if isinstance(value, str):
        return " ".join(value.split()).strip()
    return ""


def count_duplicate_questions(question_texts: list[str]) -> int:
    seen: set[str] = set()
    duplicates = 0

    for text in question_texts:
        normalized = text.casefold()
        if not normalized:
            continue
        if normalized in seen:
            duplicates += 1
            continue
        seen.add(normalized)

    return duplicates


def compare_counts(
    current_stats: dict[str, FileStats],
    baseline_stats: dict[str, FileStats],
) -> list[ComparisonRow]:
    all_paths = sorted(set(current_stats) | set(baseline_stats))
    comparisons: list[ComparisonRow] = []

    for relative_path in all_paths:
        baseline_questions = baseline_stats.get(
            relative_path,
            FileStats(relative_path, 0, 0, 0.0, 0, 0),
        ).total_questions
        current_questions = current_stats.get(
            relative_path,
            FileStats(relative_path, 0, 0, 0.0, 0, 0),
        ).total_questions
        comparisons.append(
            ComparisonRow(
                relative_path=relative_path,
                baseline_questions=baseline_questions,
                current_questions=current_questions,
                delta=current_questions - baseline_questions,
            )
        )

    return comparisons


def format_report(
    current_root: Path,
    baseline_root: Path,
    current_stats: dict[str, FileStats],
    baseline_stats: dict[str, FileStats],
    comparisons: list[ComparisonRow],
) -> str:
    current_total_questions, current_total_length, current_average_length = aggregate_totals(current_stats.values())
    baseline_total_questions, baseline_total_length, baseline_average_length = aggregate_totals(baseline_stats.values())
    current_duplicates = sum(item.duplicate_questions for item in current_stats.values())
    baseline_duplicates = sum(item.duplicate_questions for item in baseline_stats.values())
    current_long_questions = sum(item.long_questions for item in current_stats.values())
    baseline_long_questions = sum(item.long_questions for item in baseline_stats.values())

    increased, decreased, identical = split_comparisons(comparisons)
    net_change = current_total_questions - baseline_total_questions
    regressions = sorted(
        (row for row in comparisons if row.delta < 0),
        key=lambda row: (row.delta, row.relative_path),
    )[:20]
    improvements = sorted(
        (row for row in comparisons if row.delta > 0),
        key=lambda row: (-row.delta, row.relative_path),
    )[:20]

    lines = [
        "REGRESSION REPORT",
        "=" * 90,
        f"Current root               : {current_root}",
        f"Baseline root              : {baseline_root}",
        f"Current total questions    : {current_total_questions}",
        f"Baseline total questions   : {baseline_total_questions}",
        f"Current total length       : {current_total_length}",
        f"Baseline total length      : {baseline_total_length}",
        f"Current average length     : {current_average_length:.2f}",
        f"Baseline average length    : {baseline_average_length:.2f}",
        f"Current duplicate questions: {current_duplicates}",
        f"Baseline duplicate questions: {baseline_duplicates}",
        f"Current questions >500     : {current_long_questions}",
        f"Baseline questions >500    : {baseline_long_questions}",
        f"Net change                 : {net_change:+d}",
        "",
        f"PDFs with increased question count : {len(increased)}",
        f"PDFs with decreased question count : {len(decreased)}",
        f"PDFs with identical count          : {len(identical)}",
        "",
        "TOP 20 BIGGEST REGRESSIONS",
    ]

    lines.extend(format_rows(regressions))
    lines.append("")
    lines.append("TOP 20 BIGGEST IMPROVEMENTS")
    lines.extend(format_rows(improvements))

    return "\n".join(lines) + "\n"


def aggregate_totals(stats: list[FileStats] | Any) -> tuple[int, int, float]:
    total_questions = 0
    total_length = 0

    for item in stats:
        total_questions += item.total_questions
        total_length += item.total_question_length

    if total_questions == 0:
        return 0, 0, 0.0

    return total_questions, total_length, total_length / total_questions


def split_comparisons(comparisons: list[ComparisonRow]) -> tuple[list[ComparisonRow], list[ComparisonRow], list[ComparisonRow]]:
    increased: list[ComparisonRow] = []
    decreased: list[ComparisonRow] = []
    identical: list[ComparisonRow] = []

    for row in comparisons:
        if row.delta > 0:
            increased.append(row)
        elif row.delta < 0:
            decreased.append(row)
        else:
            identical.append(row)

    return increased, decreased, identical


def format_rows(rows: list[ComparisonRow]) -> list[str]:
    if not rows:
        return ["(none)"]

    formatted: list[str] = []
    for row in rows[:20]:
        formatted.append(
            f"{row.relative_path} | baseline={row.baseline_questions} | current={row.current_questions} | delta={row.delta:+d}"
        )
    return formatted


if __name__ == "__main__":
    main()