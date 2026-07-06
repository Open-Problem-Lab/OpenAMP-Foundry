"""Run-manifest verification utilities.

The manifest is the audit boundary between computed artifacts and reproducible
claims. This module verifies that recorded inputs have not drifted and that named
outputs still exist before downstream review or release steps trust a run.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MISSING_HASH_SENTINELS = {"", "N/A", None}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve_path(path: str, root: Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else root / p


def _sorted_json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def verify_run_manifest(
    manifest_path: str | Path,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Verify a run manifest against the current filesystem.

    Checks are intentionally local and deterministic:
    - required manifest fields are present;
    - every recorded input hash matches the current file content;
    - every listed output exists;
    - optional ``output_hashes`` entries are enforced when present.
    """
    manifest_p = Path(manifest_path)
    root_p = Path(root) if root is not None else Path.cwd()

    errors: list[str] = []
    warnings: list[str] = []
    observed_output_hashes: dict[str, str] = {}

    if not manifest_p.exists():
        return {
            "ok": False,
            "manifest_path": str(manifest_p),
            "errors": [f"Manifest not found: {manifest_p}"],
            "warnings": warnings,
            "observed_output_hashes": observed_output_hashes,
        }

    try:
        manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "manifest_path": str(manifest_p),
            "errors": [f"Manifest is not valid JSON: {exc}"],
            "warnings": warnings,
            "observed_output_hashes": observed_output_hashes,
        }

    required = [
        "run_id",
        "pipeline_version",
        "config_hash",
        "generated_at",
        "inputs",
        "input_hashes",
        "outputs",
    ]
    for field in required:
        if field not in manifest:
            errors.append(f"Missing required manifest field: {field}")

    input_hashes = manifest.get("input_hashes", {})
    if not isinstance(input_hashes, dict):
        errors.append("input_hashes must be an object")
        input_hashes = {}

    for path_str, expected_hash in sorted(input_hashes.items()):
        if expected_hash in MISSING_HASH_SENTINELS:
            warnings.append(f"Input has no recorded hash: {path_str}")
            continue
        input_p = _resolve_path(path_str, root_p)
        if not input_p.exists():
            errors.append(f"Input file missing: {path_str}")
            continue
        if not input_p.is_file():
            errors.append(f"Input path is not a file: {path_str}")
            continue
        actual_hash = _sha256_file(input_p)
        if actual_hash != expected_hash:
            errors.append(
                "Input hash mismatch for "
                f"{path_str}: expected {expected_hash}, actual {actual_hash}"
            )

    outputs = manifest.get("outputs", [])
    if not isinstance(outputs, list):
        errors.append("outputs must be a list")
        outputs = []

    for path_str in outputs:
        output_p = _resolve_path(str(path_str), root_p)
        if not output_p.exists():
            errors.append(f"Output path missing: {path_str}")
        elif output_p.is_file():
            observed_output_hashes[str(path_str)] = _sha256_file(output_p)

    output_hashes = manifest.get("output_hashes", {})
    if output_hashes and not isinstance(output_hashes, dict):
        errors.append("output_hashes must be an object when present")
        output_hashes = {}

    for path_str, expected_hash in sorted(output_hashes.items()):
        output_p = _resolve_path(path_str, root_p)
        if not output_p.exists():
            errors.append(f"Output hash target missing: {path_str}")
            continue
        if not output_p.is_file():
            errors.append(f"Output hash target is not a file: {path_str}")
            continue
        actual_hash = _sha256_file(output_p)
        if actual_hash != expected_hash:
            errors.append(
                "Output hash mismatch for "
                f"{path_str}: expected {expected_hash}, actual {actual_hash}"
            )

    payload_hash = hashlib.sha256(_sorted_json_dumps(manifest).encode("utf-8")).hexdigest()
    return {
        "ok": not errors,
        "manifest_path": str(manifest_p),
        "manifest_payload_sha256": payload_hash,
        "errors": errors,
        "warnings": warnings,
        "observed_output_hashes": observed_output_hashes,
    }
