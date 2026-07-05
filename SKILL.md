# OpenAMP Foundry Agent Skill

## Start Here

1. Read `AGENTS.md`, `CLAUDE.md`, `MISSION.md`, and `docs/METRICS_CURRENT.md`.
2. Treat `docs/METRICS_CURRENT.md` plus `outputs/metrics_snapshot.json` as the
   current benchmark truth when docs disagree.
3. Preserve the safety boundary: dry-lab scoring and evidence only. No wet-lab
   protocols, pathogen enablement, toxicity-maximizing objectives, or biological
   proof claims.

## High-Leverage Benchmark Checks

- `make bench-500`: broad AMP-vs-decoy discrimination.
- `make bench-easy-baseline`: trivial length/charge baselines.
- `make bench-charge-matched`: adversarial check that removes charge-density
  separation before comparing ensemble vs charge alone.
- `make bench-per-family`: structural-class blind spots.
- `make bench-selectivity`: hemolytic-vs-selective AMP ranking.
- `make metrics-snapshot`: regenerate the machine-readable source of truth.

## Current v0.5.38 Note

The charge-matched decoy benchmark shows charge density collapses to random
after exact matching (`AUROC=0.5000`) while the ensemble remains at `0.7792`.
This means the current 500-sequence benchmark is not reducible to charge density
alone. It does not prove order-aware biology; other composition features may
still carry most of the signal.
