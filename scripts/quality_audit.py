"""Audit exported question JSON files."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any


def resolve_workspace_root() -> Path:
	script_root = Path(__file__).resolve().parent.parent
	for candidate in (script_root, script_root.parent):
		json_root = candidate / "output" / "json"
		if json_root.exists() and any(json_root.rglob("*.json")):
			return candidate
	return script_root


ROOT = resolve_workspace_root()
JSON_ROOT = ROOT / "output" / "json"
REPORTS_ROOT = ROOT / "output" / "reports"
REPORT_PATH = REPORTS_ROOT / "quality_report.txt"
LONG_QUESTIONS_PATH = REPORTS_ROOT / "long_questions.json"
DUPLICATE_QUESTIONS_PATH = REPORTS_ROOT / "duplicate_questions.json"
WORST_QUESTIONS_PATH = REPORTS_ROOT / "worst_questions.json"
LONG_QUESTION_THRESHOLD = 1500


@dataclass
class QuestionEntry:
	"""Normalized representation of one exported question."""

	source_file: str
	index: int
	question_id: str | None
	question_class: Any
	subject: str
	chapter: str
	question_text: str
	question_length: int
	raw: dict[str, Any]


@dataclass
class DuplicateRecord:
	source_file: str
	index: int
	question_id: str | None
	question_class: Any
	chapter: str
	question_length: int
	question_text: str


@dataclass
class DuplicateGroup:
	normalized_question_text: str
	records: list[DuplicateRecord]


@dataclass
class WorstQuestionEntry:
	pdf: str
	question_id: str | None
	question_class: Any
	chapter: str
	subject: str
	length: int
	question_text: str
	first_300_chars: str
	last_300_chars: str
	suspected_reason: str = "UNKNOWN"


@dataclass
class AuditSummary:
	total_json_files: int = 0
	total_questions: int = 0
	empty_question_text: int = 0
	duplicate_groups: int = 0
	duplicate_records: int = 0
	long_questions: int = 0
	missing_question_id: int = 0
	missing_class: int = 0
	missing_chapter: int = 0
	missing_subject: int = 0
	average_question_length: float = 0.0
	median_question_length: float = 0.0
	maximum_question_length: int = 0


def main() -> None:
	summary, long_questions, duplicate_groups, all_questions = audit_questions(JSON_ROOT)
	write_report(summary, REPORT_PATH)
	write_long_questions(long_questions, LONG_QUESTIONS_PATH)
	write_duplicate_questions(duplicate_groups, DUPLICATE_QUESTIONS_PATH)
	
	print("TOTAL:", len(all_questions))
	print("FIRST:", all_questions[0].question_length if all_questions else "EMPTY")
	
	write_worst_questions(all_questions, WORST_QUESTIONS_PATH)


def audit_questions(root: Path) -> tuple[AuditSummary, list[QuestionEntry], list[DuplicateGroup], list[QuestionEntry]]:
	summary = AuditSummary()
	lengths: list[int] = []
	all_questions: list[QuestionEntry] = []
	long_questions: list[QuestionEntry] = []
	duplicate_map: dict[str, list[QuestionEntry]] = {}

	json_files = sorted(root.rglob("*.json")) if root.exists() else []
	summary.total_json_files = len(json_files)

	for file_path in json_files:
		for entry in load_question_entries(file_path, root):
			all_questions.append(entry)
			summary.total_questions += 1
			lengths.append(entry.question_length)

			if is_missing_text(entry.question_text):
				summary.empty_question_text += 1
			else:
				normalized_text = normalize_question_text(entry.question_text)
				duplicate_map.setdefault(normalized_text, []).append(entry)

			if entry.question_length > LONG_QUESTION_THRESHOLD:
				summary.long_questions += 1
				long_questions.append(entry)

			if is_missing_question_id(entry.question_id):
				summary.missing_question_id += 1
			if is_missing_class(entry.question_class):
				summary.missing_class += 1
			if is_missing_text(entry.chapter):
				summary.missing_chapter += 1
			if is_missing_text(entry.subject):
				summary.missing_subject += 1

	if lengths:
		summary.average_question_length = mean(lengths)
		summary.median_question_length = median(lengths)
		summary.maximum_question_length = max(lengths)

	duplicate_groups = build_duplicate_groups(duplicate_map)
	summary.duplicate_groups = len(duplicate_groups)
	summary.duplicate_records = sum(len(group.records) for group in duplicate_groups)
	long_questions.sort(key=lambda item: (-item.question_length, item.source_file, item.index))
	all_questions.sort(key=lambda item: (-item.question_length, item.source_file, item.index))
	return summary, long_questions, duplicate_groups, all_questions


def load_question_entries(file_path: Path, root: Path) -> list[QuestionEntry]:
	with file_path.open("r", encoding="utf8") as handle:
		payload = json.load(handle)

	records = extract_records(payload)
	relative_path = str(file_path.relative_to(root))
	return [to_question_entry(record, relative_path, index) for index, record in enumerate(records, start=1)]


def extract_records(payload: Any) -> list[dict[str, Any]]:
	if isinstance(payload, list):
		return [item for item in payload if isinstance(item, dict)]

	if isinstance(payload, dict):
		questions = payload.get("questions")
		if isinstance(questions, list):
			return [item for item in questions if isinstance(item, dict)]

		if any(key in payload for key in ("question_text", "question_id", "chapter", "subject")):
			return [payload]

	return []


def to_question_entry(record: dict[str, Any], source_file: str, index: int) -> QuestionEntry:
	question_text = normalize_text(record.get("question_text"))
	return QuestionEntry(
		source_file=source_file,
		index=index,
		question_id=normalize_optional_text(record.get("question_id")),
		question_class=record.get("class"),
		subject=normalize_text(record.get("subject")),
		chapter=normalize_text(record.get("chapter")),
		question_text=question_text,
		question_length=len(question_text),
		raw=record,
	)


def normalize_text(value: Any) -> str:
	if isinstance(value, str):
		return value.strip()
	return ""


def normalize_optional_text(value: Any) -> str | None:
	text = normalize_text(value)
	return text or None


def normalize_question_text(value: str) -> str:
	return " ".join(value.casefold().split())


def is_missing_text(value: str) -> bool:
	return not value.strip()


def is_missing_question_id(value: str | None) -> bool:
	return value is None or not value.strip()


def is_missing_class(value: Any) -> bool:
	if value is None:
		return True

	if isinstance(value, str):
		stripped = value.strip()
		return not stripped or stripped == "0"

	return value == 0


def write_report(summary: AuditSummary, report_path: Path) -> None:
	report_path.parent.mkdir(parents=True, exist_ok=True)
	report_path.write_text(format_report(summary), encoding="utf8")


def write_long_questions(long_questions: list[QuestionEntry], output_path: Path) -> None:
	output_path.parent.mkdir(parents=True, exist_ok=True)
	payload = [long_question_to_dict(entry) for entry in long_questions]
	output_path.write_text(
		json.dumps(payload, indent=2, ensure_ascii=False),
		encoding="utf8",
	)


def write_duplicate_questions(duplicate_groups: list[DuplicateGroup], output_path: Path) -> None:
	output_path.parent.mkdir(parents=True, exist_ok=True)
	payload = [
		{
			"normalized_question_text": group.normalized_question_text,
			"records": [duplicate_record_to_dict(record) for record in group.records],
		}
		for group in duplicate_groups
	]
	output_path.write_text(
		json.dumps(payload, indent=2, ensure_ascii=False),
		encoding="utf8",
	)


def write_worst_questions(all_questions: list[QuestionEntry], output_path: Path) -> None:
	output_path.parent.mkdir(parents=True, exist_ok=True)
	payload = [worst_question_to_dict(entry) for entry in all_questions[:100]]
	
	print("PAYLOAD:", len(payload))
	print(payload[:1])
	
	output_path.write_text(
		json.dumps(payload, indent=2, ensure_ascii=False),
		encoding="utf8",
	)


def build_duplicate_groups(duplicate_map: dict[str, list[QuestionEntry]]) -> list[DuplicateGroup]:
	groups: list[DuplicateGroup] = []
	for normalized_text, entries in duplicate_map.items():
		if len(entries) < 2:
			continue
		records = [to_duplicate_record(entry) for entry in sorted(entries, key=lambda item: (item.source_file, item.index))]
		groups.append(DuplicateGroup(normalized_question_text=normalized_text, records=records))
	groups.sort(key=lambda group: (-len(group.records), group.normalized_question_text))
	return groups


def to_duplicate_record(entry: QuestionEntry) -> DuplicateRecord:
	return DuplicateRecord(
		source_file=entry.source_file,
		index=entry.index,
		question_id=entry.question_id,
		question_class=entry.question_class,
		chapter=entry.chapter,
		question_length=entry.question_length,
		question_text=entry.question_text,
	)


def duplicate_record_to_dict(record: DuplicateRecord) -> dict[str, Any]:
	return {
		"source_file": record.source_file,
		"index": record.index,
		"question_id": record.question_id,
		"class": record.question_class,
		"chapter": record.chapter,
		"question_length": record.question_length,
		"question_text": record.question_text,
	}


def long_question_to_dict(entry: QuestionEntry) -> dict[str, Any]:
	text = entry.question_text
	return {
		"source_file": entry.source_file,
		"index": entry.index,
		"question_id": entry.question_id,
		"class": entry.question_class,
		"subject": entry.subject,
		"chapter": entry.chapter,
		"question_length": entry.question_length,
		"question_text": text,
		"contains_example": contains_keyword(text, "example"),
		"contains_activity": contains_keyword(text, "activity"),
		"contains_try_this": contains_phrase(text, "try this"),
		"contains_solution": contains_keyword(text, "solution"),
		"contains_reprint": contains_keyword(text, "reprint"),
		"contains_figure": contains_keyword(text, "figure"),
		"contains_exercise": contains_keyword(text, "exercise"),
	}


def worst_question_to_dict(entry: QuestionEntry) -> dict[str, Any]:
	text = entry.question_text
	return {
		"pdf": str(Path(entry.source_file).with_suffix(".pdf")),
		"question_id": entry.question_id,
		"class": entry.question_class,
		"chapter": entry.chapter,
		"subject": entry.subject,
		"length": entry.question_length,
		"question_text": text,
		"first_300_chars": text[:300],
		"last_300_chars": text[-300:],
		"suspected_reason": "UNKNOWN",
	}


def contains_keyword(text: str, keyword: str) -> bool:
	return keyword.casefold() in text.casefold()


def contains_phrase(text: str, phrase: str) -> bool:
	return phrase.casefold() in text.casefold()


def format_report(summary: AuditSummary) -> str:
	lines = [
		"QUALITY AUDIT REPORT",
		"=" * 80,
		f"Total JSON files             : {summary.total_json_files}",
		f"Total questions              : {summary.total_questions}",
		f"Empty question_text          : {summary.empty_question_text}",
		f"Duplicate Groups             : {summary.duplicate_groups}",
		f"Duplicate Records            : {summary.duplicate_records}",
		f"Questions > 1500 chars       : {summary.long_questions}",
		f"Missing question_id          : {summary.missing_question_id}",
		f"Missing class                : {summary.missing_class}",
		f"Missing chapter              : {summary.missing_chapter}",
		f"Missing subject              : {summary.missing_subject}",
		f"Average question length      : {summary.average_question_length:.2f}",
		f"Median question length       : {summary.median_question_length:.2f}",
		f"Maximum question length      : {summary.maximum_question_length}",
	]
	return "\n".join(lines) + "\n"


if __name__ == "__main__":
	main()