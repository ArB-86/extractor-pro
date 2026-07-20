import json
from pathlib import Path
from collections import Counter

ROOT = Path("output/json")


def normalize(text: str) -> str:
    return " ".join(text.split()).strip().lower()


print("=" * 120)
print(
    f'{"FILE":15}'
    f'{"Q":>6}'
    f'{"EMPTY":>8}'
    f'{"SHORT":>8}'
    f'{"LONG":>8}'
    f'{"MCQMISS":>10}'
    f'{"DUPID":>8}'
    f'{"DUPTXT":>8}'
    f'{"BADPAGE":>9}'
    f'{"QUALITY":>10}'
)
print("=" * 120)

overall = {
    "questions": 0,
    "empty": 0,
    "short": 0,
    "long": 0,
    "mcq": 0,
    "dupid": 0,
    "duptxt": 0,
    "badpage": 0,
}

for file in sorted(ROOT.glob("*.json")):

    with open(file, encoding="utf8") as f:
        questions = json.load(f)

    empty = 0
    short = 0
    long = 0
    mcq_missing = 0
    badpage = 0
    duplicate_ids = 0
    ids = set()
    texts = []

    for q in questions:

        # Duplicate detection (with print)
        key = (
            q["exercise"],
            q["id"]
        )

        if key in ids:
            duplicate_ids += 1
            print(
                f"\n[DUPLICATE ID] "
                f"{file.stem} "
                f"Exercise={q['exercise']} "
                f"ID={q['id']}"
            )
        else:
            ids.add(key)

        txt = q["question"].strip()

        texts.append(normalize(txt))

        if len(txt) == 0:
            empty += 1

        # SHORT condition
        if (
            0 < len(txt) < 25
            and "(A)" not in txt
            and "\n" not in txt
        ):
            short += 1

        # LONG condition (with print)
        if len(txt) > 1200:
            long += 1
            print("\n" + "=" * 80)
            print(file.stem)
            print(
                f"Exercise={q['exercise']} "
                f"ID={q['id']}"
            )
            print("Length:", len(txt))
            print(txt[:500])

        if (
            "(A)" in txt
            and len(q["options"]) == 0
        ):
            mcq_missing += 1

        if q["page_end"] < q["page_start"]:
            badpage += 1

    dupid = duplicate_ids
    duptxt = sum(v - 1 for v in Counter(texts).values() if v > 1)

    issues = (
        empty
        + short
        + long
        + mcq_missing
        + dupid
        + duptxt
        + badpage
    )

    total = max(len(questions), 1)

    quality = 100 * (1 - issues / total)

    overall["questions"] += len(questions)
    overall["empty"] += empty
    overall["short"] += short
    overall["long"] += long
    overall["mcq"] += mcq_missing
    overall["dupid"] += dupid
    overall["duptxt"] += duptxt
    overall["badpage"] += badpage

    print(
        f"{file.stem:15}"
        f"{len(questions):>6}"
        f"{empty:>8}"
        f"{short:>8}"
        f"{long:>8}"
        f"{mcq_missing:>10}"
        f"{dupid:>8}"
        f"{duptxt:>8}"
        f"{badpage:>9}"
        f"{quality:>9.1f}%"
    )

print("=" * 120)

print(f"TOTAL QUESTIONS : {overall['questions']}")
print(f"EMPTY          : {overall['empty']}")
print(f"SHORT          : {overall['short']}")
print(f"LONG           : {overall['long']}")
print(f"MCQ MISSING    : {overall['mcq']}")
print(f"DUP IDS        : {overall['dupid']}")
print(f"DUP TEXT       : {overall['duptxt']}")
print(f"BAD PAGE       : {overall['badpage']}")