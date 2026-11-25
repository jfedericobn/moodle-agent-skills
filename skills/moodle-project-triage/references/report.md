# Triage report, schema version 1

Run against a Moodle checkout or a component directory, or a directory inside either. For a standalone plugin, use an explicit Moodle root when you have the corresponding checkout.

- `kind` is `core`, `plugin`, `subplugin`, or `unknown`.
- `core` records separate repository and web roots, the branch, release, build, and source files. `plugin` records its component, type, version and required minimum core build. Either entry can be null.
- `parent` records the parent component and declaration that established a subplugin relationship. A null parent means the tool did not establish it.
- `tooling_paths` records location evidence. `runtime_verified` is always false for this static probe.

The probe checks the supplied directory and up to eleven ancestors. It does not inventory sibling or nested components. For a workspace with several components, locate each relevant root and run the probe there. It recognizes literal Moodle PHP metadata and intentionally leaves dynamic expressions unknown. Only an explicit root or discovered checkout provides core version evidence. If the explicit checkout differs from the plugin's on-disk parent checkout, run triage on both to confirm the subplugin relationship separately.
