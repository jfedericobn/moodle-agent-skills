---
name: moodle-database-upgrades
description: "Changes Moodle LMS plugin data access, XMLDB schemas and install or upgrade logic. Use for db/install.xml, db/upgrade.php, version.php bumps, backfills, DML or database portability."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Database upgrades

Keep fresh installs and upgrades consistent while preserving existing records.

## Workflow

1. Determine the current plugin version, earliest supported upgrade state and schema dependencies. Separate ordinary data access from schema changes. Use Moodle DML with parameterized values and portable APIs for runtime queries.
2. Use the XMLDB editor and DDL API for schema changes. Update the final schema in `db/install.xml`. For released installations add the matching guarded step in `db/upgrade.php`, any required backfill, the correct component savepoint after success, and a corresponding plugin version bump.
3. Keep upgrade logic compatible with the schema at that step. Avoid application helpers that assume the final schema and preserve records before tightening constraints. Look at the component's previous upgrade steps and avoid editing released steps to implement a new change.
4. For large changes, plan how to bound memory use and verify cost on representative disposable data. Check whether the project's supported databases require separate verification.

## Verification

Compare a fresh install with a prior-version upgrade containing seeded data. Verify schema, data, savepoint behavior and project database coverage.

## Official references

- [Plugin upgrades](https://moodledev.io/docs/5.3/guides/upgrade)
- [Moodle DDL and DML index](https://moodledev.io/docs/5.3/apis)
- [Common files](https://moodledev.io/docs/5.3/apis/commonfiles)
