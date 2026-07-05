from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

from openamp_foundry.calibration.policy_version import (
    validate_policy_version_update,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "configs" / "recalibration_policy.yaml"


def test_policy_version_check_passes_when_policy_unchanged(tmp_path):
    current = tmp_path / "current.yaml"
    previous = tmp_path / "previous.yaml"
    current.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    result = validate_policy_version_update(current, previous, decision_log_dir=tmp_path)

    assert result.passed is True
    assert result.changed is False
    assert result.reasons == ()


def test_policy_version_check_fails_when_changed_without_version_bump(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    current.write_text(
        POLICY_PATH.read_text(encoding="utf-8").replace(
            "threshold: 5\n    applies_to: \"report.n_matched_candidates\"",
            "threshold: 6\n    applies_to: \"report.n_matched_candidates\"",
            1,
        ),
        encoding="utf-8",
    )

    result = validate_policy_version_update(current, previous, decision_log_dir=tmp_path)

    assert result.passed is False
    assert result.changed is True
    assert any("policy_version was not bumped" in reason for reason in result.reasons)


def test_policy_version_check_fails_when_locked_change_mutates(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    mutated = POLICY_PATH.read_text(encoding="utf-8").replace(
        'reason: "Anti-cherry-picking floor below which AUROC is unstable."',
        'reason: "Changed reason."',
        1,
    ).replace("policy_version: 1", "policy_version: 2", 1)
    current.write_text(mutated, encoding="utf-8")
    (tmp_path / "DECISION_LOG_2026-07-06.md").write_text("# reasoned bump\n", encoding="utf-8")

    result = validate_policy_version_update(
        current,
        previous,
        decision_log_dir=tmp_path,
        today=date(2026, 7, 6),
    )

    assert result.passed is False
    assert any("locked_change changed" in reason for reason in result.reasons)


def test_policy_version_check_passes_with_bump_and_fresh_decision_log(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    current.write_text(
        POLICY_PATH.read_text(encoding="utf-8")
        .replace("policy_version: 1", "policy_version: 2", 1)
        .replace("threshold: 5", "threshold: 6", 1),
        encoding="utf-8",
    )
    (tmp_path / "DECISION_LOG_2026-07-06.md").write_text("# ratified\n", encoding="utf-8")

    result = validate_policy_version_update(
        current,
        previous,
        decision_log_dir=tmp_path,
        today=date(2026, 7, 6),
    )

    assert result.passed is True
    assert result.changed is True


def test_policy_version_check_requires_recent_nonempty_decision_log(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    current.write_text(
        POLICY_PATH.read_text(encoding="utf-8")
        .replace("policy_version: 1", "policy_version: 2", 1)
        .replace("threshold: 5", "threshold: 6", 1),
        encoding="utf-8",
    )
    (tmp_path / "DECISION_LOG_2026-05-01.md").write_text("# stale\n", encoding="utf-8")

    result = validate_policy_version_update(
        current,
        previous,
        decision_log_dir=tmp_path,
        today=date(2026, 7, 6),
    )

    assert result.passed is False
    assert any("no non-empty decision log" in reason for reason in result.reasons)


def test_cli_policy_version_check_smoke(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    current.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "openamp_foundry.cli",
            "policy-version-check",
            "--current-policy",
            str(current),
            "--previous-policy",
            str(previous),
            "--decision-log-dir",
            str(tmp_path),
            "--today",
            "2026-07-06",
        ],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": "src"},
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert '"passed": true' in proc.stdout


def test_cli_policy_version_check_invalid_date(tmp_path):
    previous = tmp_path / "previous.yaml"
    current = tmp_path / "current.yaml"
    previous.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    current.write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "openamp_foundry.cli",
            "policy-version-check",
            "--current-policy",
            str(current),
            "--previous-policy",
            str(previous),
            "--today",
            "bad-date",
        ],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": "src"},
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert proc.returncode == 2
    assert "invalid --today date" in proc.stdout
