from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PDF_CODE_RE = re.compile(r"^(?P<prefix>[a-z]+)(?P<chapter>\d{2})(?P<suffix>[a-z]*)$", re.I)


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    if not phrase:
        return False
    return f" {phrase} " in f" {text} "


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


@dataclass(frozen=True)
class ChapterRule:
    chapter_id: str
    class_no: int
    subject: str
    chapter_no: int
    chapter_name: str
    status: str
    source_types: set[str] = field(default_factory=set)
    pdf_codes: set[str] = field(default_factory=set)
    aliases: set[str] = field(default_factory=set)
    previous_names: set[str] = field(default_factory=set)


@dataclass
class AuditResult:
    action: str
    reason: str
    pdf_path: str
    relative_path: str
    filename: str
    folder_hint: str
    source_type: str
    class_no: int | None
    chapter_no: int | None
    chapter_id: str
    chapter_name: str
    status: str
    confidence: float
    sha256: str = ""
    evidence: str = ""


class CurriculumAuditor:
    def __init__(self, mapping_path: str | Path):
        self.mapping_path = Path(mapping_path)
        self.mapping = json.loads(self.mapping_path.read_text(encoding="utf8"))
        self.active_rules: list[ChapterRule] = []
        self.archive_rules: list[ChapterRule] = []
        self._load_rules()

    def _load_rules(self) -> None:
        for class_entry in self.mapping.get("classes", []):
            class_no = int(class_entry["class_no"])
            subject = class_entry.get("subject", self.mapping.get("subject", "Mathematics"))

            for chapter in class_entry.get("chapters", []):
                rule = ChapterRule(
                    chapter_id=chapter["chapter_id"],
                    class_no=class_no,
                    subject=subject,
                    chapter_no=int(chapter["chapter_no"]),
                    chapter_name=chapter["chapter_name"],
                    status=chapter["status"],
                    source_types=set(chapter.get("source_types", [])),
                    pdf_codes={code.lower() for code in chapter.get("pdf_codes", [])},
                    aliases={normalize_text(x) for x in chapter.get("aliases", [])},
                    previous_names={normalize_text(x) for x in chapter.get("previous_names", [])},
                )
                if rule.status == "active":
                    self.active_rules.append(rule)
                else:
                    self.archive_rules.append(rule)

    def audit_roots(self, roots: list[str | Path], compute_hash: bool = False) -> list[AuditResult]:
        results: list[AuditResult] = []
        for root in roots:
            root_path = Path(root)
            for pdf_path in sorted(root_path.rglob("*.pdf")):
                results.append(self.audit_pdf(pdf_path, root_path, compute_hash=compute_hash))
        return results

    def audit_pdf(self, pdf_path: str | Path, root_path: str | Path, compute_hash: bool = False) -> AuditResult:
        pdf = Path(pdf_path)
        root = Path(root_path)
        relative = str(pdf.relative_to(root)) if path_is_relative_to(pdf, root) else str(pdf)

        source_type = self._source_type(pdf)
        class_no = self._class_from_pdf(pdf)
        chapter_no = self._chapter_from_pdf_code(pdf)
        probe_text = self._pdf_probe_text(pdf)
        search_text = normalize_text(" ".join([pdf.stem, pdf.parent.name, probe_text]))

        archived_from_content = self._match_rule(
            self.archive_rules,
            pdf,
            source_type,
            class_no,
            chapter_no,
            search_text,
            allow_chapter_number_match=False,
            require_text_match=True,
        )
        if archived_from_content:
            return self._result(
                "archive",
                "PDF text matches removed or renamed old-curriculum chapter",
                pdf,
                relative,
                source_type,
                class_no,
                chapter_no,
                archived_from_content,
                0.92,
                compute_hash,
                probe_text,
            )

        active = self._match_rule(
            self.active_rules,
            pdf,
            source_type,
            class_no,
            chapter_no,
            search_text,
            allow_chapter_number_match=False,
        )
        if active:
            confidence = 0.95 if pdf.stem.lower() in active.pdf_codes else 0.82
            return self._result(
                "active",
                "matches active curriculum mapping",
                pdf,
                relative,
                source_type,
                class_no,
                chapter_no,
                active,
                confidence,
                compute_hash,
                probe_text,
            )

        archived = self._match_rule(
            self.archive_rules,
            pdf,
            source_type,
            class_no,
            chapter_no,
            search_text,
            allow_chapter_number_match=False,
        )
        if archived:
            return self._result(
                "archive",
                "matches removed or renamed old-curriculum chapter",
                pdf,
                relative,
                source_type,
                class_no,
                chapter_no,
                archived,
                0.86,
                compute_hash,
                probe_text,
            )

        return AuditResult(
            action="review",
            reason="could not prove latest-curriculum membership",
            pdf_path=str(pdf),
            relative_path=relative,
            filename=pdf.name,
            folder_hint=pdf.parent.name,
            source_type=source_type,
            class_no=class_no,
            chapter_no=chapter_no,
            chapter_id="",
            chapter_name="",
            status="unknown",
            confidence=0.0,
            sha256=file_sha256(pdf) if compute_hash else "",
            evidence=probe_text[:300],
        )

    def write_reports(self, results: list[AuditResult], output_dir: str | Path) -> None:
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        rows = [result.__dict__ for result in results]
        (output / "curriculum_audit.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False),
            encoding="utf8",
        )

        with (output / "curriculum_audit.csv").open("w", newline="", encoding="utf8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["action"])
            writer.writeheader()
            writer.writerows(rows)

        for action in ("active", "archive", "review"):
            subset = [row for row in rows if row["action"] == action]
            (output / f"{action}_pdfs.json").write_text(
                json.dumps(subset, indent=2, ensure_ascii=False),
                encoding="utf8",
            )

    def _match_rule(
        self,
        rules: list[ChapterRule],
        pdf: Path,
        source_type: str,
        class_no: int | None,
        chapter_no: int | None,
        search_text: str,
        allow_chapter_number_match: bool,
        require_text_match: bool = False,
    ) -> ChapterRule | None:
        stem = pdf.stem.lower()
        for rule in rules:
            if class_no is not None and rule.class_no != class_no:
                continue
            if rule.source_types and source_type not in rule.source_types:
                continue
            names = {normalize_text(rule.chapter_name), *rule.aliases, *rule.previous_names}
            text_matches = any(contains_phrase(search_text, name) for name in names)
            if require_text_match:
                if text_matches:
                    return rule
                continue
            if stem in rule.pdf_codes:
                return rule
            if allow_chapter_number_match and chapter_no is not None and rule.chapter_no == chapter_no:
                return rule
            if text_matches:
                return rule
        return None

    def _result(
        self,
        action: str,
        reason: str,
        pdf: Path,
        relative: str,
        source_type: str,
        class_no: int | None,
        chapter_no: int | None,
        rule: ChapterRule,
        confidence: float,
        compute_hash: bool,
        evidence: str,
    ) -> AuditResult:
        return AuditResult(
            action=action,
            reason=reason,
            pdf_path=str(pdf),
            relative_path=relative,
            filename=pdf.name,
            folder_hint=pdf.parent.name,
            source_type=source_type,
            class_no=class_no,
            chapter_no=chapter_no,
            chapter_id=rule.chapter_id,
            chapter_name=rule.chapter_name,
            status=rule.status,
            confidence=confidence,
            sha256=file_sha256(pdf) if compute_hash else "",
            evidence=evidence[:300],
        )

    def _pdf_probe_text(self, pdf: Path) -> str:
        try:
            import fitz  # type: ignore
        except Exception:
            return ""

        try:
            with fitz.open(pdf) as document:
                snippets: list[str] = []
                for page in document[: min(2, len(document))]:
                    snippets.append(page.get_text("text"))
                return "\n".join(snippets)
        except Exception:
            return ""

    def _source_type(self, pdf: Path) -> str:
        parts = normalize_text(" ".join(pdf.parts))
        if "sample paper" in parts or "sample" in parts:
            return "sample_paper"
        if "exemplar" in parts or "exampler" in parts:
            return "exemplar"
        return "textbook"

    def _class_from_pdf(self, pdf: Path) -> int | None:
        text = normalize_text(" ".join(pdf.parts))
        class_match = re.search(r"\bclass\s*(\d{1,2})\b", text)
        if class_match:
            return int(class_match.group(1))

        stem = pdf.stem.lower()
        prefix_map: dict[str, int] = self.mapping.get("pdf_prefix_classes", {})
        for prefix, class_no in prefix_map.items():
            if stem.startswith(prefix.lower()):
                return int(class_no)

        folder_map: dict[str, int] = self.mapping.get("pdf_folder_classes", {})
        for part in pdf.parts:
            class_no = folder_map.get(part.lower())
            if class_no is not None:
                return int(class_no)
        return None

    def _chapter_from_pdf_code(self, pdf: Path) -> int | None:
        stem = pdf.stem.lower()
        code_match = re.match(r"^[a-z]+(?P<book>\d)(?P<chapter>\d{2})(?P<suffix>[a-z]*)$", stem)
        if code_match:
            return int(code_match.group("chapter"))

        match = PDF_CODE_RE.match(stem)
        if not match:
            return None
        try:
            return int(match.group("chapter"))
        except ValueError:
            return None
