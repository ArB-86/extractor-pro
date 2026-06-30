from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

JSON_ROOT = Path("/home/jiitcah.05/nlp_research_module/extractor_pro/output/json")
REPORT_ROOT = Path("/home/jiitcah.05/nlp_research_module/extractor_pro/output/reports")

CSV_FILE = REPORT_ROOT / "parser_benchmark.csv"
TXT_FILE = REPORT_ROOT / "parser_benchmark.txt"


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def analyze_json(path: Path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lengths = []
    duplicate_counter = Counter()

    over500 = 0
    over1500 = 0

    for q in data:

        text = (
            q.get("question")
            or q.get("question_text")
            or ""
        )

        n = len(text)

        lengths.append(n)

        duplicate_counter[normalize(text)] += 1

        if n > 500:
            over500 += 1

        if n > 1500:
            over1500 += 1

    duplicates = sum(
        count - 1
        for count in duplicate_counter.values()
        if count > 1
    )

    if lengths:
        avg = statistics.mean(lengths)
        med = statistics.median(lengths)
        mx = max(lengths)
    else:
        avg = med = mx = 0

    return {
        "pdf": path.stem,
        "questions": len(lengths),
        "average_length": round(avg, 2),
        "median_length": round(med, 2),
        "maximum_length": mx,
        "over500": over500,
        "over1500": over1500,
        "duplicates": duplicates,
    }


def main():

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    rows = []

    for file in sorted(JSON_ROOT.glob("*.json")):
        rows.append(analyze_json(file))

    rows.sort(
        key=lambda r: (
            -r["over1500"],
            -r["maximum_length"],
            -r["average_length"],
        )
    )

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "pdf",
                "questions",
                "average_length",
                "median_length",
                "maximum_length",
                "over500",
                "over1500",
                "duplicates",
            ],
        )

        writer.writeheader()

        writer.writerows(rows)

    with open(TXT_FILE, "w", encoding="utf-8") as f:

        f.write("PARSER BENCHMARK\n")
        f.write("=" * 80 + "\n\n")

        f.write("TOP 25 PDFs BY LONG QUESTIONS\n\n")

        for row in rows[:25]:

            f.write(
                f"{row['pdf']:15} "
                f"questions={row['questions']:4} "
                f"avg={row['average_length']:7.2f} "
                f"max={row['maximum_length']:6} "
                f">500={row['over500']:4} "
                f">1500={row['over1500']:3} "
                f"dup={row['duplicates']:3}\n"
            )

    print(CSV_FILE)
    print(TXT_FILE)


if __name__ == "__main__":
    main()