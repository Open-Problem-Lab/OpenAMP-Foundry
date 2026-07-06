"""Virtual assay simulation layer for OpenAMP Foundry."""

from .gate import SimulationGateVerdict, evaluate_simulation_gate
from .interfaces import (
    EmulatorBaseline,
    ExternalSimulationAdapter,
    SimulationResult,
    VirtualAssayProxy,
    validate_external_adapter_result,
)
from .membrane import MembraneProxy
from .structure import StructureProxy

__all__ = [
    "SimulationResult",
    "VirtualAssayProxy",
    "ExternalSimulationAdapter",
    "EmulatorBaseline",
    "validate_external_adapter_result",
    "MembraneProxy",
    "StructureProxy",
    "SimulationGateVerdict",
    "evaluate_simulation_gate",
]
