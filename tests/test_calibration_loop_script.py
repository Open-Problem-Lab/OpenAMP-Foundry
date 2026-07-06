"""Regression tests for the synthetic calibration loop script."""

from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_loop_module():
    spec = importlib.util.spec_from_file_location(
        "run_calibration_loop",
        REPO_ROOT / "scripts" / "run_calibration_loop.py",
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_calibration_loop_reports_review_notes_not_blockers_on_passing_gate(
    tmp_path,
    capsys,
):
    """Passing gate verdicts may still have review notes; do not call them blockers."""
    module = _load_loop_module()
    result = module.run_calibration_loop(
        panel_csv=REPO_ROOT / "examples" / "lab_results_panel.csv",
        policy_yaml=REPO_ROOT / "configs" / "recalibration_policy.yaml",
        out_dir=tmp_path / "calibration_loop",
        rng_seed=42,
        n_batch_2=10,
    )

    captured = capsys.readouterr()
    assert result["may_recalibrate"] is True
    assert "n_review_notes" in result
    assert "Review notes:" in captured.out
    assert "Blockers:" not in captured.out
