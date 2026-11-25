# Authoring a skill

Keep skills focused on developer workflows that an agent can detect, carry out and verify. Put trigger terms in the frontmatter description. Establish version and scope before giving commands, link to official docs and prefer checked-in examples from the target branch. Keep supplementary references within the same skill folder.

Use this prompt when drafting a proposed skill.

```text
Author one portable Moodle Agent Skill for [workflow].
Inputs are [target versions], [official references and core permalinks],
[fixture] and [approved upstream reuse]. Inspect the target checkouts and
verify each version-sensitive API or command. Record source and attribution
for reused material. Mark unresolved facts as unknown.
Produce a concise SKILL.md with triggers, prerequisites, procedure, failure
modes and verification. Add a positive scenario and a boundary case with
concrete checks. Update the catalog and routing guide. State which checks
were executed and which branches or agents remain unverified.
```
