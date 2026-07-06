"""Tests for the virtual assay layer interfaces and contracts."""


import pytest

from openamp_foundry.simulation.dummy import DummyMembraneProxy
from openamp_foundry.simulation.interfaces import (
    ExternalSimulationAdapter,
    SimulationResult,
    validate_external_adapter_result,
)


class ExampleExternalAdapter:
    name = "example_external_adapter"
    version = "0.1.0"
    requires_network = False
    requires_model_download = False
    requires_explicit_consent = False

    def describe(self):
        return {
            "name": self.name,
            "version": self.version,
            "scope": ["contract_test_only"],
            "limits": ["does not model biology"],
        }

    def simulate_batch(self, sequences):
        return [
            SimulationResult(
                module=self.name,
                version=self.version,
                scope=["contract_test_only"],
                scores={"example_score": 0.5},
                uncertainty=1.0,
                calibration_set=None,
                validated_against=[],
                notes=["Contract fixture only."],
            )
            for _seq in sequences
        ]


def test_simulation_result_schema():
    """Verify the SimulationResult can be instantiated with the required fields."""
    result = SimulationResult(
        module="test_module",
        version="1.0.0",
        scope=["test_scope"],
        scores={"test_score": 0.95},
        uncertainty=0.1,
        calibration_set="test_dataset",
        validated_against=["test_validation_set"],
        notes=["Test note"]
    )
    
    assert result.module == "test_module"
    assert result.uncertainty == 0.1
    assert "test_note" not in result.notes
    assert "Test note" in result.notes


def test_dummy_proxy_contract():
    """Verify the DummyMembraneProxy obeys the interface contract."""
    proxy = DummyMembraneProxy()
    
    # 1. Simulate must return a SimulationResult
    result = proxy.simulate("KKLFKKILKYL")
    assert isinstance(result, SimulationResult)
    
    # 2. Uncertainty must be surfaced
    assert result.uncertainty == 1.0
    
    # 3. Must have a baseline comparison mechanism
    baseline = proxy.get_baseline()
    baseline_score = baseline.evaluate("KKLFKKILKYL")
    assert isinstance(baseline_score, float)


def test_external_adapter_protocol_runtime_checkable():
    adapter = ExampleExternalAdapter()

    assert isinstance(adapter, ExternalSimulationAdapter)
    assert adapter.describe()["name"] == "example_external_adapter"


def test_external_adapter_result_validation_accepts_matching_batch():
    adapter = ExampleExternalAdapter()
    sequences = ["KKLFKKILKYL", "GIGKFLHSAKK"]
    results = adapter.simulate_batch(sequences)

    validate_external_adapter_result(adapter, sequences, results)


def test_external_adapter_result_validation_rejects_length_mismatch():
    adapter = ExampleExternalAdapter()

    with pytest.raises(ValueError, match="returned 1 result"):
        validate_external_adapter_result(
            adapter,
            ["AAA", "KKK"],
            adapter.simulate_batch(["AAA"]),
        )


def test_external_adapter_result_validation_rejects_module_mismatch():
    adapter = ExampleExternalAdapter()
    result = adapter.simulate_batch(["AAA"])[0]
    result.module = "wrong"

    with pytest.raises(ValueError, match="does not match adapter name"):
        validate_external_adapter_result(adapter, ["AAA"], [result])


def test_external_adapter_result_validation_rejects_version_mismatch():
    adapter = ExampleExternalAdapter()
    result = adapter.simulate_batch(["AAA"])[0]
    result.version = "wrong"

    with pytest.raises(ValueError, match="does not match adapter version"):
        validate_external_adapter_result(adapter, ["AAA"], [result])


def test_external_adapter_result_validation_rejects_bad_uncertainty():
    adapter = ExampleExternalAdapter()
    result = adapter.simulate_batch(["AAA"])[0]
    result.uncertainty = 1.5

    with pytest.raises(ValueError, match="uncertainty"):
        validate_external_adapter_result(adapter, ["AAA"], [result])
