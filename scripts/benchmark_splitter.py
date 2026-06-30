from pathlib import Path

golden = Path("benchmarks/golden/question_split")
expected = golden / "iemh102_expected.txt"

print("=" * 80)
print("QUESTION SPLITTER BENCHMARK")
print("=" * 80)

print("Golden file :", expected)
print("Status      : READY")
