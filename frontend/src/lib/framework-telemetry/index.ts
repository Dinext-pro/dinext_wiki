// Vendored from frappe `develop` `ui/src/telemetry` (frappe/frappe#41671).
// `@framework/ui` is not on npm and `frappe/ui` exists only on Frappe develop.
// Dinext runs Wiki on Frappe v15, so the SPA cannot link `../../frappe/ui`.
// `fetchBootConfig` already returns {} when the v16 boot method 404s.
//
// Product telemetry for Frappe SPAs. Moved here from `frappe-ui/frappe` — the
// plugin reads its config from a Frappe backend method, so it belongs above
// frappe-ui rather than inside it.
//
// `telemetryPlugin` was frappe-ui's *default* export from `telemetry/index.ts`,
// but consumers only ever saw the re-exported name, so it is a plain named
// export here.
export { telemetryPlugin, useTelemetry } from "./telemetry";
export type { TelemetryPluginOptions } from "./telemetry";
// Referenced by `TelemetryPluginOptions.getContext` / `.anonymousMode`, so a
// consumer cannot write those options without them.
export type { PulseAnonymousMode, PulseContext } from "./pulse";
