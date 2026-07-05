"""Repo-root import shim for uninstalled subprocess CLI tests.

The source package lives in ``src/openamp_foundry``. Some integration tests run
``python -m openamp_foundry.cli`` from a clean repo root without installing the
package. Extending ``__path__`` keeps that invocation deterministic while the
normal editable-install path remains unchanged.
"""

from __future__ import annotations

from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "openamp_foundry"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))  # type: ignore[name-defined]

__version__ = "0.1.0"
