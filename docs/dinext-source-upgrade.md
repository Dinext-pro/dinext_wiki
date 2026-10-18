# Dinext source upgrade

Selected upstream release: [v3.4.0](https://github.com/frappe/wiki/releases/tag/v3.4.0).
Immutable upstream commit: `c2b5daafcf391af6d909a466018feaea686ec448`.
Dinext integration line: `main/v15`.

## Preserved company changes

Retain optional Pulse telemetry on Frappe 15, the robots response hook, production builds without sourcemaps, and compatible desktop-icon migration. Upstream 3.4.0 provides the Satori Open Graph fallback; it supersedes the old preview-only disable guard.

## Verification and activation

Use the existing Dinext validation workflow and the tests/build commands declared by the application. Browser and migration checks must use an isolated Frappe 15 test site with synthetic data. Upstream publication workflows remain disabled.

This source update does not change a running site or deployment manifest. A runtime cutover requires verified backups, the exact accepted fork commit and matching release evidence. Keep the preceding source line available for rollback.
