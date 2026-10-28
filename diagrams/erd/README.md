# Report 7 Entity Relationship Diagram

[Open the editable ERD](AI-Research-Experimentation-Platform-ERD.drawio) for
**III 3.1.5 Entity Relationship Diagram** in `FA26SE115_Report7.docx`.

The diagram follows the report example's level of visual detail: white rectangles
containing entity names, named relationships, orthogonal connectors and Crow's
Foot cardinalities. This is an **entity-relationship overview of the implemented
Platform with attributes suppressed**. It includes operational entities as well
as research entities because it maps the complete current schema. It is not a
complete logical/physical data model: attributes, data types and PK/FK lists
belong in the report's Database Design section. All rectangles, connectors,
labels and endpoints are native draw.io objects.

## Naming and notation decisions

Entity display names are meaningful singular nouns written consistently in
PascalCase. These are presentation names; database tables retain their original
names. For example, `User` maps to `users`, while `PlatformAdminGrant` maps to
`user_platform_roles`, whose constraint allows only an admin grant. `PI` means
Principal Investigator. A naming map is maintained in `platform_erd.json`, in
each draw.io entity's `data-table` field and in the table below.

Relationship labels are verb phrases read from the referenced parent to the
referencing child. For example, `User owns Project`, `Dataset has DatasetVersion`
and `StageDecision results from PIConsultation`. Stage lineage uses
`StageRun precedes StageRun`; this does not imply reuse of engine state.
They describe data
associations, not process order. The Crow's Foot markers at **both ends** specify
minimum/maximum participation independently of line direction or line style.

This file deliberately chooses the **Information Engineering variant** of
Crow's Foot: a solid line is identifying when the child's FK also participates
in its primary key; a dashed line is non-identifying otherwise. The builder
derives this from source PK membership. Currently there are **3 identifying and
67 non-identifying** relationships. Dash style is not an indicator of
optionality, layer membership or importance. Optionality is shown by the circle
in the endpoint marker. Other ERD tools use other line-style conventions, so
this choice is stated in the diagram legend rather than presented as universal.

The required parent of a child row does not imply that every parent must already
have children. A child minimum of zero is retained when the schema does not
enforce a positive minimum. Application rules beyond these schema constraints
are not silently inferred. `ProjectMembership` remains an associative entity;
no duplicate direct many-to-many link is added between `User` and `Project`.

## Source and coverage

The builder imports only the SQLAlchemy model registry under
`logos/services/management/src/management/`; it does not start the application,
connect to a database or read an environment file. The current source contains
**40 tables and 70 foreign keys**, through Alembic revision `20261022_0048`.
Each entity and connector has source/foreign-key metadata available in its
draw.io XML. There is exactly one rectangle per table; display names are unique
and differ from physical names as shown below.

The draw.io file has two layers:

- **Entities and core relationships**: visible by default, with all 40 entities
  and 54 relationships. Use this view when exporting the report image.
- **Technical provenance relationships**: 16 additional relationships recording
  creators, editors, actors or respondents. Enable it from **View → Layers**
  when checking the complete foreign-key model. These links are retained in
  the editable file and excluded from the default export to keep it legible.

The reference DOCX and the current report are local files under the Git-ignored
`docs/` directory. The report's Entities Description table uses the same 40
singular display names as the diagram and retains its row order; 11 descriptions
were previously corrected against source. The image
placeholder remains available for manual insertion of the exported diagram.

## Reading relationships

Read the relationship verb from the parent entity to the child entity. At each
endpoint the marker states how many instances at that endpoint may relate to one
instance at the other end:

| Marker | Meaning |
|---|---|
| `||` | Exactly one |
| `o|` | Zero or one |
| `o<` | Zero or many |

Required foreign keys give exactly one parent; nullable foreign keys give zero
or one. Children are optional unless the source enforces a minimum. A unique
foreign key gives zero or one child; other foreign keys give zero or many.
Composite constraints are considered where they reduce cardinality:

- `user_platform_roles.user_id` and `project_settings.project_id` are primary
  keys, so a user/project has at most one corresponding record.
- `email_otps` allows only `purpose = 'sign_in'`. Together with
  `UNIQUE(user_id, purpose)`, this gives at most one OTP record per user.
- `platform_settings` restricts its primary key to `id = 1`. There is at most one
  settings record globally, and therefore at most one per last editor.

Do not infer additional relationships from naming alone:

- `research_runs.research_case` is JSON, not an extra entity or FK table.
- `research_contexts` remains a real table for historical runs; its current
  write API is retired.
- Connection provenance in `dataset_versions.source_details` is a JSON snapshot,
  not a FK to `data_connections`.
- `cost_entries.source_id` is a polymorphic source reference, not two declared
  foreign keys to stages and PI consultations.
- Audit/monitoring project, run and worker context fields do not imply database
  FKs. The standalone telemetry tables and `cost_ledger_start` are intentionally
  unconnected; no fictitious relationship is introduced to connect every box.
- Role codes are constrained fields, not a separate `roles` table. Hypotheses,
  plans, data cards and findings are stage artifacts, not extra Platform tables.

## Regenerate and validate

From the documentation repository root:

```bash
python3 diagrams/erd/build_platform_erd.py
python3 diagrams/erd/build_platform_erd.py --check
```

The default source location is the sibling
`../capstone-projects/projects/logos`. Pass `--source-root /path/to/logos` when
using another checkout. That workspace must have its `.venv/bin/python` and
SQLAlchemy dependencies installed. Edit layout/descriptions in
[platform_erd.json](platform_erd.json); the builder derives foreign keys and
cardinalities from source, and fails if the entity inventory or checked
constraints no longer match.

`--check` validates the entity/table naming map, entity/FK coverage, relationship
direction, endpoint cardinalities, identifying/non-identifying strokes, unique
ports, entity/label and label/cardinality-marker overlap, edge/entity
intersections and byte-identical
regeneration. A real draw.io render is also required after layout changes;
syntax and geometry checks alone do not establish visual quality.

## Export for the report

Open the file in draw.io, keep the default layer visible and use **File → Export
as → PNG** (white background, crop to content, 2× or 3× scale). A vector SVG is
also available if the Word version used for the report supports it. Insert the
exported image into the existing Figure 9 placeholder yourself.

PNG/SVG/PDF renders are QA intermediates and are not committed as replacements
for the editable diagram. The previous `conceptual-erd/` files were already
deleted in the user's working tree before this work; the new files do not
restore or overwrite those deletions.

## Entity names and source tables

| Entity displayed in ERD/report | Source table |
|---|---|
| User | `users` |
| PlatformAdminGrant | `user_platform_roles` |
| AuthenticationSession | `auth_sessions` |
| EmailSignInChallenge | `email_otps` |
| GoogleConnectionGrant | `google_connection_grants` |
| Project | `projects` |
| ProjectMembership | `project_memberships` |
| ProjectConfiguration | `project_settings` |
| ProjectFile | `project_files` |
| ProjectIntegration | `project_integrations` |
| IntegrationDelivery | `integration_deliveries` |
| IntegrationCredential | `integration_secrets` |
| Comment | `comments` |
| Notification | `notifications` |
| NotificationPreference | `notification_preferences` |
| EmailNotification | `notification_emails` |
| DataConnection | `data_connections` |
| Dataset | `datasets` |
| DatasetVersion | `dataset_versions` |
| ResearchContext | `research_contexts` |
| ResearchRun | `research_runs` |
| StageRun | `stage_runs` |
| StageDecision | `stage_decisions` |
| RunEvent | `run_events` |
| RunGate | `run_gates` |
| RunArtifact | `run_artifacts` |
| FrameReview | `frame_reviews` |
| PIConsultation | `pi_consultations` |
| PINote | `pi_notes` |
| TokenUsageEntry | `cost_entries` |
| UsageLedgerStart | `cost_ledger_start` |
| SpendingAlert | `spending_alerts` |
| ModelProfile | `model_profiles` |
| PlatformConfiguration | `platform_settings` |
| EngineConfiguration | `engine_settings` |
| AuditEvent | `audit_events` |
| MonitoringEvent | `monitoring_events` |
| MonitoringAlert | `monitoring_alerts` |
| MonitoringCaptureGap | `monitoring_capture_gaps` |
| MonitoringWorkerState | `monitoring_worker_states` |

## Research references

Sources consulted on 2026-10-28; the display style follows the report example,
while these primary sources support the modeling decisions:

- [ER/Studio Object Name Rules](https://docwiki.embarcadero.com/ERStudioDA/193/en/Object_Name_Rules): descriptive singular nouns and a consistent case convention.
- [erwin Entity and Attribute Names](https://ftpdocs.broadcom.com/cadocs/0/CA%20ERwin%20%20Data%20Modeler%20r8%201-ENU/Bookshelf_Files/HTML/Methods/254614.html): name one instance of an entity and define its business meaning.
- [Microsoft Crow's Foot guidance](https://support.microsoft.com/en-gb/visio/create-a-diagram-with-crow-s-foot-database-notation): name relationships with verbs, use both endpoint markers and show each entity once; disconnected entities can exist.
- [draw.io Crow's Foot notation](https://www.drawio.com/docs/tutorials/crows-foot-notation/): circle/bar/foot combine minimum and maximum cardinality; ERD relationships differ from UML or process arrows.
- [ERD Editor relationship documentation](https://docs.erd-editor.io/docs/guide/guides/relationship-editing/): the selected identifying/non-identifying stroke convention and PK/FK interpretation.
- [IBM overview of ER model levels](https://www.ibm.com/think/topics/entity-relationship-diagram): conceptual, logical and physical models have different detail levels. Our name-only schema overview does not claim to replace the full logical/physical design.
