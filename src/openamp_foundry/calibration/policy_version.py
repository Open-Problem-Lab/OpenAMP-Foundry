"""Policy-version guard for recalibration-policy edits.

The recalibration gate validates one policy file in isolation. This module
compares a proposed policy against a prior policy so policy edits cannot slide
in without a version bump, preserved locks, and a fresh human decision log.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from openamp_foundry.calibration.policy import (
    LockedChange,
    RecalibrationPolicy,
    load_recalibration_policy,
)


@dataclass(frozen=True)
class PolicyVersionCheck:
    """Result of comparing current vs previous recalibration policy files."""

    passed: bool
    current_version: int
    previous_version: int
    changed: bool
    decision_log_path: str | None
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "current_version": self.current_version,
            "previous_version": self.previous_version,
            "changed": self.changed,
            "decision_log_path": self.decision_log_path,
            "reasons": list(self.reasons),
        }


def _policy_signature(policy: RecalibrationPolicy) -> tuple[object, ...]:
    """Return auditable policy content, excluding metadata."""

    return (
        policy.minimum_conditions,
        policy.prohibited_actions,
        policy.rate_limits,
        policy.required_reviewer_artefacts,
        policy.locked_changes,
        policy.notes,
    )


def _locked_change_map(policy: RecalibrationPolicy) -> dict[str, LockedChange]:
    return {change.rule_id: change for change in policy.locked_changes}


def _parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _fresh_decision_logs(
    decision_log_dir: Path,
    *,
    today: date,
    max_age_days: int,
) -> list[Path]:
    if not decision_log_dir.exists():
        return []

    fresh: list[Path] = []
    for path in sorted(decision_log_dir.glob("DECISION_LOG_*.md")):
        log_date = _parse_iso_date(path.stem.removeprefix("DECISION_LOG_"))
        if log_date is None:
            continue
        age_days = (today - log_date).days
        if 0 <= age_days <= max_age_days and path.read_text(encoding="utf-8").strip():
            fresh.append(path)
    return fresh


def validate_policy_version_update(
    current_policy_path: str | Path,
    previous_policy_path: str | Path,
    *,
    decision_log_dir: str | Path = "docs",
    today: date | None = None,
    max_decision_log_age_days: int = 30,
) -> PolicyVersionCheck:
    """Validate that a policy edit has an auditable version bump."""

    current = load_recalibration_policy(current_policy_path)
    previous = load_recalibration_policy(previous_policy_path)
    reasons: list[str] = []

    changed = _policy_signature(current) != _policy_signature(previous)

    if current.policy_version < previous.policy_version:
        reasons.append(
            f"policy_version decreased: {current.policy_version} < {previous.policy_version}"
        )

    previous_locks = _locked_change_map(previous)
    current_locks = _locked_change_map(current)
    for rule_id, previous_lock in previous_locks.items():
        current_lock = current_locks.get(rule_id)
        if current_lock is None:
            reasons.append(f"locked_change removed: {rule_id}")
        elif current_lock != previous_lock:
            reasons.append(f"locked_change changed without replacement policy: {rule_id}")

    decision_log_path: str | None = None
    if changed:
        if current.policy_version <= previous.policy_version:
            reasons.append(
                "policy changed but policy_version was not bumped above "
                f"{previous.policy_version}"
            )

        check_date = today or date.today()
        fresh_logs = _fresh_decision_logs(
            Path(decision_log_dir),
            today=check_date,
            max_age_days=max_decision_log_age_days,
        )
        if fresh_logs:
            decision_log_path = str(fresh_logs[-1])
        else:
            reasons.append(
                "policy changed but no non-empty decision log dated within "
                f"{max_decision_log_age_days} days was found"
            )

    return PolicyVersionCheck(
        passed=not reasons,
        current_version=current.policy_version,
        previous_version=previous.policy_version,
        changed=changed,
        decision_log_path=decision_log_path,
        reasons=tuple(reasons),
    )
