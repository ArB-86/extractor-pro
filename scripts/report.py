import json
from pathlib import Path

ROOT = Path("output/json")

print("=" * 90)
print(
    f'{"FILE":15} '
    f'{"QUESTIONS":10} '
    f'{"MCQ":8} '
    f'{"NO_OPTIONS":12}'
)
print("=" * 90)

total_questions = 0
total_mcq = 0

for file in sorted(ROOT.glob("*.json")):

    with open(file, encoding="utf8") as f:
        data = json.load(f)

    questions = len(data)

    mcq = sum(
        1
        for q in data
        if q["options"]
    )

    no_options = questions - mcq

    total_questions += questions
    total_mcq += mcq

    print(
        f"{file.stem:15}"
        f"{questions:<10}"
        f"{mcq:<8}"
        f"{no_options:<12}"
    )

print("=" * 90)

print("TOTAL QUESTIONS :", total_questions)
print("TOTAL MCQs      :", total_mcq)
