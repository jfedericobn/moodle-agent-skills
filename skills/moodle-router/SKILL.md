---
name: moodle-router
description: "Selects Moodle Agent Skills for work in Moodle LMS core, plugins, subplugins, tests and integrations. Use when a Moodle request spans multiple areas or the project type is unclear."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Router

Load the smallest set of workflows needed for a Moodle development task.

## Workflow

1. Read project instructions and identify the requested outcome and component. Use `moodle-project-triage` when the layout, component, or release is unclear.
2. Route by task intent and the affected files using the [routing guide](references/routes.md). Add access guidance whenever the work changes who can read or write Moodle data. Add the testing workflow appropriate to the observable behavior.
3. Find selected skills by their installed names. If a skill is unavailable, use the matching official documentation, and mention the coverage gap if it affects the outcome.
4. Treat App, Moodle Workplace, live site operations, and BigBlueButton server tasks as separate domains. Route Moodle-side BigBlueButton activity and subplugin changes through the same LMS workflows as other activities.

## Verification

Check that the chosen skills cover the requested change and its verification. Avoid activating Moodle workflows for unrelated PHP repositories.

## Official references

- [Moodle API index](https://moodledev.io/docs/5.3/apis)
- [Plugin types](https://moodledev.io/docs/5.3/apis/plugintypes)
