"""Tests for simulation-module cheap-baseline benchmarks."""

from __future__ import annotations

import json
import subprocess
import sys

from openamp_foundry.benchmark.simulation_baselines import (
    _auroc,
    run_simulation_baseline_benchmark,
)


def test_simulation_baseline_benchmark_runs():
    result = run_simulation_baseline_benchmark(n_bootstrap=50)

    assert result["benchmark"] == "simulation_module_vs_baseline"
    assert result["n_amp"] == 500
    assert result["n_decoy"] == 500
    assert result["n_hemolytic"] == 45
    assert result["n_selective"] == 125


def test_membrane_binding_beats_boman_on_amp_vs_decoy():
    result = run_simulation_baseline_benchmark(n_bootstrap=50)
    membrane = result["per_module"]["membrane_amp_vs_decoy"]

    assert membrane["verdict"] == "BEATS_BASELINE"
    assert membrane["module_auroc"] > membrane["baseline_auroc"]
    assert membrane["delta_auroc"] > 0.0


def test_structure_helix_weight_does_not_beat_helicity_baseline():
    result = run_simulation_baseline_benchmark(n_bootstrap=50)
    structure = result["per_module"]["structure_within_amp"]

    assert structure["verdict"] == "NO_GAIN"
    assert structure["delta_auroc"] <= 0.0


def test_non_helical_flag_does_not_beat_helicity_baseline():
    result = run_simulation_baseline_benchmark(n_bootstrap=50)
    non_helical = result["per_module"]["structure_non_helical_within_amp"]

    assert non_helical["verdict"] == "NO_GAIN"
    assert non_helical["delta_auroc"] <= 0.0


def test_best_existing_rich_selectivity_still_beats_best_simulation_within_amp():
    result = run_simulation_baseline_benchmark(n_bootstrap=50)
    rich = result["best_existing_within_amp"]["rich_selectivity_auroc"]
    best_sim = max(
        result["per_module"]["membrane_within_amp"]["module_auroc"],
        result["per_module"]["structure_within_amp"]["module_auroc"],
        result["per_module"]["structure_non_helical_within_amp"]["module_auroc"],
    )

    assert rich > best_sim


def test_cli_writes_simulation_baseline_output(tmp_path):
    out = tmp_path / "simulation_baselines.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/benchmark_simulation_baselines.py",
            "--n-bootstrap",
            "50",
            "--out",
            str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["benchmark"] == "simulation_module_vs_baseline"


def test_cli_subcommand_writes_simulation_baseline_output(tmp_path):
    out = tmp_path / "simulation_baselines.json"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "openamp_foundry.cli",
            "bench",
            "simulation-baselines",
            "--n-bootstrap",
            "50",
            "--out",
            str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": "src"},
    )

    assert completed.returncode == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "membrane_amp_vs_decoy" in payload["per_module"]


def test_auroc_ties_are_half_credit():
    assert _auroc([0.5, 1.0], [0.5, 0.0]) == 0.875
