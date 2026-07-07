from pathlib import Path

from pipeline.curriculum import CurriculumAuditor


MAPPING = Path("datasets/curriculum/curriculum_mapping.json")


def touch_pdf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.4\n%%EOF\n")


def test_active_pdf_code_match(tmp_path):
    pdf = tmp_path / "maths_pdf" / "jemh1dd" / "jemh106.pdf"
    touch_pdf(pdf)

    result = CurriculumAuditor(MAPPING).audit_pdf(pdf, tmp_path)

    assert result.action == "active"
    assert result.chapter_id == "math-10-06"
    assert result.chapter_name == "Triangles"


def test_removed_chapter_name_goes_to_archive(tmp_path):
    pdf = tmp_path / "maths_pdf" / "class_10" / "Constructions.pdf"
    touch_pdf(pdf)

    result = CurriculumAuditor(MAPPING).audit_pdf(pdf, tmp_path)

    assert result.action == "archive"
    assert result.status == "removed"


def test_unknown_pdf_goes_to_review(tmp_path):
    pdf = tmp_path / "maths_pdf" / "mystery_chapter.pdf"
    touch_pdf(pdf)

    result = CurriculumAuditor(MAPPING).audit_pdf(pdf, tmp_path)

    assert result.action == "review"
    assert result.reason == "could not prove latest-curriculum membership"


def test_dataset_path_does_not_match_sets(tmp_path):
    pdf = tmp_path / "datasets" / "raw_docs" / "gegp1dd" / "gegp101.pdf"
    touch_pdf(pdf)

    result = CurriculumAuditor(MAPPING).audit_pdf(pdf, tmp_path)

    assert result.action == "review"
    assert result.chapter_id == ""
