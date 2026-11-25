# Evaluating the skills

Each JSON scenario describes a setup, a prompt, target releases and observable checks. The repository validator checks inventory and structure. Execution requires an agent and, for live tasks, a disposable Moodle environment.

1. Pin the Moodle version, agent and model, available tools, project checkout, test fixtures and instructions.
2. Run the same prompt in a clean session without skills, then in a separate clean session with the relevant pack installed. Recreate project and test state before each run.
3. Record activation, functional checks, regressions, permissions where relevant, and applicability to the target version. Keep exact commands and evidence. Repeat across agents and versions where practical.
4. Use a core checkout and representative local plugin or activity. For BigBlueButton, start with a source-level routing scenario in the Moodle activity and isolate any runtime tests from a live conferencing service.

For installation acceptance, use each client to list or explicitly invoke the installed triage skill, verify discovery in a fresh session, run it against the same disposable checkout, and record the client's version and observed paths. Installed files alone establish layout compatibility.

Record results with date, scenario ID, agent and model, Moodle branch and patch, fixture revision, test commands, observed result and remaining limitations.
