"""Run cheap-baseline comparisons for shipped simulation modules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from openamp_foundry.benchmark.simulation_baselines import (
    run_simulation_baseline_benchmark,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulation vs cheap-baseline benchmark")
    parser.add_argument("--amp-csv", default="examples/validation/known_amps_500.csv")
    parser.add_argument("--decoy-csv", default="examples/validation/random_background_500.csv")
    parser.add_argument("--hemolysis-csv", default="examples/validation/hemolysis_reference.csv")
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    result = run_simulation_baseline_benchmark(
        amp_csv=args.amp_csv,
        decoy_csv=args.decoy_csv,
        hemolysis_csv=args.hemolysis_csv,
        n_bootstrap=args.n_bootstrap,
    )
    print(json.dumps(result, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
