#!/usr/bin/env python3
"""List, validate and install the canonical Moodle Agent Skills pack."""

import argparse
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
TARGETS = {
    "claude": (".claude/skills", ".claude/skills"),
    "codex": (".agents/skills", ".agents/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "vscode": (".github/skills", ".copilot/skills"),
}
NAME = re.compile(r"moodle-[a-z0-9]+(?:-[a-z0-9]+)*")


def catalog():
    return json.loads((ROOT / "catalog.json").read_text())["skills"]


def names():
    return [entry["name"] for entry in catalog()]


def files(directory):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Expected a real directory: {directory}")
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            raise ValueError(f"Unsupported entry: {path}")
        if path.is_file():
            result[path.relative_to(directory)] = path.read_bytes()
    return result


def validate():
    entries = catalog()
    expected = [entry["name"] for entry in entries]
    actual = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())
    if sorted(set(expected)) != actual or len(expected) != len(actual):
        raise ValueError("Catalog and skill directories differ")
    if not actual:
        raise ValueError("No skills found")
    routes = (SKILLS / "moodle-router/references/routes.md").read_text()
    route_names = re.findall(r"(?m)^- `(moodle-[a-z0-9-]+)`", routes)
    if sorted(route_names) != actual:
        raise ValueError("Routing guide does not cover exactly the catalog skills")
    scenarios = ROOT / "eval/scenarios"
    scenario_ids = [entry["scenario"] for entry in entries]
    if sorted(scenario_ids) != sorted(path.stem for path in scenarios.glob("*.json")):
        raise ValueError("Catalog and evaluation scenario files differ")
    for entry in entries:
        name = entry["name"]
        if not NAME.fullmatch(name) or len(name) > 64:
            raise ValueError(f"Invalid skill name: {name}")
        payload = files(SKILLS / name)
        content = payload[Path("SKILL.md")].decode()
        if not content.startswith("---\n") or "\n---\n" not in content[4:]:
            raise ValueError(f"Missing frontmatter in {name}")
        header, body = content[4:].split("\n---\n", 1)
        fields = {}
        for line in header.splitlines():
            key, value = line.split(": ", 1)
            if key in fields:
                raise ValueError(f"Duplicate field {key} in {name}")
            fields[key] = value if key == "name" else json.loads(value)
        if set(fields) != {"name", "description", "compatibility"} or fields["name"] != name:
            raise ValueError(f"Invalid frontmatter for {name}")
        for key, limit in (("description", 1024), ("compatibility", 500)):
            if not isinstance(fields[key], str) or not 0 < len(fields[key].strip()) <= limit:
                raise ValueError(f"Invalid {key} for {name}")
        if len(content.splitlines()) > 500 or "## Verification" not in body:
            raise ValueError(f"Invalid guidance length or verification in {name}")
        if not entry["sources"] or any(f"({url})" not in body for url in entry["sources"]):
            raise ValueError(f"Missing catalog references for {name}")
        for path in payload:
            if path.suffix == ".md":
                for link in re.findall(r"\]\(([^)]+)\)", payload[path].decode()):
                    href = link.split("#", 1)[0]
                    if not href or href.startswith(("https://", "http://")):
                        continue
                    if path.parent / href not in payload:
                        raise ValueError(f"Unpackaged link {link} in {name}/{path}")
        case = json.loads((scenarios / f"{entry['scenario']}.json").read_text())
        if (case["id"] != entry["scenario"] or name not in case["skills"]
                or not set(case["skills"]) <= set(actual)
                or not all(case[field] for field in ("prompt", "checks", "moodle_targets", "setup"))):
            raise ValueError(f"Invalid scenario for {name}")
    return len(entries)


def install(targets, scope, destination, selected, dry_run):
    paths = []
    for target in targets:
        relative = TARGETS[target][scope == "user"]
        for name in selected:
            path = destination / relative / name
            if path.resolve() != path:
                raise ValueError(f"Install path follows a symbolic link: {path}")
            payload = files(SKILLS / name)
            if path.exists():
                if files(path) != payload:
                    raise ValueError(f"Existing skill differs; move it before installing: {path}")
                print(f"Already current: {path}")
            else:
                paths.append((path, payload))
    for path, payload in paths:
        if dry_run:
            print(f"Would install: {path}")
            continue
        # Creating the final directory exclusively prevents overwriting a competing install.
        path.mkdir(parents=True, exist_ok=False)
        try:
            for relative_path, content in payload.items():
                output = path / relative_path
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(content)
        except OSError:
            shutil.rmtree(path)
            raise
        print(f"Installed: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    commands.add_parser("validate")
    installer = commands.add_parser("install")
    installer.add_argument("--agent", choices=[*TARGETS, "all"], action="append", required=True)
    installer.add_argument("--scope", choices=("project", "user"), default="project")
    installer.add_argument("--dest", type=Path, help="Override the project or home root")
    installer.add_argument("--skill", choices=names(), action="append")
    installer.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "list":
            print("\n".join(names()))
        elif args.command == "validate":
            print(f"Validated {validate()} skills and their evaluation scenarios.")
        else:
            targets = list(TARGETS) if "all" in args.agent else list(dict.fromkeys(args.agent))
            default_root = Path.home() if args.scope == "user" else Path.cwd()
            destination = (args.dest or default_root).resolve()
            selected = list(dict.fromkeys(args.skill or names()))
            if "moodle-router" in selected and "moodle-project-triage" not in selected:
                selected.append("moodle-project-triage")
            install(targets, args.scope, destination, selected, args.dry_run)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
