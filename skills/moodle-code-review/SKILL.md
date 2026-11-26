---
name: moodle-code-review
description: "Reviews Moodle LMS core patches, plugins, and subplugins for security, reliability, compatibility, and regressions. Use for peer review, reviewing PRs or release candidates, pre-release checks, Marketplace readiness, or checking whether previous findings are resolved."
compatibility: "Use the component's supported Moodle versions and test matrix. The pack's pilot targets are Moodle 5.3 and 4.5."
---

# Moodle code review

Review the change and its impact. Report evidence-backed findings and the checks that remain outstanding.

## Workflow

1. Establish the scope, component, target versions, and repository instructions. For a patch or PR, review its diff plus surrounding code. For a stable plugin release, compare the intended candidate commit with the previous stable tag for that release line. Confirm both refs before claiming coverage. Review the complete diff, including runtime code, dependencies, schema, build, and packaging changes.
2. Read the [review checklist](references/review-checklist.md) and use the specialist skills for access, external APIs, upgrades, and tests as applicable. Trace changed behavior across callers, contexts, and dependencies. Check previous review records and use them to select regression checks. Verify their status from current code and tests.
3. Run suitable checks in a disposable development environment, or record the exact CI and sandbox evidence provided for the candidate. Use the supported Moodle, PHP, and database combinations. For behavioral changes, examine both expected and failure paths. Document checks that were skipped or could not be verified.
4. Report findings with severity, a file and line, the affected behavior, supporting evidence, and a practical fix or regression check. Mark each as new, recurring, or previously known when that can be established. Provide an independent review checklist for changes to security boundaries. Keep sensitive findings within the project's authorized disclosure process.
5. For a release, state whether the candidate is ready for maintainer sign-off, changes are needed, or required evidence is pending. Report any open high or critical finding and any missing required check as a blocker. Record a maintainer decision for each medium finding before release. If a later bump changes runtime code, schema, or upgrades, review and verify those changes against the final commit. For core patches, follow Moodle's peer review and integration process.

## Verification

Record the component, compared commits, target versions, review scope, test commands or evidence links, and open findings. Distinguish code inspection, recorded test results, and sandbox acceptance. Report approval only when the responsible maintainer has provided it.

## Official references

- [Moodle peer review process](https://moodledev.io/general/development/process/peer-review)
- [Moodle testing process](https://moodledev.io/general/development/process/testing)
- [Moodle plugin code prechecks](https://moodledev.io/general/community/plugincontribution/codeprechecks)
- [OWASP Application Security Verification Standard](https://asvs.owasp.org/)
- [NIST Secure Software Development Framework 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)
