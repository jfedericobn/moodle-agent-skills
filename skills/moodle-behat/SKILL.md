---
name: moodle-behat
description: "Writes and runs Moodle LMS Behat acceptance scenarios. Use for .feature files, teacher or student workflows, Behat generators, browser drivers, JavaScript scenarios and reliable selectors."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Behat

Demonstrate user-visible behavior through Moodle's acceptance harness.

## Workflow

1. Find nearby component features, the documented step catalog and the project's execution setup. Confirm the Behat site, its data root, and any browser driver are isolated from live Moodle.
2. Use existing data generator steps and selectors that reflect user-visible behavior. Keep each scenario focused on one outcome. Add a JavaScript tag when browser interaction requires it and add a custom step only when existing steps cannot express the behavior clearly.
3. Check the relevant user roles and expected visible state. Use Moodle's supported synchronization and selectors instead of arbitrary sleep steps.
4. Run the affected feature or scenario with the project's configured runner. Confirm the test demonstrates the regression when practical, and inspect logs or screenshots when the site fails to act as expected.

## Verification

Record the scenario, runner command and outcome. If the browser harness is missing, report that limitation and the setup needed for a valid run.

## Official references

- [Moodle acceptance test entry points](https://moodledev.io/general/development/process/testing)
- [Activity modules](https://moodledev.io/docs/5.3/apis/plugintypes/mod)
- [Moodle Docker](https://github.com/moodlehq/moodle-docker)
