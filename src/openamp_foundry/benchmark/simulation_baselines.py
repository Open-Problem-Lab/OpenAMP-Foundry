"""Cheap-baseline benchmark for simulation modules.

Every virtual-assay proxy must beat its own cheap baseline on the task it claims
to help with. This module measures that delta directly on the current reference
sets and reports negative results honestly.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from openamp_foundry.features.physchem import compute_features
from openamp_foundry.scoring.activity import activity_likeness_score
from openamp_foundry.scoring.ensemble import ensemble_score
from openamp_foundry.scoring.safety import safety_score
from openamp_foundry.scoring.selectivity_rich import rich_selectivity_score
from openamp_foundry.simulation.membrane import MembraneProxy
from openamp_foundry.simulation.structure import StructureProxy


def _auroc(scores_pos: list[float], scores_neg: list[float]) -> float:
    n_p = len(scores_pos)
    n_n = len(scores_neg)
    if n_p == 0 or n_n == 0:
        return 0.5
    better = 0
    ties = 0
    for sp in scores_pos:
        for sn in scores_neg:
            if sp > sn:
                better += 1
            elif sp == sn:
                ties += 1
    total = n_p * n_n
    return (better + 0.5 * ties) / total if total else 0.5


def _detection_auroc(
    positives: list[float],
    negatives: list[float],
    *,
    invert: bool = False,
) -> float:
    raw = _auroc(positives, negatives)
    return 1.0 - raw if invert else raw


def _bootstrap_ci(
    positives: list[float],
    negatives: list[float],
    *,
    invert: bool = False,
    n_bootstrap: int = 1000,
    rng_seed: int = 1729,
) -> tuple[float, float]:
    if not positives or not negatives:
        return (0.5, 0.5)
    rng = random.Random(rng_seed)
    vals: list[float] = []
    for _ in range(n_bootstrap):
        pos_sample = [positives[rng.randrange(len(positives))] for _ in positives]
        neg_sample = [negatives[rng.randrange(len(negatives))] for _ in negatives]
        vals.append(_detection_auroc(pos_sample, neg_sample, invert=invert))
    vals.sort()
    lo_idx = int(0.025 * (len(vals) - 1))
    hi_idx = int(0.975 * (len(vals) - 1))
    return (round(vals[lo_idx], 4), round(vals[hi_idx], 4))


def _load_sequences(csv_path: str | Path, *, id_key: str = "id") -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    with Path(csv_path).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq = row.get("sequence", "").strip().upper()
            if seq:
                rows.append((row.get(id_key, "unknown"), seq))
    return rows


def _load_hemolysis_pairs(csv_path: str | Path) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    hemolytic: list[tuple[str, str]] = []
    selective: list[tuple[str, str]] = []
    with Path(csv_path).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq = row.get("sequence", "").strip().upper()
            cls = row.get("hemolysis_class", "").strip().upper()
            if not seq:
                continue
            cid = row.get("id", "unknown")
            if cls == "HEMOLYTIC":
                hemolytic.append((cid, seq))
            elif cls == "SELECTIVE":
                selective.append((cid, seq))
    return hemolytic, selective


def _pipeline_ensemble(sequence: str) -> float:
    feats = compute_features(sequence)
    raw = {
        "activity": activity_likeness_score(feats),
        "safety": safety_score(feats),
        "novelty": 0.5,
        "synthesis": 0.5,
    }
    return ensemble_score(raw, {"activity": 0.40, "safety": 0.25, "synthesis": 0.15, "novelty": 0.20})


def _summarize_comparison(
    *,
    benchmark: str,
    task: str,
    module: str,
    baseline: str,
    positives: list[float],
    negatives: list[float],
    baseline_pos: list[float],
    baseline_neg: list[float],
    invert_module: bool = False,
    invert_baseline: bool = False,
    n_bootstrap: int = 1000,
) -> dict:
    module_auroc = round(_detection_auroc(positives, negatives, invert=invert_module), 4)
    baseline_auroc = round(
        _detection_auroc(baseline_pos, baseline_neg, invert=invert_baseline), 4,
    )
    delta = round(module_auroc - baseline_auroc, 4)
    module_ci = _bootstrap_ci(
        positives, negatives, invert=invert_module, n_bootstrap=n_bootstrap,
    )
    baseline_ci = _bootstrap_ci(
        baseline_pos, baseline_neg, invert=invert_baseline, n_bootstrap=n_bootstrap,
    )
    verdict = "BEATS_BASELINE" if delta > 0.0 else "NO_GAIN"
    return {
        "benchmark": benchmark,
        "task": task,
        "module": module,
        "baseline": baseline,
        "module_auroc": module_auroc,
        "module_ci95": list(module_ci),
        "baseline_auroc": baseline_auroc,
        "baseline_ci95": list(baseline_ci),
        "delta_auroc": delta,
        "verdict": verdict,
    }


def run_simulation_baseline_benchmark(
    *,
    amp_csv: str | Path = "examples/validation/known_amps_500.csv",
    decoy_csv: str | Path = "examples/validation/random_background_500.csv",
    hemolysis_csv: str | Path = "examples/validation/hemolysis_reference.csv",
    n_bootstrap: int = 1000,
) -> dict:
    """Compare each shipped simulation module against its cheap baseline."""
    membrane = MembraneProxy()
    structure = StructureProxy()
    membrane_baseline = membrane.get_baseline()
    structure_baseline = structure.get_baseline()

    amps = _load_sequences(amp_csv)
    decoys = _load_sequences(decoy_csv)
    hemolytic, selective = _load_hemolysis_pairs(hemolysis_csv)

    amp_bact = [membrane.simulate(seq).scores["bacterial_binding"] for _cid, seq in amps]
    decoy_bact = [membrane.simulate(seq).scores["bacterial_binding"] for _cid, seq in decoys]
    amp_boman = [membrane_baseline.evaluate(seq) for _cid, seq in amps]
    decoy_boman = [membrane_baseline.evaluate(seq) for _cid, seq in decoys]

    membrane_amp_vs_decoy = _summarize_comparison(
        benchmark="simulation_baseline_amp_vs_decoy",
        task="amp_vs_decoy",
        module="membrane_proxy.bacterial_binding",
        baseline="boman_baseline",
        positives=amp_bact,
        negatives=decoy_bact,
        baseline_pos=amp_boman,
        baseline_neg=decoy_boman,
        n_bootstrap=n_bootstrap,
    )

    hemo_sel_ratio = [membrane.simulate(seq).scores["selectivity_ratio"] for _cid, seq in hemolytic]
    sel_sel_ratio = [membrane.simulate(seq).scores["selectivity_ratio"] for _cid, seq in selective]
    hemo_boman = [membrane_baseline.evaluate(seq) for _cid, seq in hemolytic]
    sel_boman = [membrane_baseline.evaluate(seq) for _cid, seq in selective]

    membrane_within_amp = _summarize_comparison(
        benchmark="simulation_baseline_within_amp",
        task="hemolytic_vs_selective",
        module="membrane_proxy.selectivity_ratio",
        baseline="boman_baseline",
        positives=hemo_sel_ratio,
        negatives=sel_sel_ratio,
        baseline_pos=hemo_boman,
        baseline_neg=sel_boman,
        invert_module=True,
        n_bootstrap=n_bootstrap,
    )

    hemo_helix = [structure.simulate(seq).scores["helix_weight"] for _cid, seq in hemolytic]
    sel_helix = [structure.simulate(seq).scores["helix_weight"] for _cid, seq in selective]
    hemo_helicity = [structure_baseline.evaluate(seq) for _cid, seq in hemolytic]
    sel_helicity = [structure_baseline.evaluate(seq) for _cid, seq in selective]

    structure_within_amp = _summarize_comparison(
        benchmark="simulation_baseline_within_amp",
        task="hemolytic_vs_selective",
        module="structure_proxy.helix_weight",
        baseline="helicity_baseline",
        positives=hemo_helix,
        negatives=sel_helix,
        baseline_pos=hemo_helicity,
        baseline_neg=sel_helicity,
        n_bootstrap=n_bootstrap,
    )

    hemo_non_helical = [structure.simulate(seq).scores["non_helical"] for _cid, seq in hemolytic]
    sel_non_helical = [structure.simulate(seq).scores["non_helical"] for _cid, seq in selective]
    non_helical_flag = _summarize_comparison(
        benchmark="simulation_baseline_within_amp",
        task="hemolytic_vs_selective",
        module="structure_proxy.non_helical",
        baseline="helicity_baseline",
        positives=hemo_non_helical,
        negatives=sel_non_helical,
        baseline_pos=hemo_helicity,
        baseline_neg=sel_helicity,
        invert_module=True,
        n_bootstrap=n_bootstrap,
    )

    rich_sel_hemo = [rich_selectivity_score(compute_features(seq)) for _cid, seq in hemolytic]
    rich_sel_sel = [rich_selectivity_score(compute_features(seq)) for _cid, seq in selective]
    ensemble_hemo = [_pipeline_ensemble(seq) for _cid, seq in hemolytic]
    ensemble_sel = [_pipeline_ensemble(seq) for _cid, seq in selective]

    best_existing = {
        "rich_selectivity_auroc": round(_detection_auroc(rich_sel_hemo, rich_sel_sel, invert=True), 4),
        "ensemble_auroc": round(_detection_auroc(ensemble_hemo, ensemble_sel), 4),
    }

    attempts = [
        membrane_amp_vs_decoy,
        membrane_within_amp,
        structure_within_amp,
        non_helical_flag,
    ]
    no_gain_count = sum(1 for item in attempts if item["delta_auroc"] <= 0.0)
    recommendation = (
        "Keep simulation informational only."
        if no_gain_count >= 3
        else "Some modules beat their cheap baseline, but weighted mode still requires the simulation gate."
    )

    return {
        "benchmark": "simulation_module_vs_baseline",
        "n_amp": len(amps),
        "n_decoy": len(decoys),
        "n_hemolytic": len(hemolytic),
        "n_selective": len(selective),
        "per_module": {
            "membrane_amp_vs_decoy": membrane_amp_vs_decoy,
            "membrane_within_amp": membrane_within_amp,
            "structure_within_amp": structure_within_amp,
            "structure_non_helical_within_amp": non_helical_flag,
        },
        "best_existing_within_amp": best_existing,
        "summary": {
            "modules_beating_baseline": [
                key for key, item in {
                    "membrane_amp_vs_decoy": membrane_amp_vs_decoy,
                    "membrane_within_amp": membrane_within_amp,
                    "structure_within_amp": structure_within_amp,
                    "structure_non_helical_within_amp": non_helical_flag,
                }.items()
                if item["delta_auroc"] > 0.0
            ],
            "modules_not_beating_baseline": [
                key for key, item in {
                    "membrane_amp_vs_decoy": membrane_amp_vs_decoy,
                    "membrane_within_amp": membrane_within_amp,
                    "structure_within_amp": structure_within_amp,
                    "structure_non_helical_within_amp": non_helical_flag,
                }.items()
                if item["delta_auroc"] <= 0.0
            ],
            "recommendation": recommendation,
        },
    }
