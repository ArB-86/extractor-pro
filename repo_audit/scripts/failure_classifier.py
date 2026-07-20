from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

ROOT = Path("/home/jiitcah.05/nlp_research_module/extractor_pro/output/json")
REPORT = Path("/home/jiitcah.05/nlp_research_module/extractor_pro/output/reports/failure_report.txt")

HEADINGS = [
    "Figure it Out",
    "Math Talk",
    "Activity",
    "Try This",
    "Example",
    "Exercise",
    "Summary",
    "Project",
    "Making Solids",
    "Representation of",
    "Shortest Paths",
    "Projections",
    "Isometric",
    "Drawing on Isometric",
    "Build it in Your Imagination",
]

counter = Counter()
examples = {}

for file in sorted(ROOT.glob("*.json")):

    data = json.loads(file.read_text())

    for q in data:

        text = q.get("question_text") or q.get("question") or ""

        if len(text) < 500:
            continue

        found = False

        for h in HEADINGS:
            if h.lower() in text.lower():
                counter[h] += 1
                examples.setdefault(h, []).append(
                    (
                        file.stem,
                        q.get("question_id", q.get("id")),
                        len(text),
                    )
                )
                found = True

        if not found:
            counter["UNKNOWN"] += 1
            examples.setdefault("UNKNOWN", []).append(
                {
                    "pdf": file.stem,
                    "question_id": q.get("question_id", q.get("id")),
                    "length": len(text),
                    "first_500": text[:500],
                    "last_500": text[-500:],
                }
            )

with REPORT.open("w") as f:

    f.write("FAILURE CLASSIFIER REPORT\n")
    f.write("=" * 80 + "\n\n")

    for name, count in counter.most_common():

        f.write(f"{name:35} {count}\n")

        if name == "UNKNOWN":
            for item in examples[name][:20]:
                f.write("=" * 80 + "\n")
                f.write(f"PDF: {item['pdf']}\n")
                f.write(f"Length: {item['length']}\n\n")
                f.write(item["first_500"])
                f.write("\n\n...\n\n")
                f.write(item["last_500"])
                f.write("\n\n")
        else:
            for pdf, qid, length in examples[name][:5]:
                f.write(f"    {pdf:15} q={qid} len={length}\n")

        f.write("\n")

print(REPORT)