---
name: moodle-plugin-development
description: "Builds and modifies Moodle LMS plugins, activity modules and subplugins. Use for plugin scaffolding, Frankenstyle names, version.php, component metadata, lifecycle callbacks, settings and parent plugin contracts."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Plugin development

Choose the appropriate plugin type and follow the target branch's component contracts.

## Workflow

1. Establish the component, minimum supported Moodle version, installation location and plugin type. Start with an existing plugin of that type on the target branch. Prefer a specific type when it provides the needed extension point.
2. Use the type's required files and lifecycle in the guides. Keep `version.php` as metadata, use the Frankenstyle namespace for autoloaded classes, and put interface strings in the plugin language file. Keep callbacks required by Moodle in their documented locations.
3. If modifying an activity, inspect add, update and delete behavior, capabilities, course-module context and any related completion, files or backup contracts. If modifying a subplugin, use the parent's `db/subplugins.json` and inspect a sibling subplugin. Check metadata keys and relative paths against the target branch.
4. For new capabilities, external functions or schema changes, review the plugin version bump and corresponding install or upgrade behavior. Use the dedicated access, database and external API skills where available.

## Verification

Install on a disposable site and exercise the changed lifecycle, then run the existing component tests and coding checks. Validate fresh install and prior-version upgrade when altering installation metadata.

## Official references

- [Plugin types](https://moodledev.io/docs/5.3/apis/plugintypes)
- [Common plugin files](https://moodledev.io/docs/5.3/apis/commonfiles)
- [Activity modules](https://moodledev.io/docs/5.3/apis/plugintypes/mod)
- [Subplugin metadata](https://moodledev.io/general/development/tools/metadata)
