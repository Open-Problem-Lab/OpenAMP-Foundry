Warning: truncated output (original token count: 38410)
Total output lines: 2537

# Roadmap

## Current state — 2026-07-15

Phase AC is complete as of 2026-07-15. AC1 records one explicit disconfirming
test as a DTR- artifact. AC2 aggregates those records into an ACDG- gate. AC3
exposes that gate through a CLI and make target, with nonzero status for
partial or not-established results so the review control is usable in
repeatable loops. This is an auditability improvement only. It does not
validate biology, improve benchmark performance, or authorize release.

On 2026-07-16, the Phase AA reproducibility gate became runnable through the
CLI and Make surface. It fails closed unless RMC, DCR, CFP, and SBW artifact
IDs are present. This makes the provenance gate easier to execute; it does not
certify that the referenced artifacts are accurate or that any biology is
validated.

This file is the current milestone authority. The older
[`50_LOOP_PLAN.md`](50_LOOP_PLAN.md) is a historical execution record, not a
live status page. Select the next bottleneck from
[`HIGH_LEVERAGE_TASKS.md`](../operations/HIGH_LEVERAGE_TASKS.md) and
[`NEXT_100_PR_MAP.md`](NEXT_100_PR_MAP.md); do not infer a new scientific phase
from the completion of Phase AC alone. The strategic bottleneck remains
external truth: qualified review, fair baseline-controlled pilots, and real
result intake.

### v0.10.3 - Phase O O5: Calibration Readiness Gate (COMPLETES PHASE O)
- CalibrationReadinessEntry: binary gate consuming CBA- aggregators
- gate_passed consistent with failure_reasons; degrading-trend and marginal-Brier warnings
- Phase O (O1-O5 Calibration QA) fully complete

### v0.10.2 - Phase O O4: Cross-Batch Performance Aggregator
- CrossBatchAggregatorEntry aggregates CalibrationPerformanceEntry results across N>=2 batches
- trend field (improving/stable/degrading) feeds calibration readiness gate
- min/mean/max Brier scores, high-variance warning

### v0.10.1 - Phase O O3: Calibration Improvement Record
- CalibrationImprovementEntry schema documents recalibration actions taken after drift/quality failures
- 6 action categories, trigger_ids linked to CPS-/DRM- records
- Closes the loop between detection and correction

### v0.10.0 — Phase O O2: Prediction Drift Monitor
- Added `PredictionDriftEntry` schema tracking mean/std score shifts between reference and evaluation batches
- Detects silent model degradation before wet-lab confirmation
- Constants: SIGNIFICANT_DRIFT_THRESHOLD=0.1, VARIANCE_EXPLOSION_RATIO=2.0
- CLI: `openamp-foundry prediction-drift-check`
- 68 tests; all passing

### v0.9.9 — Phase O O1: Calibration Performance Summary (starts Phase O)
- Added `CalibrationPerformanceEntry` schema tracking prediction accuracy over batches with known outcomes
- Confusion matrix validation; Brier score; FP rate, recall, and small-sample warnings
- dry_lab_only=False (requires real experimental data)
- CLI: `openamp-foundry calibration-performance-check`
- 46 tests; all passing

### v0.9.8 — Phase N N5: Experiment Priority Justification (Completes Phase N)
- Added `ExperimentPriorityEntry` schema documenting why a batch was selected over alternatives
- Safety review enforcement; post-hoc selection warning; resource constraint transparency
- Requires at least 2 criteria and 1 rejected alternative — selection without alternatives is not a decision
- CLI: `openamp-foundry experiment-priority-check`
- 62 tests; all passing
- Phase N (Pre-registration & Baseline Honesty) complete

### v0.9.7 — Phase N N4: Negative Result Record
- Added `NegativeResultEntry` schema ensuring failed experiments are documented, not discarded
- 6 failure categories, 5 assay types; warns on suppressed reporting, systematic failures, uncalibrated overprediction
- dry_lab_only=False supported for real lab data
- CLI: `openamp-foundry negative-result-check`
- 68 tests; all passing

### v0.9.6 — Phase N N3: Baseline Comparison Manifest
- Added `BaselineComparisonEntry` schema for machine-verifiable proof the pipeline beats cheap baselines
- 6 metric names, 2 comparison directions, p_value sentinel for uncomputed significance
- Detects inconsistent beat/lose verdicts, missing p-values, large unchecked effects
- CLI: `openamp-foundry baseline-comparison-check`
- 68 tests; all passing

### v0.9.5 — Phase N N2: Hypothesis Outcome Record
- Added `HypothesisOutcomeEntry` schema linking pre-registration to actual experimental outcomes
- Records confirmed/refuted/inconclusive/partially_confirmed verdicts with observed metric value
- Warns on threshold/verdict inconsistency and undocumented inconclusive deviations
- dry_lab_only=False supported (real lab data can be recorded)
- CLI: `openamp-foundry hypothesis-outcome-check`
- 48 tests; all passing

### v0.9.4 — Phase N N1: Pre-Registration Form (starts Phase N)
- Added `PreRegistrationEntry` schema for machine-verifiable experiment pre-commitment
- Records hypothesis, outcome metric, success threshold, and baseline comparators before results are observed
- Prevents HARKing (Hypothesising After Results are Known)
- Warns when random baseline is absent, hypothesis is underspecified, or statistical test is a placeholder
- CLI: `openamp-foundry pre-registration-check`
- 62 tests; all passing

### v0.9.3 — Phase M M5: Audit Chain Completeness Checker (Completes Phase M)
- Added `AuditChainEntry` schema validating all 9 evidence chain links exist for a batch
- Detects gaps from sequence input through benchmark, filter, scoring, selection, certificate, claims, decision audit, and reviewer briefing
- missing_links consistency check catches declaration errors
- CLI: `openamp-foundry audit-chain-check`
- 39 tests; all passing
- Phase M (Audit Trail Infrastructure) complete

### v0.9.2 — Phase M M4: Reviewer Briefing Package
- Added `ReviewerBriefingEntry` schema for one-stop external auditor handoff packages
- Validates CoI declaration, minimum artifact count, scope, candidate count
- 4 warning conditions: large batch, underfocused questions, long scope, minimal artifacts
- CLI: `openamp-foundry reviewer-briefing-check`
- 52 tests; all passing

### v0.9.1 — Phase M M3: Score Decomposition Report
- Added `ScoreDecompositionEntry` schema documenting how composite scores decompose into components
- 6 valid scoring methods; weight-sum tolerance; dominant/unbalanced/low-score warnings
- CLI: `openamp-foundry score-decomposition-check`
- 54 tests; all passing

### v0.9.0 — Phase M M2: Claim-to-Evidence Mapper
- Added `ClaimToEvidenceEntry` schema mapping each claim to supporting artifacts
- 7 valid claim types; 4 warning conditions for exploratory or weakly-evidenced claims
- CLI: `openamp-foundry claim-to-evidence-check`
- 50 tests; all passing

### v0.8.9
- Phase M M1: pipeline decision audit entry schema — records each filter/threshold/rank decision with rationale and alternatives considered for external audit. PipelineDecisionAuditEntry dataclass, validate_pipeline_decision_audit(), CLI pipeline-decision-audit-check.

### v0.8.8
- Phase L L5: dataset release package checker — validates that open dataset releases meet data governance requirements (license, provenance, dual-use assessment, release approval). DatasetReleaseEntry dataclass, validate_dataset_release(), CLI dataset-release-check. Completes Phase L.

### v0.8.7
- Phase L L4: multi-candidate comparison schema — validates structured side-by-side comparisons of two or more candidates for publication-ready supplementary tables. MultiCandidateComparisonEntry dataclass, validate_multi_candidate_comparison(), CLI multi-candidate-comparison-check.

### v0.8.6
- Phase L L3: candidate summary card schema — validates publication-ready per-candidate structured summaries with sequence, evidence level, activity prediction, and safety flags. CandidateSummaryCardEntry dataclass, validate_candidate_summary_card(), CLI candidate-summary-card-check.

### v0.8.5
- Phase L L2: reproducibility manifest schema — captures exact software versions, data checksums, and random seeds for a pipeline run. ReproducibilityManifestEntry dataclass, validate_reproducibility_manifest(), CLI reproducibility-manifest-check.

### v0.8.4
- Phase L L1: preprint evidence bundle schema — ties K-phase artifacts into a submission-ready record for scientific preprints. PreprintBundleEntry dataclass, validate_preprint_bundle(), CLI preprint-bundle-check.

### v0.8.3
- Phase K K5: uncertainty quantification report schema — validates prediction intervals, confidence levels, and calibration source for dry-lab candidate recommendations. UncertaintyReportEntry dataclass, validate_uncertainty_report(), CLI uncertainty-report-check.

### v0.8.2
- Phase K K4: post-experiment calibration intake schema — captures structured comparison of pipeline dry-lab prediction against actual experimental outcome. CalibrationIntakeEntry dataclass (dry_lab_only=False enforced), validate_calibration_intake(), CLI calibration-intake-check.

## v0.8.1 — Loop 121: Phase K K3 — Pilot Package Completeness Checker

`docs/evidence/PILOT_PACKAGE_GUIDE.md` with purpose, required field table (11
fields), mandatory artifact types table (3 types: selection_rationale,
batch_priority, evidence_certificate), valid artifact types (8 types), warnings,
validation workflow, honest-use boundary.

`src/openamp_foundry/evidence/pilot_package.py` with `PilotPackageEntry`
dataclass (11 fields, dry_lab_only=True enforced), `PilotPackageResult`
dataclass (5 fields, dry_lab_only=True), `MINIMUM_REQUIRED_ARTIFACTS` (3),
`READINESS_SCORE_THRESHOLD` (0.80), `MANDATORY_ARTIFACT_TYPES` (3:
batch_priority, evidence_certificate, selection_rationale),
`VALID_ARTIFACT_TYPES` (8 types), `validate_pilot_package()` (11 checks, 3
warning conditions: missing artifacts, low completeness score, same
reviewer/approver), `validate_pilot_package_dict()` (10 required fields guard).

CLI: `openamp-foundry pilot-package-check`. `make pilot-package-check` target.
**v0.8.1 milestone** — every pilot submission is machine-validated for
completeness before external lab submission.

## v0.8.0 — Loop 120: Phase K K2 — Batch Experiment Priority Ranker ✓ (2026-07-09)

`docs/evidence/BATCH_PRIORITY_GUIDE.md` with field table and validation workflow
for batch synthesis wave priority entries.

`src/openamp_foundry/evidence/batch_priority.py` with `BatchPriorityEntry`
dataclass (12 fields, dry_lab_only=True enforced), `BatchPriorityResult`
dataclass (6 fields), `VALID_SYNTHESIS_COMPLEXITIES` (3: high/low/medium),
`VALID_NOVELTY_TIERS` (3: high/low/medium), `VALID_EVIDENCE_LEVELS` (1–6),
`validate_batch_priority()` (11 checks, 3 warning conditions: low evidence,
top-rank+high-complexity, low score), `validate_batch_priority_dict()`
(10 required fields guard).
CLI: `openamp-foundry batch-priority-check`. `make batch-priority-check` target.
**v0.8.0 milestone** — synthesis wave ranking is now machine-validated with
explicit evidence level and complexity signals.

## v0.7.9 — Loop 119: Phase K K1 — Selection Rationale Schema ✓ (2026-07-09)

`docs/evidence/SELECTION_RATIONALE_GUIDE.md` documenting what selection rationale
entries must contain, why they are needed for external review, and how evidence
levels map to `PROOF_LADDER.md`.

`src/openamp_foundry/evidence/selection_rationale.py` with `SelectionRationaleEntry`
dataclass (11 fields, dry_lab_only=True enforced), `SelectionRationaleResult`
dataclass (5 fields), `VALID_EVIDENCE_LEVELS` (1–6), `MINIMUM_SAFETY_FLAGS` (1),
`validate_selection_rationale()` (11 checks, 1 warning condition for low evidence
levels), `validate_selection_rationale_dict()` (10 required fields guard).
CLI: `openamp-foundry selection-rationale-check`. `make selection-rationale-check` target.
**Phase K milestone: v0.7.9** — every candidate selection now requires a
machine-validated rationale with evidence level and baseline comparison.

## v0.7.8 — Loop 118: Phase J J10 — Annual Safety and Benchmark Review Checklist ✓ (2026-07-09)

`docs/governance/ANNUAL_REVIEW_CHECKLIST.md` with 5-section structured annual
review checklist (safety_policy: 6 checks covering dual-use safeguards,
dry_lab_only enforcement, toxicity/hemolysis filter thresholds, evidence_level
guard; benchmark_thresholds: 6 checks covering threshold loosening guard,
easy-baseline requirement, selectivity benchmarks, deprecation check;
calibration_status: 4 checks covering recalibration gate, decision checklist,
rollback plan; governance_decisions: 4 checks covering active decisions,
COI disclosures, maintainer rotation; data_governance: 3 checks covering
proprietary data license flags, external source documentation).

`src/openamp_foundry/governance/annual_review.py` with `AnnualReviewEntry`
dataclass (10 fields: review_id, year, section, reviewer, finding_count,
action_items_count, status, notes, completion_date, dry_lab_only),
`AnnualReviewResult` dataclass (6 fields, dry_lab_only=True),
`VALID_REVIEW_SECTIONS` (5: benchmark_thresholds, calibration_status,
data_governance, governance_decisions, safety_policy),
`VALID_ENTRY_STATUSES` (5: completed, deferred, in_progress, not_applicable,
pending), `validate_annual_review_entry()` (9 checks: ANN- prefix, 4-digit year,
valid section, non-empty reviewer, non-negative finding_count,
non-negative action_items_count, valid status, completed requires YYYY-MM-DD
completion_date, dry_lab_only must be True; completed+no-notes warns, deferred
warns, findings+no-action-items warns), `validate_annual_review_dict()` (7
required fields guard). CLI (`openamp-foundry annual-review-check`) with
`--entry-json`, `--format text|json`. `make annual-review-check` target.
Long-term trust: annual review entries are now machine-validated.

## v0.7.7 — Loop 117: Phase J J9 — External Advisory Review Process ✓ (2026-07-09)

`docs/governance/EXTERNAL_ADVISORY_REVIEW_PROCESS.md` with reviewer eligibility
criteria (4 requirements), review scope table (5 review types with minimum
reviewer counts: candidate_review and safety_policy_review require ≥2 reviewers,
others ≥1), 5-step process (prepare packet, assign+disclose COI, receive+log,
respond to findings by severity, close and record), finding severity handling
(critical halts release, major resolves before release, minor defers, informational
notes), limitations section.

`src/openamp_foundry/governance/advisory_review.py` with `AdvisoryReview` dataclass
(11 fields: review_id, review_type, artifact_id, reviewer_handle, assigned_date,
deadline_date, status, finding_severity, finding_summary, resolved, dry_lab_only),
`AdvisoryReviewResult` dataclass (5 fields, dry_lab_only=True),
`VALID_REVIEW_TYPES` (5: benchmark_audit, candidate_review, evidence_review,
governance_review, safety_policy_review), `VALID_REVIEW_STATUSES` (5: assigned,
completed, deferred, in_progress, pending), `VALID_FINDING_SEVERITIES` (4:
critical, informational, major, minor), `MINIMUM_REVIEWER_COUNTS` (5 entries),
`validate_advisory_review()` (9 checks + 3 warning conditions),
`validate_advisory_review_dict()` (7 required fields guard).

CLI (`openamp-foundry advisory-review-check`) with `--review-json` (required),
`--format text|json`. Handler `_run_advisory_review_check` in reports.py.

`make advisory-review-check` target. 29 tests. **3653 total.**

Credibility: external advisory reviews now have a validated structure, documented
eligibility criteria, and a clear process from assignment to closure.

## v0.7.6 — Loop 116: Phase J J8 — Roadmap-to-Issue Sync Checklist ✓ (2026-07-09)

`docs/governance/ROADMAP_ISSUE_SYNC_CHECKLIST.md` with 5-section checklist:
roadmap items → issues (5 checks), issues → roadmap (3 checks), completed
items (4 checks), priority alignment (3 checks), version consistency (3 checks).

`src/openamp_foundry/governance/roadmap_sync.py` with `RoadmapSyncEntry`
dataclass (10 fields: item_id, phase, description, priority, sync_status,
issue_number, pr_number, completed, completion_date, dry_lab_only),
`RoadmapSyncResult` dataclass (5 fields, dry_lab_only=True),
`VALID_SYNC_STATUSES` (5: synced, missing_issue, orphaned_issue, stale,
completed), `VALID_PRIORITY_LEVELS` (4: A, B, C, D), `VALID_PHASES` (7:
E, F, G, H, I, J, K), `validate_roadmap_sync_entry()` (8 checks + 4 warning
conditions), `validate_roadmap_sync_dict()` (5 required fields guard).

CLI (`openamp-foundry roadmap-sync-check`) with `--entry-json` (required),
`--format text|json`. Handler `_run_roadmap_sync_check` in reports.py.

`make roadmap-sync-check` target. 24 tests. **3624 total.**

Keeps strategy actionable: roadmap sync entries are machine-validated,
priority A items without issues get an immediate warning, and stale or
orphaned items are flagged for cleanup.

## v0.7.5 — Loop 115: Phase J J7 — Citation and Reuse Guide ✓ (2026-07-09)

`docs/governance/CITATION_AND_REUSE_GUIDE.md` with citation formats (inline,
BibTeX), reuse table (4 artifact types with open/attribution_required/
contact_required/restricted classes), attribution requirements, honest-use
boundary (dry-lab outputs only), contact information, linked policies.

`src/openamp_foundry/governance/citation_policy.py` with
`CitationEntry` dataclass (11 fields: artifact_id, citation_type, title,
version, authors, year, license_identifier, reuse_class, url, bibtex_key,
dry_lab_only), `CitationValidationResult` dataclass (6 fields,
dry_lab_only=True), `VALID_CITATION_TYPES` (4: dataset, method, schema,
software), `VALID_REUSE_CLASSES` (4: attribution_required, contact_required,
open, restricted), `VALID_LICENSE_IDENTIFIERS` (5: Apache-2.0, CC-BY-4.0,
CC-BY-NC-4.0, MIT, Proprietary), `validate_citation_entry()` (9 checks
+ 3 warning conditions), `validate_citation_dict()` (8 required fields guard).

CLI (`openamp-foundry citation-check`) with `--citation-json` (required),
`--format text|json`. Handler `_run_citation_check` in reports.py.

`make citation-check` target. 24 tests. **3599 total.**

Ecosystem clarity: citation entries are machine-validated, reuse classes are
explicit, and the honest-use boundary is documented in the guide.

## v0.7.4 — Loop 114: Phase J J6 — Security Policy ✓ (2026-07-09)

`docs/governance/SECURITY_POLICY.md` with private vulnerability reporting
process, response timeline (48h acknowledgment, 30d patch), severity
classification (critical/high/medium/low), 5 vulnerability categories
(code_vulnerability, secret_leakage, dependency_vulnerability,
safety_guardrail_bypass, dual_use_risk), out-of-scope items, disclosure
process.

`src/openamp_foundry/governance/security_policy.py` with
`VulnerabilityReport` dataclass (9 fields: report_id, severity, category,
description, affected_version, reporter_handle, report_date, status,
dry_lab_only), `SecurityReportValidationResult` dataclass (6 fields:
report_id, severity, passed, errors, warnings, dry_lab_only=True),
`VALID_SEVERITY_LEVELS` (4: critical, high, medium, low),
`VALID_VULNERABILITY_CATEGORIES` (5: code_vulnerability, secret_leakage,
dependency_vulnerability, safety_guardrail_bypass, dual_use_risk),
`VALID_REPORT_STATUSES` (6: received, acknowledged, under_review, patched,
disclosed, not_applicable), `validate_vulnerability_report()` (9 checks:
report_id SEC- prefix, valid severity, valid category, non-empty
description, non-empty affected_version, non-empty reporter_handle,
YYYY-MM-DD date, valid status, dry_lab_only must be True; critical+received
warning, safety_guardrail_bypass warning), `validate_report_dict()` (dict
input with 8 required fields guard, missing fields returns passed=False
early).

CLI (`openamp-foundry security-report-check`) with `--report-json`
(required), `--format text|json`. Handler `_run_security_report_check` in
reports.py.

`make security-report-check` target. 18 tests. **3575 total.**

Private vulnerability reporting now has a validated structure and
documented process — security reporters have a clear channel and the
project has a documented response process.

Changes:
- `docs/governance/SECURITY_POLICY.md` (J6) — Private vulnerability
  reporting process with response timeline, severity classification
  (critical/high/medium/low), 5 vulnerability categories, out-of-scope
  items, disclosure process.
- `src/openamp_foundry/governance/security_policy.py` (J6) — Core module
  with `VulnerabilityReport` (9 fields), `SecurityReportValidationResult`
  (6 fields, dry_lab_only=True), `VALID_SEVERITY_LEVELS` (4),
  `VALID_VULNERABILITY_CATEGORIES` (5), `VALID_REPORT_STATUSES` (6),
  `validate_vulnerability_report()` (9 checks with critical+received
  warning and safety_guardrail_bypass warning),
  `validate_report_dict()` (dict input with 8 required fields guard).
- `tests/governance/test_security_policy.py` (J6) — 18 tests covering:
  valid report passes, report_id not SEC- fails, empty report_id fails,
  invalid severity fails, invalid category fails, empty description fails,
  empty affected_version fails, empty reporter_handle fails, invalid date
  fails, invalid status fails, dry_lab_only=False fails, critical+received
  warns, safety_guardrail_bypass warns, validate_report_dict passes,
  validate_report_dict missing fields fails, all results dry_lab_only=True,
  VALID_SEVERITY_LEVELS has 4, VALID_VULNERABILITY_CATEGORIES has 5.
- `src/openamp_foundry/cli/main.py` (J6) — Registered `security-report-check`
  subcommand with `--report-json`, `--format` flags. Added import and
  dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J6) — Added
  `_run_security_report_check()` CLI handler with JSON parsing,
  `validate_report_dict()` call, text and JSON output, exit code 3 on
  validation failure.
- `Makefile` (J6) — Added `security-report-check` target with demo
  invocation using dependency_vulnerability severity medium. Added to
  `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J6) — v0.7.4 J6 changelog. Pipeline
  version: v0.7.4. Test count: 3575.
- `tests/test_test_count_regression.py` — baseline updated to 3575.

Honest boundaries:
- Security policy validation checks structural and policy requirements
  only. It does not verify that the vulnerability actually exists, that
  the reporter has accurately described it, or that the severity
  assessment is correct.
- `dry_lab_only: true` is a const field on all dataclasses — security
  reports are governance artifacts, not biological findings.
- The validator checks that the report_date is in YYYY-MM-DD format but
  does not verify that the date is reasonable (e.g. not in the future).
- Critical severity with received status produces a warning but does not
  fail validation — the maintainer may have good reasons for delayed
  acknowledgment, but the warning ensures it is visible.
- Safety guardrail bypass reports always produce a warning to ensure
  immediate maintainer attention, regardless of other validation status.
- The security policy defines a process and timeline but does not
  guarantee that maintainers will actually meet those timelines.
- The policy covers code vulnerabilities, secret leakage, dependency
  vulnerabilities, safety guardrail bypass, and dual-use risks. It does
  not cover theoretical vulnerabilities without a reproducible PoC,
  social engineering, or upstream dependency issues without fixes.

## v0.7.3 — Loop 113: Phase J J5 — Maintainer Rotation Plan ✓ (2026-07-09)

`docs/governance/MAINTAINER_ROTATION_PLAN.md` with maintainer rotation and
bus-factor plan (purpose, current maintainers table with 3 entries covering
primary_maintainer, secondary_maintainer, external_advisor, role definitions
for 4 roles, bus-factor assessment with target >=2 per critical function,
rotation schedule every 6 months, onboarding and offboarding checklists,
linked policies).

`src/openamp_foundry/governance/maintainer_rotation.py` with `MaintainerEntry`
dataclass (6 fields: github_handle, role, backup_handle, responsibilities,
status, dry_lab_only), `RotationPlanValidationResult` dataclass (7 fields:
passed, errors, warnings, maintainer_count, critical_role_coverage,
bus_factor_sufficient, dry_lab_only), `VALID_ROLES` (4: primary_maintainer,
secondary_maintainer, external_advisor, contributor), `CRITICAL_ROLES` (2:
primary_maintainer, secondary_maintainer), `VALID_STATUSES` (4: active,
on_leave, emeritus, departing), `validate_maintainer_entry()` (6 checks:
non-empty github_handle, valid role, critical role requires backup_handle,
non-empty responsibilities, valid status, dry_lab_only=True),
`validate_rotation_plan()` (aggregates entry validation + bus-factor
coverage: missing critical role is error, single coverage is warning),
`validate_rotation_plan_dict()` (dict input with missing-fields guard).

CLI (`openamp-foundry rotation-plan-check`) with `--plan-json` (required),
`--format text|json`. Handler `_run_rotation_plan_check` in reports.py.

`make rotation-plan-check` target. 21 tests. **3557 total.**

Maintainer rotation and bus-factor coverage is now machine-validated — the
project can detect when critical roles lack backups.

Changes:
- `docs/governance/MAINTAINER_ROTATION_PLAN.md` (J5) — Maintainer rotation
  and bus-factor plan with purpose, current maintainers table (3 entries),
  role definitions (4 roles), bus-factor assessment, rotation schedule
  (every 6 months), onboarding checklist (11 items), offboarding checklist
  (7 items), linked policies.
- `src/openamp_foundry/governance/maintainer_rotation.py` (J5) — Core module
  with `MaintainerEntry` (6 fields), `RotationPlanValidationResult` (7 fields,
  dry_lab_only=True), `VALID_ROLES` (4), `CRITICAL_ROLES` (2),
  `VALID_STATUSES` (4), `validate_maintainer_entry()` (6 checks),
  `validate_rotation_plan()` (bus-factor coverage: missing critical role is
  error, single coverage is warning), `validate_rotation_plan_dict()` (dict
  input with missing-fields guard).
- `tests/governance/test_maintainer_rotation.py` (J5) — 21 tests covering:
  valid plan passes, empty entries fails, empty github_handle fails, invalid
  role fails, critical role without backup fails, empty responsibilities fails,
  invalid status fails, dry_lab_only=False fails, no active primary maintainer
  fails, no active secondary maintainer fails, single primary maintainer warns,
  single secondary maintainer warns, validate_rotation_plan_dict missing
  'entries' key fails, validate_rotation_plan_dict valid dict passes,
  validate_rotation_plan_dict missing entry fields fails, all results
  dry_lab_only=True, VALID_ROLES has 4 entries, CRITICAL_ROLES has 2 entries,
  contributor role valid, on_leave status valid, emeritus status valid.
- `src/openamp_foundry/cli/main.py` (J5) — Registered `rotation-plan-check`
  subcommand with `--plan-json`, `--format` flags. Added import and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J5) — Added
  `_run_rotation_plan_check()` CLI handler with JSON parsing,
  `validate_rotation_plan_dict()` call, text and JSON output, exit code 3 on
  validation failure.
- `Makefile` (J5) — Added `rotation-plan-check` target with demo invocation
  using maintainer and backup-maintainer. Added to `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J5) — v0.7.3 J5 changelog. Pipeline
  version: v0.7.3. Test count: 3557.
- `tests/test_test_count_regression.py` — baseline updated to 3557.

Honest boundaries:
- Maintainer rotation validation checks structural and policy requirements only.
  It does not verify that the listed maintainers actually have the skills or
  availability to perform their roles.
- `dry_lab_only: true` is a const field on all dataclasses — rotation plan
  validation is a governance artifact, not a legal determination.
- Bus-factor assessment is a project-durability estimate, not a security
  guarantee. A bus-factor of 2 means two named people can cover a function,
  but both might be unavailable simultaneously.
- The validator cannot detect unlisted critical dependencies (e.g., institutional
  knowledge, CI secrets, domain expertise held by only one person).
- The rotation schedule is a policy declaration; this validator does not track
  whether rotations actually occurred.
- Onboarding and offboarding checklists are documentation and guidance — they
  do not replace judgment about whether a new maintainer is ready.

## v0.7.2 — Loop 112: Phase J J4 — COI Disclosure Template ✓ (2026-07-09)

`docs/governance/COI_DISCLOSURE_TEMPLATE.md` with structured COI disclosure
template (purpose, fill-in-the-blank format with 10 fields: Disclosure ID
COI-YYYY-NNN, disclosure type reviewer|contributor|maintainer|external_advisor,
subject GitHub handle, related artifact or PR, relationship type
financial|institutional|competitive|personal|none, description (required unless
none), date YYYY-MM-DD, recusal_required true|false, reviewer GitHub handle,
review_status pending|acknowledged|resolved).

`src/openamp_foundry/governance/coi_disclosure.py` with `COIDisclosure`
dataclass (10 fields), `COIValidationResult` dataclass (6 fields,
dry_lab_only=True), `VALID_DISCLOSURE_TYPES` (4: contributor, external_advisor,
maintainer, reviewer), `VALID_RELATIONSHIP_TYPES` (5: competitive, financial,
institutional, none, personal), `VALID_REVIEW_STATUSES` (3: acknowledged,
pending, resolved), `validate_coi_disclosure()` (10 checks: disclosure_id
starts with COI-, valid disclosure_type, non-empty subject/related_artifact,
valid relationship_type, description required unless none, YYYY-MM-DD date,
non-empty reviewer, valid review_status, dry_lab_only must be True; financial
without recusal yields warning not error), `validate_coi_dict()` (dict input
with 10 required fields guard).

CLI (`openamp-foundry coi-check`) with `--disclosure-json` (required),
`--format text|json`. Handler `_run_coi_check` in reports.py.

`make coi-check` target. 20 tests. **3536 total.**

COI disclosures now have a validated structure that builds institutional trust.

Changes:
- `docs/governance/COI_DISCLOSURE_TEMPLATE.md` (J4) — Structured COI disclosure
  template with purpose, template (10 fields), when to disclose (financial,
  institutional, competitive, personal), process (5 steps with escalation).
- `src/openamp_foundry/governance/coi_disclosure.py` (J4) — Core module with
  `COIDisclosure` (10 fields), `COIValidationResult` (6 fields,
  dry_lab_only=True), `VALID_DISCLOSURE_TYPES` (4), `VALID_RELATIONSHIP_TYPES`
  (5), `VALID_REVIEW_STATUSES` (3), `validate_coi_disclosure()` (10 checks),
  `validate_coi_dict()` (dict input with 10 required fields guard).
- `tests/governance/test_coi_disclosure.py` (J4) — 20 tests covering: valid
  reviewer none relationship passes, valid contributor financial passes,
  disclosure_id not starting with COI- fails, empty disclosure_id fails, invalid
  disclosure_type fails, empty subject fails, empty related_artifact fails,
  invalid relationship_type fails, relationship not none with empty description
  fails, relationship none with empty description passes, invalid date format
  fails, empty reviewer fails, invalid review_status fails, dry_lab_only=False
  fails, financial without recusal warns, validate_coi_dict passes, validate_
  coi_dict with missing fields fails, all results dry_lab_only=True,
  VALID_DISCLOSURE_TYPES has 4, VALID_RELATIONSHIP_TYPES has 5.
- `src/openamp_foundry/cli/main.py` (J4) — Registered `coi-check` subcommand
  with `--disclosure-json`, `--format` flags. Added import and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J4) — Added `_run_coi_check()`
  CLI handler with JSON parsing, validate_coi_dict call, text and JSON output,
  exit code 3 on validation failure.
- `Makefile` (J4) — Added `coi-check` target. Added to `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J4) — v0.7.2 J4 changelog. Pipeline
  version: v0.7.2. Test count: 3536.
- `tests/test_test_count_regression.py` — baseline updated to 3536.

Honest boundaries:
- COI disclosure validation checks structural and policy requirements only.
  It does not verify that the disclosed information is true, complete, or
  accurate.
- Financial relationship without recusal produces a warning, not an error —
  the reviewer retains discretion to determine whether recusal is necessary.
- The validator cannot detect undisclosed conflicts — it only checks that
  disclosed conflicts are well-formed.
- `dry_lab_only: true` is a const field on all dataclasses — COI disclosures
  are governance artifacts, not legal determinations.
- The COI template is a transparency and governance tool — it does not replace
  the judgment of the human reviewer or governance team.

## v0.7.1 — Loop 111: Phase J J3 — Release Request Template ✓ (2026-07-09)

`docs/governance/RELEASE_REQUEST_TEMPLATE.md` with structured release request
template (purpose, fill-in-the-blank format with 17 fields: Release ID,
release type, artifact ID/version, requestor name/institution, request date,
evidence level 1-6, dry_lab_only, safety_review_status, benchmark_summary,
known_limitations, intended_use, data_license, human_reviewer, review_class
A-D, approval_status; review criteria with 8 checks; process with classes A-D
timelines and escalation path).

`src/openamp_foundry/governance/release_request.py` with `ReleaseRequest`
dataclass (17 fields), `ReleaseRequestValidationResult` dataclass (6 fields,
dry_lab_only=True), `VALID_RELEASE_TYPES` (5: candidate, model, dataset,
evidence_packet, schema), `VALID_SAFETY_STATUSES` (3: pending, approved,
not_required), `VALID_INTENDED_USES` (4: research, internal, external_partner,
public), `VALID_APPROVAL_STATUSES` (4: pending, approved, rejected, deferred),
`VALID_REVIEW_CLASSES` (4: A, B, C, D), `validate_release_request()` (17 checks:
release_id format, release_type valid, non-empty artifact_id/artifact_version/
requestor_name/requestor_institution, request_date YYYY-MM-DD, evidence_level
1-6, dry_lab_only must be True, safety_review_status valid, non-empty
benchmark_summary/known_limitations/data_license/human_reviewer, intended_use
valid, review_class valid, approval_status valid, dry_lab_only+evidence_level>4
error, public+safety_pending error, model+review_class warning).

`validate_request_dict()` (dict input with 17 required fields guard, missing
fields returns passed=False early).

CLI (`openamp-foundry release-request-check`) with `--request-json` (required),
`--format text|json`. Handler `_run_release_request_check` in reports.py.

`make release-request-check` target. 25 tests. **3516 total.**

Blocks public releases with pending safety review, blocks dry_lab_only
artifacts with evidence_level>4. Formal release requests now have a validated
structure before entering human review.

Changes:
- `docs/governance/RELEASE_REQUEST_TEMPLATE.md` (J3) — Structured release
  request template with purpose, template (17 fields), review criteria (8
  checks), process (5 steps with A-D timelines and escalation path).
- `src/openamp_foundry/governance/release_request.py` (J3) — Core module with
  `ReleaseRequest` (17 fields), `ReleaseRequestValidationResult` (6 fields,
  dry_lab_only=True), `VALID_RELEASE_TYPES` (5), `VALID_SAFETY_STATUSES` (3),
  `VALID_INTENDED_USES` (4), `VALID_APPROVAL_STATUSES` (4),
  `VALID_REVIEW_CLASSES` (4), `validate_release_request()` (17 checks),
  `validate_request_dict()` (dict input with missing-fields guard).
- `tests/governance/test_release_request.py` (J3) — 25 tests covering: valid
  candidate release request passes, release_id not starting with REL- fails,
  invalid release_type fails, empty artifact_id fails, empty requestor_name
  fails, invalid request_date format fails, evidence_level=0 fails,
  evidence_level=7 fails, dry_lab_only=False fails, invalid safety_review_status
  fails, empty benchmark_summary fails, empty known_limitations fails, invalid
  intended_use fails, public release with pending safety fails, dry_lab_only
  with evidence_level=5 fails, all results dry_lab_only=True, validate_request_
  dict passes, VALID_RELEASE_TYPES has 5, VALID_SAFETY_STATUSES has 3,
  VALID_INTENDED_USES has 4, VALID_APPROVAL_STATUSES has 4, VALID_REVIEW_CLASSES
  has 4, model review_class warning, dict missing fields fails.
- `src/openamp_foundry/cli/main.py` (J3) — Registered `release-request-check`
  subcommand with `--request-json`, `--format` flags. Added import and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J3) — Added
  `_run_release_request_check()` CLI handler with JSON parsing, validate_request
  _dict call, text and JSON output, exit code 3 on validation failure.
- `Makefile` (J3) — Added `release-request-check` target. Added to `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J3) — v0.7.1 J3 changelog. Pipeline
  version: v0.7.1. Test count: 3516.
- `tests/test_test_count_regression.py` — baseline updated to 3516.

Honest boundaries:
- Release request validation checks structural and policy requirements only.
  It does not verify that the artifact actually exists, that the evidence level
  claim is accurate, or that the safety review was thorough.
- `dry_lab_only: true` is a const field on all dataclasses — release requests
  are governance artifacts, not biological findings.
- The validator blocks public releases with pending safety review, but it cannot
  verify that the safety review was correctly performed or that the reviewer was
  qualified.
- Review classes are policy declarations — the validator checks that the class
  is valid (A-D) but not that the appropriate review process was followed.
- The release request template is a communication and governance tool — it does
  not replace the judgment of the human reviewer.

## v0.7.0 — Loop 110: Phase J J2 — Governance Decision Log ✓ (2026-07-09)

`docs/governance/DECISION_LOG.md` with structured governance decision log
(purpose, decision index with 8 entries GOV-001 through GOV-008 covering
safety/benchmark/release/evidence/data/adapter/contribution/docs scopes,
how to add entries, linked policies).

`src/openamp_foundry/governance/decision_log.py` with `VALID_SCOPES` (8:
safety, benchmark, release, evidence, data, adapter, contribution, docs),
`VALID_STATUSES` (4: active, superseded, under_review, proposed),
`VALID_REVIEW_CLASSES` (4: A, B, C, D), `GovernanceDecision` dataclass
(8 fields: decision_id, date, scope, decision, status, rationale,
review_class, dry_lab_only=True), `DecisionValidationResult` dataclass
(5 fields: decision_id, passed, errors, warnings, dry_lab_only=True),
`GOVERNANCE_DECISIONS` list (8 entries: GOV-001 through GOV-008),
`validate_governance_decision()` (9 checks: decision_id format, date
format, valid scope, non-empty decision, valid status, non-empty rationale,
valid review_class, dry_lab_only must be True, superseded warning),
`validate_all_decisions()` (aggregates total/passed/failed/all_passed/
results/dry_lab_only), `get_decisions_by_scope()` (filters by scope),
`get_decisions_by_status()` (filters by status).

CLI (`openamp-foundry decision-log`) with `--validate`, `--scope`,
`--format text|json`. Handler `_run_decision_log` in reports.py.

`make decision-log` target. 27 tests. **3491 total.**

**Phase J milestone: v0.7.0** — governance decisions are now discoverable
and machine-validated.

Changes:
- `docs/governance/DECISION_LOG.md` (J2) — Structured governance decision
  log with purpose, decision index (8 entries GOV-001 through GOV-008),
  how to add entries, linked policies.
- `src/openamp_foundry/governance/decision_log.py` (J2) — Core module with
  `VALID_SCOPES` (8), `VALID_STATUSES` (4), `VALID_REVIEW_CLASSES` (4),
  `GovernanceDecision` (8 fields, dry_lab_only=True default),
  `DecisionValidationResult` (5 fields, dry_lab_only=True default),
  `GOVERNANCE_DECISIONS` (8 entries: GOV-001 through GOV-008),
  `validate_governance_decision()` (9 checks),
  `validate_all_decisions()` (aggregates total/passed/failed/all_passed),
  `get_decisions_by_scope()`, `get_decisions_by_status()`.
- `tests/governance/test_decision_log.py` (J2) — 27 tests covering all
  8 GOV entries pass validation, empty/invalid decision_id, invalid date
  format, invalid scope (parametrized), empty decision text, invalid
  status (parametrized), empty rationale, invalid review_class
  (parametrized), dry_lab_only=False failure, superseded warning,
  validate_all_decisions passes, get_decisions_by_scope safety → GOV-001,
  get_decisions_by_status active → all 8, 8 entries constant check,
  all results dry_lab_only=True, valid set counts, DecisionValidationResult
  dataclass fields.
- `src/openamp_foundry/cli/main.py` (J2) — Registered `decision-log`
  subcommand with `--validate`, `--scope`, `--format` flags. Added import
  and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J2) — Added
  `_run_decision_log()` CLI handler with validate/scope filtering/list all
  modes, text and JSON output, exit code 3 on validation failure.
- `Makefile` (J2) — Added `decision-log` target. Added to `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J2) — v0.7.0 J2 changelog. Pipeline
  version: v0.7.0. Test count: 3491.
- `tests/test_test_count_regression.py` — baseline updated to 3491.

Honest boundaries:
- Decision log tracks governance decisions only — it does not measure
  biological activity, safety, or clinical value.
- `dry_lab_only: true` is a const field on all dataclasses — the decision
  log is a computational governance artifact, not a biological finding.
- The list of valid scopes and statuses is policy-defined and may need
  expansion as governance matures.
- Validation checks structural and policy requirements only — it does
  not verify that the decision was correctly implemented or enforced.
- Review classes are declarations stored on each decision; the validator
  does not verify that the declared review class was actually applied.
- The decision log is a documentation and validation tool — it does not
  replace human judgment about whether a decision is appropriate.

## v0.7.1 — Loop 111: Phase J J3 — Release Request Template ✓ (2026-07-09)

`docs/governance/RELEASE_REQUEST_TEMPLATE.md` with structured release
request template (purpose, fill-in template with 17 fields, review
criteria with 8 checks, process with classes A-D timelines and escalation).

`src/openamp_foundry/governance/release_request.py` with `ReleaseRequest`
dataclass (17 fields), `ReleaseRequestValidationResult` dataclass (6 fields,
dry_lab_only=True), `VALID_RELEASE_TYPES` (5), `VALID_SAFETY_STATUSES` (3),
`VALID_INTENDED_USES` (4), `VALID_APPROVAL_STATUSES` (4),
`VALID_REVIEW_CLASSES` (4), `validate_release_request()` (17 checks with
dry_lab_only+evidence_level>4 error, public+safety_pending error,
model+review_class warning), `validate_request_dict()` (dict input with
missing-fields guard).

CLI (`openamp-foundry release-request-check`) with `--request-json`,
`--format text|json`. Handler `_run_release_request_check` in reports.py.

`make release-request-check` target. 25 tests. **3516 total.**

Changes:
- `docs/governance/RELEASE_REQUEST_TEMPLATE.md` (J3) — Structured release
  request template with purpose, fill-in template (17 fields), review
  criteria (8 checks), process (submit→validate→review→decision→release),
  expected timelines per class A-D, escalation path.
- `src/openamp_foundry/governance/release_request.py` (J3) — Core module
  with `ReleaseRequest` (17 fields), `ReleaseRequestValidationResult`
  (6 fields, dry_lab_only=True), `VALID_RELEASE_TYPES` (5),
  `VALID_SAFETY_STATUSES` (3), `VALID_INTENDED_USES` (4),
  `VALID_APPROVAL_STATUSES` (4), `VALID_REVIEW_CLASSES` (4),
  `validate_release_request()` (17 checks including cross-field rules:
  dry_lab_only+evidence_level>4 error, public+safety_pending error,
  model+review_class C/D warning), `validate_request_dict()`.
- `tests/governance/test_release_request.py` (J3) — 25 tests covering:
  valid candidate passes, release_id must start with REL-, invalid type,
  empty artifact_id/requestor_name, invalid date format, evidence_level
  0/7, dry_lab_only=False, invalid safety_status, empty benchmark_summary/
  known_limitations, invalid intended_use, public+safety_pending fails,
  dry_lab_only+evidence_level 5 fails, dry_lab_only=True on results,
  valid dict passes, VALID_RELEASE_TYPES has 5 entries, VALID_SAFETY_STATUSES
  has 3, VALID_INTENDED_USES has 4, VALID_APPROVAL_STATUSES has 4,
  VALID_REVIEW_CLASSES has 4, model+low review_class warning, dict missing
  fields, invalid type via dict.
- `src/openamp_foundry/cli/main.py` (J3) — Registered `release-request-check`
  subcommand with `--request-json` (required), `--format` flags. Added import
  and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` (J3) — Added
  `_run_release_request_check()` CLI handler with JSON parsing,
  `validate_request_dict()` call, text and JSON output, exit code 3
  on failure.
- `Makefile` (J3) — Added `release-request-check` target with demo invocation
  using schema release type with all fields valid. Added to `.PHONY`.
- `docs/evidence/METRICS_CURRENT.md` (J3) — v0.7.1 J3 changelog. Pipeline
  version: v0.7.1. Test count: 3516.
- `tests/test_test_count_regression.py` — baseline updated to 3516.

Honest boundaries:
- Release request validation checks structural and policy requirements only.
  It does not verify that the release was actually performed, that the
  artifact exists, or that the benchmark claims are biologically meaningful.
- `dry_lab_only: true` is a const field on all dataclasses — release requests
  are computational governance artifacts, not biological findings.
- The validator does not verify that the human reviewer has actually reviewed
  the request — it only checks that a GitHub handle was provided.
- Review class appropriateness is advisory: the validator warns about model
  releases with low review classes but does not block them.
- The template and process are governance tools — they do not replace human
  judgment about whether a release is appropriate or safe.

## v0.6.9 — Loop 109: Phase J J1 — Release Checklist ✓ (2026-07-09)

`docs/governance/RELEASE_CHECKLIST.md` with structured release checklist
cross-referencing `docs/trust/RELEASE_CHECKLIST.md`.

`src/openamp_foundry/governance/release_gate.py` with `RELEASE_TYPES` (5:
candidate, model, dataset, evidence_packet, schema), `UNIVERSAL_GATES` (7:
ci_tests_pass, agent_check_passes, no_critical_issues, dry_lab_only_confirmed,
safety_flags_reviewed, data_license_verified, no_hardcoded_secrets),
`EXTRA_GATES_BY_TYPE` (per-type additional gates), `ReleaseGateResult`
dataclass (8 fields, dry_lab_only=True), `validate_release_gate()` (validates
all required gates, treats missing gates as failed, raises CRITICAL error
on dry_lab_only_confirmed failure).

CLI (`openamp-foundry release-gate-check`) with `--release-type`,
`--artifact-id`, `--gates-json`, `--format text|json`.

`make release-gate-check` target. 18 tests. **3478 total.**

**Starts Phase J (Governance and release maturity)** — releases now require
all gates to pass before external release, preventing accidental bypass of
required checks.

Changes:
- `docs/governance/RELEASE_CHECKLIST.md` — Structured release checklist with
  pre-release gates, release-type gates (5 types), post-release checklist.
- `src/openamp_foundry/governance/__init__.py` — Empty package init.
- `src/openamp_foundry/governance/release_gate.py` (J1) — Core module with
  `RELEASE_TYPES` (5), `UNIVERSAL_GATES` (7), `EXTRA_GATES_BY_TYPE`,
  `ReleaseGateResult` (8 fields, dry_lab_only=True),
  `validate_release_gate()`.
- `tests/governance/__init__.py` — Empty package init.
- `tests/governance/test_release_gate.py` (J1) — 18 tests covering all
  release types, universal gate failure, missing gates, invalid release
  type, empty artifact_id, dry_lab_only_confirmed CRITICAL error, constant
  checks.
- `src/openamp_foundry/cli/commands/gates.py` (J1) — Added
  `_run_release_gate_check()` CLI handler with JSON parsing,
  `validate_release_gate()`…14410 tokens truncated…-id`, `--module-id`, `--module-version`, `--timestamp-utc`,
  `--input-sequence`, `--scores-json`, `--calibration-set`, `--format` flags.
  Added import and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` — Added `_run_simulation_provenance()`
  CLI handler with JSON parsing, validation, text and JSON output, exit code 3 on
  validation error.
- `Makefile` — Added `simulation-provenance` target with demo invocation using
  `test-run-001`. Added to `.PHONY`.
- `tests/simulation/test_provenance.py` — 19 tests covering: record creation,
  deterministic hashes, dry_lab_only always True, all validation checks
  (empty fields, bad timestamp, wrong-length hash, dry_lab_only=False),
  provenance_summary with 0 and N records.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.93 H5 changelog. Test count: 3181.
- `tests/test_test_count_regression.py` — baseline updated to 3181.

Honest boundaries:
- SHA-256 hashes prove content integrity, not biological activity.
- The provenance record attests that a simulation ran, not that the result
  is biologically meaningful.
- `input_hash` covers the input sequence only; other input parameters
  (e.g., engine settings) are not hashed.
- `result_hash` uses JSON serialisation with sort_keys=True; any future
  change to the serialisation format will change the hash for identical data.
- Timestamps are self-reported by the caller and not independently verified.
- Provenance records are dry-lab only and must not be presented as
  biological proof.

## v0.5.92 — Loop 92: Phase H H4 — Fail-Closed Adapter Integration Tests ✓ (2026-07-09)

`FAIL_CLOSED_REASONS` dict (6 keys) enumerates known adapter failure reasons.
`AdapterGateResult` dataclass with module_id, passed, failure_reason, failure_detail,
dry_lab_only. `evaluate_adapter_gate()` fail-closed: returns passed=False on ANY
failure signal with strict priority ordering (timeout > connection_refused >
invalid_response > schema_violation > module_unavailable > baseline_not_beaten).
`run_adapter_gate_batch()` aggregates multiple adapter calls with total/passed/failed/
any_failed/results/dry_lab_only. Avoids hidden external failures — when the adapter
to an external simulation service is down or misbehaves, the pipeline must fail
loudly rather than silently passing garbage through.

Changes:
- `src/openamp_foundry/simulation/adapter_gate.py` (H4) — Core module with
  `FAIL_CLOSED_REASONS` dict (6 entries), `AdapterGateResult` dataclass (5 fields:
  module_id, passed, failure_reason, failure_detail, dry_lab_only),
  `evaluate_adapter_gate()` with 7-path priority logic,
  `run_adapter_gate_batch()` aggregating results with counts and any_failed flag.
- `src/openamp_foundry/simulation/__init__.py` — Exports `AdapterGateResult`,
  `FAIL_CLOSED_REASONS`, `evaluate_adapter_gate`, `run_adapter_gate_batch`.
- `src/openamp_foundry/cli/main.py` — Registered `adapter-gate-check` subcommand
  with `--module-id`, `--timeout`, `--connection-refused`, `--schema-errors`,
  `--module-unavailable`, `--baseline-beaten`, `--format` flags. Added import
  and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` — Added `_run_adapter_gate_check()`
  CLI handler with text and JSON output, JSON parsing for schema errors,
  exit code 3 on failure.
- `Makefile` — Added `adapter-gate-check` target with default `membrane_proxy`
  check. Added to `.PHONY`.
- `tests/simulation/test_adapter_gate.py` — 20 tests covering: all 6 failure
  reasons, all-clear pass, dry_lab_only always True, priority ordering (timeout
  beats connection_refused, connection_refused beats result=None, schema_errors
  beat module_unavailable), baseline_beaten=True passes, baseline_beaten=None
  does not trigger, batch counts, batch any_failed, batch dry_lab_only.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.92 H4 changelog. Test count: 3161.
- `tests/test_test_count_regression.py` — baseline updated to 3161.

Honest boundaries:
- The adapter gate checks for known failure signals only. An adapter that
  returns plausible-looking but biologically meaningless results will pass.
- Failure detection depends on the caller correctly setting the failure
  flags. An adapter that silently hangs (neither timeout nor connection
  refused) may not be caught.
- Schema validation errors detect structural contract violations, not
  biological correctness. A schema-valid response can still be biologically
  meaningless.
- The `baseline_not_beaten` check requires the caller to run the baseline
  comparison externally; the gate does not compute it.
- All adapter gate checks are dry-lab only and must not be presented as
  biological proof.

## v0.5.91 — Loop 91: Phase H H3 — Per-Module Cheapest-Baseline Declaration ✓ (2026-07-09)

`BaselineDeclaration` dataclass with module_id, module_name, baseline_description,
baseline_type, evidence_level_ceiling, and notes. `BASELINE_DECLARATIONS` list
(4 entries: membrane_proxy, structure_proxy, dummy_membrane_proxy,
external_adapter_placeholder). `get_baseline_declaration()` and
`list_baseline_declarations()` for lookup. `check_baseline_requirement()` caps
effective_evidence_level to ceiling when baseline not beaten.
`validate_baseline_declarations()` checks module_id, baseline_description,
baseline_type, evidence_level_ceiling, and duplicate detection. Forces honest
enemy comparison — every simulation module must declare the simplest baseline
it must beat, making it easy to detect "simulation theater."

Changes:
- `src/openamp_foundry/simulation/baseline_registry.py` (H3) — Core module with
  `BaselineDeclaration` dataclass (6 fields), `BASELINE_DECLARATIONS` list
  (4 entries), `get_baseline_declaration()`, `list_baseline_declarations()`,
  `check_baseline_requirement()` with ceiling logic,
  `validate_baseline_declarations()` with 5 checks.
- `src/openamp_foundry/simulation/__init__.py` — Exports all baseline registry
  symbols.
- `src/openamp_foundry/cli/main.py` — Registered `simulation-baseline-check`
  subcommand with `--module-id`, `--claimed-level`, `--baseline-beaten`,
  `--format` flags. Added import and dispatch.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_simulation_baseline_check()` CLI handler with text and JSON output,
  error handling for unknown module IDs, exit code 3 if capped.
- `Makefile` — Added `simulation-baseline-check` target with default
  `membrane_proxy` check. Added to `.PHONY`.
- `tests/simulation/test_baseline_registry.py` — 16 tests covering: at least
  4 entries, validation passes, get/list lookup, required field presence,
  baseline type validity, check logic (beaten/not beaten/capped/uncapped),
  dry_lab_only always True, unknown module handling, duplicate detection,
  invalid baseline type detection.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.91 H3 changelog. Test count: 3141.
- `tests/test_test_count_regression.py` — baseline updated to 3141.

Honest boundaries:
- Baseline declarations are self-reported by module maintainers and must be
  manually kept in sync with the module registry.
- `check_baseline_requirement()` caps evidence levels based on declared
  ceilings, not on independent biological validation.
- A module that beats its cheapest baseline may still produce biologically
  meaningless results — beating a heuristic baseline is a necessary condition
  for evidence, not a sufficient one.
- Baseline types are categorical labels; a "heuristic" baseline and a "length"
  baseline are not directly comparable in difficulty.
- The evidence_level_ceiling is a policy rule, not a biological guarantee.
  Higher ceilings should be justified by actual benchmark performance.
- All baseline comparisons are dry-lab only and must not be presented as
  biological proof.

## v0.5.90 — Loop 90: Phase H H2 — Simulation-Result Schema and Validator ✓ (2026-07-09)

`schemas/simulation_result.schema.json` (Draft 2020-12) validates SimulationResult
outputs with uncertainty 0.0–1.0 range and all required fields.
`validate_simulation_result()` checks module, version, scope, scores, uncertainty,
validated_against, notes. Strict mode rejects dummy/stub modules, uncertainty=1.0,
and empty validated_against. `validate_simulation_result_batch()` aggregates
results with counts and `any_invalid` flag. CLI (`openamp-foundry
validate-simulation-result`) with `--results-json`, `--strict`, `--out-json`.
Prevents undocumented proxy output — every SimulationResult is now
machine-checkable against a formal JSON schema.

Changes:
- `schemas/simulation_result.schema.json` (H2) — JSON Schema Draft 2020-12
  for SimulationResult outputs. Required fields: module, version, scope, scores,
  uncertainty (min 0.0, max 1.0), calibration_set (string or null),
  validated_against, notes. Optional `dry_lab_context` const "dry-lab-only".
- `src/openamp_foundry/simulation/result_validator.py` (H2) —
  `validate_simulation_result()` with 6 always-checked rules and 3 strict-mode
  rules. `validate_simulation_result_batch()` with checked/valid/invalid/
  errors_by_module/any_invalid/dry_lab_only keys.
- `src/openamp_foundry/simulation/__init__.py` — Exports
  `validate_simulation_result`, `validate_simulation_result_batch`.
- `src/openamp_foundry/cli/main.py` — Registered `validate-simulation-result`
  subcommand with `--results-json`, `--strict`, `--out-json` flags.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_validate_simulation_result()` CLI handler with JSON loading,
  SimulationResult deserialization, batch validation, and output.
- `Makefile` — Added `validate-simulation-result-schema` target to `.PHONY`.
  Fixed duplicate `.PHONY` entry for `simulation-registry`.
- `tests/simulation/test_result_validator.py` — 19 tests covering: valid
  result, empty module/version, uncertainty bounds, strict mode rules,
  batch validation, and non-finite scores.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.90 H2 changelog. Test count: 3125.
- `tests/test_test_count_regression.py` — baseline updated to 3125.

Honest boundaries:
- Schema validation checks structural correctness, not biological truth.
- A schema-valid SimulationResult may still be biologically meaningless.
- Uncertainties are self-reported by simulation modules and not independently
  verified by this validation layer.
- Strict mode is an additional policy layer; it does not guarantee that a
  passing result is biologically meaningful.
- All simulation results are dry-lab only and must not be presented as
  biological proof.

## v0.5.89 — Loop 89: Phase H H1 — Simulation Module Registry ✓ (2026-07-09)

`SIMULATION_MODULE_REGISTRY` with 4 entries (membrane_proxy, structure_proxy,
dummy_membrane_proxy, external_adapter_placeholder). `SimulationModuleEntry`
dataclass tracks module_id, name, description, status, evidence_level,
baseline_comparison, scope, maintainer, and notes. Lookup functions:
`get_module_entry()`, `list_module_entries()` with status/min_evidence
filtering, `get_active_modules()`, `registry_summary()` with
total/by_status/by_evidence_level/active_module_ids keys.
`validate_registry()` checks module_id, name, baseline_comparison,
evidence_level 1-6, valid status, duplicate detection.
CLI (`openamp-foundry simulation-registry`) with `--list`, `--show`,
`--status`, `--min-evidence`, `--format text|json`.
Schema (`schemas/simulation_module_registry.schema.json`).
`make simulation-registry` target. 28 tests. 3106 total.
Starts Phase H (virtual assay discipline).

Changes:
- `src/openamp_foundry/simulation/module_registry.py` (H1) — Core module with
  `SimulationModuleStatus` literal type, `SimulationModuleEntry` dataclass
  (9 fields), `SIMULATION_MODULE_REGISTRY` list (4 entries),
  `get_module_entry()`, `list_module_entries()`, `get_active_modules()`,
  `registry_summary()` with aggregation, `validate_registry()` with 6 checks.
  Imports `PROOF_LADDER_LEVELS` from `evidence/synthetic_result_policy.py`.
- `schemas/simulation_module_registry.schema.json` (H1) — JSON Schema Draft
  2020-12 for the registry_summary() output. Validates total, by_status
  (all 4 status keys), by_evidence_level, active_module_ids.
- `src/openamp_foundry/simulation/__init__.py` — Exports all module registry
  symbols.
- `src/openamp_foundry/cli/main.py` — Registered `simulation-registry`
  subcommand with `--list`, `--show`, `--status`, `--min-evidence`,
  `--format` flags.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_simulation_registry()` CLI handler with text and JSON output,
  per-module details, status/evidence filtering, and validation.
- `Makefile` — Added `simulation-registry` target with `--list` default.
  Added to `.PHONY`.
- `tests/simulation/test_module_registry.py` — 28 tests covering: registry
  size ≥ 4, all entries pass validation, required field presence, evidence
  level range 1-6, valid status values, get_module_entry known/unknown,
  list_module_entries no filter/status filter/min_evidence filter,
  get_active_modules returns only active, registry_summary keys and totals,
  validate_registry detection of empty fields, invalid level, invalid
  status, duplicate ids, PROOF_LADDER_LEVELS completeness.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.89 H1 changelog. Test count: 3106.
- `tests/test_test_count_regression.py` — baseline updated to 3106.

Honest boundaries:
- The registry lists module status and evidence level for informational
  purposes only. It does not measure biological activity, safety, or
  real-world performance.
- Registry validation checks structural correctness, not scientific validity.
  A valid entry may still produce biologically meaningless results.
- The PROOF_LADDER_LEVELS mapping is a claim-level taxonomy. An evidence_level
  of 2 ("virtual-assay support") means the module supports computational
  exploration — it does not constitute biological proof.
- The registry is dry-lab only. All module entries carry dry-lab caveats
  regardless of their status or evidence_level.
- "active" status means the module is available for use, not that it has
  been biologically validated.

## v0.5.88 — Loop 88: Phase G G10 — Recalibration Rollback Plan ✓ (2026-07-09)

`build_rollback_plan()` produces a structured `RollbackPlan` with 5 rollback
triggers (RT-01 through RT-05) and 6 default rollback steps covering halt,
document, restore, verify, root-cause, and log. `RollbackPlan` dataclass with
plan_id, version, triggered_by, steps, notes, dry_lab_only, and to_dict().
`RollbackStep` dataclass with step_number, action, responsible, detail, and
dry_lab_only. CLI (`openamp-foundry calibration-rollback-plan`).
JSON + Markdown output. Schema (`schemas/calibration_rollback_plan.schema.json`).
`make calibration-rollback-plan` target. 15 tests. 3078 total.
This completes Phase G (G1-G10 — calibration and active-learning rigor).

Changes:
- `src/openamp_foundry/calibration/rollback_plan.py` (G10) — Core module with
  `ROLLBACK_TRIGGERS` list (5 triggers: RT-01 through RT-05), `RollbackStep`
  dataclass (5 fields: step_number, action, responsible, detail, dry_lab_only),
  `RollbackPlan` dataclass (6 fields: plan_id, version, triggered_by, steps,
  notes, dry_lab_only), `DEFAULT_ROLLBACK_STEPS` list (6 steps),
  `build_rollback_plan()` with trigger ID validation, `write_rollback_plan_json()`
  and `write_rollback_plan_markdown()` for structured output.
- `schemas/calibration_rollback_plan.schema.json` (G10) — JSON Schema Draft
  2020-12 for the rollback plan. Validates all 6 required fields including
  plan_id, version, triggered_by with RT-NN pattern, steps with ordered
  actions, and dry_lab_only const=true.
- `src/openamp_foundry/calibration/__init__.py` — Exports all rollback plan
  symbols.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_calibration_rollback_plan()` CLI handler with `--plan-id`, `--version`,
  `--triggered-by`, `--notes`, `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `calibration-rollback-plan`
  subcommand with all argument flags and dispatch to handler.
- `Makefile` — Added `calibration-rollback-plan` target with default example
  writing to `/tmp/rollback_plan.json` and `/tmp/rollback_plan.md`.
  Added to `.PHONY`.
- `tests/calibration/test_rollback_plan.py` — 18 tests covering: valid triggers
  pass, unknown trigger raises ValueError, triggered_by stored correctly, steps
  include all default steps, extra_steps appended correctly, dry_lab_only always
  True, ROLLBACK_TRIGGERS count and required fields, plan_id stored correctly,
  version stored correctly, to_dict has required keys, notes stored correctly,
  default steps have correct responsible parties, JSON writer, Markdown writer.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.88 G10 changelog. Test count: 3081.
- `tests/test_test_count_regression.py` — baseline updated to 3081.

Honest boundaries:
- The rollback plan restores weight configurations only. It does not undo
  candidate selections, synthesis decisions, or code-level regressions.
- Rollback triggers are detection rules, not guarantees. A regression that
  does not match any trigger may still be harmful.
- All rollback steps require human review (steps 2, 5, 6 explicitly).
  Automated rollback without documented human oversight is not permitted.
- The plan is a procedural framework. Actual rollback execution may require
  additional context-specific steps.
- Dry-lab only. Rollback affects computational scoring, not biological
  activity, safety, or real-world outcomes.

## v0.5.87 — Loop 87: Phase G G9 — Calibration Decision Review Checklist ✓ (2026-07-09)

`build_checklist()` produces a structured `CalibrationDecisionChecklist` with 12
checklist items (10 required) covering data quality, statistical validity, safety
consistency, approval, and documentation. Each item has an id, category, question,
rationale, and required flag. `CalibrationDecisionChecklist` dataclass tracks
responses, notes, overall_pass, and missing_required. JSON + Markdown output.
Schema (`schemas/calibration_decision_checklist.schema.json`).
CLI (`openamp-foundry calibration-decision-checklist`).
`make calibration-decision-checklist` target. 14 tests. 3063 total.
Makes human review structured and auditable.

Changes:
- `src/openamp_foundry/calibration/decision_checklist.py` (G9) — Core module with
  `CHECKLIST_ITEMS` list (12 items), `CalibrationDecisionChecklist` dataclass
  (8 fields: checklist_id, date, reviewer, responses, notes, overall_pass,
  missing_required, dry_lab_only), `build_checklist()` applying response validation
  and missing-required analysis, `write_checklist_json()` and
  `write_checklist_markdown()` for structured output.
- `schemas/calibration_decision_checklist.schema.json` (G9) — JSON Schema Draft
  2020-12 for the decision checklist. Validates all 8 required fields including
  date pattern, responses object, and dry_lab_only const=true.
- `src/openamp_foundry/calibration/__init__.py` — Exports all decision checklist
  symbols.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_calibration_decision_checklist()` CLI handler with `--checklist-id`,
  `--date`, `--reviewer`, `--responses-json`, `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `calibration-decision-checklist`
  subcommand with all argument flags and dispatch to handler.
- `Makefile` — Added `calibration-decision-checklist` target with default example
  data writing to `/tmp/checklist_output.json` and `/tmp/checklist_output.md`.
  Added to `.PHONY`.
- `tests/calibration/test_decision_checklist.py` — 14 tests covering: all required
  pass → overall_pass=True, missing required → overall_pass=False, missing_required
  list correct, unknown response id raises ValueError, dry_lab_only always True,
  notes stored correctly, checklist_id stored correctly, reviewer stored correctly,
  date stored correctly, CHECKLIST_ITEMS minimum count, required items have
  required=True attribute, all items have required fields, JSON writer, Markdown
  writer with table and icons.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.87 G9 changelog. Test count: 3063.
- `tests/test_test_count_regression.py` — baseline updated to 3063.

Honest boundaries:
- The checklist validates structured human-review completion, not biological
  correctness. A passing checklist does not confirm biological activity or safety.
- Required items are policy-defined. Missing or false required items block the
  overall_pass, but a pass does not guarantee that human review was thorough.
- All calibration decisions require qualified human review regardless of checklist
  results.
- The dry_lab_only=True constraint is an attestation, not a technical proof.

## v0.5.86 — Loop 86: Phase G G8 — Synthetic-Result Policy (Anti-Overclaim) ✓ (2026-07-09)

`check_synthetic_result_policy()` and `run_policy_batch()` enforce that synthetic/
simulation results cannot raise the proof-ladder level of a candidate. Levels 4+
require wet-lab evidence; synthetic or unknown sources are blocked for such proposals.
CLI (`openamp-foundry synthetic-result-policy-check`). Schema
(`schemas/synthetic_result_policy_check.schema.json`). `make synthetic-result-policy-check`
target. 27 tests. 3049 total. Anti-overclaim safeguard.

## v0.5.86 — Loop 86: Phase G G8 — Synthetic Result Policy — Anti-Overclaim ✓ (2026-07-09)

`check_synthetic_result_policy()` enforces that synthetic/simulation outputs cannot
raise a candidate's proof-ladder level. Simulation outputs are anti-overclaim —
they must not be used as evidence to move a candidate up the proof ladder.

Changes:
- `src/openamp_foundry/evidence/synthetic_result_policy.py` (G8) — Core module with
  `PROOF_LADDER_LEVELS` dictionary (1–6 mapping to descriptions),
  `SyntheticResultPolicyCheck` dataclass (8 fields: candidate_id, current_level,
  proposed_level, evidence_source, policy_pass, violation, recommendation,
  dry_lab_only), `check_synthetic_result_policy()` applying multi-tier rules
  (synthetic cannot raise, synthetic cannot lower, levels 4+ require wet-lab
  evidence, invalid level raises ValueError), `run_policy_batch()` aggregating
  results with summary counts and any_violation flag,
  `write_policy_check_json()` and `write_policy_check_markdown()` for output.
- `schemas/synthetic_result_policy_check.schema.json` (G8) — JSON Schema Draft 07
  for single or batch policy check results. Validates all 8 required fields
  including evidence_source enum constraint and dry_lab_only const=true.
- `src/openamp_foundry/evidence/__init__.py` — Exports all synthetic result policy
  symbols.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_synthetic_result_policy_check()` CLI handler with `--proposals-json`,
  `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `synthetic-result-policy-check`
  subcommand with all argument flags and dispatch to handler.
- `Makefile` — Added `synthetic-result-policy-check` target with default example
  data writing to `/tmp/srp_output.json` and `/tmp/srp_output.md`. Added to
  `.PHONY`.
- `tests/evidence/test_synthetic_result_policy.py` — 27 tests covering: synthetic
  raising level, synthetic maintaining level, synthetic lowering level, lab raising
  level, literature raising level, proposed_level > 3 with synthetic/unknown source
  violation, proposed_level > 3 with lab/literature pass, invalid current_level,
  invalid proposed_level, unknown source normalization, unknown source + level 4
  violation, dry_lab_only always True, run_policy_batch summary counts, all-pass
  batch, any_violation flag, to_dict output, PROOF_LADDER_LEVELS completeness,
  JSON writer (single + batch), Markdown writer (single + batch), recommendation
  non-empty for violation, recommendation for pass, empty batch list.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.86 G8 changelog. Test count: 3049.
- `tests/test_test_count_regression.py` — baseline updated to 3049.

Honest boundaries:
- This policy check validates evidence-source discipline, not biological truth.
  A PASS does not confirm biological activity or safety.
- Synthetic evidence can still be useful for negative-result documentation and
  exploratory research — the policy restricts proof-ladder movement, not usage.
- Level 4+ wet-lab evidence requirement is a policy rule, not a biological
  guarantee. Wet-lab evidence can be wrong, inconclusive, or non-reproducible.
- The evidence_source classification relies on the submitter's honest labeling.
  A "lab" source may still be noisy or erroneous.
- All proof-ladder determinations require qualified human review regardless of
  policy check results.

## v0.5.85 — Loop 85: Phase G G7 — Result-Quality Flag Propagation into Calibration Engine ✓ (2026-07-09)

`assess_result_quality()` and `filter_results_for_calibration()` propagate
result-quality flags into the calibration engine. Low-quality outcomes cannot
drive updates — garbage results must not update the scoring model.

Changes:
- `src/openamp_foundry/calibration/result_quality.py` (G7) — Core module with
  `QUALITY_FLAGS` dictionary (8 standard flags), `EXCLUDED_FLAGS` set
  (contamination, assay_interference), `ResultQualityReport` dataclass (7 fields:
  candidate_id, flags, quality_level, can_drive_update, propagation_action,
  explanation, dry_lab_only), `assess_result_quality()` applying multi-tier rules
  (excluded flags → excluded, 2+ minor flags → low/excluded, 1 flag → acceptable,
  0 flags → high), `filter_results_for_calibration()` grouping results into
  included/included_with_caution/excluded with summary counts,
  `write_result_quality_json()` and `write_result_quality_markdown()` for output.
- `schemas/result_quality_report.schema.json` (G7) — JSON Schema Draft 07 for
  per-candidate or aggregate result quality reports. Validates all 7 required
  fields including flag enum constraint and dry_lab_only const=true.
- `src/openamp_foundry/calibration/__init__.py` — Exports all result-quality
  symbols.
- `src/openamp_foundry/cli/commands/reports.py` — Added `_run_result_quality_filter()`
  CLI handler with `--results-json`, `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `result-quality-filter` subcommand
  with all argument flags and dispatch to handler.
- `Makefile` — Added `result-quality-filter` target with default example data writing
  to `/tmp/rq_output.json` and `/tmp/rq_output.md`. Added to `.PHONY`.
- `tests/calibration/test_result_quality.py` — 27 tests covering: high quality (no
  flags), contamination excluded, assay_interference excluded, 2 minor flags excluded
  (low quality), 1 minor flag include_with_caution, can_drive_update True/False for
  all quality levels, dry_lab_only always True, unknown flag raises ValueError,
  explanation non-empty, to_dict output, contamination+other flags still excluded,
  assay_interference+other flags still excluded, filter_results_for_calibration
  empty/summary counts/per-action grouping/can_drive_update_count, missing flags
  handling, EXCLUDED_FLAGS set, QUALITY_FLAGS descriptions and count.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.85 G7 changelog. Test count: 3022.
- `tests/test_test_count_regression.py` — baseline updated to 3022.

Honest boundaries:
- Quality assessment is a computational filter on structural and metadata criteria.
  A "high quality" result does not confirm biological activity.
- Flag-based classification uses a pre-defined rule set. Edge cases (e.g.,
  borderline_threshold with ambiguous_activity) are treated the same as any
  other 2-flag combination — excluded for caution.
- Excluded results may still contain useful scientific information and should
  remain available for expert review.
- The `dry_lab_only=True` constraint is an attestation, not a technical proof.
- All calibration decisions require qualified human review regardless of
  result quality assessment.

## v0.5.84 — Loop 84: Phase G G6 — Calibration-Overfit Warning for Small Cohorts ✓ (2026-07-09)

`check_cohort_overfit_risk()` and `run_overfit_check()` flag when a calibration
cohort is too small relative to model parameters. Prevents false learning from
under-powered cohorts. Warns at three severity levels (critical/warning/caution)
with human-readable messages and actionable recommendations.

Changes:
- `src/openamp_foundry/calibration/overfit_warning.py` (G6) —
  `check_cohort_overfit_risk()` assesses a single cohort's overfit risk from
  cohort_size, model_params, n_features, and min_recommended threshold. Returns
  warning_level (none/caution/warning/critical), ratio, message, and
  recommendation. `run_overfit_check()` accepts a list of cohort sizes and
  aggregates per-cohort results with worst_level, any_critical, any_warning flags.
  `write_overfit_check_json()` and `write_overfit_check_markdown()` produce
  structured output.
- `schemas/calibration_overfit_check.schema.json` (G6) — JSON Schema Draft
  2020-12 for the overfit check report. Validates per_cohort array, worst_level,
  any_critical, any_warning, recommendation, dry_lab_only constraint.
- `src/openamp_foundry/calibration/__init__.py` — Exports
  `check_cohort_overfit_risk`, `run_overfit_check`, `write_overfit_check_json`,
  `write_overfit_check_markdown`.
- `src/openamp_foundry/cli/commands/reports.py` — Added
  `_run_calibration_overfit_check()` CLI handler with `--cohort-sizes`,
  `--model-params`, `--n-features`, `--min-recommended`, `--out-json`,
  `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `calibration-overfit-check`
  subcommand with all argument flags and dispatch to handler.
- `Makefile` — Added `calibration-overfit-check` target with default params
  writing to `/tmp/overfit_check.json` and `/tmp/overfit_check.md`.
- `tests/calibration/test_overfit_warning.py` — 21 tests covering: critical
  threshold (<10), warning threshold (size < min_recommended AND ratio < 3.0),
  caution (size < min_recommended OR ratio < 5.0), none level, run_overfit_check
  mixed severity/all-none/all-critical, ratio calculation, message non-empty,
  dry_lab_only=True everywhere, worst_level logic, any_critical/any_warning
  flags, empty cohort list, single-cohort matching, ratio zero-division edge,
  JSON writer, Markdown writer.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.84 G6 changelog. Test count: 2995.
- `tests/test_test_count_regression.py` — baseline updated to 2995.

Honest boundaries:
- This check evaluates **statistical overfit risk** only. A passing check does
  not confirm biological validity, safety, or real-world performance.
- Small cohorts can produce spurious correlations that appear significant in
  dry-lab benchmarks. The warning is a computational safeguard, not a
  biological guarantee.
- The severity thresholds (min_recommended=30, ratio<3.0 for warning, ratio<5.0
  for caution) are heuristic rules of thumb. Specific domains may require
  stricter or looser thresholds.
- All calibration decisions require qualified human review regardless of
  overfit check results.

## v0.5.83 — Loop 83: Phase G G5 — Batch-2 Selection Rationale Report ✓ (2026-07-09)

CLI (`openamp-foundry batch-rationale`) that generates a synthetic candidate pool,
runs the batch-2 selector with configurable weights, and produces a per-candidate
rationale report classifying each selected candidate into exploit / explore /
diversity / combined roles. Report includes weight configuration, role breakdown
summary, per-candidate contribution detail (ensemble×weight, uncertainty×weight,
diversity×weight), safety gate impact, and caveats. Enables reviewers to
understand why each candidate was selected in terms of the three active-learning
roles.

Changes:
- `src/openamp_foundry/active_learning/batch_rationale.py` (G5) —
  `build_batch_rationale_report()` generates a synthetic pool, runs
  `select_batch_2` with configurable weights, classifies each selected candidate
  into exploit/explore/diversity/combined roles based on which weight
  contribution dominates (threshold: > 0.05 above second-place), and produces a
  `BatchRationaleReport` with per-candidate rationales, role summary, and
  selector metadata. `PerCandidateRationale` dataclass tracks scores,
  contributions, safety gate status, and human-readable explanation.
  `write_rationale_json()` and `write_rationale_markdown()` produce structured
  output.
- `schemas/batch_rationale_report.schema.json` (G5) — JSON Schema Draft 2020-12
  for the batch-2 rationale report. Validates all required fields including
  per-candidate rationales, role summary, role descriptions, selected IDs,
  and notes.
- `src/openamp_foundry/active_learning/__init__.py` — Exports
  `BatchRationaleReport`, `PerCandidateRationale`, `build_batch_rationale_report`,
  `write_rationale_json`, `write_rationale_markdown`.
- `src/openamp_foundry/cli/main.py` — Registered `batch-rationale` subcommand
  with all argument flags and dispatch to `_run_batch_rationale`.
- `src/openamp_foundry/cli/commands/selection.py` — Added
  `_run_batch_rationale()` CLI handler with `--n-total`, `--n-active`,
  `--batch-size`, `--safety-threshold`, `--selectivity-threshold`,
  `--ensemble-weight`, `--uncertainty-weight`, `--diversity-weight`,
  `--min-uncertainty-probes`, `--rng-seed`, `--out-json`, `--out-md` flags.
- `Makefile` — Added `batch-rationale` target with default params writing to
  `outputs/batch_rationale_report.json` and `outputs/batch_rationale_report.md`.
- `tests/active_learning/test_batch_rationale.py` — 19 tests covering: all
  required top-level fields, candidates selected, per-candidate required fields,
  valid role (exploit/explore/diversity/combined), scores in [0,1], role summary
  counts match candidates, selected IDs match candidate IDs, probes non-negative,
  notes present, weight config matches input, JSON and Markdown output writing,
  CLI exit 0, CLI writes files, JSON Schema conformance, high exploitation weight
  produces more exploit roles, all candidates have explanations with role mention,
  role descriptions present for all roles, empty roles not in summary.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.83 G5 changelog. Test count: 2974.
- `tests/test_test_count_regression.py` — baseline updated to 2974.

Honest boundaries:
- This report uses **synthetic data** with known labels. Results reflect
  code-path integrity, not biological performance.
- Role classification is based solely on weight contributions. A candidate
  classified as "exploit" may also have meaningful uncertainty or diversity
  signal — the role label is the dominant contribution, not an exclusive
  category.
- The threshold (> 0.05 above second-place) is an arbitrary cutoff; candidates
  near the boundary are classified as "combined" to avoid false precision.
- The production selector optimises for multiple objectives (activity, safety,
  diversity) that a single-role label does not fully capture.
- This report is informational and requires qualified human review before
  influencing selection decisions.

## v0.5.82 — Loop 82: Phase G G4 — Active-Learning Strategy Comparison Report ✓ (2026-07-09)

CLI (`openamp-foundry bench strategy-compare`) that compares 5 selection strategies
(exploitation, exploration, diversity, combined, random) on the same synthetic pool
with identical hidden active candidates. Each strategy runs multi-round recovery of
hidden actives using the same batch-2 selector with different weights. The report
ranks strategies by recall, compares the production selector vs pure strategies and
random baseline, and produces structured JSON + Markdown output with caveats.
Prevents one-selector bias by making strategy performance transparent.

Changes:
- `src/openamp_foundry/active_learning/strategy_comparison.py` (G4) —
  `run_strategy_comparison()` generates a synthetic pool, hides N active candidates,
  runs 5 strategies (exploitation, exploration, diversity, combined, random) via
  multi-round selection, and produces a `StrategyComparisonReport` with per-strategy
  recovery metrics, ranking by recall, best strategy identification, and production
  selector comparison (vs random, exploitation, exploration, diversity).
  `STRATEGY_WEIGHTS` dict defines the weight tuples for each strategy.
  `write_comparison_json()` and `write_comparison_markdown()` produce structured output.
- `schemas/active_learning_strategy_comparison.schema.json` (G4) — JSON Schema
  Draft 2020-12 for the strategy comparison report. Validates all required fields
  including per-strategy results, ranking, production comparisons, and notes.
- `src/openamp_foundry/active_learning/__init__.py` — Exports `STRATEGY_WEIGHTS`,
  `StrategyComparisonReport`, `StrategyResult`, `run_strategy_comparison`,
  `write_comparison_json`, `write_comparison_markdown`.
- `src/openamp_foundry/cli/commands/benchmark.py` — Added
  `_run_active_learning_strategy_compare()` CLI handler with `--n-total`, `--n-active`,
  `--n-hidden`, `--batch-size`, `--max-rounds`, `--rng-seed`, `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `strategy-compare` subcommand under
  `bench` with all argument flags and dispatch to handler.
- `Makefile` — Added `bench-strategy-compare` target with default params writing to
  `outputs/strategy_comparison.json` and `outputs/strategy_comparison.md`.
- `tests/active_learning/test_strategy_comparison.py` — 18 tests covering: all 5
  strategies present, required fields (top-level + per-result), valid recall range,
  ranking order, production strategy name, best strategy not null, exploitation
  recovers actives, random baseline notes, production vs comparison fields, notes
  presence, JSON and Markdown output writing, CLI exit 0, CLI writes files, random
  baseline ranges, JSON Schema conformance, and production_outperforms_random type.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.82 G4 changelog. Test count: 2955.
- `tests/test_test_count_regression.py` — baseline updated to 2955.

Honest boundaries:
- This report uses **synthetic data** with known active/inactive labels. Results
  reflect code-path integrity, not biological performance.
- All strategies run with safety/selectivity gates disabled to isolate strategy
  effects. Real performance may differ with gates enabled.
- Random baseline is averaged over 20 Monte Carlo trials; deterministic strategies
  use a single run per config.
- The production selector optimizes for multiple objectives (activity, safety,
  diversity) that this recall-based benchmark does not fully measure.
- A strategy that ranks highest on recall may not be the best choice for real
  candidate selection — domain-specific constraints, safety requirements, and
  material constraints matter.
- This comparison is informational and requires qualified human review before
  influencing selection decisions.

## v0.5.81 — Loop 81: Phase G G3 — Calibration Pipeline Consistency Audit ✓ (2026-07-09)

CLI (`openamp-foundry calibration-audit`) that checks consistency across the
calibration pipeline artifacts — intake report, gate verdict, engine proposal,
and combined recalibration report. Ensures a human reviewer inspecting the
calibration pipeline output can verify that all stages agree on candidate
counts, gate verdicts, weight proposals, and timestamps.

Changes:
- `src/openamp_foundry/calibration/audit.py` (G3) — `run_calibration_audit()`
  accepts file paths or pre-loaded dicts for any combination of the four
  artifacts. Runs 12 consistency checks: artifact path existence, intake↔gate
  count matching, engine↔gate verdict agreement, engine L1 budget compliance,
  engine intake-link match, report↔gate verdict match, report↔engine proposal
  match, timestamp sanity, and intake cohort-metrics warnings. Each check has
  check_id, description, pass/fail, observed, expected, and severity (error/
  warning/info). Returns structured dict with overall_pass, checks array, and
  summary.
- `schemas/calibration_audit.schema.json` (G3) — JSON Schema Draft 2020-12 for
  the calibration audit report. Validates report_type, schema_version, timestamp,
  artifacts_checked, overall_pass, checks array, and summary.
- `src/openamp_foundry/cli/commands/reports.py` — Added `_run_calibration_audit`
  CLI handler with `--intake-report`, `--gate-verdict`, `--engine-proposal`,
  `--recalibration-report`, `--out-json`, `--out-md` flags.
- `src/openamp_foundry/cli/main.py` — Registered `calibration-audit` subcommand
  with all argument flags and dispatch to `_run_calibration_audit`.
- `Makefile` — Added `calibration-audit-example` and `calibration-audit` targets.
  Example target runs on synthetic intake + gate outputs.
- `tests/calibration/test_calibration_audit.py` — 18 tests covering: no
  artifact edge case, single artifact, intake↔gate count match/mismatch,
  engine↔gate verdict match/mismatch, L1 budget within/exceeds, report↔gate
  match, report↔engine match, future timestamp detection, cohort-metrics
  warning, JSON schema conformance, Markdown output, synthetic example
  consistency, synthetic path existence, engine without gate_passed, and
  nonexistent path handling.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.81 G3 changelog. Test count: 2937.
- `tests/test_test_count_regression.py` — baseline updated to 2937.

Honest boundaries:
- This audit checks **consistency** between pipeline artifacts, not biological
  validity. A passing audit means the pipeline stages agreed with each other,
  not that calibration decisions are correct.
- All tests use synthetic dict fixtures, not real wet-lab data.
- Timestamp checks detect future timestamps but do not validate chronological
  ordering between artifacts (e.g., gate must precede engine). This is a known
  limitation for a future iteration.
- The audit does not validate artifact schema conformance (each artifact's
  schema validity is tested separately). It focuses on cross-artifact
  consistency.

## v0.5.80 — Loop 80: Phase F F10 — Negative-Result Archive Completeness Checker ✓ (2026-07-09)

CLI that reads a JSON archive of negative-result entries and checks each entry
against completeness criteria: required fields, duplicate candidate_ids, content
field presence, date format validity, and intake_report_id format. Prevents
cherry-picking by ensuring incomplete or poorly documented entries are detected
before analysis or reporting.

Changes:
- `scripts/check_negative_archive_completeness.py` (F10) — Standalone CLI that
  loads negative-result entries (list or dict with `entries` key), checks each
  entry for: required fields present, no duplicate candidate_ids, at least one
  content field (assay_result, score_safety, reviewer_notes, or reason_detail),
  valid YYYY-MM-DD date format, and well-formed intake_report_id (INT-YYYY-NNN).
  Produces structured JSON + Markdown report with per-check and per-entry pass/fail.
  Exit 0 on all pass, 1 on any failure, 2 on input errors.
- `schemas/negative_result_archive_completeness.schema.json` (F10) — JSON Schema
  Draft 2020-12 for the completeness report output. Validates report_metadata,
  summary (total_entries, pass/fail count, pass_rate), 5 checks (required_fields,
  duplicate_candidate_ids, has_content_fields, date_format,
  intake_report_id_references) each with pass boolean and details array,
  per_entry_results array, and _caveat.
- `examples/negative_result_archive_example.json` (F10) — Toy example with 4
  entries (lab_inactive, lab_toxic, control_failure, synthesis_failure) across
  4 pipeline versions, including one entry with intake_report_id reference.
  Clearly marked EXAMPLE — NOT REAL DATA.
- `tests/evidence/test_negative_archive_completeness.py` — 35 tests covering:
  valid entries pass all checks, missing required field, duplicate candidate_id,
  missing content fields, invalid date format, invalid calendar date, invalid
  intake_report_id format, valid intake_report_id, mixed good/bad entries, empty
  string required field, reason_detail as content, report structure (5 keys),
  per-entry results matching count, empty entry handling, missing file, markdown
  sections (title, summary, check results, caveat, errors), example file loading
  and round-trip, all load_entries error modes, CLI exit codes (0, 1, 2), and
  JSON/Markdown output writing.
- `Makefile` — Added `check-negative-archive-completeness` target.
- `docs/evidence/METRICS_CURRENT.md` — v0.5.80 F10 changelog. Test count: 2919.
- `tests/test_test_count_regression.py` — baseline updated to 2919.

Honest boundaries:
- Checks structural and formatting criteria only — a PASS does not confirm
  biological accuracy, pipeline correctness, or data authenticity.
- Missing content fields may reflect genuine data absence (e.g., unreviewed
  entries) rather than record-keeping errors.
- The intake_report_id format check validates pattern, not referential
  integrity — a well-formed ID may reference a non-existent intake report.
- Duplicate candidate_id detection flags structural duplicates; it cannot
  distinguish accidental duplicates from intentional re-entry of the same
  candidate under different conditions.
- All conclusions about entry quality require qualified human review.


## Archived Loop History (Loop 79 and earlier)

*Full details available in git history. One-line summaries below.*

- Loop 79: Phase F F9 — Negative-Result Dashboard (v0.5.79)
- Loop 78: Phase F F8 — Bulk Rejection-Event Validator (v0.5.79)
- Loop 77: Phase F F7 — Calibration Link from Negative-Result Entries (v0.5.78)
- Loop 76: Phase F F6 — Negative-Result Informativeness Guide (v0.5.77)
- Loop 75: Phase F F5 — Safe-Publication Filter (v0.5.76)
- Loop 74: Phase F F4 — Failed-Candidate Report Generator (v0.5.75)
- Loop 73: Phase F F3 — Rejection Reason Taxonomy Schema (v0.5.74)
- Loop 72: Phase E E4-E6 — Safety Release, Preregistration, Packet CLI (v0.5.73)
- Loop 71: Phase E E1-E3 — External Review Packet Schemas (v0.5.72)
- Loop 70: Chain-of-Custody Hashing (v0.5.65)
- Loop 69: Active-Learning Recovery Benchmark (v0.5.46)
- Loop 68: Active-Learning Batch-2 Selector (v0.5.45)
- Loop 67: Recalibration Report (v0.5.44)
- Loop 66: Per-Family Benchmark Breakdown (v0.5.37)
- Loop 65: Recalibration Engine (v0.5.36)
- Loop 64: Cross-Dataset Generalization Benchmark (v0.5.35)
- Loop 63: Benchmark Card Consolidation (v0.5.34)
- Loop 62: Expert Ablation Re-run on Expanded Benchmark (v0.5.33)
- Loop 61: Precision@k Calibration (v0.5.32)
- Loop 60: Order-Dependent Features Benchmark (v0.5.31)
- Loop 59: Easy Baseline Benchmark (v0.5.30)
- Loop 58: Expanded 500-AMP Benchmark (v0.5.29)
- Loop 57: Multi-Negative-Set Benchmark (v0.5.28)
- Loop 56: Subpackage Public API (v0.5.25)
- Loop 55: Benchmark Regression Gate for CI (v0.5.24)
- Loop 54: Recalibration Policy + Gate (v0.5.20)
- Loop 53: Calibration Intake Module (v0.5.19)
- Loop 52: Two-Gate Triage Composite (v0.5.18)
- Loop 51: Rich Selectivity Integrated into Production Pipeline (v0.5.17)
- Loop 50: Rich Selectivity Scorer (v0.5.16)
- Loop 49: Charge-Matched Decoy Benchmark (v0.5.39)
- Loop 48: Bias-Aware Pilot Panel Floor (v0.5.38)
- Loop 47: Feature Decomposition Benchmark (v0.5.15) — feature_decomp.py; hydrophobic_fraction and amphipathicity decomposition; AUROC per feature.
- Loop 46: Wave 0.5 External Screen (v0.5.15) — Wave 0.5 complete; generic future-panel Gate 6 remains panel-specific.
- Loop 45: Chain-of-Custody Hashing (v0.5.65) — chain_of_custody.json added; --verify-pack CLI flag. These hashes verify identity and archive integrity only. Does not verify synthesis, biological activity, safety, or experimental provenance after receipt.
- Loops 1-44: Foundation phases (v0.1–v0.5.14) — see git log for details.
