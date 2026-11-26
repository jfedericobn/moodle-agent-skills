# Moodle review checklist

Select checks based on the diff, affected behavior, support policy, and release audience. For security, map applicable controls to the versioned OWASP ASVS 5.0 requirements and use NIST SSDF 1.1 to guide source review and executable verification. Record which controls were examined and what proves them. A scoped review supports a release decision within its stated scope.

## Security and privacy

- Identify actors, protected records, and Moodle contexts for each changed page, action, external function, file, and callback. Verify scoped capabilities, group and ownership rules, and the behavior for a permitted user and a user without access.
- Check input validation, server-side constraints, session and request protections, parameterized database access, and context-aware output. Review legacy AJAX actions and multipart upload paths using the External API skill.
- Review guest and recording access, callback identity, credential and token storage and expiry, file access, and disclosure through errors, logs or client code. Review changes to personal data collection, retention, export, or deletion.
- Review new dependencies and generated assets. Use relevant secret, dependency, and static analysis checks alongside source review. Assign an independent reviewer when a change affects an authentication, authorization, data, or external-service trust boundary.

## Reliability and compatibility

- Confirm the supported version and database matrix. Use the project's Moodle CI, PHPUnit, and Behat checks as applicable. Associate results with the candidate and record the actual environment tested.
- For changes to install metadata or upgrades, compare a fresh installation with an upgrade from a supported prior release containing representative data. Verify schema, data preservation, savepoints and recovery steps.
- Review failure handling, consistency, retries, and duplicate events for scheduled tasks and external services. Check that partial failures preserve expected state and that reporting gives operators enough information to diagnose issues.
- Check backward compatibility of changed API responses, settings, and integrations. Include backup and restore when data lifecycle changes, and bounded work or performance checks when a job, report, or query may scale with site data.

## Release profile

- Moodle core patches follow Moodle's peer review and integration process. For independently released plugins, review the release range before the stable bump and verify the final commit after it.
- Marketplace packages need applicable packaging, license, metadata, and compatibility evidence. Treat Moodle plugin prechecks as evidence for the criteria they exercise.
- Customer or platform-specific releases may require separate sandbox acceptance. Track environment prerequisites and owner verification alongside source findings. An implementation can be complete while acceptance evidence is still pending.

## Examples from prior review patterns

- **BNX:** Check role and context behavior for guest and recording access, reminder task reliability, and subscription behavior. Reopen verification if a version bump also changes upgrade code.
- **BNX Datahub:** Check package readiness, compatibility on the declared databases, and backup and restore. Record which results came from the actual release candidate.
- **USTAPI:** Check API contracts and role restrictions, then separately verify meeting creation and recording readback in a compatible sandbox with its required platform services.

## Review record

Record the baseline and candidate SHAs, component, target releases, review type, findings, and evidence. For each finding capture severity, location, behavior, relevant control, recommended action, and disposition. For each required check, record the result, evidence and owner if still pending. Treat unresolved critical or high findings, failed required checks, and missing required evidence as blockers. Record a maintainer decision for medium findings.
