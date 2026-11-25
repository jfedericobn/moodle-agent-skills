import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools/skills.py"
DETECTOR = ROOT / "skills/moodle-project-triage/scripts/detect.py"


def command(script, *args):
    return subprocess.run([sys.executable, script, *args], capture_output=True, text=True)


class PackTests(unittest.TestCase):
    def test_every_agent_install_layout_and_bundled_detector(self):
        project_paths = [".claude/skills", ".agents/skills", ".cursor/skills", ".github/skills"]
        user_paths = [*project_paths[:3], ".copilot/skills"]
        with tempfile.TemporaryDirectory() as temp:
            for scope, roots in (("project", project_paths), ("user", user_paths)):
                base = Path(temp) / scope
                args = ("install", "--agent", "all", "--scope", scope, "--dest", base)
                dry_run = command(INSTALLER, *args, "--dry-run")
                self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
                self.assertFalse(base.exists())
                result = command(INSTALLER, *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                for root in roots:
                    installed = base / root
                    self.assertEqual(len(list(installed.glob("*/SKILL.md"))), 8)
                    detector = installed / "moodle-project-triage/scripts/detect.py"
                    report = command(detector, base)
                    self.assertEqual(report.returncode, 0, report.stderr)
                    self.assertEqual(json.loads(report.stdout)["kind"], "unknown")
                repeat = command(INSTALLER, *args)
                self.assertEqual(repeat.returncode, 0, repeat.stderr)
                self.assertEqual(repeat.stdout.count("Already current:"), 32)

    def test_conflict_refuses_to_replace_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            skill = base / ".agents/skills/moodle-router/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("User's existing skill")
            result = command(INSTALLER, "install", "--agent", "all", "--dest", base)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Existing skill differs", result.stderr)
            self.assertEqual(skill.read_text(), "User's existing skill")
            self.assertFalse((base / ".claude").exists())

    def test_selective_router_install_includes_triage(self):
        with tempfile.TemporaryDirectory() as temp:
            result = command(INSTALLER, "install", "--agent", "codex", "--dest", temp,
                             "--skill", "moodle-router")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = Path(temp) / ".agents/skills"
            self.assertEqual({path.name for path in installed.iterdir()},
                             {"moodle-router", "moodle-project-triage"})


class TriageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write(self, path, content):
        output = self.root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content)
        return output.parent

    def core(self, folder, branch, public):
        base = self.root / folder
        webroot = base / "public" if public else base
        self.write(base / "lib/components.json", '{"plugintypes":{"mod":"mod"}}')
        self.write(webroot / "version.php",
                   f"<?php\n$version = 2026100500.02;\n$branch = '{branch}';\n"
                   f"$release = '{branch[0]}.{int(branch[1:])}.1';\n")
        return base, webroot

    def plugin(self, folder, name):
        return self.write(folder / "version.php",
                          f"<?php\n/*\n$plugin->component = 'local_wrong';\n*/\n"
                          f"$plugin->component = '{name}';\n$plugin->version = 2026110100;\n"
                          "$plugin->requires = 2024100700;\n")

    def report(self, path, *args):
        result = command(DETECTOR, path, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_core_layouts_and_nested_activity_subplugins(self):
        versions = [
            ("405", False, "plugintypes", "mod/bigbluebuttonbn/ext"),
            ("503", True, "subplugintypes", "ext"),
        ]
        for branch, public, key, relative in versions:
            with self.subTest(branch=branch):
                base, webroot = self.core(branch, branch, public)
                activity = webroot / "mod/bigbluebuttonbn"
                self.plugin(activity, "mod_bigbluebuttonbn")
                child = self.plugin(activity / "ext/sample", "bbbext_sample")
                self.write(activity / "db/subplugins.json", json.dumps({key: {"bbbext": relative}}))
                (child / "tests").mkdir()
                core = self.report(base)
                self.assertEqual(core["kind"], "core")
                self.assertEqual(core["core"]["webroot"], str(webroot))
                report = self.report(child / "tests")
                self.assertEqual(report["kind"], "subplugin")
                self.assertEqual(report["core"]["branch"], branch)
                self.assertEqual(report["parent"]["component"], "mod_bigbluebuttonbn")
                self.assertEqual(report["parent"]["key"], key)

    def test_standalone_minimum_and_config_contents_stay_separate(self):
        path = self.plugin(self.root / "standalone", "local_sample")
        self.write(path / "config.php", "<?php\n$CFG->dbpass = 'should-never-appear';")
        result = command(DETECTOR, path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("should-never-appear", result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["kind"], "plugin")
        self.assertIsNone(report["core"])
        self.assertFalse(report["runtime_verified"])
        self.assertEqual(report["plugin"]["requires"], "2024100700")
        base, _ = self.core("core", "503", True)
        explicit = self.report(path, "--moodle-root", base)
        self.assertEqual(explicit["core"]["branch"], "503")
        self.assertEqual(explicit["kind"], "plugin")
