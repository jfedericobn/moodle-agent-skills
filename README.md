# Moodle Agent Skills

A community pilot of portable development workflows for Moodle LMS, modeled on [WordPress Agent Skills](https://github.com/WordPress/agent-skills). Skills guide an agent through project triage, plugin development, Moodle APIs and testing. They use the open [Agent Skills format](https://agentskills.io/specification).

One set of nine skills supports four agent layouts. The pilot targets Moodle 5.3 LTS and 4.5 LTS. See the [compatibility policy](docs/compatibility.md) for the current evidence.

## Install from a checkout

Python 3.10 or later is required for the installer and project detector. Run the installer on the machine that hosts the agent, or install into a project checkout that the agent can open.

```sh
python3 tools/skills.py list
python3 tools/skills.py install --agent codex --dest /path/to/your/moodle-project
python3 tools/skills.py install --agent all --dest /path/to/your/moodle-project
python3 tools/skills.py install --agent claude --scope user
```

Use `--dry-run` to preview and repeat `--skill` for a subset. Selecting the router also installs triage. Identical installs are skipped. The installer rejects a conflicting existing skill and preserves it. With project scope and no destination, installation uses the current directory. With user scope it uses the current user's home unless explicitly overridden.

| Agent or IDE | Flag | Project path | User path |
| --- | --- | --- | --- |
| Claude Code | `claude` | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |
| VS Code with GitHub Copilot | `vscode` | `.github/skills/` | `~/.copilot/skills/` |

For one agent, install only its target. Some clients read multiple compatible paths, so installing all layouts in a shared checkout may make a skill appear more than once in those clients. You can also copy each entire skill folder manually. Keep bundled scripts and references with their skill.

Agent documentation includes [Claude Code skills](https://code.claude.com/docs/en/skills), [OpenAI's Codex project and user paths](https://developers.openai.com/api/reference/cli), [Cursor skill discovery](https://cursor.com/docs/skills), and [VS Code skill locations](https://code.visualstudio.com/docs/agent-customization/agent-skills).

## Try it

Open the target project in your agent and start a new session. Ask it to use `moodle-project-triage` to identify the component, Moodle target, and available tests. For a multi-step request, ask it to use `moodle-router` to choose the relevant workflows.

```sh
python3 skills/moodle-project-triage/scripts/detect.py /path/to/component
```

For a standalone plugin with a separate Moodle checkout, add `--moodle-root /path/to/moodle`.

## Skill catalog

- [Router](skills/moodle-router/SKILL.md)
- [Project triage](skills/moodle-project-triage/SKILL.md)
- [Plugin and subplugin development](skills/moodle-plugin-development/SKILL.md)
- [Access and security](skills/moodle-access-and-security/SKILL.md)
- [Database and upgrades](skills/moodle-database-upgrades/SKILL.md)
- [External API](skills/moodle-external-api/SKILL.md)
- [PHPUnit](skills/moodle-phpunit/SKILL.md)
- [Behat](skills/moodle-behat/SKILL.md)
- [Code and release review](skills/moodle-code-review/SKILL.md)

See the [implementation plan](docs/PLAN.md), [source and reuse notes](docs/sources.md), [authoring guide](docs/authoring.md), and [evaluation instructions](eval/README.md).

```sh
python3 tools/skills.py validate
python3 -m unittest discover -s tests -v
```

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
