---
name: moodle-project-triage
description: "Identifies Moodle LMS checkout layout, core release, plugin component and possible subplugin parents. Use when setting up or inspecting an unfamiliar Moodle repository or deciding which version and tests apply."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance. Python 3.10+ is required for the detector."
---

# Project triage

Collect project facts and distinguish detected metadata from runtime assumptions.

## Workflow

1. Run the bundled `python3 scripts/detect.py <checkout-or-component-path>` using the path to the script inside this installed skill. Supply `--moodle-root <checkout>` when the plugin is maintained separately and the intended core checkout is known.
2. Report the classification, component, target Moodle release or unknown, declared plugin requirements, and paths that support those conclusions. In a standalone plugin, `requires` is the minimum core build rather than the installed version. Recognize multiple components or a partial checkout as uncertainty.
3. Review project instructions, Composer and package scripts, CI workflows and test layout before choosing commands. Found config and scripts are evidence of file presence. Verify the intended dev or test environment separately before running commands that change state.
4. Confirm the actual target when release or plugin placement materially affects the change. Use the metadata map for plugin types and the parent declaration for subplugins.

## Verification

Compare the report to the source files. Confirm that a standalone plugin without a core checkout keeps core release unknown. See the [report contract](references/report.md).

## Official references

- [Plugin and subplugin metadata](https://moodledev.io/general/development/tools/metadata)
- [Moodle 5.1 layout update](https://moodledev.io/docs/5.1/devupdate)
- [Release builds](https://moodledev.io/general/releases)
