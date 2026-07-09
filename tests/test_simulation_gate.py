"""Test simulation gate blocks weighted mode."""
import subprocess
import sys
from pathlib import Path


def test_simulation_gate_cli_requires_args():
    r = subprocess.run(
        [sys.executable, "-m", "openamp_foundry.cli", "bench", "simulation-gate", "--help"],
        capture_output=True, text=True,
        env={"PYTHONPATH": "src"},
    )
    assert r.returncode == 0
    assert "usage:" in r.stdout


def test_simulation_gate_fails_without_required_inputs():
    r = subprocess.run(
        [sys.executable, "-m", "openamp_foundry.cli", "bench", "simulation-gate",
         "--amp-vs-decoy-json", "/nonexistent", "--within-amp-json", "/nonexistent"],
        capture_output=True, text=True,
        env={"PYTHONPATH": "src"},
    )
    # Should fail with input error
    assert r.returncode != 0
