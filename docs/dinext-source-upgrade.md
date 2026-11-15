# Dinext source upgrade

Selected upstream release: [v3.5.0](https://github.com/frappe/wiki/releases/tag/v3.5.0).
Immutable upstream commit: `b7d605113248de5faa6f81640fa7a0951c5f8829`.
Dinext integration line: `dinext/main/v15`.

## Preserved company changes

The v15 line retains the optional Pulse helpers and frontend telemetry adapter, the robots response hook, the desktop icon migration guard, and production builds without sourcemaps. The upstream editor, reader, revision and space-permission changes ship with the release.

## Verification and activation

The Dinext acceptance workflow builds the candidate, migrates a disposable Frappe and ERPNext 15 site from the preceding fork revision, and runs the compatibility and browser suites. It reports the tested revision in the run summary. Test fixtures use synthetic records and require an enabled development test site and the System Manager role.

Deployments use an independently verified release and manifest. Upstream publication workflows are archived under `.github/imported-workflows-disabled`.

## Verification record — 2026-10-18

On the isolated Frappe **15.119.0** site, 100 Markdown tests, 41 permission tests and four compatibility regressions passed. Frozen root/frontend dependencies, the complete root build (including Satori/OG assets) and the bench asset build passed. The Cypress scenario opens a synthetic Wiki space, updates a document and verifies its published reader page.

The selected upstream Satori renderer supersedes the old preview-disable workaround. The existing no-sourcemap policy, telemetry client backport, optional telemetry helpers and robots header hook remain. This does not resolve the separately tracked WIKI-01 production source mismatch.

The repeatable Cypress project lives in this application. Its synthetic-fixture endpoints check `allow_tests`, development/test context and the System Manager role on every call; fixture data uses only reserved test identities. Run it only on a disposable test site.
