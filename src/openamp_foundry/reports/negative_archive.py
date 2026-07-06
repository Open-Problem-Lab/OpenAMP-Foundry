"""Append-only negative-result archive helpers."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REASON_CATEGORIES = {
    "pre_selection_reject",
    "selected_untested",
    "lab_inactive",
    "lab_toxic",
    "control_failure",
    "synthesis_failure",
}

FIELDNAMES = [
    "entry_id",
    "date",
    "candidate_id",
    "sequence",
    "reason_category",
    "reason_detail",
    "pipeline_version",
    "source_batch",
    "assay_type",
    "assay_result",
    "assay_unit",
    "score_activity",
    "score_safety",
    "score_novelty",
    "score_ensemble",
    "recalibration_used",
    "superseded_by",
    "reviewer_notes",
]


@dataclass(frozen=True)
class NegativeArchiveRow:
    candidate_id: str
    sequence: str
    reason_category: str
    reason_detail: str
    pipeline_version: str
    source_batch: str
    date: str | None = None
    assay_type: str = ""
    assay_result: str = ""
    assay_unit: str = ""
    score_activity: str = ""
    score_safety: str = ""
    score_novelty: str = ""
    score_ensemble: str = ""
    recalibration_used: str = "no"
    superseded_by: str = ""
    reviewer_notes: str = ""

    def as_csv_row(self, entry_id: int) -> dict[str, str]:
        if self.reason_category not in REASON_CATEGORIES:
            raise ValueError(f"invalid reason_category: {self.reason_category}")
        return {
            "entry_id": str(entry_id),
            "date": self.date or date.today().isoformat(),
            "candidate_id": self.candidate_id,
            "sequence": self.sequence,
            "reason_category": self.reason_category,
            "reason_detail": self.reason_detail,
            "pipeline_version": self.pipeline_version,
            "source_batch": self.source_batch,
            "assay_type": self.assay_type,
            "assay_result": self.assay_result,
            "assay_unit": self.assay_unit,
            "score_activity": self.score_activity,
            "score_safety": self.score_safety,
            "score_novelty": self.score_novelty,
            "score_ensemble": self.score_ensemble,
            "recalibration_used": self.recalibration_used,
            "superseded_by": self.superseded_by,
            "reviewer_notes": self.reviewer_notes,
        }


def read_negative_archive(path: str | Path) -> list[dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_negative_archive_rows(path: str | Path, rows: list[NegativeArchiveRow]) -> int:
    if not rows:
        return 0
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    existing = read_negative_archive(p)
    next_id = _next_entry_id(existing)
    write_header = not p.exists() or p.stat().st_size == 0
    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        for offset, row in enumerate(rows):
            writer.writerow(row.as_csv_row(next_id + offset))
    return len(rows)


def _next_entry_id(rows: list[dict[str, str]]) -> int:
    ids: list[int] = []
    for row in rows:
        try:
            ids.append(int(row.get("entry_id", "")))
        except ValueError:
            continue
    return max(ids, default=0) + 1
