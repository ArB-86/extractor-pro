from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.curriculum import CurriculumAuditor


def path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit NCERT mathematics PDFs against the approved curriculum map."
    )
    parser.add_argument(
        "roots",
        nargs="+",
        help="PDF source folders, e.g. maths_pdf maths_exampler 'cbse sample paper_maths'",
    )
    parser.add_argument(
        "--mapping",
        default="datasets/curriculum/curriculum_mapping.json",
        help="Curriculum mapping JSON file.",
    )
    parser.add_argument(
        "--out",
        default="datasets/curriculum/reports",
        help="Report output folder.",
    )
    parser.add_argument(
        "--hash",
        action="store_true",
        help="Compute SHA256 for every PDF. Slower, but better for provenance.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Move archived PDFs into the archive folder. Default is dry-run only.",
    )
    parser.add_argument(
        "--archive-dir",
        default="datasets/archive/old_ncert",
        help="Destination for archived PDFs when --apply is used.",
    )
    return parser.parse_args()


def unique_destination(base_dir: Path, source_root: Path, pdf_path: Path) -> Path:
    relative = pdf_path.relative_to(source_root)
    destination = base_dir / relative
    if not destination.exists():
        return destination

    counter = 2
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> None:
    args = parse_args()
    roots = [Path(root).resolve() for root in args.roots]

    auditor = CurriculumAuditor(args.mapping)
    results = auditor.audit_roots(roots, compute_hash=args.hash)
    auditor.write_reports(results, args.out)

    counts = {action: sum(1 for result in results if result.action == action) for action in ("active", "archive", "review")}
    print("Curriculum audit complete")
    print(f"Active : {counts['active']}")
    print(f"Archive: {counts['archive']}")
    print(f"Review : {counts['review']}")
    print(f"Reports: {Path(args.out).resolve()}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to move archive candidates.")
        return

    archive_dir = Path(args.archive_dir).resolve()
    moved = 0
    root_by_path = {root: root for root in roots}

    for result in results:
        if result.action != "archive":
            continue
        pdf_path = Path(result.pdf_path).resolve()
        source_root = next((root for root in root_by_path if path_is_relative_to(pdf_path, root)), pdf_path.parent)
        destination = unique_destination(archive_dir, source_root, pdf_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf_path), str(destination))
        moved += 1

    print(f"Moved {moved} old-curriculum PDFs to {archive_dir}")


if __name__ == "__main__":
    main()
