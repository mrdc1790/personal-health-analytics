# Implementation plan

## Delivery boundary

The first delivery is documentation, sanitization, and public GitHub publication. No full pipeline, live connector, dashboard, Android app, or account-data import is implemented here. Existing prototype files are retained as legacy examples. The [broader experience-app vision](PERSONAL_EXPERIENCE_VISION.md) is a later extension, not a dependency of health ingestion.

## Milestones and acceptance

| Milestone | Deliverable | Acceptance / dependency |
| --- | --- | --- |
| 0. Publish planning repository | README, source audit, proposed model, this roadmap, broader vision; local private audit | Public files contain schema-only source evidence; explicit staged allowlist reviewed; private data excluded; GitHub remote contents verified |
| 1. Complete source inspection | Detailed local inventories and sanitized mappings for journal, Samsung, Strava, HabitShare | Representative files inspected; units, timezones, IDs and observed metrics documented; two overlapping snapshots and edited records available; no invented schemas |
| 2. Database and configuration | Versioned SQLite migrations, provenance and identity model, local mapping/config validation | Synthetic schema/relationship tests; explicit reconciliation rules validated against milestone 1; backup/restore procedure documented |
| 3. Immutable ingestion | Python adapters, validation/quarantine, import manifests, initial CLI | Reimport leaves canonical counts unchanged; overlapping exports preserve legitimate multiplicity; edits/retries/unknown IDs are traceable; raw bytes remain unchanged |
| 4. Unified timeline and quality | Queryable timeline, coverage view, `status`, `validate`, `doctor` | Overnight/DST/date-only behavior verified; owner filter honored; missing metrics visible; cross-source copied workouts do not inflate totals |
| 5. Initial features | Sleep/exposure/activity/nutrition/hydration/habit features | Documented formulas, config versions, precision and coverage; required exposure windows and multiple doses verified; unsupported source metrics remain unavailable |
| 6. Exploratory reports | Timeline, calendar, baseline comparisons, event plots and matrix | Counts and uncertainty displayed; comparisons account for context and completeness; small samples reported as insufficient; monthly report reproducible |
| 7. Emotional/context annotation | Manual editing and optional AI candidate review | Unconfirmed candidates never enter validated outcomes; user edits/rejections retained; no silent classification of journal prose |
| 8. Hypothesis analyses | Sleep/emotion, rebound, combinations and emotional-volatility report | Prespecified versus exploratory questions distinguished; confounders and alternatives documented; lag, dose, matching and sensitivity methods reproducible |
| 9. Local dashboard | Streamlit views for imports, timeline, quality, features and annotations | Uses the same analysis functions as CLI; local binding by default; no external resources/telemetry; synthetic walkthrough and real local QA |
| 10. Recurring workflow and AI export | Inbox sync, optional Windows Task Scheduler, selective AI package | New files discovered/hashed; incomplete copies deferred; imports validated before source archive copy; errors recoverable; exported package reviewed explicitly |
| 11. Optional Android/experience modules | Kotlin Health Connect exporter; media/music/planning extensions | Feature/permission checks on device; revocation handled; adapter samples verified; no automatic medical upload or planning write-back |

Milestones 2 onward require review of the audited source mappings; missing sources must not delay a clearly bounded journal-only implementation if explicitly chosen later. Every added adapter has its own sample/audit acceptance gate.

## Planned interfaces

Use a Python package under `src/`, SQLite migrations, YAML local configuration, reusable analysis/report functions, synthetic fixtures, and a `health` CLI. Documentation separates observed data, derived features, assumptions, and interpretation. Notebook exploration may inform methods but does not replace reproducible functions.

```text
health import journal <file>
health import samsung <directory-or-zip>
health import strava <directory-or-zip>
health import habits <csv>                 # manual contract; HabitShare adapter later
health sync
health status
health validate
health doctor
health timeline --from YYYY-MM-DD --to YYYY-MM-DD
health substance <canonical-name>
health analyze sleep
health analyze emotional-events
health analyze rebound <substance>
health analyze combinations
health report monthly YYYY-MM
health report therapist
health export ai-context --from YYYY-MM-DD --to YYYY-MM-DD
health export ai-context --question emotional-volatility --window 90d
```

These are proposed commands. Start with ingestion/quality commands; do not implement empty commands that imply unsupported capability. Validate inputs and return nonzero exit status for failed imports/invalid arguments; record recoverable row errors and expose them in quality reporting. UI imports must invoke the same services.

Raw data lives outside tracked code (default `data/raw/` or a configured external directory), with inbox, processed database, reports, and exports ignored. Store parser and configuration versions. Manual remapping regenerates derived views without rewriting raw files. Archive only verified successful input copies, retaining immutable originals and a manifest; do not delete the user's export.

## Analytical definitions to implement

- Substance identity and category-level comparisons remain distinct. Exposure windows: 1/3/6/12/24/48/72 hours and 7 days; time since dose, frequency, cumulative known dose, consecutive-use days, days since confirmed substance-free day, rolling 7/30 days, and unique psychoactives over 24/72 hours.
- Sleep: duration, bedtime/wake/midpoint, awake/awakenings/efficiency/stages where supported; configurable 3/7-day debt and 7-day timing/duration variability. Compare subsequent sleep, next-day, and 48-hour outcomes separately.
- Explicit baselines: strict, medication-adjusted, single-substance, polysubstance, post-heavy-use and festival/recovery, each with configurable rules and membership counts. Inadequate logging yields unknown membership.
- Outcomes: sleep, cardiovascular measures actually available, emotional-event rate/intensity, nutrition/hydration and habit adherence. Cross-source duplicates and sensor coverage are resolved before comparing outcomes.
- Start with descriptive statistics and event studies; use within-person matched comparisons by weekday, context, sleep and activity where appropriate. Report unmatched exclusions and avoid matching on an outcome mediator when the question requires a total association.
- Add interpretable lagged regression, block-aware bootstrap/permutation uncertainty, dose-response, and sensitivity analyses only when data support them. Account for autocorrelation, overlapping exposure windows, logging gaps and multiple comparisons; do not report tiny samples as reliable dose-response evidence.
- Treat emotional volatility as a hypothesis. Competing explanations include sleep/circadian disruption, offset/rebound, polysubstance use, baseline sensitivity, relationships, work stress, illness, travel/festival recovery and coincidence. The therapist report states exposure/outcome definitions, sample sizes, effect sizes when meaningful, uncertainty, confounders and alternatives.
- AI context package: `AI_CONTEXT.md`, `daily_features.csv`, `substance_events.csv`, `emotional_events.csv`, `sleep.csv`, `DATA_DICTIONARY.md`; include coverage, aliases, missing-data conventions, baseline rules and causal limits. Strip identifying fields/prose/location by default; write locally for explicit user review.

Do not assign universal adequate-sleep targets, heavy-use thresholds, medication statuses, dose bins, minimum sample sufficiency, or drug half-lives from the brief. Document and configure these before the corresponding analysis; optional pharmacokinetic estimates remain separately labeled models.

## Test and review strategy

| Area | Required scenarios |
| --- | --- |
| Import identity | Same file twice, renamed identical file, overlapping exports, edits, disappeared records, duplicate source IDs, legitimate identical doses, simultaneous distinct doses, retry after failure |
| Schema/data quality | Unknown custom IDs, multiple/nested components, incompatible units, missing doses/times, malformed JSON, absent metrics, high-resolution sidecars, named other consumers, hidden events |
| Time/features | DST fall/spring boundaries, naive ambiguous timestamps, travel, overnight sleep, naps, midnight/festival boundaries, exact exposure-window endpoints, multiple doses, unknown history |
| Cross-source summaries | Samsung-to-Strava copied workout, uncertain workout match, overlapping cumulative steps, raw-plus-source aggregate conflict, missing-versus-zero nutrition/hydration/habits |
| Analysis/annotations | Sparse groups, baseline completeness unknown, autocorrelated data, multiple outcomes, candidate rejection/confirmation, unannotated outcome days, reproducibility after remapping |
| Operations/privacy | Private files ignored, secrets absent, archive hash preserved, partial inbox file deferred, backup restore, report provenance, default AI redaction, Android permission denial/revocation |

Tests begin with synthetic fixtures; real inputs remain local. For this documentation-only delivery, run existing synthetic prototype tests, verify document links and status claims, inspect all staged content, and compare the remote commit and file inventory after push. Future CI uses synthetic data only and must not publish reports from private runs.

## Publication and defaults

Target: public `mrdc1790/personal-health-analytics`, initial branch `main`. Preserve the existing workspace and legacy code; move personal findings to ignored storage. Stage only README, ignore rules, reviewed prototype/test files, and the four public documents. Authenticate the CLI, create the remote, push, then verify visibility, commit identity and remote file tree. Stop after this delivery for document review.

Defaults: Windows, Python, SQLite, local Streamlit, `America/New_York` display, midnight calendar day, sleep assigned to wake date, no telemetry/cloud uploads/subscription dependency. Optional integrations never imply automatic writes to calendars, tasks, social accounts, or ChatGPT Health.
