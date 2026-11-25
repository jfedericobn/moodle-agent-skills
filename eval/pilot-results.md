# Pilot verification, November 24, 2026

- On `moodle-edge`, the structural validator passed for eight skills and eight scenarios. All five tool tests passed with Python 3.12. The tests installed all eight skills in each of four agent layouts in both scopes, and exercised dry runs, repeated installs, conflicts, selective installation, and triage fixtures.
- A local Codex CLI 0.171.0-alpha.13 app-server skill listing discovered all eight skills after a project install in a temporary Git checkout. This checked discovery without a model run.
- The detector recognized `mod_bigbluebuttonbn` and its core branch from actual Moodle 4.5, 5.1, 5.2 and 5.3 stable-branch source metadata. The probe used version files, component maps and subplugin declarations in disposable directories. This checked source triage.
- All 15 catalog source URLs returned HTTP 200 during verification.

Live discovery in Claude Code, Cursor and VS Code Copilot and paired agent trials against an installed Moodle site remain pending. Structural and discovery results do not establish functional performance gains.
