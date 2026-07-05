# Decision Log Template

Use this template when changing `configs/recalibration_policy.yaml` or applying
any human-approved recalibration proposal.

Copy to:

```text
docs/DECISION_LOG_YYYY-MM-DD.md
```

The file must be non-empty and dated within 30 days for
`policy-version-check` to accept a substantive policy edit.

## Decision

- Date:
- Reviewer:
- Policy version before:
- Policy version after:
- Related intake report:
- Related gate verdict:
- Related recalibration proposal:

## Evidence Reviewed

- Cohort size:
- Positive controls:
- Negative controls:
- Orphan predictions/results:
- Metrics available:
- Benchmark regressions checked:

## Change Requested

Describe exactly which rule, threshold, weight, or locked change is being
altered.

## Why This Is Not Cherry-Picking

State why the change follows pre-registered criteria or why the old rule is now
scientifically wrong.

## Safety Review

Confirm that the change does not relax prohibited actions for toxicity,
hemolysis, novelty, pathogen enhancement, or post-hoc success redefinition.

## Decision

- [ ] Approved
- [ ] Rejected
- [ ] Deferred pending more evidence

## Signature

- Reviewer:
- Date:
