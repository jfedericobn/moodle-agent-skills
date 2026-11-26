# Implementation plan

## Pilot

1. Maintain one portable catalog and install layout for Claude Code, OpenAI Codex, Cursor, and VS Code Copilot.
2. Deliver eight workflows covering routing, project triage, plugins and subplugins, access, database upgrades, external APIs, PHPUnit, and Behat. Use versioned Moodle documentation and target checkout evidence.
3. Validate metadata and packaged references, and test installation in temporary directories. Exercise triage for legacy and public layouts, standalone plugins, subplugins, and unknown projects.
4. Verify actual skill discovery in each agent. Evaluate with and without the skills on 5.3 and 4.5 using isolated Moodle installs. Publish findings and adjust workflows before calling the pilot stable.

## Review coverage

The pack now includes `moodle-code-review` for source review and security, reliability, and acceptance evidence before a plugin release.

## Expansion

Use pilot results to prioritize privacy, hooks and events, tasks, forms, files, output, backup and restore, frontend, themes, accessibility, plugin CI and release workflows. Use Moodle Docker to reproduce live tests. Consider optional Moodle Playground integration after confirming version and skill format support. Maintain BigBlueButton-specific workflows in a companion pack where applicable.

## Adoption

Agree on maintainers and domain reviewers. Use the pilot and its evaluation results in a discussion with upstream community projects and Moodle maintainers. Record release-specific guidance and compatibility evidence in this repository.
