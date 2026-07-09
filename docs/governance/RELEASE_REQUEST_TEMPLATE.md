# Release Request Template

> **Purpose:** A release request is the formal mechanism for requesting that a
> model, candidate, dataset, evidence packet, or schema be released for external
> use. File one when you have an artifact ready for review and want to initiate
> the release process. All release requests are reviewed by a human reviewer
> before the release is approved.
>
> **When to file:** After the artifact passes the release gate checks
> (`make release-gate-check`) and all required gates are green.
>
> **Who reviews it:** The assigned human reviewer (GitHub handle) — a
> maintainer or domain expert who verifies the request meets all criteria.

---

## Release Request

### Metadata

- **Release ID:** `REL-YYYY-NNN` (auto-assigned)
- **Release type:** (candidate | model | dataset | evidence_packet | schema)
- **Artifact ID:** \_\_\_\_\_\_\_\_\_\_
- **Artifact version:** \_\_\_\_\_\_\_\_\_\_

### Requestor

- **Name:** \_\_\_\_\_\_\_\_\_\_
- **Institution:** \_\_\_\_\_\_\_\_\_\_
- **Date of request:** \_\_\_\_\_\_\_\_\_\_ (YYYY-MM-DD)

### Evidence and safety

- **Evidence level:** \_\_\_\_\_ (1–6, see PROOF_LADDER.md)
- **Dry-lab only:** \_\_\_\_\_ (must be True)
- **Safety review status:** \_\_\_\_\_ (pending | approved | not_required)

### Benchmark comparison

- **Baseline beaten:** \_\_\_\_\_\_\_\_\_\_
- **Summary of comparison:** \_\_\_\_\_\_\_\_\_\_

### Limitations

- **Known limitations:** \_\_\_\_\_\_\_\_\_\_ (must not be empty)

### Use and license

- **Intended use:** \_\_\_\_\_ (research | internal | external_partner | public)
- **Data license:** \_\_\_\_\_\_\_\_\_\_ (must specify)

### Review assignment

- **Human reviewer:** \_\_\_\_\_\_\_\_\_\_ (GitHub handle)
- **Review class:** \_\_\_\_\_ (A | B | C | D)

### Approval

- **Approval status:** \_\_\_\_\_ (pending | approved | rejected | deferred)
- **Review notes:** \_\_\_\_\_\_\_\_\_\_

---

## Review Criteria

The human reviewer checks the following before approving:

1. **Formal completeness** — all required fields are present and valid.
2. **Evidence level honesty** — the claimed evidence level matches the actual
   proof-ladder evidence. Dry-lab-only artifacts are capped at level 4.
3. **Safety review** — if intended use is "public", safety review must be
   `approved` (not `pending`).
4. **Benchmark honesty** — the claimed baseline must actually be beaten. If no
   baseline exists, the request should note this and the evidence ceiling is
   adjusted accordingly.
5. **Limitations documented** — known limitations must be explicitly stated,
   not empty or generic. If there are genuinely no known limitations, state
   "None documented at this time."
6. **Data license valid** — the data license must be a standard open license
   (e.g. CC-BY-4.0, MIT, Apache-2.0) or explicitly documented with
   governance approval.
7. **Review class appropriate** — the review class must match the artifact
   type and intended use:
   - **Class A** — documentation, config, schema-only changes (fast-track)
   - **Class B** — evidence packets, benchmark cards, candidate manifests
   - **Class C** — datasets, models, candidate releases for limited use
   - **Class D** — public releases, safety-significant artifacts
8. **Model releases require class C or D** — model releases must not use
   class A or B.

---

## Process

1. **Submit** — Fill out the template and submit it as a GitHub issue or PR.
2. **Validation** — The release request is automatically validated by
   `openamp-foundry release-request-check` to ensure all required fields
   are present.
3. **Human review** — The assigned human reviewer checks the request against
   the review criteria.
4. **Decision** — The reviewer sets approval status to `approved`, `rejected`,
   or `deferred`. If deferred, review notes explain what must change before
   re-submission.
5. **Release** — Once approved, the maintainer performs the actual release
   (tag, publish, announce, etc.).

### Expected timeline

- **Class A:** 1–2 business days
- **Class B:** 3–5 business days
- **Class C:** 5–10 business days
- **Class D:** 10–15 business days (may require governance board review)

### Escalation

If the release request is not reviewed within the expected timeline, the
requestor may escalate by tagging `@openamp-foundry/maintainers` on the
submission thread with a note about the delay.

---

## Safety constraints

- `dry_lab_only` must always be `True` for dry-lab artifacts. Wet-lab
  releases follow a separate process.
- Public releases require safety review to be `approved`, not `pending`.
- Evidence level 5 or 6 cannot be claimed for dry-lab-only artifacts.
- All releases require human review — no auto-approval.
