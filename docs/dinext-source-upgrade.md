# Dinext source upgrade

Selected upstream release: [v3.4.0](https://github.com/frappe/wiki/releases/tag/v3.4.0).
Immutable upstream commit: `c2b5daafcf391af6d909a466018feaea686ec448`.
Dinext integration line: `main/v15`.

## Preserved company changes

Retain optional Pulse telemetry on Frappe 15, the robots response hook, production builds without sourcemaps, and compatible desktop-icon migration. Upstream 3.4.0 provides the Satori Open Graph fallback; it supersedes the old preview-only disable guard.

## Verification and activation

Use the existing Dinext validation workflow and the tests/build commands declared by the application. Browser and migration checks must use an isolated Frappe 15 test site with synthetic data. Upstream publication workflows remain disabled.

This source update does not change a running site or deployment manifest. A runtime cutover requires verified backups, the exact accepted fork commit and matching release evidence. Keep the preceding source line available for rollback.

## Verification record — 2026-10-18

On the isolated Frappe **15.119.0** site, 100 Markdown tests, 41 permission tests and four compatibility regressions passed. Frozen root/frontend dependencies, the complete root build (including Satori/OG assets) and the bench asset build passed. The Cypress scenario opens a synthetic Wiki space, updates a document and verifies its published reader page.

The selected upstream Satori renderer supersedes the old preview-disable workaround. The existing no-sourcemap policy, telemetry client backport, optional telemetry helpers and robots header hook remain. This does not resolve the separately tracked WIKI-01 production source mismatch.

The repeatable Cypress project lives in this application. Its synthetic-fixture endpoints check `allow_tests`, development/test context and the System Manager role on every call; fixture data uses only reserved test identities. Run it only on a disposable test site.
