# Moodle routing guide

Select workflows by intent and file scope. Resolve the target checkout first when version or plugin type could change the outcome.

- `moodle-router` coordinates a request with more than one Moodle workflow.
- `moodle-project-triage` identifies mixed or unfamiliar checkouts, core versions and plugin or parent metadata.
- `moodle-plugin-development` covers component architecture, activities, and parent and subplugin contracts.
- `moodle-access-and-security` covers permissions, contexts, state changes, and data exposure.
- `moodle-database-upgrades` covers data access, XMLDB, version bumps and install or upgrade paths.
- `moodle-external-api` covers external functions, service schemas, transports, and migration of legacy `ajax.php` actions to `core/ajax`.
- `moodle-phpunit` covers server behavior, isolated state, generators and role-sensitive tests.
- `moodle-behat` covers user-visible behavior, roles, features and browser checks.

For example, an activity setting exposed through an external function calls for plugin, external API and access guidance. Use PHPUnit for the endpoint behavior and Behat when user-visible flows change. A schema change adds database and upgrade guidance.
