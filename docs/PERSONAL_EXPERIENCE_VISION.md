# Personal experience app: vision and portfolio opportunities

## Product direction

Build a private, local-first record of experiences: books read, films watched/rated, games played, artists ranked, live sets attended, habits, workouts, meals, sleep, and journal context. The shared timeline should help recall and reflect, while each domain retains its own meaning and precision. This repository starts with health analytics; broadening it does not require replacing useful source apps.

Examples below are proposals, not statements about the user's habits, attendance, rankings, or health. No personal spreadsheets or account exports were inspected for this vision. Project-specific column mappings and examples require a separate local source audit; public demonstrations use synthetic data.

## Modules and integration approach

| Module | Initial input | Useful capability | Constraint / evidence |
| --- | --- | --- | --- |
| Music and live experiences | Artist-ranking and sets-seen spreadsheet exports | Attendance history, ranking changes, discovery gaps, event recap | Inspect actual headers and rating scales; repeated sets and artist aliases are distinct cases |
| Films | IMDb ratings/list CSV | Film diary, personal rating patterns, backlog | [IMDb supports ratings export](https://help.imdb.com/article/imdb/track-movies-tv/faq-for-imdb-ratings/G67Y87TFYYP6TWAV); rating date is not automatically watched date |
| Books | Goodreads library export | Reading history, shelves, reading goals | Inspect user export and account export availability; [official moderator guidance](https://help.goodreads.com/s/question/0D5ar00000XtvJ3CAJ/how-do-i-download-my-library-as-a-csv-file); missing read dates stay unknown |
| Games | Manual session log or optional Steam snapshot | Library/playtime trends and experience notes | [Steam IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService) exposes owned/recently played data; cumulative snapshots do not reconstruct exact sessions |
| Health and journal | Audited local exports | Sleep, food, water, exercise and substance associations | No causal/clinical inference; actual coverage and data-quality gates required |
| Habits | Verified HabitShare export or manual CSV | Adherence, routine changes, context | No supported live API assumed |
| Planning | Calendar export/read-only API and Tasks read-only API | Planned-versus-recorded routines and context | Plans are not attendance or completion; OAuth is explicit and optional |
| AI reflection | User-selected local or sanitized context | Recaps, questions, candidate labels and task drafts | Human review, evidence links, no implicit external transfer |

Start with local file imports, not an all-service sync platform. Preserve stable external IDs when supplied, aliases, units/rating scales, time precision, source provenance, and repeated experience occurrences. An artist ranking is preference; a live-set occurrence is attendance; a rating timestamp, task due date, and watch time are different facts.

Use separate private domain modules and export projections. Public music demos should operate on synthetic fixtures and have no access to health databases or private calendar/journal data. A single cross-domain timeline can link entities without copying sensitive fields into every module.

## Solution engineering portfolio projects

These are candidate projects to validate against real spreadsheet formats and target job requirements. Choose one complete workflow before building the whole personal app.

### 1. Artist and live-set explorer — recommended first public demo

**Problem:** rankings and attendance sheets answer separate questions, but linking them can explain what has been explored and what remains on a personal wishlist.

**Workflow:** import two spreadsheets, preview column mappings and data-quality issues, resolve artist aliases, preserve rating scales and repeated set occurrences, then show ranking-versus-attendance and a filterable festival/year/venue timeline. Distinguish missing attendance from a confirmed never-seen status. Optional future lineup import can produce a user-ranked shortlist with transparent reasons, not scrape ticket sites or book events.

**Demo:** synthetic artist names and attendance records, one alias conflict, a repeated set, a date-only record and an incomplete ranking. Show the import-review screen, resolution step and resulting insight in five minutes.

**Engineering evidence:** adapter contracts, entity resolution, provenance, validation, clear UX, recoverable failures, tests and an architecture diagram. Package a problem statement, success measures, limitations, runnable synthetic demo and short walkthrough. This makes technical choices and customer discovery visible without exposing private history.

### 2. Festival planning and reflection

Combine ranked artists, a manually imported lineup and calendar availability to propose a set schedule and recap attended sets. Show schedule conflicts, date/time precision and user preference explanations. Attendance requires confirmation after the event; a calendar booking is insufficient. Health/recovery overlays are optional private views with context and uncertainty, never a public drug-history demo.

### 3. Planned routine versus recorded activity

Compare calendar blocks and task completion with recorded workouts, meals, hydration and sleep coverage. For example, a workout block without sensor data becomes an unresolved plan rather than a failed workout. Surface recurring timing conflicts and offer an editable draft routine. Never infer meal quality or skipped meals from absent food logs.

### 4. Personal experience retrospective

A weekly or monthly timeline of reading, films, games, live music, workouts and user-confirmed journal highlights. AI can draft a recap with citations to local records, identify missing detail and suggest questions. The user chooses domains and removes sensitive context before any external model call. Avoid a universal life score or automatic psychological interpretation.

## Journal, AI, Calendar, and Tasks experiments

- **Event context:** suggest that a journal entry may relate to a concert, travel day or workout; display supporting time/source evidence and request user confirmation of the link.
- **Private weekly reflection:** combine sleep coverage, activity, food/water logging and confirmed habits with selected journal annotations; show what is known and missing before producing a recap.
- **Festival follow-up:** after a confirmed event, prepare a recap prompt or draft reminder to review missing logs. No automatic inference of substances or recovery needs.
- **Food/workout timing:** explore logged meal timing and nutrients relative to workouts and sleep, allowing missing or estimated portions; compare associations with enough context rather than assigning a health score.
- **Planning assistance:** draft a meal-log reminder, reflection task or proposed exercise block from user-defined goals. Show exact task/event text and destination for explicit approval before writing to Google.

Calendar read access and Tasks read access are separate optional permissions. Prefer narrow scopes and preserve revocation behavior; follow official [Calendar authorization](https://developers.google.com/workspace/calendar/api/auth) and [Tasks scopes](https://developers.google.com/workspace/tasks/auth). Calendar all-day events remain dates; task due dates are not proof of execution time. Store tokens outside Git, and do not append journal excerpts to shared calendars/tasks by default.

## Extension sequence and success criteria

1. Complete health source audits and the ingestion/quality foundation.
2. In a separate bounded milestone, inspect the EDM ranking and sets-seen spreadsheet headers locally; publish only a synthetic mapping contract.
3. Build the artist/set explorer as the first complete public demo using shared provenance concepts, with isolated data access.
4. Add IMDb/Goodreads imports and manual game/session records; verify each actual source before typed adapters.
5. Add read-only Calendar/Tasks and optional Steam snapshots, then explicit AI reflection exports. Plan Android after confirming the export bridge is useful.

Success means a traceable, useful personal workflow and a reproducible public demonstration of integration design. It does not mean every service is connected, every experience has a timestamp, or personal health data becomes portfolio material. No job outcome is promised; portfolio value depends on demonstrating the problem, solution, tradeoffs and measurable behavior clearly.
