from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 90.0


@dataclass(slots=True)
class Question:
    number: str
    text: str


@dataclass(slots=True)
class Match:
    gt: Question | None
    pred: Question | None
    score: float


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("ﬁ", "fi")
    text = text.replace("ﬂ", "fl")
    text = text.replace("—", "-")
    text = text.replace("–", "-")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return text.strip()


def load_ground_truth(path: Path) -> list[Question]:
    data = json.loads(path.read_text(encoding="utf-8"))
    output = []
    for item in data:
        output.append(
            Question(
                number=str(item["number"]),
                text=item["text"],
            )
        )
    return output


def load_predictions(path: Path) -> list[Question]:
    output = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            number = obj.get("question_number") or obj.get("number") or ""
            text = obj.get("question_text") or obj.get("text") or ""
            output.append(
                Question(
                    number=str(number),
                    text=text,
                )
            )
    return output


def similarity(a: Question, b: Question) -> float:
    if a.number and b.number:
        if a.number != b.number:
            return 0.0
    return fuzz.token_sort_ratio(
        normalize(a.text),
        normalize(b.text),
    )


def match_questions(
    ground_truth: list[Question],
    predictions: list[Question],
) -> list[Match]:
    used = set()
    matches = []

    for gt in ground_truth:
        best_score = -1.0
        best_idx = None
        for i, pred in enumerate(predictions):
            if i in used:
                continue
            score = similarity(gt, pred)
            if score > best_score:
                best_score = score
                best_idx = i

        if best_idx is not None and best_score >= SIMILARITY_THRESHOLD:
            used.add(best_idx)
            matches.append(
                Match(
                    gt=gt,
                    pred=predictions[best_idx],
                    score=best_score,
                )
            )
        else:
            matches.append(
                Match(
                    gt=gt,
                    pred=None,
                    score=0,
                )
            )

    for i, pred in enumerate(predictions):
        if i not in used:
            matches.append(
                Match(
                    gt=None,
                    pred=pred,
                    score=0,
                )
            )

    return matches


# ------------------------------------------------------------
# Part 2
# ------------------------------------------------------------

@dataclass(slots=True)
class Metrics:
    ground_truth: int
    predicted: int
    matched: int
    missed: int
    false_positive: int
    duplicates: int
    merged: int
    split: int
    precision: float
    recall: float
    f1: float


def detect_duplicates(predictions: list[Question]) -> int:
    seen = set()
    duplicates = 0
    for q in predictions:
        key = (q.number, normalize(q.text))
        if key in seen:
            duplicates += 1
        else:
            seen.add(key)
    return duplicates


def detect_merged(matches: list[Match]) -> int:
    merged = 0
    for m in matches:
        if m.gt is None or m.pred is None:
            continue
        gt_words = len(normalize(m.gt.text).split())
        pred_words = len(normalize(m.pred.text).split())
        if pred_words > gt_words * 1.75:
            merged += 1
    return merged


def detect_split(matches: list[Match]) -> int:
    split = 0
    for m in matches:
        if m.gt is None or m.pred is None:
            continue
        gt_words = len(normalize(m.gt.text).split())
        pred_words = len(normalize(m.pred.text).split())
        if gt_words > pred_words * 1.75:
            split += 1
    return split


def compute_metrics(
    ground_truth: list[Question],
    predictions: list[Question],
    matches: list[Match],
) -> Metrics:
    matched = sum(1 for m in matches if m.gt is not None and m.pred is not None)
    missed = sum(1 for m in matches if m.gt is not None and m.pred is None)
    false_positive = sum(1 for m in matches if m.gt is None and m.pred is not None)

    duplicates = detect_duplicates(predictions)
    merged = detect_merged(matches)
    split = detect_split(matches)

    precision = matched / len(predictions) if predictions else 0.0
    recall = matched / len(ground_truth) if ground_truth else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return Metrics(
        ground_truth=len(ground_truth),
        predicted=len(predictions),
        matched=matched,
        missed=missed,
        false_positive=false_positive,
        duplicates=duplicates,
        merged=merged,
        split=split,
        precision=precision,
        recall=recall,
        f1=f1,
    )


def print_report(metrics: Metrics) -> None:
    print()
    print("=" * 60)
    print("Extractor-Pro Evaluation")
    print("=" * 60)
    print()
    print(f"Ground Truth      : {metrics.ground_truth}")
    print(f"Predicted         : {metrics.predicted}")
    print(f"Matched           : {metrics.matched}")
    print(f"Missed            : {metrics.missed}")
    print(f"False Positive    : {metrics.false_positive}")
    print(f"Duplicates        : {metrics.duplicates}")
    print(f"Merged            : {metrics.merged}")
    print(f"Split             : {metrics.split}")
    print()
    print(f"Precision         : {metrics.precision:.2%}")
    print(f"Recall            : {metrics.recall:.2%}")
    print(f"F1                : {metrics.f1:.2%}")


# ------------------------------------------------------------
# Part 3
# ------------------------------------------------------------

def write_markdown_report(metrics: Metrics, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Extractor-Pro Evaluation",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Ground Truth | {metrics.ground_truth} |",
        f"| Predicted | {metrics.predicted} |",
        f"| Matched | {metrics.matched} |",
        f"| Missed | {metrics.missed} |",
        f"| False Positive | {metrics.false_positive} |",
        f"| Duplicates | {metrics.duplicates} |",
        f"| Merged | {metrics.merged} |",
        f"| Split | {metrics.split} |",
        "",
        f"| Precision | {metrics.precision:.2%} |",
        f"| Recall | {metrics.recall:.2%} |",
        f"| F1 | {metrics.f1:.2%} |",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description="Extractor-Pro evaluator")
    parser.add_argument("ground_truth", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("evaluation/reports/report.md"),
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=90.0,
    )
    return parser


def main() -> int:
    global SIMILARITY_THRESHOLD

    parser = build_parser()
    args = parser.parse_args()

    SIMILARITY_THRESHOLD = args.threshold

    if not args.ground_truth.exists():
        print(f"Ground truth not found: {args.ground_truth}", file=sys.stderr)
        return 2

    if not args.predictions.exists():
        print(f"Predictions not found: {args.predictions}", file=sys.stderr)
        return 2

    ground_truth = load_ground_truth(args.ground_truth)
    predictions = load_predictions(args.predictions)

    matches = match_questions(ground_truth, predictions)
    metrics = compute_metrics(ground_truth, predictions, matches)

    print_report(metrics)
    write_markdown_report(metrics, args.report)

    print()
    print(f"Markdown report written to: {args.report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
