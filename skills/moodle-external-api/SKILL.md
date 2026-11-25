---
name: moodle-external-api
description: "Designs or modifies Moodle LMS external functions and web services. Use for db/services.php, classes/external, parameter and return schemas, legacy ajax.php migration, core/ajax, AJAX registration, REST callers or function-level access checks."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# External API

Build an external function with an explicit and verified data contract.

## Workflow

1. Identify the consumers and transport. Search nearby external functions on the matching Moodle release. Determine which existing service, if any, should expose the function, and whether AJAX exposure is explicitly required.
2. Use the documented namespaced `core_external` API for the pilot branches. Define parameter and return structures, validate inputs, resolve the protected Moodle object, validate its context, and check the required capability before exposing data or making changes. Declaring capabilities in the service metadata does not perform those checks.
3. Register the class in `db/services.php` with a stable function name and the necessary metadata. Keep exposed fields limited to the contract. Check the return value with the External API's documented validation helper and review the version bump for registration changes.
4. Review compatibility for callers when altering parameters, defaults or returned fields. Follow existing project tests and inspect the matching branch if documentation and code differ.

## Migrate legacy browser AJAX

1. Trace each legacy action to its JavaScript callers. Classify it by request payload and behavior. A JSON action is a candidate for an external function. A multipart `FormData` request whose handler reads `$_FILES` needs a file-upload transport.
2. For a JSON action, reuse a suitable function or add one under `classes/external/`. In `execute()`, validate parameters, validate the object's context, and enforce the required capability and ownership or group rules before accessing data. Register the function in `db/services.php` with `'ajax' => true` for browser callers. Preserve existing login requirements.
3. Switch the JavaScript caller to `core/ajax` with `methodname` set to the registered name and `args` matching the parameter schema. Preserve success and error behavior, rebuild assets with the project's tooling, bump the plugin version for service-definition changes, and run the upgrade in the test environment. Remove a legacy action only after checking for remaining supported callers.
4. Keep an existing multipart upload flow in place unless the task includes redesigning file handling. `core/ajax` sends JSON and cannot submit the same request to a handler expecting `$_FILES`. For an in-scope redesign, consider Moodle's form and draft-file APIs for browser uploads and pass a draft item ID to an external function when appropriate. Verify draft ownership and context when processing it.

## Verification

Test allowed, disallowed and invalid inputs with Moodle's testing tools, using the real function and return-schema handling on an isolated site. Verify service registration in the intended transport when available. For an AJAX migration, check the real browser caller and regression-test any multipart upload alongside it.

## Official references

- [External function definitions](https://moodledev.io/docs/5.3/apis/subsystems/external/functions)
- [External function security](https://moodledev.io/docs/5.2/apis/subsystems/external/security)
- [Common plugin files](https://moodledev.io/docs/5.3/apis/commonfiles)
- [AJAX in Moodle 4.5](https://moodledev.io/docs/4.5/guides/javascript/ajax)
- [AJAX in Moodle 5.3](https://moodledev.io/docs/5.3/guides/javascript/ajax)
- [Files in Moodle forms](https://moodledev.io/docs/4.5/apis/subsystems/form/usage/files)
