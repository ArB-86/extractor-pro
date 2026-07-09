from pathlib import Path

ROOT = Path("src")
TARGETS = ["evaluation", "pipeline", "question", "document"]

with open("repo_snapshot.txt", "w", encoding="utf-8") as out:
    for t in TARGETS:
        d = ROOT / t
        if not d.exists():
            continue

        out.write("=" * 120 + "\n")
        out.write(str(d) + "\n")
        out.write("=" * 120 + "\n\n")

        for f in sorted(d.rglob("*.py")):
            out.write("-" * 120 + "\n")
            out.write(str(f) + "\n")
            out.write("-" * 120 + "\n")
            try:
                out.write(f.read_text(encoding="utf-8"))
            except Exception as e:
                out.write(str(e))
            out.write("\n\n")

print("Done")
