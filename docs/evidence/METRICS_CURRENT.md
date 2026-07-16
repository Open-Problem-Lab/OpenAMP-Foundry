Warning: truncated output (original token count: 44657)
Total output lines: 1471

# Current Pipeline Metrics — Single Source of Truth

Machine-readable snapshot: `outputs/metrics_snapshot.json` regenerated with `make metrics-snapshot`.

> **Purpose:** One authoritative table of current pipeline metrics. If any doc disagrees
> with this file, this file wins. Updated whenever benchmark/benchmark config changes.
>
> **Last updated:** 2026-07-16 (Phase AA reproducibility gate workflow integration)

> **Current verification note (2026-07-16):** Phase AA exposes the AARG-
> reproducibility gate as a repeatable CLI/Make workflow. It returns success
> only when all four required artifact IDs are present; this structural check
> does not establish biological validation, artifact correctness, or benchmark
> improvement.

## Changelog

### Phase AA — Reproducibility gate workflow integration
- Added `phase-aa-reproducibility-gate-check` and
  `make phase-aa-reproducibility-gate-check`.
- CLI rebuilds the AARG- gate from the four required artifact IDs and emits
  text or JSON; partial and not-established verdicts exit nonzero.
- Added CLI integration coverage for a verified gate and missing components,
  plus command help coverage.
- This is a dry-lab provenance control. It does not prove that the underlying
  run was scientifically correct or biologically valid.

### Phase AC AC3 — Aggregate disconfirming-evidence gate workflow integration
- Added `phase-ac-disconfirming-gate-check` CLI command and
  `make phase-ac-disconfirming-gate-check` demo target.
- CLI rebuilds DTR- records from their derived fields, reports the ACDG- verdict
  as text or JSON, and exits nonzero unless the verdict is verified.
- Added CLI help and integration coverage for verified and unresolved cases.
- This workflow check remains a dry-lab review control; it does not establish
  biological activity, safety, novelty, or benchmark improvement.

### Phase AC AC2 — Aggregate disconfirming-evidence gate
- Added `src/openamp_foundry/evidence/phase_ac_disconfirming_gate.py`.
- Aggregates validated DTR- records and exposes unresolved claim-affecting actions.
- Verdicts are `disconfirming_evidence_verified`, `disconfirming_evidence_partial`,
  or `disconfirming_evidence_not_established`.
- Refuted findings require `downgrade_claim`; inconclusive findings require
  `investigate`; neither can silently pass as verified.
- 18 focused tests in `tests/evidence/test_phase_ac_disconfirming_gate.py`.
- This gate is a review-control artifact, not evidence of biological activity,
  safety, novelty, or wet-lab performance.

### v0.10.36 — Phase C C3: Charge distribution report for benchmark shortcut visibility
- Added `src/openamp_foundry/evidence/charge_distribution_report.py`
- compute_charge_report(sequences, labels) → ChargeDistributionReport
- Stats: n_positive, n_negative, mean/median charge for both groups, fraction_positive_high_charge, fraction_negative_high_charge, charge_ratio (pos/neg mean ratio), charge_shortcut_likely flag, shortcut_warning string
- Shortcut detection: fires when fraction_positive_high_charge >= 0.60 OR charge_ratio >= 1.5
- format_charge_report() for human-readable output
- 63 tests in `tests/evidence/test_charge_distribution_report.py`
- BASELINE 6835→6898
- Closes Phase C C3 — every benchmark can now be analyzed for the charge shortcut; shortcut_likely=True is an explicit CI-checkable signal

### v0.10.35 — Phase C C8: Benchmark deprecation banner system
- Added `src/openamp_foundry/evidence/benchmark_deprecation.py`
- Functions: get_deprecated_cards(), get_active_cards(), build_deprecation_banner(), print_all_deprecation_banners(), check_no_deprecated_in_ranking() (raises DeprecatedBenchmarkError), deprecation_status_report()
- DeprecatedBenchmarkError: raised when deprecated benchmarks are used in ranking context
- Main registry confirmed: all 5 BMC- cards are active (no deprecated)
- 63 tests in `tests/evidence/test_benchmark_deprecation.py`
- BASELINE 6772→6835
- Closes Phase C C8 — stale benchmark authority is now machine-preventable via check_no_deprecated_in_ranking()

### v0.10.34 — Phase C C1: Machine-readable benchmark registry
- Added `src/openamp_foundry/evidence/benchmark_registry.py` — benchmark card registry
- 5 BMC- cards: BMC-0001 (precision@k, leakage_aware_split), BMC-0002 (charge-matched, charge_stratified), BMC-0003 (calibration, random_70_30), BMC-0004 (family-stratified, family_stratified), BMC-0005 (cheap enemy comparison, leakage_aware_split)
- API: get_card(bmc_id) → BenchmarkCard | None, validate_registry() → list[str]
- All 5 cards have ≥2 cheap enemy baselines and ≥2 known limitations
- 63 tests in `tests/evidence/test_benchmark_registry.py`
- BASELINE 6709→6772
- Closes Phase C C1 — governance is now enforceable: validate_registry() fails CI if any card is invalid

### v0.10.33 — Phase C C2: Benchmark card schema (BMC-)
- Added `src/openamp_foundry/evidence/benchmark_card.py` — BenchmarkCard schema
- BMC- schema: 12 fields (bmc_id, pipeline_version, benchmark_name, measurement_target, split_strategy, cheap_enemy_baselines, evaluation_metrics, known_limitations, deprecated, created_date, last_updated_date, notes)
- 14 validation rules: BMC- prefix, controlled vocabs for measurement_target (10 values)/split_strategy (10 values)/evaluation_metrics (12 values), cheap_enemy_baselines ≥1 required, known_limitations ≥1 required, deprecated+notes dependency, notes ≤500 chars
- 2 warnings: <2 cheap enemies, <2 known limitations
- 63 tests in `tests/evidence/test_benchmark_card.py`
- BASELINE 6646→6709
- Closes Phase C C2 — benchmark documentation is now machine-checkable; incomplete benchmark docs are blocked at schema level

### v0.10.32 — Phase B B8: Certificates linked to run manifest hashes
- Added `run_id` and `run_manifest_hash` optional parameters to `build_certificate()` in `src/openamp_foundry/evidence/certificate.py`
- Every certificate now carries the pipeline run_id and the SHA256 hash of the run manifest that produced it
- Backward-compatible: both fields default to empty string when not provided
- Makes every certificate traceable to the exact pipeline run for reproducibility auditing
- 63 tests in `tests/test_certificate_run_link.py`
- BASELINE 6583→6646
- Closes Phase B B8 — certificate-to-run-manifest traceability is now machine-verifiable

### v0.10.31 — Phase B B7: Candidate rejection certificate (CRC-)
- Added `src/openamp_foundry/evidence/candidate_rejection_certificate.py`
- CRC- schema: 12 fields (crc_id, pipeline_version, candidate_id, sequence, rejection_date, rejection_gate, rejection_reason, evidence_summary, proof_ladder_level_at_rejection, dry_lab_only, scores, notes)
- 13 validation rules: CRC- prefix, sequence validation, ISO date, gate/reason controlled vocab (10 gates, 12 reasons), evidence_summary non-empty, dry_lab_only=True enforced, proof-ladder cap at multi_signal_candidate_evidence
- 2 warnings: short evidence_summary, empty notes
- 63 tests in `tests/evidence/test_candidate_rejection_certificate.py`
- BASELINE 6520→6583
- Closes Phase B B7 — pipeline rejections are now first-class auditable artifacts

### v0.10.30 — Phase B B6: Human-readable certificate report
- Added `src/openamp_foundry/evidence/certificate_report.py` — build_certificate_report() function
- Converts cert dict to formatted text with labelled sections: CANDIDATE, PROOF LADDER, SCORES (with not-biological-proof notice), CHEAP-EXPLANATION CHECK, SELECTION REASON, KNOWN FAILURE MODES, RECOMMENDED NEXT STEPS, REFERENCES CHECKED, optional QUALITY TIER
- Footer: DRY-LAB COMPUTATIONAL OUTPUTS ONLY notice on every report
- Optional quality_report parameter integrates with assess_certificate_quality()
- 63 tests in `tests/test_certificate_report.py`
- BASELINE 6457→6520
- Closes Phase B B6 — domain experts can now inspect candidate certificates as readable text

### v0.10.29 — Phase B B5: Certificate quality-tier validator
- Added `src/openamp_foundry/evidence/certificate_quality.py` — assess_certificate_quality() function
- Three tiers: draft (candidate_id+sequence+scores) → internal_review (+selection_reason+known_failure_modes+proof_ladder_level+baseline_caveat+pipeline_version, no forbidden claims) → external_review_ready (+recommended_next_steps+references_checked+config_hash, no warnings)
- Returns: quality_tier, missing_fields, claim_violations, warnings, is_external_review_ready
- 63 tests in `tests/test_certificate_quality_validator.py`
- BASELINE 6394→6457
- Closes Phase B B5 — external-review readiness is now machine-verifiable, not reviewer-dependent

### v0.10.28 — Phase B B3: baseline_caveat field in certificates
- Added `baseline_caveat` field to `build_certificate()` in `src/openamp_foundry/evidence/certificate.py`
- Auto-computes three cheap-baseline flags: charge≥4, length 10-40aa, hydrophobic_fraction≥0.30
- Warns when all three pass: "simple conjunction rule would select this candidate without ML scoring"
- 63 tests in `tests/test_certificate_baseline_caveat.py` covering presence, charge/length/hydro flags, all-YES/NO paths, claim discipline, integration
- BASELINE 6331→6394
- Closes Phase B B3 — cheap-explanation visibility is now mandatory in every certificate

### v0.10.27 — Phase B B2: CertificateClaimBoundary schema
- Added `CertificateClaimBoundary` (CCB-) schema
- 10 fields: ccb_id, pipeline_version, certificate_id, candidate_id, boundary_date, unsupported_claim_classes (8-value vocab), boundary_statement, dry_lab_only, all_listed_classes_unsupported, notes
- 13 validation rules; 2 warnings; 63 tests
- BASELINE 6268→6331
- CLI: openamp-foundry certificate-claim-boundary-check
- Closes Phase B B2 — negative complement of PLC-; prevents score-to-proof drift by requiring explicit enumeration of unsupported claims

### v0.10.26 — Phase B B1: ProofLadderLevelCertificate schema
- Added `ProofLadderLevelCertificate` (PLC-) schema
- 14 fields: plc_id, pipeline_version, candidate_id, certificate_id, claimed_level, evidence_type, verifier_type, verification_date, supporting_artifact_ids, unsupported_claims, human_review_required, human_review_completed, dry_lab_only, notes
- 14 validation rules; 3 warnings; 63 tests
- BASELINE 6205→6268
- CLI: openamp-foundry proof-ladder-level-certificate-check
- Closes Phase B B1 — proof-ladder level claim is now a machine-checkable structured assertion

### v0.10.25 — Phase B B9: Certificate claim discipline CI gate
- Added `tests/test_certificate_claim_discipline.py` — 35-test CI gate
- Scans all certificate text fields against RISKY_PATTERNS (check_claims.py) and FORBIDDEN_CLAIM_PATTERNS (wave0_5_gate_checker.py)
- Tests: default cert clean, risky phrases detected, forbidden phrases detected, scanner coverage, JSON roundtrip discipline
- BASELINE 6170→6205
- Closes Phase B B9 — dry-lab certificate claim discipline is now machine-verifiable in CI

### v0.10.24 — Phase E E10: ExpertReviewExamplePackage schema
- Added `ExpertReviewExamplePackage` (ERP-) schema
- 14 fields: erp_id, pipeline_version, example_version, creation_date, review_domain, mock_candidates (1-10), overall_clarity_rating, synthesis_recommendation, reviewer_comments, dry_lab_only, is_example_data, example_use_case, summary, notes
- 16 validation rules; 3 warnings; 63 tests
- BASELINE 6107→6170
- CLI: openamp-foundry expert-review-example-package-check
- Closes Phase E E10 — CI-checkable example package that cannot leak real candidates

### v0.10.23 — Phase G G8: SyntheticBoundaryAuditRecord schema
- Added `SyntheticBoundaryAuditRecord` (SBR-) schema
- 14 fields: sbr_id, pipeline_version, batch_id, audit_date, evidence_source, total_candidates_checked, total_violations, violation_rate, blocked_upgrades, max_proposed_ladder_level, policy_enforced, enforcement_outcome, summary, notes
- 16 validation rules; 3 warnings; 63 tests
- BASELINE 6044→6107
- CLI: openamp-foundry synthetic-boundary-audit-record-check
- Closes Phase G G8 — proof-ladder boundary enforcement is now an auditable evidence artifact

### v0.10.22 — Phase G G2: RecalibrationRejectionSummary schema
- Added `RecalibrationRejectionSummary` (RRS-) schema
- 13 fields: rrs_id, pipeline_version, period_start, period_end, total_checkpoints_reviewed, total_refused, total_approved, refusal_rate, top_refusal_reason, gate_status, all_refusals_have_rrf, summary, notes
- 15 validation rules; 3 warnings; 63 tests
- BASELINE 5981→6044
- CLI: openamp-foundry recalibration-rejection-summary-check
- Closes Phase G G2 — aggregate refusal audit trail showing gate effectiveness

## v0.10.20 — Phase F F9 — Negative Result Dashboard (NRD-)

- **Schema**: `NegativeResultDashboard` — 13 fields, aggregate rejection statistics across a batch
- **Validation**: 13 rules — NRD- prefix, pipeline_version+batch_id non-empty, ISO date, total_candidates_evaluated ≥1, total_rejections in [0,evaluated], rejection_rate in [0,1] and consistent (tol 0.01), top_rejection_stage vocab (7 values), top_rejection_reason vocab (9 values), high_confidence_rejections in [0,total], all_rejections_have_nrr=True enforced, summary non-empty and ≤400 chars, notes ≤300 chars
- **Warnings**: 3 — rejection_rate >0.8, 100% rejection, notes empty
- **Tests**: 63 tests across 9 test classes; BASELINE 5855→5918
- **CLI**: `openamp-foundry negative-result-dashboard-check`
- **Completes NRR→NAS→FCR→NRD chain**: NRD- is the aggregate summary layer above individual failure records

> **New in v0.10.19 — Phase K K4 — Post-Experiment Calibration Intake (PCI-)**

> - **Schema**: `PostExperimentCalibrationIntake` — 13 fields, structured result-to-prediction comparison
> - **Validation**: 12 rules — PCI- prefix, pipeline_version+batch_id non-empty, ISO date, candidates_tested ≥1, candidates_with_results in [1,tested], observed_active in [0,with_results], hit rate in [0,1], hit rate consistency (tol 0.01), rationale non-empty and ≤400 chars, data_quality_confirmed=True enforced, notes ≤300 chars
> - **Warnings**: 3 — incomplete results (some candidates without results), observed_active=0, low hit rate without calibration update
> - **Tests**: 63 tests across 9 test classes; BASELINE 5792→5855
> - **CLI**: `openamp-foundry post-experiment-calibration-intake-check`
> - **Closes wet-lab loop**: PCI- feeds CIR- (calibration improvement) and P3/P5 (cycle summary)

> **New in v0.10.18 (Phase O O3 — Calibration Improvement Record (CIR-)):** CalibrationImprovementRecord — 12 fields, before/after audit record for calibration updates. 11 validation rules — CIR- prefix, pipeline_version non-empty, calibration_version_before/after non-empty and must differ, ISO date, metric_name controlled vocab (8 values), improvement_confirmed=True enforced, improvement_rationale non-empty and ≤400 chars, data_source_id non-empty, notes ≤300 chars. 3 warnings — wrong direction for higher-is-better/lower-is-better metrics, very small improvement (<0.005), notes empty. 63 tests across 9 test classes; BASELINE 5729→5792. CLI: openamp-foundry calibration-improvement-record-check. Completes Phase O: joins O1/O2/O4/O5 with the missing before/after change record.
> **New in v0.10.17 (Phase K K2 — Batch Experiment Priority Ranker):** BatchExperimentPriorityRanker — 11 fields, synthesis wave priority ordering. 10 validation rules — BPR- prefix, pipeline_version+batch_id non-empty, CSR- prefix, ISO date, priority_method controlled vocab (6 values), top_priority_candidates non-empty, priority_rationale non-empty and ≤400 chars, synthesis_wave ≥1, notes ≤300 chars. 3 warnings — resource_constraint_considered=False, expert_ranked without notes, synthesis_wave >5. 63 tests across 9 test classes; BASELINE 5666→5729. CLI: openamp-foundry batch-experiment-priority-ranker-check. BPR- records which candidates to synthesize first; CSR- records why candidates were selected.
> **New in v0.10.16 (Phase K K1 — Candidate Selection Rationale):** CandidateSelectionRationale — 12 fields, auditable candidate selection decisions. 12 validation rules: CSR- prefix, pipeline_version+batch_id non-empty, BSP- prefix, ISO date, strategy controlled vocab (4 values), candidate_count ≥1, count/ids consistency, ranking_method controlled vocab (6 values), calibration_gate_passed=True enforced, rationale non-empty and ≤400 chars, notes ≤300 chars. 3 warnings: large batch (>20), random_balanced without notes, expert_review without notes. 63 tests; BASELINE 5603→5666. CLI: openamp-foundry candidate-selection-rationale-check.
> **New in v0.10.15 (Phase K K3):** PilotPackageCompletenessReport — PPC- completeness gate: confirms CCS-+BSP-+PSC-+PRE-+BCM- all present and ESC- cleared before external sharing (12 fields, 12 validation rules, 3 warnings, 63 tests, BASELINE 5540→5603)
> **New in v0.10.14 (Phase F F1):** NegativeResultEntry — atomic NRR- failure record with stage/reason/confidence vocabulary, foundation for NAS- and FCR- chain (12 fields, 10 validation rules, 4 warnings, 63 tests, BASELINE 5477→5540)
> **New in v0.10.14 (Phase E E9):** DomainReviewOutcome — controlled taxonomy expert verdict on a PEP (11 fields, 9 validation rules, 3 warnings, 63 tests, BASELINE 5414→5477); closes ESC→RVQ→DRO review chain
> **New in v0.10.13 (Phase E E3):** ReviewerQuestionnaire — structured external review feedback with Likert clarity ratings, synthesis recommendation, and comments (13 fields, 10 validation rules, 4 warnings, 63 tests, BASELINE 5351→5414)
> **New in v0.10.12 (Phase F F4):** FailedCandidateBatchReport — batch-level failure summary linking RJR- and NAS- with failure rate consistency check (13 fields, 11 validation rules, 4 warnings, 63 tests, BASELINE 5288→5351)
> **New in v0.10.11 (Phase F F2):** NegativeResultArchiveSummary — validates batch of NRR- entries is complete before archiving (11 fields, 9 validation rules, 3 warnings, 63 tests, BASELINE 5225→5288)
> **New in v0.10.10 (Phase F F3):** RejectionReasonEntry — controlled vocabulary for pipeline rejections (11 fields, 9 validation rules, 3 warnings, 63 tests, BASELINE 5162→5225)
> **New in v0.10.9 (Phase Q Q3):** ExternalSharingClearance — auditable release gate before external PEP sharing (12 fields, 9 validation rules, 3 warnings, 63 tests, BASELINE 5099→5162)
> **New in v0.10.8 (Phase Q Q2):** PreRegistrationEntry — pre-experiment plan lock (14 fields, 9 validation rules, 4 warnings, 63 tests, BASELINE 5036→5099)
> **New in v0.10.7 (Phase Q Q1):** PilotEvidencePackageEntry — external export bundle (14 fields, CCS+BSP+PSC+PRE+BCM refs, completeness+safety enforcement, 63 tests, BASELINE 4973→5036).
> **New in v0.10.5 (Phase P P2):** RecalibrationRefusalEntry schema (10 fields: rrf_id, pipeline_version, trigger_id, recalibration_refused, refusal_reason, minimum_batches_required, batches_evaluated, refusal_notes, reviewer, dry_lab_only). recalibration_refused must be True — this schema only records valid refusals. 7 validation rules (RRF- prefix, CPS-/DRM- trigger prefix, recalibration_refused=True enforced, reason in 5 valid values, minimum_batches>=1, batches_evaluated>=0, notes<=400 chars). 2 warnings (insufficient_data but meets minimum; reviewer_override without documentation). Complements CalibrationImprovementRecord (O3). Added validate_recalibration_refusal() and validate_recalibration_refusal_dict(). Added 63 tests. CLI: openamp-foundry recalibration-refusal-check with --entry-json and --format text|json. Corrected inflated BASELINE from 4889 to 4784 (actual count 4721 + 63 = 4784).
> **New in v0.10.4 (Phase P P1):** BatchSelectionProposalEntry schema (12 fields: bsp_id, pipeline_version, gate_id, gate_passed, candidate_ids, selection_strategy, exploitation_fraction, exploration_fraction, max_brier_score_allowed, proposal_notes, reviewer, dry_lab_only). gate_passed must be True — a batch can only be proposed when the calibration readiness gate passes. 9 validation rules (BSP- prefix, CRG- prefix, gate_passed=True enforced, candidate_ids >=1, strategy in 5 valid values, fraction bounds, fraction sum=1.0 to 0.001 tolerance, Brier bounds [0.0,1.0], notes <=400 chars). 3 warnings (pure exploitation >=0.99, single candidate, marginal Brier >=0.25). Added validate_batch_selection_proposal() and validate_batch_selection_proposal_dict(). Added 68 tests. CLI: openamp-foundry batch-selection-proposal-check with --entry-json and --format text|json. Closes the calibration-to-selection loop from Phase O.
> **New in v0.10.3 (Phase O O5):** CalibrationReadinessEntry schema (11 fields, 8 validation rules, 2 warnings). Added validate_calibration_readiness() and validate_calibration_readiness_dict(). Added 68 tests. CLI: openamp-foundry calibration-readiness-check. Phase O (Calibration Quality Assurance) COMPLETE.
> **New in v0.10.2 (Phase O O4):** CrossBatchAggregatorEntry schema (12 fields, 9 validation rules, 3 warnings). Added validate_cross_batch_aggregator() and validate_cross_batch_aggregator_dict(). Added 68 tests. CLI: openamp-foundry cross-batch-aggregator-check.
> **New in v0.10.0 (Phase O O2):** PredictionDriftEntry schema (15 fields: monitor_id, pipeline_version, reference_batch_id, evaluation_batch_id, reference_mean_score, reference_std_score, evaluation_mean_score, evaluation_std_score, mean_shift_magnitude, population_size_reference, population_size_evaluation, drift_flag, drift_notes, reviewer, dry_lab_only). 8 validation rules (DRM- prefix, batch id must differ, scores 0.0-1.0, std >= 0.0, mean shift tolerance ±0.001, population >=1, notes <=400 chars, drift_flag=True requires non-empty notes). 4 warning conditions (unreported large shift >=0.1, small population <10, variance explosion >2x). 5 constants (DRIFT_NOTES_MAX_LENGTH=400, MEAN_SHIFT_TOLERANCE=0.001, SIGNIFICANT_DRIFT_THRESHOLD=0.1, MIN_POPULATION_FOR_RELIABLE_DRIFT=10, VARIANCE_EXPLOSION_RATIO=2.0). PredictionDriftEntry (15 fields), PredictionDriftResult (8 fields: monitor_id, pipeline_version, mean_shift_magnitude, drift_flag, passed, errors, warnings, dry_lab_only). validate_prediction_drift() (12+ error checks, 4 warning conditions). validate_prediction_drift_dict() (14 required fields guard). CLI (openamp-foundry prediction-drift-check) with --entry-json, --format text|json. make prediction-drift-check target. 68 tests. Phase O O2: prediction drift monitor is the earliest warning signal for pipeline score distribution shifts before wet-lab validation data arrives.
> **New in v0.9.9:** Calibration performance summary schema (O1 — Loop 138) — docs/evidence/CALIBRATION_PERFORMANCE_GUIDE.md with purpose, schema fields table (13 fields: summary_id, pipeline_version, evaluation_date, batch_ids_evaluated, total_candidates_evaluated, true_positive_count, false_positive_count, true_negative_count, false_negative_count, brier_score, calibration_notes, reviewer, dry_lab_only), 4 derived metrics (precision, recall, specificity, F1), 9 validation rules (CPS- prefix, >=1 batch, >=1 candidates, all counts >=0, total == TP+FP+TN+FN, Brier 0.0-1.0, notes<=400 chars, non-empty reviewer, dry_lab_only must be False), 4 warning conditions (high FP rate >0.5, low recall <0.3, poor Brier >0.25, small sample <10), honest-use boundary. CalibrationPerformanceEntry dataclass (13 fields, dry_lab_only=False), CalibrationPerformanceResult dataclass (8 fields: summary_id, pipeline_version, total_candidates_evaluated, brier_score, passed, errors, warnings, dry_lab_only=False), MAX_CALIBRATION_NOTES_LENGTH=400, MIN_CANDIDATES_FOR_RELIABLE_ESTIMATE=10, HIGH_FP_RATE_THRESHOLD=0.5, LOW_RECALL_THRESHOLD=0.3, POOR_BRIER_SCORE_THRESHOLD=0.25. validate_calibration_performance() (9+ error checks: CPS- prefix, >=1 batch, >=1 candidates, >=0 counts, confusion sum match, Brier bounds, notes<=400, non-empty reviewer, dry_lab_only must be False; 4 warnings: high FP, low recall, poor Brier, small sample). validate_calibration_performance_dict() (12 required fields guard). CLI (openamp-foundry calibration-performance-check) with --entry-json, --format text|json. make calibration-performance-check target. 68 tests. Phase O O1: calibration performance summaries now measure how well predictions match experimental outcomes. Phase O (Calibration Quality Assurance) started.
> **New in v0.9.8:** Experiment priority justification schema (N5 — Loop 137) — docs/evidence/EXPERIMENT_PRIORITY_GUIDE.md with purpose, schema fields table (12 fields: justification_id, batch_id, pipeline_version, decision_date, selection_criteria, rejected_alternatives, rejection_rationale, resource_constraint, safety_reviewed, pre_specified, decided_by, dry_lab_only), 8 validation rules (EPJ- prefix, >=2 selection criteria, >=1 rejected alternative, non-empty rejection_rationale<=500 chars, resource_constraint<=200 chars, safety_reviewed must be True, non-empty decided_by, dry_lab_only must be True), 4 warning conditions (post-hoc, minimum criteria, no resource constraint, many criteria), honest-use boundary. ExperimentPriorityEntry dataclass (12 fields, dry_lab_only=True), ExperimentPriorityResult dataclass (8 fields: justification_id, batch_id, criteria_count, rejected_alternative_count, safety_reviewed, passed, errors, warnings, dry_lab_only=True), MINIMUM_SELECTION_CRITERIA=2, MAXIMUM_SELECTION_CRITERIA_WARNING=6, MAX_REJECTION_RATIONALE_LENGTH=500, MAX_RESOURCE_CONSTRAINT_LENGTH=200. validate_experiment_priority() (8+ error checks: EPJ- prefix, >=2 criteria, >=1 alternative, non-empty rationale<=500 chars, constraint<=200 chars, safety_reviewed must be True, non-empty decided_by, dry_lab_only must be True; 4 warnings: post-hoc, minimum criteria, no constraint, many criteria). validate_experiment_priority_dict() (11 required fields guard). CLI (openamp-foundry experiment-priority-check) with --entry-json, --format text|json. make experiment-priority-check target. 62 tests. Phase N N5: batch selection decisions are now documented with full audit trail over alternatives. Phase N (Pre-registration & Baseline Honesty) is fully complete with N1-N5.
> **New in v0.9.7:** Negative result record schema (N4 — Loop 136) — docs/evidence/NEGATIVE_RESULT_GUIDE.md with purpose, schema fields table (14 fields: record_id, batch_id, pipeline_version, record_date, failure_category, failure_description, candidate_ids, assay_type, expected_outcome, observed_outcome, hypothesis_impact, will_be_reported, recorded_by, dry_lab_only), 6 valid failure categories (assay_quality_failure, below_activity_threshold, excessive_toxicity, model_overprediction, pipeline_error, stability_failure), 5 valid assay types (cytotoxicity_assay, hemolysis_assay, membrane_disruption_assay, mic_assay, stability_assay), 9 validation rules, 3 warning conditions (not reported, large failure set, model overprediction without recalibration), honest-use boundary. NegativeResultEntry dataclass (14 fields), NegativeResultResult dataclass (7 fields), validate_negative_result() (9+ error checks: NRR- prefix, valid failure_category, non-empty failure_description<=500 chars, >=1 candidate_ids, valid assay_type, non-empty expected_outcome/observed_outcome, non-empty hypothesis_impact<=300 chars, non-empty recorded_by; 3 warnings: not reported contributes to publication bias, >10 candidates suggests systematic issue, model_overprediction without calibration mention triggers calibration review), validate_negative_result_dict() (13 required fields guard). CLI (openamp-foundry negative-result-check) with --entry-json, --format text|json. make negative-result-check target. 68 tests. Phase N N4: failed experiments are now documented, not discarded.
> **New in v0.9.6:** Baseline comparison manifest schema (N3 — Loop 135) — docs/evidence/BASELINE_COMPARISON_GUIDE.md with purpose, schema fields table (14 fields: manifest_id, batch_id, pipeline_version, comparison_date, metric_name, pipeline_score, baseline_scores, pipeline_beats_all_baselines, effect_size, p_value, comparison_direction, notes, reviewer, dry_lab_only), 6 valid metric names (fold_change_mic, hemolysis_fraction, hit_rate, mic_value, novelty_score, selectivity_index), 2 valid comparison directions (higher_is_better, lower_is_better), 11 validation rules, 4 warning conditions (pipeline loses, inconsistent verdict, no p-value, large unchecked effect), honest-use boundary. BaselineComparisonEntry dataclass (14 fields), BaselineComparisonResult dataclass (7 fields), validate_baseline_comparison() (11+ error checks: BCM- prefix, valid metric_name, finite pipeline_score, >=1 baseline, finite baseline_scores, finite effect_size, p_value in [0.0,1.0] or -1.0, valid comparison_direction, notes<=300, non-empty reviewer, dry_lab_only must be True; 4 warning conditions: underperforms, inconsistent verdict, no p-value, large+unchecked), validate_baseline_comparison_dict() (13 required fields guard). CLI (openamp-foundry baseline-comparison-check) with --entry-json, --format text|json. make baseline-comparison-check target. 68 tests. Phase N N3: every performance claim against a baseline is now machine-verifiable.
> **New in v0.9.5:** Pre-registration form schema (N1 — Loop 133) — docs/evidence/PRE_REGISTRATION_GUIDE.md with purpose, schema fields table (13 fields: registration_id, batch_id, pipeline_version, registration_date, primary_hypothesis, primary_outcome_metric, success_threshold, baseline_comparators, candidate_ids, assay_type, statistical_test, registered_by, dry_lab_only), 6 valid primary outcome metrics, 5 valid assay types, 10 validation rules, 4 warning conditions, honest-use boundary. PreRegistrationEntry dataclass (13 fields), PreRegistrationResult dataclass (6 fields), validate_pre_registration() (10+ error checks: PRE- prefix, non-empty hypothesis<=500 chars, valid outcome metric, finite success_threshold, >=1 baseline_comparators, >=1 candidate_ids, valid assay_type, non-empty statistical_test<=200 chars, non-empty registered_by, dry_lab_only must be True; 4 warning conditions: no random baseline, large candidate set >20, short hypothesis <50 chars, placeholder statistical test TBD/N/A/NA/none), validate_pre_registration_dict() (12 required fields guard). CLI (openamp-foundry pre-registration-check) with --entry-json, --format text|json. make pre-registration-check target. 62 tests. Phase N (Pre-registration & Baseline Honesty) started with N1.
> > **New in v0.9.3:** Audit chain completeness checker (M5 — Loop 132) — docs/evidence/AUDIT_CHAIN_GUIDE.md with purpose, schema fields table (16 fields: chain_id, batch_id, pipeline_version, audit_date, 9 has_* bools, missing_links, auditor, dry_lab_only), 9 required chain links, validation rules (5), warning conditions (2: single auditor, future date), honest-use boundary. src/openamp_foundry/evidence/audit_chain_completeness.py with AuditChainEntry dataclass (16 fields: chain_id, batch_id, pipeline_version, audit_date, 9 has_* bools, missing_links list[str], auditor, dry_lab_only=True), AuditChainResult dataclass (7 fields: chain_id, batch_id, missing_link_count, passed, errors, warnings, dry_lab_only=True), CHAIN_LINK_FIELDS (9 entries), CHAIN_LINK_COUNT (9), AUDITOR_EMAIL_HINT ("@"), IMPLAUSIBLE_YEAR_THRESHOLD (2030), validate_audit_chain() (5+ error checks: ACH- prefix, non-empty auditor, dry_lab_only must be True, each false chain link errors, missing_links consistency; 2 warnings: no email, future date), validate_audit_chain_dict() (15 required fields guard). CLI (openamp-foundry audit-chain-check) with --entry-json, --format text|json. make audit-chain-check target. 39 tests. Phase M M5: the evidence chain is now machine-checkable end to end. Phase M (Audit Trail Infrastructure) is fully complete with M1-M5.
> **New in v0.9.1:** Score decomposition report schema (M3 — Loop 130) — docs/evidence/SCORE_DECOMPOSITION_GUIDE.md with purpose, schema fields table (12 fields), valid scoring methods (6), validation rules (9), warning conditions (4), honest-use boundary. src/openamp_foundry/evidence/score_decomposition_report.py with ScoreDecompositionEntry dataclass (12 fields: report_id, batch_id, candidate_id, pipeline_version, composite_score, component_scores, component_weights, scoring_method, score_range_min, score_range_max, reviewer, dry_lab_only=True), ScoreDecompositionResult dataclass (7 fields: report_id, batch_id, candidate_id, scoring_method, passed, errors, warnings, dry_lab_only=True), VALID_SCORING_METHODS (6: additive_weighted, geometric_mean, harmonic_mean, max_component, min_component, rank_aggregation), MINIMUM_COMPONENTS (2), WEIGHT_SUM_TOLERANCE (0.01), DOMINANT_WEIGHT_THRESHOLD (0.6), UNBALANCED_RATIO_THRESHOLD (5.0), MAX_COMPONENTS_WARNING (8), LOW_SCORE_FRACTION (0.2), validate_score_decomposition() (9 error checks: SDR- prefix, score_range_min<score_range_max, composite_score in range, >=2 components, weight keys match score keys, weights sum to ~1.0, valid scoring_method, non-empty reviewer, dry_lab_only must be True; 4 warning conditions: dominant component, unbalanced weights, many components, low composite score), validate_score_decomposition_dict() (11 required fields guard). CLI (openamp-foundry score-decomposition-check) with --entry-json, --format text|json. make score-decomposition-check target. Phase M M3: every composite score is now machine-decomposable into its named components for external audit.
> **New in v0.9.0:** Claim-to-evidence mapper schema (M2 — Loop 129) — docs/evidence/CLAIM_TO_EVIDENCE_GUIDE.md with purpose, schema fields table (10 fields), valid claim types (7), validation rules (7), warning conditions (4), honest-use boundary, CLI usage. src/openamp_foundry/evidence/claim_to_evidence_mapper.py with ClaimToEvidenceEntry dataclass (10 fields: mapping_id, batch_id, pipeline_version, claim_text, claim_type, supporting_artifact_ids, evidence_level, pre_specified, reviewer, dry_lab_only=True), ClaimToEvidenceResult dataclass (7 fields: mapping_id, batch_id, claim_type, passed, errors, warnings, dry_lab_only=True), VALID_CLAIM_TYPES (7: activity_prediction, calibration_statement, novelty_claim, performance_comparison, reproducibility_claim, safety_assessment, selection_rationale), VALID_EVIDENCE_LEVELS (6: 1-6), MAX_CLAIM_TEXT_LENGTH (500), LONG_CLAIM_TEXT_THRESHOLD (300), WEAK_EVIDENCE_THRESHOLD (2), validate_claim_to_evidence() (7 error checks: CEM- prefix, non-empty claim_text<=500 chars, valid claim_type, non-empty supporting_artifact_ids, valid evidence_level 1-6, non-empty reviewer, dry_lab_only must be True; 4 warning conditions: post-hoc, weak evidence, single artifact, long claim text), validate_claim_to_evidence_dict() (9 required fields guard). CLI (openamp-foundry claim-to-evidence-check) with --entry-json, --format text|json. make claim-to-evidence-check target. Phase M M2: every scientific claim is now machine-mapped to its supporting artifacts for external audit.
> **New in v0.8.9:** Pipeline decision audit entry schema (M1 — Loop 128) — docs/evidence/PIPELINE_DECISION_AUDIT_GUIDE.md with purpose, required field table (13 fields), valid decision types (7), warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/pipeline_decision_audit.py with PipelineDecisionAuditEntry dataclass (13 fields: audit_id, batch_id, pipeline_version, decision_date, decision_type, decision_description, rationale, alternatives_considered, affected_candidate_count, evidence_level, pre_specified, reviewer, dry_lab_only), PipelineDecisionAuditResult dataclass (5 fields: audit_id, batch_id, decision_type, passed, errors, warnings, dry_lab_only=True), VALID_DECISION_TYPES (7: benchmark_updated, calibration_adjusted, candidate_ranked, candidate_rejected, filter_applied, safety_flag_applied, threshold_chosen), VALID_EVIDENCE_LEVELS (6: 1-6), MAX_DESCRIPTION_LENGTH (500), MAX_RATIONALE_LENGTH (1000), validate_pipeline_decision_audit() (12 checks: AUD- prefix, non-empty batch_id/pipeline_version/reviewer, YYYY-MM-DD decision_date, valid decision_type, non-empty description<=500 chars, non-empty rationale<=1000 chars, affected_candidate_count>=0, valid evidence_level, dry_lab_only must be True; post-hoc warns, empty alternatives warns, low evidence warns, zero affected warns), validate_pipeline_decision_audit_dict() (12 required fields guard). CLI (openamp-foundry pipeline-decision-audit-check) with --entry-json, --format text|json. make pipeline-decision-audit-check target. Phase M M1: every pipeline decision is now machine-validated and traceable for external audit.
> **New in v0.8.8:** Dataset release package checker (L5 — Loop 127) — docs/evidence/DATASET_RELEASE_GUIDE.md with purpose, required field table (13 fields), valid license identifiers (5), warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/dataset_release.py with DatasetReleaseEntry dataclass (13 fields: release_id, dataset_name, dataset_version, release_date, license_identifier, data_sources, contains_sequences, contains_activity_data, dual_use_assessed, usage_policy_url, contact_email, release_approved, dry_lab_only), DatasetReleaseResult dataclass (4 fields: release_id, dataset_name, passed, errors, warnings, dry_lab_only=True), VALID_LICENSE_IDENTIFIERS (5: Apache-2.0, CC-BY-4.0, CC-BY-NC-4.0, CC0-1.0, MIT), MINIMUM_DATA_SOURCES (1), validate_dataset_release() (11 checks: DSR- prefix, non-empty dataset_name/dataset_version/usage_policy_url/contact_email, YYYY-MM-DD release_date, valid license_identifier, data_sources>=1, dual_use_assessed must be True, release_approved must be True, dry_lab_only must be True; CC-BY-NC-4.0 warns, single source warns), validate_dataset_release_dict() (12 required fields guard). CLI (openamp-foundry dataset-release-check) with --entry-json, --format text|json. make dataset-release-check target. Phase L L5 completes Phase L: open dataset releases now have machine-validated data governance checks.
> **New in v0.8.7:** Multi-candidate comparison schema (L4 — Loop 126b) — docs/evidence/MULTI_CANDIDATE_COMPARISON_GUIDE.md with purpose, required field table (11 fields), minimum requirements (2 candidates, 2 criteria), warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/multi_candidate_comparison.py with MultiCandidateComparisonEntry dataclass (11 fields: comparison_id, batch_id, pipeline_version, comparison_date, candidate_ids, comparison_criteria, top_candidate_id, top_candidate_rationale, evidence_level, reviewer, dry_lab_only), MultiCandidateComparisonResult dataclass (5 fields: comparison_id, batch_id, candidate_count, passed, errors, warnings, dry_lab_only=True), MINIMUM_CANDIDATES (2), MINIMUM_CRITERIA (2), RECOMMENDED_CRITERIA (3), MAX_RATIONALE_LENGTH (500), LARGE_CANDIDATE_SET_THRESHOLD (10), VALID_EVIDENCE_LEVELS (6: 1-6), validate_multi_candidate_comparison() (11 checks: CMP- prefix, non-empty batch_id/pipeline_version/reviewer, YYYY-MM-DD comparison_date, candidate_ids>=2, comparison_criteria>=2, top_candidate_id in candidate_ids, non-empty rationale<=500 chars, valid evidence_level, dry_lab_only must be True; evidence_level<=2 warns, candidate_count>10 warns, criteria_count<3 warns), validate_multi_candidate_comparison_dict() (10 required fields guard). CLI (openamp-foundry multi-candidate-comparison-check) with --entry-json, --format text|json. make multi-candidate-comparison-check target. Phase L L4: side-by-side candidate comparisons are now machine-validated for publication-ready supplementary tables.
> **New in v0.8.6:** Candidate summary card schema (L3 — Loop 126) — docs/evidence/CANDIDATE_SUMMARY_CARD_GUIDE.md with purpose, required field table (12 fields), valid activity labels (5), valid amino acid set (20 standard), warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/candidate_summary_card.py with CandidateSummaryCardEntry dataclass (12 fields: card_id, candidate_id, batch_id, pipeline_version, sequence, sequence_length, evidence_level, predicted_activity, safety_flags, selection_rationale_id, reviewer, dry_lab_only), CandidateSummaryCardResult dataclass (5 fields: card_id, candidate_id, sequence_length, passed, errors, warnings, dry_lab_only=True), VALID_ACTIVITY_LABELS (5: high_activity, inactive, low_activity, moderate_activity, uncertain), VALID_AMINO_ACIDS (20 standard one-letter codes), LONG_PEPTIDE_THRESHOLD (50), VALID_EVIDENCE_LEVELS (6: 1-6), validate_candidate_summary_card() (11 checks: CRD- prefix, non-empty candidate_id/batch_id/pipeline_version/reviewer, non-empty sequence with valid amino acids, sequence_length==len(sequence), valid evidence_level, valid predicted_activity, SEL- prefix on selection_rationale_id, dry_lab_only must be True; evidence_level<=2 warns, safety_flags non-empty warns, uncertain activity warns, length>50 warns), validate_candidate_summary_card_dict() (11 required fields guard). CLI (openamp-foundry candidate-summary-card-check) with --entry-json, --format text|json. make candidate-summary-card-check target. Phase L L3: every candidate now has a machine-validated publication-ready summary card.
> **New in v0.8.5:** Reproducibility manifest schema (L2 — Loop 125) — docs/evidence/REPRODUCIBILITY_MANIFEST_GUIDE.md with purpose, required field table (11 fields), package checksums format, data checksums format, warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/reproducibility_manifest.py with ReproducibilityManifestEntry dataclass (11 fields: manifest_id, batch_id, pipeline_version, run_date, python_version, package_checksums, data_checksums, random_seeds, hardware_summary, reviewer, dry_lab_only), ReproducibilityManifestResult dataclass (6 fields: manifest_id, batch_id, package_count, data_file_count, passed, errors, warnings, dry_lab_only=True), MINIMUM_PACKAGES (3), MINIMUM_DATA_FILES (1), RECOMMENDED_PACKAGES (5), validate_reproducibility_manifest() (10 checks: RPM- prefix, non-empty batch_id/pipeline_version/python_version/hardware_summary/reviewer, YYYY-MM-DD run_date, package_checksums>=3, data_checksums>=1, dry_lab_only must be True; empty random_seeds warns, package_count<5 warns, hardware_summary contains 'unknown' warns), validate_reproducibility_manifest_dict() (10 required fields guard). CLI (openamp-foundry reproducibility-manifest-check) with --entry-json, --format text|json. make reproducibility-manifest-check target. Phase L L2: every pipeline run now has a machine-validated reproducibility record.
> **New in v0.8.4:** Preprint evidence bundle schema (L1 — Loop 124) — docs/evidence/PREPRINT_BUNDLE_GUIDE.md with purpose, required field table (11 fields), minimum artifact count (3), evidence level guide, warnings, validation workflow, honest-use boundary. src/openamp_foundry/evidence/preprint_bundle.py with PreprintBundleEntry dataclass (11 fields: bundle_id, batch_id, pipeline_version, submission_date, title, artifact_ids, evidence_level, preprint_doi, contact_email, release_approved, dry_lab_only), PreprintBundleResult dataclass (5 fields: bundle_id, batch_id, artifact_count, passed, errors, warnings, dry_lab_only=True), MINIMUM_ARTIFACTS (3), RECOMMENDED_ARTIFACT_COUNT (5), MAX_TITLE_LENGTH (300), VALID_EVIDENCE_LEVELS (6: 1-6), validate_preprint_bundle() (10 checks: BND- prefix, non-empty batch_id/pipeline_version/contact_email, YYYY-MM-DD submission_date, non-empty title<=300 chars, artifact_ids>=3, valid evidence_level 1-6, release_approved must be True, dry_lab_only must be True; evidence_level<=2 warns, empty preprint_doi warns, artifact_count<5 warns), validate_preprint_bundle_dict() (10 required fields guard). CLI (openamp-foundry preprint-bundle-check) with --entry-json, --format text|json. make preprint-bundle-check target. Phase L L1: scientific preprints now have a machine-validated evidence bundle structure.
> **New in v0.8.3:** Uncertainty quantification report schema (K5 — Loop 123) — docs/evidence/UNCERTAINTY_REPORT…22657 tokens truncated…n) |
| synthesis | 0.4228 | Anti-signal | **0.4968** | Near-zero | **↗ Reclassified** — n=191 artifact |
| boman_activity | 0.4620 | Near-zero | **0.3291** | Anti-signal | **↘ Reclassified** — stronger anti-AMP on diverse set |
| safety | 0.3487 | Anti-signal | **0.4459** | Anti-signal | ↑0.0972 (less extreme) |
| serum_stability | 0.2231 | Anti-signal | **0.3767** | Anti-signal | ↑0.1536 (less extreme) |
| rich_selectivity | 0.1973 | Anti-signal | **0.3407** | Anti-signal | ↑0.1434 (less extreme) |

### Updated key findings

The expanded benchmark (n=1000) **changes two classifications** and **tightens uncertainty**:

1. **synthesis was an anti-signal artifact on n=191.** At 0.4968 on n=1000, synthesis feasibility is essentially neutral — AMPs and decoys have similar average synthesis difficulty. The original finding (0.4228) was a small-n artifact on the original 95-sequence benchmark, which was enriched for manually curated AMPs with unusual biophysical properties. On the more diverse 500-AMP set, this bias disappears.

2. **boman_activity is more strongly anti-AMP than previously known.** At 0.3291 on n=1000, random decoys score substantially higher on Boman activity than most AMPs. The Boman index (a measure of overall residue solubility) is designed to detect peptides with broad-spectrum binding potential — a property that random decoys drawn from Swiss-Prot frequencies happen to have. This does NOT mean the Boman signal is harmful; its contribution to the ensemble works through the disagreement signal (|activity − boman|), not through independent discrimination. A high-disagreement candidate is one where the activity and Boman scorers disagree — this is the intended signal.

3. **selectivity_proxy is weaker on the diverse set** (0.6702 vs 0.7729). The charge+GRAVY heuristic distinguishes AMPs from random decoys less reliably when applied to a broader AMP diversity (UniProt-reviewed + APD6 natural). This is expected: the original 95-AMP benchmark was manually curated and enriched for canonical amphipathic helix AMPs that have characteristic charge and GRAVY values.

4. **activity remains the dominant signal** (0.7969, signal-bearing). The ensemble's primary discriminative power still comes from the activity scorer, as expected.

5. **rich_selectivity, safety, and serum_stability remain anti-signal** but are less extreme on n=1000 (moving toward 0.5). The expanded set includes more diverse AMPs with more moderate biophysical properties, so the anti-AMP penalty is less severe on average.

6. **The expert composite's delta widens from −0.0735 to −0.0935** because the selectivity-focused components penalize more diverse AMPs more heavily. The expert composite is NOT a good binary discriminator — this is by design, as its components focus on within-AMP differentiation.

### What this means for the pipeline:

1. The expert composite should NOT replace the ensemble for AMP/non-AMP triage. However, the rich_selectivity component (AUROC=0.3407 for AMP-vs-decoy but detection AUROC=0.7138 for hemolysis) is anti-AMP by design — it penalises high hydrophobicity and charge that define AMPs. This is the correct tradeoff.
2. The ensemble (activity + safety + synthesis + novelty + Boman) remains the primary synthesis gate.
3. The expert components may still add value for **within-AMP ranking** (selectivity and safety differentiation among candidates that already pass the activity gate) — but this has not been demonstrated and should not be assumed.
4. The `boman_activity` scorer (AUROC 0.329, well below random) does NOT discriminate AMPs from random decoys. Its only useful contribution to the ensemble is through the disagreement signal — which requires a partner scorer to disagree with.
5. `motif_novelty` and `novelty` are 0.5 by construction (no k-mer index, no references in this benchmark) — they are correctly neutral, not noise.

**Honest limitation:** This benchmark measures binary AMP-vs-decoy discrimination
only. The expert composite's selectivity, safety, and synthesis components are
designed for within-AMP candidate differentiation, not for separating AMPs from
non-AMPs. A within-AMP ranking benchmark (comparing selective vs hemolytic AMPs)
has been added in v0.5.9 (see Within-AMP Selectivity Benchmark section below).

---


## Within-AMP Selectivity Benchmark (v0.5.x — added 2026-07-01)

> The expert ablation benchmark found that safety, synthesis, and serum stability are
> anti-signal for AMP-vs-decoy discrimination. But those scorers were designed for
> *within-AMP ranking*: distinguishing hemolytic AMPs from selective AMPs. This benchmark
> tests them on that intended task.
>
> Run: `make bench-selectivity`

**Dataset:** 42 known AMPs with literature HC50 values (hemolysis_reference.csv)

| Class | HC50 threshold | Count |
|-------|:--------------:|:-----:|
| HEMOLYTIC | < 25 µg/mL | 14 |
| SELECTIVE | >= 100 µg/mL | 21 |
| BORDER (excluded from AUROC) | 25-100 µg/mL | 7 |

**Task:** Can pipeline scorers distinguish hemolytic AMPs from selective AMPs?
For safety/selectivity scorers, the correct direction is: hemolytic AMPs score *lower*
(less safe, less selective). We report "hemolysis detection AUROC" where higher = better
risk detection (1 - raw AUROC for safety-type scorers).

### Per-score hemolysis detection AUROC

| Score | Detection AUROC | CI₉₅ | Significant? | Verdict |
|-------|:--------------:|:----:|:------------:|---------|
| synthesis | 0.8027 | 0.63-0.95 | **YES** | Synthesis difficulty correlates with hemolysis — hemolytic AMPs are harder to synthesize |
| boman_activity | 0.6837 | 0.49-0.85 | No (CI lo < 0.5) | Weak trend: hemolytic AMPs have lower Boman activity |
| serum_stability | 0.6020 | 0.40-0.80 | No (CI lo < 0.5) | Weak trend: hemolytic AMPs less serum-stable |
| expert_composite | 0.5119 | 0.31-0.71 | No (CI lo < 0.5) | Better than ensemble but not significant |
| hinge_selectivity | 0.4456 | 0.24-0.64 | No | No selectivity signal from hinge detection |
| selectivity_proxy | 0.4133 | 0.28-0.55 | No | **FAILS** — charge/GRAVY does not capture hemolysis |
| safety | 0.3844 | 0.26-0.52 | No | **FAILS** — confirms melittin blind spot |
| activity | 0.3401 | 0.16-0.52 | No | Activity scorer ranks hemolytic AMPs *higher* (anti-selective) |
| ensemble | 0.3486 | 0.17-0.54 | No | Ensemble inherits activity scorer's anti-selective bias |

**Key findings:**

1. **The safety scorer does NOT detect hemolysis** (detection AUROC = 0.3844, CI lo = 0.26).
   This confirms the expert ablation's prediction and the previously documented melittin
   blind spot. All 14 hemolytic AMPs in the reference set score safety >= 0.8 — the scorer
   cannot distinguish them from selective AMPs.

2. **The selectivity proxy does NOT detect hemolysis** (detection AUROC = 0.4133, CI lo = 0.28).
   The charge/GRAVY heuristic is insufficient for capturing hemolysis risk. Hemolytic AMPs
   like melittin and protegrin have optimal charge (+2 to +7) and moderate GRAVY, so the
   proxy assigns them high selectivity scores.

3. **Synthesis feasibility is the only significant risk detector** (detection AUROC = 0.8027,
   CI lo = 0.63). Hemolytic AMPs tend to be harder to synthesize: they have more cysteines
   (protegrins, tachyplesins), repeat runs, and hydrophobic segments. This is an incidental
   correlation, not a designed safety feature — but it means the synthesis gate provides
   partial hemolysis filtering as a side effect.

4. **The activity scorer is anti-selective** (detection AUROC = 0.34): it ranks hemolytic
   AMPs *higher* than selective AMPs. This is expected: hemolytic AMPs like melittin have
   strong amphipathic helices, high hydrophobic moment, and high charge — exactly the
   features the activity scorer rewards. The ensemble inherits this bias.

5. **The expert composite now includes rich_selectivity** (detection AUROC=0.7138, CI 0.63-0.80) as its hemolysis-risk component, replacing the old hemolysis_safety (was 0.5119 vs
   0.3486) but not significantly so (CI includes 0.5). The added selectivity and safety
   components partially offset the activity scorer's anti-selective bias, but not enough
   to reach significance at n=14 vs n=21.

**Honest limitation:** HC50 values are approximate literature values with high inter-assay
variability (RBC source, buffer, incubation time, concentration range). The binary
thresholds (25 / 100 µg/mL) are coarse. A larger reference set with standardized HC50
measurements would tighten the CIs and might flip some near-zero results to significant.
The current sample size (14 vs 21) is too small for confident conclusions on any score
with CI lower bound below 0.5.

**Implication for the pipeline:** Hemolysis remains unpredictable by the current
physicochemical scorers. The melittin blind spot is confirmed quantitatively. Hemolysis
must be assayed experimentally for every candidate regardless of safety or selectivity
score. The synthesis gate provides partial indirect filtering but should not be relied
upon as a hemolysis predictor.

## Dedicated Hemolysis Risk Scorer (v0.5.10 — added 2026-07-01)

> The selectivity benchmark (v0.5.9) confirmed that the safety scorer fails
> hemolysis detection (AUROC=0.3844). A dedicated hemolysis risk scorer was
> built from empirically-validated components identified in that benchmark.
>
> **v0.5.11 correction:** The original 42-peptide reference set (14 hemolytic
> vs 21 selective, n=35) produced detection AUROC=0.9218 (CI 0.82-0.99). This
> was **small-sample inflation**. Expansion to 238 peptides using DBAASP human
> erythrocyte data (54 hemolytic vs 125 selective, n=179) dropped the detection
> AUROC to 0.5650 (CI 0.47-0.66) — direction correct but NOT statistically
> significant. The scorer retains weak directional signal but should not be
> trusted as a standalone hemolysis detector.
>
> Run: `make bench-selectivity` (hemolysis_risk column in the output)

**Module:** `src/openamp_foundry/scoring/hemolysis.py`

**Components** (individual AUROC from original n=14 vs n=21; may not replicate on expanded set):

| Component | Individual AUROC (n=35) | Weight | Signal source |
|-----------|:-----------------------:|:------:|---------------|
| Synthesis difficulty (1 - synth_feasibility) | 0.8027 | 0.30 | Incidental: hemolytic AMPs harder to synthesize |
| Aromatic fraction (F/W/Y density) | 0.8299 | 0.30 | Trp/Phe intercalation in both membrane types |
| Cationic-on-hydrophobic-face fraction | 0.7585 | 0.20 | Poor amphipathic face segregation |
| Cysteine fraction | 0.7500 | 0.20 | Beta-sheet defensin/protegrin class |

**Combined performance (expanded n=179):**

| Metric | Original (n=35) | Expanded (n=179) | Notes |
|--------|:---------------:|:-----------------:|-------|
| **Detection AUROC** | **0.9218** | **0.5650** | Small-sample inflation corrected |
| CI₉₅ lower bound | 0.82 | 0.47 | No longer > 0.5 — not significant |
| CI₉₅ upper bound | 0.99 | 0.66 | |
| Mean hemolytic risk | 0.4064 (n=14) | 0.2042 (n=54) | Direction still correct |
| Mean selective risk | 0.1501 (n=21) | 0.1535 (n=125) | |
| Safety scorer detection | 0.3844 | 0.5116 | Safety also improves slightly with more data |

**Expert composite integration (expanded n=179):**

| Metric | Before (v0.5.9, n=35) | After (v0.5.10, n=35) | Expanded (n=179) |
|--------|:---------------------:|:---------------------:|:-----------------:|
| Expert composite detection AUROC | 0.5119 | 0.6429 | 0.5459 |
| Expert composite CI lo | 0.3129 | 0.4490 | 0.4562 |
| Ensemble detection AUROC | 0.3486 | 0.3486 | 0.4201 |

**Expert ablation (AMP-vs-decoy, unchanged):**

| Metric | Value | Classification |
|--------|:-----:|:--------------:|
| rich_selectivity AUROC | 0.1973 | **Anti-signal** (above_random = -0.3027) — replaces hemolysis_safety (was 0.3285) |
| Expert composite AUROC | 0.7097 | Down from 0.7119 (rich_selectivity replaces hemolysis_safety as expert component) |

**Key finding (corrected):** The hemolysis risk scorer's original detection
AUROC=0.9218 on n=35 was small-sample inflation. On the expanded n=179
reference set, detection AUROC=0.5650 (CI 0.47-0.66) — direction is correct
(hemolytic > selective on average) but not statistically significant. The
scorer should NOT be described as a "statistically significant hemolysis
detector." It provides weak directional signal that may be useful as one
factor in a composite but cannot be relied upon for hemolysis triage. Hemolysis
must still be assayed experimentally for every candidate.

**Honest limitation:** The expanded reference set (n=179) provides a more honest
estimate, but HC50 values are approximate literature values with high inter-assay
variability. Melittin's risk score (0.13) remains modest because its bent-helix
hemolysis mechanism is not fully captured by 1D features.

---

## Multi-Class Triage Benchmark (v0.5.12 — added 2026-07-01)

> Tests the v1.1 ROADMAP item: "benchmark candidate triage against a reference
> panel that includes selective AMPs, hemolytic positives, inactive peptides,
> and random controls." Prior benchmarks tested two separate 2-class problems
> (AMP vs decoy, hemolytic vs selective). This benchmark tests the combined
> triage task the virtual assay layer must solve: rank selective AMPs above
> hemolytic AMPs above random decoys in a single panel.
>
> Run: `make bench-triage`

**Dataset:** 125 selective AMPs (HC50 >= 100 µg/mL) + 54 hemolytic AMPs (HC50 < 25 µg/mL)
+ 96 random background decoys = 275 total.

### Per-scorer pairwise AUROCs

A scorer that triages correctly should have all three AUROCs > 0.5:
  - selective > decoy (identifies AMPs)
  - hemolytic > decoy (identifies AMPs)
  - selective > hemolytic (prefers safe AMPs)

| Scorer | sel > decoy | hem > decoy | sel > hem | Triages correctly? |
|--------|:-----------:|:-----------:|:---------:|:------------------:|
| ensemble | 0.848 | 0.891 | 0.466 | **NO** (anti-selective) |
| activity | 0.885 | 0.934 | 0.430 | NO |
| selectivity_proxy | 0.782 | 0.795 | 0.610 | **YES** |
| expert_composite | 0.757 | 0.746 | 0.545 | **YES** |
| triage_score (activity × (1 - hemo_risk)) | 0.863 | 0.902 | 0.462 | NO |
| safe_weighted_ensemble | 0.849 | 0.890 | 0.483 | NO |
| safety | 0.344 | 0.300 | 0.538 | NO |
| synthesis | 0.590 | 0.634 | 0.469 | NO |
| hemolysis_risk (inverted) | 0.485 | 0.492 | 0.488 | NO |
| serum_stability | 0.217 | 0.160 | 0.569 | NO |
| **gate_triage** (activity × rich_sel) | **0.779** | **0.686** | **0.666** | **YES** |

**Key findings:**

1. **The ensemble does NOT triage correctly.** It ranks hemolytic AMPs above
   selective AMPs (sel_vs_hem AUROC = 0.466 < 0.5). This is the anti-selective
   bias documented in the selectivity benchmark, now confirmed in the combined
   triage context.

2. **selectivity_proxy and expert_composite triage correctly by pairwise AUROC**
   (all three AUROCs > 0.5). selectivity_proxy remains the best scorer because it
   has stronger selective-vs-hemolytic separation (0.610 vs expert_composite 0.545)
   while keeping slightly better selective-vs-decoy discrimination (0.782 vs 0.757).

3. **The naive triage_score (activity × (1 - hemolysis_risk)) does NOT fix the
   anti-selective bias** (sel_vs_hem = 0.462). This is because hemolysis_risk
   is too weak (detection AUROC 0.565, not significant on expanded benchmark).
   A naive virtual-assay composite does not outperform the ensemble.

6. **The gate_triage scorer (activity × rich_selectivity) is the first scorer
   to triage correctly with strong selective_vs_hemolytic separation** (0.666).
   Unlike the old triage_score, it uses rich_selectivity (detection AUROC 0.714,
   significant) instead of hemolysis_risk (not significant). It also achieves
   selective_vs_decoy 0.779 and hemolytic_vs_decoy 0.686, and ranks 16 selective
   / 1 hemolytic / 3 decoys in its top-20 — the best distribution of any benchmarked
   scorer. However, its AMP-vs-decoy discrimination is weaker than the ensemble
   (0.779 vs 0.848) because the rich_selectivity gate penalizes AMP-like features.
   It must NOT replace the ensemble activity gate; it is a complementary signal.

4. **Top-20 distribution shift:** The triage_score moves 2 more selective AMPs
   into the top-20 (16 vs 14 for ensemble), removing 2 hemolytic AMPs (4 vs 6).
   The shift is in the right direction but modest — the hemolysis_risk penalty
   is weak.

5. **Expert-composite top-k failure:** The expert_composite removes hemolytic
   AMPs from its top-20 (15 selective / 0 hemolytic), but admits 5 random decoys.
   That is a useful negative result: expert ranking is not a replacement for the
   ensemble activity gate, even when its pairwise AUROCs clear 0.5.

**Implication for the virtual assay layer:** Any future virtual assay module
must beat this triage benchmark baseline. The minimum bar is: triage correctly
(all three AUROCs > 0.5), keep decoys out of the top-k selection surface, and
maintain near-ensemble decoy discrimination (sel_vs_decoy > 0.80). The
selectivity_proxy achieves correct triage but loses decoy-discrimination margin.
The expert_composite achieves correct pairwise triage but admits decoys into its
top-20. A successful virtual assay must avoid both failures.

**Honest limitation:** The benchmark uses literature HC50 values with high
inter-assay variability. The binary thresholds (25 / 100 µg/mL) are coarse.
The MODERATE class (HC50 25-100, n=68) is excluded from the binary task.

### Strict Triage: Composition-Matched Decoys (v0.5.14 — added 2026-07-02)

> The standard triage benchmark uses random background peptides as decoys.
> These are trivially distinguishable from AMPs because their composition is
> protein-like, not AMP-like. This inflates selective_vs_decoy and
> hemolytic_vs_decoy AUROCs, making scorers appear to triage well.
>
> The strict triage benchmark replaces random decoys with **composition-matched
> scrambled versions** of the selective AMPs — same amino acids, permuted order.
> This destroys amphipathic helical phase, hydrophobic moment, and charge
> distribution patterns while preserving all composition-based features.

**Key finding: standard triage success was partly an illusion.**

| Scorer | Std sel_vs_dec | Strict sel_vs_dec | Std sel_vs_hemo | Strict sel_vs_hemo | Std correct | Strict correct |
|-------|-----------------|-------------------|------------------|---------------------|--------------|----------------|
| ensemble | 0.848 | **0.572** | 0.466 | 0.466 | NO | NO |
| activity | 0.885 | **0.617** | 0.430 | 0.430 | NO | NO |
| selectivity_proxy | 0.782 | **0.500** | 0.610 | 0.610 | YES | **NO** |
| expert_composite | 0.757 | **0.510** | 0.545 | 0.545 | YES | **NO** |
| triage_score | 0.863 | **0.674** | 0.462 | 0.462 | NO | NO |
| hemolysis_risk | 0.485 | 0.617 | 0.488 | 0.488 | NO | NO |
| gate_triage | 0.779 | **0.624** | 0.666 | 0.666 | YES | **NO** |

**What this reveals:**

1. **selectivity_proxy collapses to exactly 0.5000** on selective_vs_decoy —
   confirming it is purely composition-driven (charge and GRAVY are identical
   between a sequence and its scrambled version).

2. **The ensemble drops from 0.848 to 0.572** — most of its apparent triage
   power was composition-based, not order-based.

3. **No scorer triages correctly** with composition-matched decoys. The standard
   triage "success" of selectivity_proxy and expert_composite was an artifact
   of trivially distinguishable decoys.

4. **selective_vs_hemolytic is stable** across both benchmarks (identical AUROCs)
   — as expected, since both classes are real AMP sequences and only the decoy
   class changes.

5. **The ensemble admits 7 scrambled decoys into top-20** (vs 0 with random
   decoys) — it cannot distinguish real AMPs from scrambled versions of themselves.

6. **gate_triage retains partial order-dependent signal** (sel_vs_dec 0.624,
   hem_vs_dec 0.489). It fails strict triage because rich_selectivity penalizes
   the AMP-like composition that hemolytic AMPs share with their scrambled
   versions. But its selective_vs_decoy remains above 0.5, unlike selectivity_proxy
   which collapses to exactly 0.500 — suggesting the activity gate contributes
   order-dependent signal that the selectivity gate alone lacks.

**Implication:** The pipeline's triage signal is almost entirely composition-driven.
The real bottleneck is selective-vs-hemolytic discrimination, which requires
structural or contextual features beyond what current 1D physicochemical scorers
can capture. Any future virtual assay layer must demonstrate order-dependent
triage signal on this strict benchmark before claiming to improve candidate
selection.

## Feature Decomposition: Per-Feature Selective vs Hemolytic (v0.5.15 — added 2026-07-03)

> The strict triage benchmark (v0.5.14) proved that NO composite scorer passes
> selective_vs_hemolytic discrimination (AUROC 0.43-0.54). But it did not explain
> *why*. This benchmark tests every scalar physicochemical feature individually
> for selective_vs_hemolytic AUROC, with bootstrap confidence intervals.

**Key finding: the selectivity proxy ignores the strongest discriminative features.**

The selectivity proxy uses only `net_charge_ph74` and `gravy`. The top feature,
`hydrophobic_fraction` (AUROC 0.6745, CI 0.58-0.77), is NOT used by the proxy.
Six of eight significant features are not used by the current selectivity model.

| Feature | Detection AUROC | CI 95% | Direction | Used by proxy? |
|---------|-----------------|--------|-----------|----------------|
| hydrophobic_fraction | **0.6745** | 0.58-0.77 | risk | **NO** |
| helix_propensity | **0.6489** | 0.54-0.75 | risk | **NO** |
| net_charge_proxy | **0.6394** | 0.54-0.73 | risk | **NO** |
| net_charge_ph74 | **0.6332** | 0.54-0.73 | risk | YES |
| selectivity_proxy | **0.6095** | 0.52-0.70 | protective | YES |
| interior_trypsin_sites | **0.6089** | 0.51-0.70 | risk | **NO** |
| longest_repeat_run | **0.5946** | 0.52-0.68 | risk | **NO** |
| length | **0.5785** | 0.51-0.66 | risk | **NO** |

**What this reveals:**

1. **`hydrophobic_fraction` is the strongest single discriminative feature**
   (AUROC 0.6745), yet the selectivity proxy does not use it. The proxy relies
   on charge and overall hydrophobicity (GRAVY), but the *fraction* of
   hydrophobic residues carries more signal.

2. **All significant risk indicators point in the expected direction**
   (higher = more hemolytic). The features the pipeline already tracks (charge,
   hydrophobicity, helix propensity) have real signal for hemolysis, but the
   composite scorers cancel it out.

3. **The selectivity proxy itself has weak but significant signal** (0.6095)
   as a protective indicator. It is doing the right thing but is underpowered
   because it ignores the strongest axes.

4. **22 of 30 features tested have NO significant signal** for selective vs
   hemolytic discrimination. This confirms the strict triage finding: 1D
   physicochemical descriptors alone cannot solve this task well.

**Implication for next steps:**

A richer selectivity scorer combining `hydrophobic_fraction`, `helix_propensity`,
`net_charge`, and `interior_trypsin_sites` in a learned or hand-tuned model
could plausibly improve selective_vs_hemolytic AUROC above the current 0.55
ceiling. However, the best single feature (0.6745) is still modest, and
the CI is wide. 3D structural modelling or sequence-pattern features may
ultimately be needed for clinically meaningful discrimination.

Run: `make bench-feature-decomp` or `python -m openamp_foundry.cli bench feature-decomp`

## Rich Selectivity Scorer (v0.5.16 — added 2026-07-03)

The feature decomposition benchmark identified 8 significant features for selective_vs_hemolytic
discrimination, but the old `selectivity_proxy` (charge + GRAVY) used only 2. The rich selectivity
scorer (`scoring/selectivity_rich.py`) combines all 8 significant features, weighted by detection
AUROC, to produce a composite selectivity score.

| Scorer | Detection AUROC | CI 95% | Significant? |
|--------|----------------|--------|-------------|
| **rich_selectivity** | **0.7138** | **0.6266-0.7951** | **YES** |
| selectivity_proxy (old) | 0.5744 | 0.4954-0.6558 | Marginal |
| hemolysis_risk | 0.5650 | 0.4664-0.6601 | NO |
| expert_composite | 0.5459 | 0.4562-0.6305 | NO |
| safety | 0.5116 | 0.4321-0.5954 | NO |
| ensemble | 0.4201 | 0.3335-0.5067 | NO (anti-signal) |

**Key finding:** The rich selectivity scorer is the **first pipeline score with statistically
significant hemolysis detection** on the expanded n=179 benchmark (CI lower bound 0.6266 > 0.5).
It outperforms the old selectivity_proxy by +0.14 AUROC and is the only scorer whose CI excludes 0.5.

**Features combined (by detection AUROC):**
`hydrophobic_fraction` (0.6745), `net_charge_proxy` (0.6394), `net_charge_ph74` (0.6332),
`helix_propensity` (0.6489), `interior_trypsin_sites` (0.6089), `selectivity_proxy` (0.6095,
protective), `longest_repeat_run` (0.5946), `length` (0.5900).

**Honest limitations:**
- The rich selectivity scorer does NOT triage AMP-vs-decoy correctly (selective_vs_decoy = 0.19).
  It is designed for within-AMP ranking, not activity detection. It must be combined with an
  activity gate to be useful for candidate selection.
- Individual feature AUROCs are weak (0.59-0.67); the composite's CI is wide (0.63-0.80).
- Normalisation thresholds are empirical and may not generalise beyond the reference set.
- Does not model 3D structure, oligomeric state, or membrane curvature.
- HC50 values are approximate literature values with high inter-assay variability.
- This is a triage signal, NOT a hemolysis predictor. Wet-lab hemolysis assay remains mandatory.

Run: `make bench-selectivity` (rich_selectivity is included in the selectivity benchmark output)

## Two-Gate Triage Composite (v0.5.17 — added 2026-07-03)

> The triage benchmark showed that no scorer could pass all three pairwise
> AUROC conditions (selective_vs_decoy, hemolytic_vs_decoy, selective_vs_hemolytic)
> with strong selective-vs-hemolytic separation. selectivity_proxy passed but
> had weak separation (0.610). expert_composite passed but admitted 5 decoys
> into top-20. The old triage_score used hemolysis_risk (not significant).
>
> This scorer combines two complementary signals as a multiplicative gate:
> activity (strong AMP-vs-decoy, AUROC 0.885-0.934) × rich_selectivity
> (strong selective-vs-hemolytic, AUROC 0.745, significant).
>
> Run: `make bench-triage`

**Key result: gate_triage is the first scorer to pass all three standard triage conditions
with selective_vs_hemolytic > 0.65.**

| Scorer | sel > decoy | hem > decoy | sel > hem | Top-20 (sel/hem/dec) | Correct? |
|--------|:-----------:|:-----------:|:---------:|:---------------------:|:--------:|
| ensemble | 0.848 | 0.891 | 0.466 | 14/6/0 | NO |
| selectivity_proxy | 0.782 | 0.795 | 0.610 | — | YES (weak) |
| expert_composite | 0.757 | 0.746 | 0.545 | 15/0/5 | YES (decoy leak) |
| triage_score (old) | 0.863 | 0.902 | 0.462 | 16/4/0 | NO |
| **gate_triage** | **0.779** | **0.686** | **0.666** | **16/1/3** | **YES** |

**Design rationale:**

The two gates solve complementary problems:
- activity gate: detects AMP-likeness (composition + amphipathicity) —
  strong vs random decoys but anti-selective (rewards hemolytic AMPs)
- rich_selectivity gate: detects hemolysis risk from 8 evidence-identified
  features — strong vs hemolytic AMPs but anti-AMP (penalizes AMP-like composition)

Their product leverages both: a candidate must score high on BOTH AMP-likeness
AND selectivity. Hemolytic AMPs score high on activity but low on rich_selectivity.
Decoys score low on activity. Selective AMPs score moderately on both.

**Honest limitations:**

1. gate_triage does NOT pass strict triage (composition-matched decoys).
   Its hemolytic_vs_decoy drops to 0.489 because rich_selectivity penalizes
   the AMP-like composition that hemolytic AMPs share with their scrambled
   versions. It retains partial order-dependent signal (sel_vs_dec 0.624),
   but this is from the activity gate, not the selectivity gate.

2. gate_triage is weaker than ensemble on pure AMP-vs-decoy detection
   (0.779 vs 0.848). It must NOT replace the ensemble activity gate.
   It is a complementary triage signal, not a replacement.

3. A decoy leaks into the top-20 (3 decoys vs 0 for ensemble). The
   selectivity gate removes some hemolytic AMPs but admits some decoys
   that happen to have moderate activity and moderate selectivity.

4. This is still a dry-lab triage signal. Wet-lab hemolysis assay
   remains mandatory for all candidates.

## Test Suite

| Metric | Value |
|--------|-------|
| Total tests | 4162 |
| Coverage (branch) | 99% (6 CLI guard lines only) |
| Source modules at 100% | All pipeline, QC, scoring, adapter modules |

---

## Key Limitations

| Limitation | Impact |
|------------|--------|
| 500-AMP AUROC 0.7792 | ~22% of benchmark pairs misranked; charge-inflated; wet-lab is the judge |
| Safety model blind spot | Melittin scores Safety=1.0; hemolysis assay mandatory |
| No structural modeling | Helical assumption may misclassify non-helical mechanisms |
| Near-seed generation only | Novel sequence space not explored de novo |
| APD/DRAMP novelty (v2) | Complete — 27,234-sequence combined DB (APD6+DRAMP+UniProt); BLOSUM62 local alignment; Wave 0.5 results updated |
| No wet-lab data | All probabilities are upper bounds; true hit rate unknown |
| Rich selectivity scope | Designed for within-AMP selectivity only; does not distinguish AMPs from decoys (selective_vs_decoy=0.19) |

---

## Change Log

### v0.10.21 — Phase G G1: RecalibrationDecisionLog schema
- Added `RecalibrationDecisionLog` (RDL-) schema
- 13 fields: rdl_id, pipeline_version, calibration_checkpoint, decision_date, trigger_type, trigger_artifact_id, decision_outcome, decision_authority, evidence_summary, rationale, next_review_date, conditions_if_deferred, notes
- 13 validation rules; 3 warnings; 63 tests
- BASELINE 5918→5981
- CLI: openamp-foundry recalibration-decision-log-check
- Closes Phase G G1 — governance audit trail for calibration decisions

| Date | Change | Author |
|------|--------|--------|
| 2026-07-10 | **Calibration cycle summary schema (Phase P P5 — Phase P complete):** CalibrationCycleSummaryEntry (13 fields: ccs_id, pipeline_version, bsp_id, psc_id, bos_id, cps_id, cba_id, crg_id_previous, crg_id_next, cycle_outcome, cycle_notes, reviewer, dry_lab_only). Index record for one complete calibration loop — CRG→BSP→PSC→Lab→BOS→CPS→CBA→CRG. 11 validation rules (7 artifact prefixes: CCS-/BSP-/PSC-/BOS-/CPS-/CBA-/CRG-, crg_id_previous≠crg_id_next, cycle_outcome in {improved,stable,degraded}, notes≤400 chars). 2 warnings: degraded outcome, dry-lab-only cycle. 63 tests. CLI: openamp-foundry calibration-cycle-summary-check. Completes Phase P: P1 BSP + P2 RRF + P3 BOS + P4 PSC + P5 CCS form the full calibration bridge. BASELINE 4910->4973. | OpenAMP Loop |
| 2026-07-10 | **Pilot batch safety clearance schema (Phase P P4):** PilotBatchSafetyClearanceEntry (13 fields: psc_id, bsp_id, pipeline_version, dual_use_risk_checked, novelty_verified, toxicity_screened, hemolysis_screened, max_safety_risk_tier, cleared_for_synthesis, rejection_ids, safety_notes, reviewer, dry_lab_only). All 4 safety screens mandatory. 8 validation rules: PSC-/BSP- prefixes, 4 screens all required True, risk tier in {low,moderate,high}, high-risk cannot be cleared (cleared_for_synthesis must be False), notes<=400 chars. 3 warnings: moderate-risk cleared, rejection_ids present, dry_lab_only clearance needs human review. 63 tests. CLI: openamp-foundry pilot-batch-safety-clearance-check. Safety constraint: max_safety_risk_tier=high cannot set cleared_for_synthesis=True. BASELINE 4847->4910. | OpenAMP Loop |
| 2026-07-10 | **Batch outcome summary schema (Phase P P3):** BatchOutcomeSummaryEntry (12 fields: bos_id, pipeline_version, bsp_id, batch_id, candidates_proposed, candidates_tested, candidates_active, candidates_inactive, is_synthetic, outcome_notes, reviewer, dry_lab_only). 9 validation rules (BOS-/BSP- prefixes, count constraints, synthetic/real boundary: is_synthetic=True requires dry_lab_only=True, notes<=400 chars). 3 warnings (untested candidates, real results marked dry-lab-only, zero active). 63 tests. CLI: openamp-foundry batch-outcome-summary-check. Closes the BSP-to-outcomes feedback loop. BASELINE 4784->4847. | OpenAMP Loop |
| 2026-07-10 | **Recalibration refusal record schema (Phase P P2):** RecalibrationRefusalEntry (10 fields, recalibration_refused must be True). 7 validation rules, 2 warnings. 63 tests. CLI: openamp-foundry recalibration-refusal-check. Complements CalibrationImprovementRecord (O3) with the rejection path. Corrected inflated BASELINE 4889->4784. | OpenAMP Loop |
| 2026-07-09 | **Release checklist and gate validator (J1, starts Phase J):** `docs/governance/RELEASE_CHECKLIST.md` with structured checklist. `src/openamp_foundry/governance/release_gate.py` with `RELEASE_TYPES` (5), `UNIVERSAL_GATES` (7), `EXTRA_GATES_BY_TYPE`, `ReleaseGateResult`, `validate_release_gate()`. CLI `release-gate-check`. `make release-gate-check`. 18 tests. **Phase J (Governance and release maturity) started. 3478 total.** | OpenAMP Loop 109 |
| 2026-07-09 | **Adoption scorecard dashboard added (I10):** `src/openamp_foundry/adoption/scorecard.py` with `SCORECARD_DIMENSIONS` (5, weights sum 1.0), `ADOPTION_TIERS` (4), `DimensionScore`, `AdoptionScorecard`, `build_scorecard()`, `compute_adoption_tier()`. CLI `adoption-scorecard` with `--scores-json` and `--format`. `make adoption-scorecard`. 17 tests. **Phase I (Interoperability and Adoption) is now complete** — all 10 items I1–I10 implemented. **3446 total.** | OpenAMP Loop 108 |
| 2026-07-09 | **Adapter author validator added (I6):** `src/openamp_foundry/adapters/adapter_validator.py` with `AdapterDeclaration` (14 fields), `AdapterValidationResult` (5 fields), `validate_adapter_declaration()` (10 checks enforcing ADAPTER_AUTHOR_GUIDE contract), `validate_adapter_dict()` (dict input with missing-fields guard). 4 valid-value sets (VALID_ADAPTER_MODES, VALID_OUTPUT_STATUSES, VALID_RANKING_EFFECTS, VALID_RELEASE_STATUSES). CLI (`openamp-foundry adapter-check`) with `--adapter-json`, `--format text|json`. `make adapter-author-check` target. 31 tests. **3387 total.** | OpenAMP Loop 104 |
| 2026-07-08 | **Calibration benchmark added:** Brier score decomposition, reliability diagram, and calibration slope for pipeline ensemble scores. Brier=0.3178 (>0.25=uninformative), skill=-0.27 (worse than base rate), slope=0.43 (ideal=1.0). Honest finding: pipeline ranks well (AUROC~0.78) but scores are not meaningful probabilities. Expanded 500-AMP set confirms same pattern (Brier=0.2772, slope=2.31 — dataset-dependent). Integrated into `make bench-500` and `make bench-calibration`. `scripts/benchmarks/benchmark_calibration.py`, JSON output to `outputs/bench_calibration*.json`. | OpenAMP loop 18 |
| 2026-06-29 | Novelty audit v2: BioPython BLOSUM62 local alignment vs 27,234 AMPs (APD6+DRAMP+UniProt); panel updated (15 families, 4 SAR_CONTROL); all 7 gates PASS | OpenAMP Wave 0.5 |
| 2026-06-29 | Wave 0.5b: 23-candidate safety-optimized shortlist (SEED-020–024, no aromatics) | OpenAMP Wave 0.5b |
| 2026-06-29 | External predictor results filled from wave05_combined_consensus.csv; all 7 gates PASS | OpenAMP Wave 0.5 |
| 2026-06-29 | Wave 0.5 scaffold diversification — 24-candidate Wave 1 panel across 14 families | OpenAMP Wave 0.5 |
| 2026-07-01 | Expert ablation benchmark added: expert composite AUROC 0.7119 vs ensemble 0.7832 (delta −0.0713); anti-signal components documented; ensemble remains primary gate | OpenAMP loop |
| 2026-07-01 | **Hemolysis benchmark expanded:** 42 -> 238 peptides using DBAASP human erythrocyte data (54 hemolytic vs 125 selective, n=179 binary). Hemolysis risk scorer detection AUROC drops 0.9218 -> 0.5650 (CI 0.47-0.66) — original performance was small-sample inflation. Direction correct, not significant. Safety scorer detection improves 0.3844 -> 0.5116 (still not significant). 196 new peptides from DBAASP v3. | OpenAMP loop |
| 2026-07-01 | Dedicated hemolysis risk scorer: 4-component score (synth+aromatic+face+cys) achieves detection AUROC=0.9218 (CI: 0.82-0.99); integrated into expert composite (detection 0.5119→0.6429); safety scorer unchanged; 1471 tests | OpenAMP loop |
| 2026-07-01 | Within-AMP selectivity benchmark added: safety scorer FAILS hemolysis detection (AUROC=0.3844); synthesis is only significant risk detector (AUROC=0.8027); expert composite better than ensemble but not significant (0.5119 vs 0.3486) | OpenAMP loop |
| 2026-07-01 | Expert composite ranking integration: `score_candidates()` now computes `expert_composite` and `hemolysis_risk`; `--ranking-mode expert` CLI flag; expert-ranked top-5 have lower mean hemolysis_risk than ensemble | OpenAMP loop |
| 2026-07-02 | **Strict triage benchmark added:** composition-matched scrambled decoys replace random background. No scorer triages correctly — standard triage "success" of selectivity_proxy (0.782 sel_vs_dec) and expert_composite (0.757) was inflated by trivially distinguishable decoys. selectivity_proxy collapses to 0.500 (purely composition-driven), ensemble drops to 0.572. Real bottleneck (selective_vs_hemolytic) unchanged. | OpenAMP loop |
| 2026-07-02 | Ranking policy contract added: machine-readable recommendation now states `ensemble` remains default broad synthesis gate, `expert` is narrower safety-aware alternative only | OpenAMP loop |
| 2026-07-03 | **Rich selectivity scorer added:** composite of 8 evidence-identified features from the feature decomposition benchmark. Detection AUROC=0.7138 (CI 0.63-0.80) on n=179 — first pipeline score with statistically significant selective_vs_hemolytic discrimination. Old selectivity_proxy=0.5744 (CI 0.50-0.66). Honest limitation: does not triage AMP-vs-decoy (0.19); must be combined with activity gate. | OpenAMP loop |
| 2026-07-05 | **Order-dependent features benchmark added:** dipeptide_order_score is the strongest order-dependent feature (AUROC 0.7861 on AMP-vs-scrambled). Only 7/31 features survive scrambling. All composition features are exactly position-independent (0.5000). `src/openamp_foundry/features/dipeptide.py`, `scripts/benchmarks/benchmark_order_dependent.py`, `make bench-order-dependent`. | OpenAMP loop 13 |
| 2026-07-05 | **Cross-dataset generalization benchmark:** DRAMP AMPs (independent database) vs Swiss-Prot decoys: AUROC 0.7803 (CI 0.75–0.81). Baseline 0.7832 from APD6/UniProt — Δ=-0.0029. Pipeline is source-independent: heuristic features generalise to DRAMP with essentially identical discrimination. Phase 1 exit criterion #5 satisfied. `scripts/benchmarks/benchmark_cross_dataset.py`, `make bench-cross-dataset`. | OpenAMP loop 17 |
| 2026-07-05 | **Precision@k calibration benchmark added:** top-20 precision 1.000, top-50 precision 0.900, top-200 precision 0.835. Best F1 threshold 0.6323 (F1=0.7518). At 80% recall, precision drops to base-rate (0.5000) — honest limitation documented. `scripts/benchmarks/benchmark_precision_at_k.py`, `make bench-precision-at-k`. | OpenAMP loop 14 |
| 2026-07-05 | **Expert ablation re-run on expanded benchmark (n=1000):** 2 components reclassified — synthesis was anti-signal artifact on n=191 (0.4228→0.4968, now near-zero); boman_activity more strongly anti-AMP (0.3291). selectivity_proxy weaker on diverse set. Activity remains dominant (0.7969). `make bench-expert-ablation-500`. | OpenAMP loop 15 |
| 2026-07-05 | **Benchmark card consolidated** with all Phase 1 findings: expanded benchmark, cluster-split-500, multi-negative, easy baseline, order-dependence, precision@k, rich selectivity, gate_triage, expert ablation (n=1000), updated known biases. Phase 1 exit criterion: benchmark card is now externally reviewable. `docs/evidence/BENCHMARK_CARD.md`. | OpenAMP loop 16 |
| 2026-07-05 | **Easy baseline benchmark added:** charge density alone (AUROC 0.8166) beats pipeline ensemble (0.7792, Δ=−0.0374). Honest finding: expected — pipeline optimizes for safety, not raw discrimination. `scripts/benchmarks/baseline_trivial.py`, `make bench-easy-baseline`, CI informational step. | OpenAMP loop 12 |
| 2026-07-03 | **Rich selectivity integrated into production pipeline:** rich_selectivity_score now computed in score_candidates() (pipeline.py), replaces hemolysis_safety as the expert composite hemolysis-risk component (weight 0.10), used in pilot_priority formula, displayed in pilot panel report, and included in evidence certificates. Expert AUROC drops 0.7119→0.7097 (−0.0022) — acceptable tradeoff: the expert now includes a significant hemolysis detector (CI excludes 0.5) instead of the old non-significant one. | OpenAMP loop |
| 2026-07-03 | **Two-gate triage composite added:** gate_triage = activity × rich_selectivity, added to triage benchmark. First scorer to pass all three standard triage conditions with strong selective_vs_hemolytic separation (0.666). Top-20: 16 selective / 1 hemolytic / 3 decoy — best distribution. Does NOT pass strict triage (hem_vs_dec 0.489) — honest limitation. Must not replace ensemble activity gate. | OpenAMP loop |
| 2026-07-03 | **Feature decomposition benchmark added:** per-feature selective_vs_hemolytic AUROC for all 30 scalar physicochemical features. hydrophobic_fraction is the strongest single discriminative feature (0.6745, CI 0.58-0.77) but is NOT used by the selectivity proxy. 8/30 features have significant signal; 6 of those are unused. Provides actionable diagnostic for why composite scorers fail selective_vs_hemolytic discrimination. | OpenAMP loop |
| 2026-07-04 | **Calibration intake module added:** `openamp-foundry calibration-intake` joins a pilot panel CSV with a directory of validated lab result JSON files, produces a per-candidate prediction-vs-actual report with cohort metrics gated by `MIN_COHORT_SIZE=5`. Descriptive only — does NOT trigger recalibration, weight updates, or selection-rule changes. Synthetic example data in `examples/lab_results/` is clearly labeled in every file and in `examples/lab_results/README.md`. 29 new tests; total 1614 passing. | OpenAMP loop |
| 2026-06-29 | Initial — expanded benchmark (PR #110) | OpenAMP CI |
| 2026-07-05 | **Per-family benchmark breakdown added:** stratifies 500 AMPs by structural class (cysteine_rich, proline_rich, short, highly_cationic, moderately_cationic, low_charge). Pipeline is charge-dominated: highly_cationic AUROC 0.958 vs proline_rich AUROC 0.586 — a 0.37 gap. Proline-rich, short, and low-charge AMPs are consistently undervalued. Diversity selection should deliberately compensate for pipeline's helic/charge bias. `scripts/benchmarks/benchmark_per_family.py`, `make bench-per-family`, CI informational step. 27 new tests. | OpenAMP loop 18 |
| 2026-07-04 | **Recalibration policy + gate module added:** `openamp-foundry recalibration-gate` evaluates a calibration intake report against the pre-registered policy in `configs/recalibration_policy.yaml` and emits a binary `may_recalibrate` verdict. The policy file encodes 7 minimum conditions (cohort size, controls, orphans, positives, negatives, metrics availability), 5 permanent prohibited actions (toxicity, hemolysis, novelty, pathogen enhancement, post-hoc success redefinition), and 2 rate limits (L1 weight budget, cooldown). The validator rejects policy files that omit any canonical prohibited action or any `locked_changes` entry. The gate does NOT trigger weight updates; it is the missing permission layer between v0.5.19 intake and a future recalibration engine. Exit code 0 when `may_recalibrate=true`, 3 when false. 39 new tests; total 1647 passing. See `docs/evidence/CALIBRATION_POLICY.md`. | OpenAMP loop |
