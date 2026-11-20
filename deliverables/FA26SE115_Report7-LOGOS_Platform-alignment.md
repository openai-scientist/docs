# FA26SE115 Report 7 — LOGOS Platform alignment audit

Date: 19 November 2026  
Scope: text and requirement baseline only. Diagrams were intentionally not redrawn in this pass.

## Source of truth

The comparison uses the frozen `LOGOS_Platform` specification dated 19 November 2026:

- 12 Platform modules: M01–M12
- 198 catalog features: 115 P0, 75 P1 and 8 P2
- 49 business decisions: Q1–Q49
- 11 Core contracts: C1–C11
- The repository `id-mapping.md` records the historical Report 7 identifiers and explicitly says the migration is not a one-to-one rename.

## Confirmed gaps in the original Report 7

1. **Requirement model and traceability.** Report 7 uses the earlier `FE`, `FR`, `BR`, `NFR` and `SR` scheme and an eight-group Platform model. The current specification uses module ownership M01–M12, feature identifiers F/N, edge cases EC/EN, business rules BR, technical validations TV, cross-system rules XH, decisions Q and Core contracts C. Deprecated requirements can split, move or disappear; they cannot be renamed mechanically.
2. **Roles and tenant boundary.** The old Platform Admin/Data Authority model is not the current access model. The normative actors are Platform Operator, Tenant Admin, Project Manager, Researcher (student) and Reviewer. Data authority is a source-steward responsibility. Tenant isolation is required, and administrative visibility does not grant research-content access.
3. **Project lifecycle and authority.** A Researcher may create a draft, but activation requires an active Project Manager different from the creator. The six authority kinds are scientific commitment, independent review, resource, data use, data release and governance change. An immutable `AuthorityReceipt` is tied to object version/digest, approvers and policy. The specification contains two related controls: M01/F-002 triggers re-authentication when the last authentication is older than five minutes, while PRD NFR-08 and XH-BM-02 require audit evidence within 15 minutes for all six kinds. Report 7 adopts the stricter five-minute runtime trigger; the 15-minute value is an upper evidence bound, not a relaxation. Strong-consistency checks apply for five minutes after a related revocation.
4. **Data governance and release.** Uploaded tables belong in M04 tenant-isolated object storage as immutable file versions with digests. The relational schema contains no data rows. Classification, licence, malware and parse checks precede DataSource/DataVersionRef creation; the uploader is the steward. DataUseGrant and versioned ReleaseReview govern use and export. Preview is capped at 20 rows. Local Node is only for data that remains local; raw rows never enter the Platform, prompts or published artifacts.
5. **Core gateway and run semantics.** M06 is the only Platform-to-Scientific-Core path. Commands are idempotent and carry authority context; events have IDs, aggregate versions and replay information. Exploratory runs are allowed before Lock when labelled and gated. The current control is cancellation only; pause/resume/stop/abandon are not normative. Processing, authority, scientific and release states remain separate and every run ends with its gaps recorded.
6. **Policy, providers and resources.** M08 owns versioned policy/admission snapshots. M09 issues credential leases of at most 60 minutes, keeps secrets out of logs/outputs, and permits only the `reasoning_full` model role for a run. M10 uses credits, effective-dated RateCards, atomic holds, append-only ledger entries, quotas and late-usage adjustment.
7. **Inbox, audit and operations.** M11 is the unified permission-filtered Decision Inbox; external notices expose metadata only and are limited to blocking pinned items and spending items in the first release. M12 owns append-only audit, hash checkpoints, retention, legal hold, deletion evidence, recovery and time-limited support access.
8. **Non-functional baseline.** The current targets are 99.5% monthly availability, RPO 15 minutes, RTO 4 hours with quarterly recovery drills, workspace read p95 ≤500 ms at 100 concurrent users, admission p95 ≤5 seconds, inbox update p95 ≤5 seconds and run timeline p95 ≤2 seconds. The interface is WCAG 2.2 AA and Vietnamese/English. Zero cross-tenant or plaintext-secret leakage is required.

## Changes made to Report 7

The report now contains tracked, normative alignment notices before the Platform, NFR, requirement appendix, design, testing and release-package sections. These notices:

- make the M01–M12/Q1–Q49/C1–C11 baseline authoritative;
- identify the old requirement IDs and diagrams as historical traceability only;
- state the current role, tenant, authority, data, run, resource, notification and audit semantics;
- replace the conflicting NFR baseline with the current measurable targets;
- mark design, test and user-guide sections for regeneration against the aligned baseline.

The existing diagrams, diagram sources and embedded images were not modified. Legacy tables remain visible for traceability and are explicitly non-normative where they conflict with the current specification. A later pass must migrate their IDs and redraw the diagrams from the M01–M12 ownership graph.

## Validation

- OOXML redline validator: passed; all inserted content is tracked.
- Office OOXML schema/relationship validator: passed.
- The source file contained ten duplicate bookmark IDs; the aligned copy repairs only those non-visible anchor IDs so the final DOCX validates.
- LibreOffice conversion and PDF render completed successfully (440 pages); the six alignment notices render in the expected sections.
- No backend source files remain modified; no commit, push or merge was performed.

## Next scope

The next pass is diagram-only: regenerate architecture, ownership, sequence, state, data-boundary and release diagrams from the aligned M01–M12/Q/C baseline, then update the legacy requirement tables and test evidence with the `id-mapping.md` traceability map.
