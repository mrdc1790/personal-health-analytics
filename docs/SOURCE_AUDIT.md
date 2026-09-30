# Source audit

## Disclosure and evidence

This public audit contains schema observations only. Personal filenames, hashes, counts, coverage dates, mappings, prose, and findings remain in ignored `private/SOURCE_AUDIT_LOCAL.md`. Facts below come from the available JSON; they do not establish compatibility with all app versions.

| Source | Evidence | Status |
| --- | --- | --- |
| PsychonautWiki Journal | Local Android Journal 15.5 JSON snapshot | Structure inspected; recurring exports not verified |
| Samsung Health | No representative export supplied | Metrics, schemas, IDs, coverage unverified |
| Strava | No representative export supplied | Bulk-export workflow documented; layout unverified |
| HabitShare | Product identified; no export supplied | Export support and layout unverified |
| Health Connect | Official Android documentation | Optional bridge; actual device data unverified |

Planning briefs are requirements, not health exports. The existing analyzer and template are prototypes; private summaries are derived data, not independent sources.

## Journal fields observed

Root fields: `exportSource`, `experiences`, `substanceCompanions`, `customUnits`. Retain unmodeled fields and sections in local source payloads.

| Entity | Observed fields |
| --- | --- |
| Experience | `title`, `text`, `creationDate`, `sortDate`, `isFavorite`, `ingestions`, `location`, `ratings`, `timedNotes` |
| Ingestion | `substanceName`, `time`, `endTime`, `creationDate`, `administrationRoute`, `dose`, `isDoseAnEstimate`, `estimatedDoseStandardDeviation`, `units`, `notes`, `stomachFullness`, `consumerName`, `customUnitId`, `isHiddenInTimeline` |
| Custom unit | `id`, `name`, `creationDate`, `isArchived`, `unit`, `unitPlural`, `note`, `color`, `areTimelinesOfSubcomponentsShown`, `areTolerancesOfSubcomponentsShown`, `halfToleranceInDays`, `zeroToleranceInDays`, `roaInfos`, `doseComponents` |

Ingestion `time` is numeric Unix epoch milliseconds in the snapshot. Audit each timestamp field independently for type, range, nullability, and consistency. Epoch times identify instants but do not recover historical travel timezones. Null end times are valid for point events.

Experience and ingestion objects have no stable exported `id` field in this snapshot. Custom units have source-scoped IDs. Colors do not identify substances. A custom unit can have multiple dose components: preserve product, component, route, formulation, and component assumptions separately. The prototype's single-component conversion is not a general policy.

Preserve `consumerName`; owner-only analysis excludes named other consumers. Retain unknown custom IDs, null doses, raw units, estimate flags, hidden events, and source text. Ratings and timed-note containers exist, but typed inner schemas need populated examples. Empty ratings and unclassified prose do not provide mood scores. User-specific mappings are not published.

The local schema reference in the ignored journal-data checkout provides supporting context; its [upstream schema document](https://github.com/crnvl/journal-data/blob/main/docs/v15-export-schema.md) is a secondary implementation reference, not evidence for absent source data.

## Repeated-export identity

Only one snapshot is available: overlap, revisions, and deletions remain unverified.

- File hashes prevent repeated processing of identical files.
- Timestamp-only matching collapses simultaneous legitimate doses; full-content hashes alone duplicate edited events.
- Retain each source occurrence with its file and JSON location. Use internal IDs and an auditable reconciliation layer; unresolved records must not silently enter analytical totals.
- Validate against overlapping snapshots, an edited event, and identical legitimate occurrences before accepting a reconciliation policy.

## Remaining audits

**Samsung Health:** inventory archive files, metadata/header rows, JSON sidecars, high-resolution samples, units, IDs, source devices, timestamps, revisions, and overlap. Inspect every present metric, explicitly including nutrition and hydration. Sleep stages, resting HR, HRV, and body composition are conditional, not confirmed. Distinguish source summaries from raw observations.

**Strava:** begin with [bulk exports](https://support.strava.com/en-us/articles/15401919-how-do-i-export-my-strava-data). Inspect actual summary and activity formats. Samsung-origin copies must preserve both source records without doubling workout totals. The [developer guide](https://developers.strava.com/docs/getting-started/) currently requires a subscription to create an API app; optional OAuth is deferred.

**HabitShare:** the [official site](https://habitshareapp.com/) establishes the product, not a supported export schema or public API. Verify export availability on the Android installation. Do not promise live sync or scrape private endpoints. Manual CSV fallback: `habit`, `date`, `status`, optional `value`, `unit`, `notes`; statuses `completed`, `not_completed`, `skipped`, `unknown`.

**Health Connect:** [official reading guidance](https://developer.android.com/health-and-fitness/health-connect/read-data) covers pagination, additional history/background permissions, and aggregation for cumulative metrics. Verify Samsung-origin nutrition, hydration, sleep, and activity on-device. Preserve source attribution and keep Samsung exports for unavailable fields.

## Questions for source inspection

- Which IDs survive re-export, editing, and deletion?
- Which fields preserve offsets, and which require timezone assumptions?
- Are nutrition/water records actually populated and transferred?
- What establishes a complete journal day, confirmed non-use, and sufficient sensor coverage?
- Which local substance mappings, medication classifications, travel intervals, and baseline definitions need confirmation?

Missing samples block verified adapter schemas, not publication of this provisional plan.
