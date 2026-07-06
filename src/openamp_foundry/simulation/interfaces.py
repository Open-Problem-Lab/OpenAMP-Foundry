"""Interfaces and schemas for the OpenAMP virtual assay layer."""

import abc
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, runtime_checkable


@dataclass
class SimulationResult:
    """Schema for outputs from any virtual assay or simulation module.
    
    This exact schema is mandated by docs/ARCHITECTURE.md.
    """
    module: str
    version: str
    scope: List[str]
    scores: Dict[str, float]
    uncertainty: float
    calibration_set: Optional[str]
    validated_against: List[str]
    notes: List[str] = field(default_factory=list)


class EmulatorBaseline(abc.ABC):
    """Contract for cheap heuristic baselines.
    
    Every virtual assay must prove it beats a cheap baseline 
    to avoid 'simulation theater'.
    """
    
    @abc.abstractmethod
    def evaluate(self, sequence: str) -> float:
        """Evaluate the sequence using the cheap heuristic baseline."""
        pass


class VirtualAssayProxy(abc.ABC):
    """Abstract base class for all virtual assay modules.
    
    Modules (e.g., membrane interaction proxies, stability proxies, 
    or learned surrogate models) must implement this interface.
    """
    
    @abc.abstractmethod
    def simulate(self, sequence: str) -> SimulationResult:
        """Run the virtual assay simulation on the sequence.
        
        Returns:
            SimulationResult object containing scores and explicit uncertainty.
        """
        pass
    
    @abc.abstractmethod
    def get_baseline(self) -> EmulatorBaseline:
        """Return the baseline heuristic this simulation must beat."""
        pass


@runtime_checkable
class ExternalSimulationAdapter(Protocol):
    """Protocol for third-party or high-cost simulation adapters.

    External adapters may wrap molecular dynamics packages, structure predictors,
    or remote inference services. They must expose consent-sensitive behavior so
    OpenAMP never silently downloads model weights, transmits sequences, or runs
    heavyweight jobs.
    """

    name: str
    version: str
    requires_network: bool
    requires_model_download: bool
    requires_explicit_consent: bool

    def describe(self) -> dict[str, object]:
        """Return metadata, scope, limits, and consent requirements."""
        ...

    def simulate_batch(self, sequences: list[str]) -> list[SimulationResult]:
        """Run the adapter and return one result per input sequence."""
        ...


def validate_external_adapter_result(
    adapter: ExternalSimulationAdapter,
    sequences: list[str],
    results: list[SimulationResult],
) -> None:
    """Validate the minimum output contract for external adapters."""
    if adapter.requires_explicit_consent and not (
        adapter.requires_network or adapter.requires_model_download
    ):
        raise ValueError(
            "requires_explicit_consent may only be true when network or model "
            "download consent is actually needed."
        )
    if len(results) != len(sequences):
        raise ValueError(
            f"adapter returned {len(results)} result(s) for {len(sequences)} sequence(s)"
        )
    for result in results:
        if result.module != adapter.name:
            raise ValueError(
                f"adapter result module {result.module!r} does not match adapter "
                f"name {adapter.name!r}"
            )
        if result.version != adapter.version:
            raise ValueError(
                f"adapter result version {result.version!r} does not match adapter "
                f"version {adapter.version!r}"
            )
        if not 0.0 <= result.uncertainty <= 1.0:
            raise ValueError("adapter uncertainty must be in [0, 1]")
