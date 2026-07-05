"""Repo-root import shim for subprocess CLI tests.

The package source lives under ``src/openamp_foundry``. Some subprocess tests
run ``python -m openamp_foundry.cli`` from the repository root without an
editable install. This shim extends the package search path so those calls use
the real source package without duplicating code.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "openamp_foundry"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))  # type: ignore[name-defined]

__version__ = "0.1.0"
