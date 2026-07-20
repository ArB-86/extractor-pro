from __future__ import annotations

import json
from pathlib import Path

from scripts.regression_report import collect_stats, compare_counts, format_report


def write_question_file(path: Path, questions: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            [{"question_text": question} for question in questions],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf8",
    )


def test_regression_report_summarizes_and_compares(tmp_path: Path) -> None:
    current_root = tmp_path / "current" / "output" / "json"
    baseline_root = tmp_path / "baseline" / "output" / "json"

    write_question_file(current_root / "a.json", ["one", "two", "two", "x" * 501])
    write_question_file(current_root / "nested" / "b.json", ["alpha", "beta"])

    write_question_file(baseline_root / "a.json", ["one", "two"])
    write_question_file(baseline_root / "nested" / "b.json", ["alpha", "beta", "gamma"])
    write_question_file(baseline_root / "c.json", ["delta"])

    current_stats = collect_stats(current_root)
    baseline_stats = collect_stats(baseline_root)
    comparisons = compare_counts(current_stats, baseline_stats)

    report = format_report(current_root, baseline_root, current_stats, baseline_stats, comparisons)

    assert "Current total questions    : 6" in report
    assert "Baseline total questions   : 6" in report
    assert "Current total length       : 519" in report
    assert "Baseline total length      : 25" in report
    assert "Current duplicate questions: 1" in report
    assert "Current questions >500     : 1" in report
    assert "PDFs with increased question count : 1" in report
    assert "PDFs with decreased question count : 2" in report
    assert "PDFs with identical count          : 0" in report
    assert "TOP 20 BIGGEST REGRESSIONS" in report
    assert "TOP 20 BIGGEST IMPROVEMENTS" in report