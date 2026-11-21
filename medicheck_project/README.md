# MediCheck — Field Project-I (24CsDscU3002)

Diagnostic Lab & Home Sample Collection Booking + Management System.
Mass tier = standard walk-in booking. Premium tier = home collection,
priority processing. Stack: **Flask (Python) + PostgreSQL**.

## What's in here, mapped to your workbook

| Workbook Assignment | Files |
|---|---|
| 1. Introduction & Objectives | `docs/MediCheck_Project_Documentation.docx` (Section 1) |
| 2. Requirement Gathering, ER Diagram, Normalized DB | `docs/...docx` (Section 2) + `database/schema.sql` + `diagrams/er_diagram.png` |
| 3. Functional Requirements (queries) | `database/queries.sql` (10 queries) |
| 4. Website (min. 5 pages) | `website/` (Flask app, 6 pages) |
| 5. Data Visualization | `visualization/` (CSV + script + 3 charts, already run) |

The `.docx` in `docs/` is written in the same section order as your
printed workbook — copy the text across, or print it and staple it in.

## Setup — do this yourself before submitting

### 1. Database
```bash
createdb medicheck
psql medicheck -f database/schema.sql
psql medicheck -f database/seed_data.sql
psql medicheck -f database/queries.sql      # screenshot the real output
```

### 2. Website
```bash
cd website
pip install -r requirements.txt
export DB_NAME=medicheck DB_USER=postgres DB_PASSWORD=yourpassword
python3 app.py
# open http://localhost:5000 and screenshot each of the 6 pages
```
Try the flow once end-to-end: book a test on `/book`, then look it up
on `/my-bookings` with the same phone number, then go to `/admin` and
mark it "Report Ready".

### 3. Visualization (already run once — files included)
```bash
cd visualization
python3 visualize.py
```
Re-run it any time; it regenerates the 3 PNGs from `bookings_data.csv`.

### 4. ER Diagram
`diagrams/er_diagram.png` is ready to use as-is. Editable sources are
included too: `er_diagram.mmd` (paste into mermaid.live) and
`er_diagram.dot` (`dot -Tpng er_diagram.dot -o out.png`, or open in
any Graphviz-compatible tool). Redraw in draw.io/Lucidchart instead if
your department expects a specific tool — the entities/relationships
are the same either way.

## What was actually verified vs. what needs your machine

- **Verified**: `schema.sql` + `seed_data.sql` load cleanly with zero
  orphaned foreign keys, and all 10 queries in `queries.sql` return
  correct, non-empty results (checked against an equivalent in-memory
  database, since this environment has no PostgreSQL server).
  `visualize.py` was actually run — the 3 chart PNGs in
  `visualization/` are real output, not mockups.
- **Not verified here (needs your machine)**: the Flask app was
  syntax-checked but not run against a live PostgreSQL connection,
  since no Postgres server is available in this environment either.
  Run it locally per the steps above before you trust it for a demo.

## Do

- Run schema.sql + seed_data.sql on your own Postgres and screenshot
  the real query output — graders check for this.
- Spend 15 minutes on real research (call/visit 1-2 local labs, or
  check their websites) so your "existing system" section reflects
  genuine field observation, per Step 2 of the workbook.
- Be ready to explain every table and every query in your viva —
  examiners often ask you to modify a query live.
- Make it feel like yours: change the name, colors, or add a test
  category relevant to your area.

## Avoid

- Don't submit without running the whole thing once yourself — a
  screenshot of an error looks worse than a late submission.
- Don't memorize queries without understanding joins vs. nested
  subqueries vs. aggregates — that's what gets probed in viva.
- Don't skip the ER diagram just because schema.sql exists — it's
  graded separately.
- Don't claim field-visit research you didn't do.

## Extending it

- Swap `booking_type` choices or `tests` categories for whatever your
  local reference lab actually offers, once you've done your field
  visit.
- Add authentication to `/admin` before calling it "real" — right now
  anyone can reach the staff dashboard, which is fine for a college
  demo but should be flagged in your report as a known limitation.
