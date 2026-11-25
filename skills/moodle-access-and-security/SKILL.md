---
name: moodle-access-and-security
description: "Reviews and implements Moodle LMS access checks for pages, actions, files and external functions. Use when changing contexts, capabilities, groups, request validation, session keys or output handling."
compatibility: "Moodle LMS 5.3 and 4.5 are pilot targets. Check the target branch before applying version-specific guidance."
---

# Access and security

Preserve Moodle authorization at the point where data is read or changed.

## Workflow

1. Identify each entry point, the actor, the protected object, and the context that owns it. For an activity, derive its context from the actual course module and validate that related records belong to it. Include group or ownership rules when the feature requires them.
2. Apply the entry point's documented authentication and authorization pattern. Ordinary pages and forms use Moodle's login and capability APIs where applicable. External functions follow context validation and capability enforcement under the External API.
3. Use Moodle parameter and form APIs, require sesskey validation for applicable browser state changes, and preserve context-specific formatting and escaping. Use DML placeholders for query values. For file serving, check context, the component file area and access before serving.
4. Review read paths, writes and returned data with the same policy. UI visibility can support usability while the server enforces access independently.

## Verification

Run generated-data tests for an authorized user, an unauthorized user, and a user or object in an unrelated context. Use the target's test environment and report unverified paths.

## Official references

- [Moodle API index](https://moodledev.io/docs/5.3/apis)
- [External function security](https://moodledev.io/docs/5.2/apis/subsystems/external/security)
- [File API](https://moodledev.io/docs/5.3/apis/subsystems/files)
- [Peer review](https://moodledev.io/general/development/process/peer-review)
