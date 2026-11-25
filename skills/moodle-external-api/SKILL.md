---
name: moodle-external-api
description: "Designs or modifies Moodle LMS external functions and web services. Use for db/services.php, classes/external, parameter and return schemas, AJAX registration, REST callers or function-level access checks."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# External api

Build an external function with an explicit and verified data contract.

## Workflow

1. Identify the consumers and transport. Search nearby external functions on the matching Moodle release. Determine which existing service, if any, should expose the function, and whether AJAX exposure is explicitly required.
2. Use the documented namespaced `core_external` API for the pilot branches. Define parameter and return structures, validate inputs, resolve the protected Moodle object, validate its context, and check the required capability before exposing data or making changes. Declaring capabilities in the service metadata does not perform those checks.
3. Register the class in `db/services.php` with a stable function name and the necessary metadata. Keep exposed fields limited to the contract. Check the return value with the External API's documented validation helper and review the version bump for registration changes.
4. Review compatibility for callers when altering parameters, defaults or returned fields. Follow existing project tests and inspect the matching branch if documentation and code differ.

## Verification

Test allowed, disallowed and invalid inputs with Moodle's testing tools, using the real function and return-schema handling on an isolated site. Verify service registration in the intended transport when available.

## Official references

- [External function definitions](https://moodledev.io/docs/5.3/apis/subsystems/external/functions)
- [External function security](https://moodledev.io/docs/5.2/apis/subsystems/external/security)
- [Common plugin files](https://moodledev.io/docs/5.3/apis/commonfiles)
