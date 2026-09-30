# Proposed data model

## Status and conventions

SQLite is the initial local canonical store; Python performs imports and analysis. This is a proposal, not an implemented migration. Journal field availability is grounded in the [source audit](SOURCE_AUDIT.md); other source mappings remain provisional until actual exports are inspected. Public examples must be synthetic.

Use internal opaque primary keys and explicit foreign keys. Raw payloads remain local. A canonical entity can have multiple source occurrences, and a source occurrence can produce multiple typed entities. Preserve source identifiers as text with source namespace; never assume IDs are globally unique.

Times representing instants use UTC epoch milliseconds. Store original timestamp values, original offset/zone when supplied, precision, timezone-resolution status, and any assumption used. Date-only facts remain dates; do not manufacture midnight timestamps. Missing numeric measurements and doses are SQL `NULL`, never zero. Units must be explicit; retain raw values alongside conversions.

## Provenance and reconciliation

| Proposed table | Minimum fields and relationships |
| --- | --- |
| `source_files` | source namespace, relative private storage path, original filename, SHA-256, byte size, export timestamp if supplied; unique source + hash |
| `import_runs` | source file FK, import time, parser/schema version, status, discovered/imported/quarantined counts, warnings/errors; retries are separately recorded |
| `source_records` | file FK, record locator (JSON path or file/row/sample path), optional source ID, payload hash, original local payload, validation status; unique file + locator |
| `entity_sources` | canonical entity type/key, source record FK, reconciliation decision and version; retains lineage from every accepted entity to raw data |
| `reconciliation_decisions` | candidate entities/records, decision (`match`, `new`, `revision`, `unresolved`), reason, actor, timestamp; no silent destructive merge |
| `quality_issues` | import/record/entity reference, issue code, severity, detail, resolution status |

File-level idempotence does not replace record-level overlap detection. In the journal snapshot, experiences and ingestions lack stable exported IDs. Preserve every occurrence, including identical ones. Reconcile repeated snapshots using occurrence multiplicity and context; treat an exact-content fingerprint as evidence, not a universal entity ID. Creation timestamps are supporting evidence, not guaranteed unique keys. Ambiguous edits or matches remain unresolved and appear in `health doctor`; reports exclude unresolved candidates and disclose the excluded counts. Do not interpret disappearance from a new export as deletion until source behavior is established.

Native stable IDs, if a source provides them, must be scoped to the source and revision policy. Cross-source workout links are separate from within-source deduplication: retain both originals and choose a preferred analytical representation rather than adding their calories/durations together.

## Journal and substance entities: grounded fields

| Proposed table | Fields and intended behavior |
| --- | --- |
| `journal_entries` | internal ID; title, text, creation/sort timestamps, favorite, raw location; source-backed snapshots/revisions; preserve ratings and timed notes pending populated schemas |
| `ingestion_events` | entry FK; time/end/creation timestamps; raw substance name and unit; dose, route, estimate flag/SD, notes, stomach fullness, consumer, hidden flag, raw custom ID; nullable resolved substance/custom-unit version references |
| `custom_unit_versions` | source-scoped exported ID and snapshot/version; names/units, archived flag, creation time, note, color, component/timeline/tolerance configuration and raw `roaInfos` |
| `custom_unit_components` | custom-unit-version FK, ordinal, raw component payload, optional resolved substance/unit and dose; permit multiple components and nested references |
| `substances` | canonical identity, category; retain distinct members of a category |
| `substance_aliases` | raw name/source/custom ID mapping to canonical identity, version, confirmation, validity interval and provenance |
| `journal_ratings`, `journal_timed_notes` | entry FK, ordinal, local raw payload initially; typed fields follow populated-schema inspection |

Do not discard unknown IDs or automatically equate product identity with display grouping. Preserve XR/IR and routes even when grouped for display. Component quantities are user-defined export mappings, not independently verified product strengths. Snapshot mappings do not reconstruct historical strength changes. Incompatible or unresolved units prevent dose aggregation but not event counting.

Preserve other consumers, while all owner analyses filter named other consumers out by default. Hidden timeline events remain analytical records. Notes and experience text are sensitive, user-written observations; they are not validated diagnoses or emotional labels.

## Health and habit entities: provisional source mappings

| Proposed table | Capability and minimum canonical fields |
| --- | --- |
| `health_observations` | metric key, instant/interval, numeric or categorical value, unit, source/device, raw value/unit, precision and quality; high-resolution samples retained |
| `sleep_sessions` | start/end, supplied duration/awake/efficiency metrics, source, primary-sleep/nap classification and method |
| `sleep_stages` | session FK, interval, raw and canonical stage, source; missing stage data is not zero |
| `workouts` | start/end, sport/type, duration/distance/calories/elevation when supplied, origin, optional source ID; location/routes private |
| `workout_links` | candidate workout pair, match method/confidence, confirmation, selected representative; uncertain matches require review |
| `nutrition_entries` | timestamp or source date, meal/item if supplied, amount/unit, source |
| `nutrition_values` | entry FK, nutrient key, amount/unit; preserve calories and macro/micronutrients actually available |
| `hydration_events` | timestamp/date precision, volume and raw unit, source |
| `habits` | local/source-scoped identity, name, schedule/goal metadata, unit, version |
| `habit_observations` | habit FK, source date/instant, completion status, optional value/unit, notes, source; skipped/unknown distinct from failure |
| `coverage_intervals` | source/metric, interval, evidence and coverage status; distinguish device coverage from explicit journaling completeness |

The list describes intended capabilities, not confirmed Samsung/Strava/HabitShare columns. Add adapters only after source audits. Do not infer resting HR from arbitrary HR samples without a separately named, documented estimate. Use either trusted source aggregates or derived nonoverlapping observations for a metric; never sum both. Body measurements fit `health_observations` with explicit units.

Manual habit CSV accepts `habit`, ISO `date`, `status` (`completed`, `not_completed`, `skipped`, `unknown`) and optional `value`, `unit`, `notes`. Blank status stays unknown; invalid dates/statuses are quarantined. Repeated rows require the same provenance and multiplicity treatment as other imports. A HabitShare adapter must map its actual format to this model, not assume it uses these headers.

## Annotation, context, and derived data

| Proposed table | Fields and intended behavior |
| --- | --- |
| `emotional_event_candidates` | entry/source FK, proposed date/instant and precision, type, intensity/duration, trigger, valence, interpersonal flag, model/version/confidence, evidence locator; unconfirmed |
| `emotional_events` | user-created or confirmed annotation; candidate/entry reference, timing, type/intensity/duration, trigger/context, valence, interpersonal flag, annotation source, user confidence and notes, revision history |
| `context_events` | date/interval, tag (workday, festival, travel, illness, conflict, stress, exercise, etc.), annotation source/confidence; no forced extraction from prose |
| `configuration_versions` | definitions of aliases, categories, baseline rules, day boundaries, windows, sleep target, matching and optional half-life assumptions; local configuration content/hash |
| `feature_runs` | input revision, feature implementation/config versions, interval, execution timestamp/status |
| `daily_features`, `sleep_features`, `exposure_features` | date/session/outcome anchor, typed derived values, coverage/completeness, feature-run FK; recomputable outputs |
| `analysis_runs` | question, exploratory/confirmatory designation, population/window/outcome/exposure definitions, configuration/features version, methods, exclusions, results/uncertainty and report path |

Candidate AI annotations never become validated outcomes automatically. An unannotated day is not a confirmed absence of emotional events. Any optional external model receives only a user-selected package; a local AI implementation can operate on local material.

## Time, exposure, and missing-data semantics

- Display defaults to `America/New_York`; preserve known source zones and configured travel intervals. Naive ambiguous/nonexistent DST times require explicit resolution or quarantine. Never silently shift instants.
- Calendar days default to local midnight. A separately configured analysis-day boundary can associate after-midnight events with the prior evening/festival day without changing source timestamps.
- Keep sleep sessions intact across midnight; assign daily summaries to wake date by default, keep naps separate, and anchor pre-sleep exposures to session start. Same-night, next-day, and 48-hour outcomes have separate definitions.
- Exposure windows are `(anchor - window, anchor]`; use elapsed UTC time, not clock-hour subtraction. Support 1/3/6/12/24/48/72 hours and 7 days, plus time since dose, daily frequency/dose, consecutive-use days, and rolling 7/30-day features.
- Sum doses only within compatible substance/route/unit definitions. Exclude unknown doses from numeric sums and report their counts; do not claim known totals are complete totals.
- Baseline membership needs configured exposure rules **and** recording-completeness evidence. No journal record alone cannot establish a strict baseline. Report unknown membership separately.
- Sleep debt uses a configurable target and explicit valid-night coverage; bedtime/wake variability uses circular/time-unwrapped methods. Document every formula before implementation.
- Optional half-life decay is labeled modeled relative exposure, with assumptions/version and compatible units, never measured concentration or effect intensity. Substance complexity measures distinct exposures, not health risk.

## Extension boundary

The broader [experience vision](PERSONAL_EXPERIENCE_VISION.md) may add media entities, live-set occurrences, ratings, playtime snapshots, and read-only planning context later. Shared provenance and time primitives should support them, but do not implement a universal personal-data schema or flatten every experience into one undifferentiated table now. Health storage and public portfolio exports require separate permissions and projections.
