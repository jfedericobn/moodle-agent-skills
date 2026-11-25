---
name: moodle-phpunit
description: "Writes and runs Moodle LMS PHPUnit tests. Use for tests under a Moodle component, data generators, advanced_testcase, permissions, external functions and debugging the target branch's test runner."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Phpunit

Verify Moodle server-side behavior with the project's real test conventions.

## Workflow

1. Identify the core branch, component and project test entry point. Inspect Composer, CI and nearby tests for the installed PHPUnit major and invocation. Determine whether a disposable PHPUnit site is already configured.
2. Choose the existing base class appropriate to the test. For database or global state changes use Moodle's isolation conventions, including `resetAfterTest()` where appropriate. Create users, courses and activities with generators inside the test or shared setup.
3. Assert externally observable behavior and cover meaningful boundary cases. For capability-dependent behavior, use users and contexts that reflect the planned roles. Keep data providers independent of Moodle state.
4. Run the smallest affected test first, then the relevant component suite when available. Use the branch's tooling for initialization and never point test setup at a live database.

## Verification

Report the exact test command and outcome. If setup prevents a run, state the missing prerequisite and distinguish authored tests from executed tests.

## Official references

- [Writing Moodle PHPUnit tests](https://moodledev.io/docs/5.3/guides/testing)
- [Moodle testing process](https://moodledev.io/general/development/process/testing)
- [Moodle Docker](https://github.com/moodlehq/moodle-docker)
