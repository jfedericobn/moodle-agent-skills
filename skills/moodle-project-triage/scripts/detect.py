#!/usr/bin/env python3
"""Inspect literal Moodle checkout metadata without bootstrapping a site."""

import argparse
import json
from pathlib import Path
import re

MAX_BYTES = 262_144
TOKEN = re.compile(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\n]*|\#[^\n]*""", re.S)


def metadata(path):
    if not path.is_file() or path.is_symlink():
        return ""
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    return data.decode("utf-8", errors="replace") if len(data) <= MAX_BYTES else ""


def php_literal(text, key):
    # Moodle declares these fields as top-level literals, one per line.
    cleaned = TOKEN.sub(
        lambda match: match[0] if match[0][0] in ('"', "'") else
        re.sub(r"[^\n]", " ", match[0]),
        text,
    )
    match = re.search(
        r"(?m)^\s*" + re.escape("$" + key)
        + r"""\s*=\s*(?:'([^'\n]*)'|"([^"\n]*)"|(\d+(?:\.\d+)?))\s*;""",
        cleaned,
    )
    if match:
        return next(value for value in match.groups() if value is not None)
    return None


def json_object(path):
    try:
        value = json.loads(metadata(path))
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def core_checkout(directory):
    component_map = directory / "lib/components.json"
    if not isinstance(json_object(component_map).get("plugintypes"), dict):
        return None
    for webroot in (directory / "public", directory):
        version_file = webroot / "version.php"
        content = metadata(version_file)
        branch = php_literal(content, "branch")
        if branch and branch.isdecimal():
            return {
                "root": str(directory), "webroot": str(webroot),
                "branch": branch, "release": php_literal(content, "release"),
                "build": php_literal(content, "version"), "version_file": str(version_file),
                "component_map": str(component_map),
            }
    return None


def plugin_checkout(directory):
    version_file = directory / "version.php"
    content = metadata(version_file)
    component = php_literal(content, "plugin->component")
    if not component or not re.fullmatch(r"[a-z][a-z0-9]*_[a-z][a-z0-9_]*", component):
        return None
    plugin_type, name = component.split("_", 1)
    return {
        "root": str(directory), "component": component, "type": plugin_type, "name": name,
        "version": php_literal(content, "plugin->version"),
        "requires": php_literal(content, "plugin->requires"),
        "version_file": str(version_file),
    }


def parent_plugin(plugin, directories, core):
    for directory in directories:
        declaration = directory / "db/subplugins.json"
        values = json_object(declaration)
        if not values or not (parent := plugin_checkout(directory)):
            continue
        for key in ("subplugintypes", "plugintypes"):
            mapping = values.get(key)
            relative = mapping.get(plugin["type"]) if isinstance(mapping, dict) else None
            if not isinstance(relative, str):
                continue
            suffix = Path(relative)
            if suffix.is_absolute() or ".." in suffix.parts:
                continue
            bases = [directory] if key == "subplugintypes" else []
            if key == "plugintypes" and core:
                bases.extend(Path(core[field]) for field in ("webroot", "root"))
            if any(
                (base / suffix / plugin["name"]).resolve() == Path(plugin["root"])
                for base in bases
            ):
                return {"component": parent["component"], "declaration": str(declaration), "key": key}
    return None


def inspect(target, explicit_core=None):
    directories = [target, *target.parents][:12]
    if explicit_core:
        core = core_checkout(explicit_core)
        if not core:
            raise ValueError("The explicit Moodle root has no recognized core metadata")
    else:
        core = next((value for directory in directories if (value := core_checkout(directory))), None)
    plugin = next((value for directory in directories if (value := plugin_checkout(directory))), None)
    parent = None
    if plugin:
        plugin_root = Path(plugin["root"])
        containing_core = (
            core if core and plugin_root.is_relative_to(core["webroot"]) else None
        )
        parent = parent_plugin(plugin, list(plugin_root.parents)[:12], containing_core)
    kind = "subplugin" if parent else "plugin" if plugin else "unknown"
    if not plugin and core and target.is_relative_to(core["root"]):
        kind = "core"
    roots = [target]
    if core:
        roots = [Path(core["root"]), Path(core["webroot"]), *roots]
    if plugin:
        roots.append(Path(plugin["root"]))
    indicators = {
        "composer": "composer.json", "node": "package.json", "config": "config.php",
        "phpunit": "vendor/bin/phpunit", "phpunit_init": "admin/tool/phpunit/cli/init.php",
        "behat_init": "admin/tool/behat/cli/init.php", "component_tests": "tests",
        "github_workflows": ".github/workflows",
    }
    found = {
        label: list(dict.fromkeys(str(base / path) for base in roots if (base / path).exists()))
        for label, path in indicators.items()
    }
    return {
        "schema_version": 1, "target": str(target), "kind": kind, "core": core,
        "plugin": plugin, "parent": parent, "tooling_paths": found,
        "runtime_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--moodle-root", type=Path)
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.is_dir():
        parser.error("target must be an existing directory")
    try:
        report = inspect(target, args.moodle_root.resolve() if args.moodle_root else None)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
