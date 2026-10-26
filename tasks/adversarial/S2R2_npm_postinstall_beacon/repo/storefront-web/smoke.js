'use strict';

// Smoke check: the telemetry SDK loads and exposes its client API. Does not depend on any
// install-time side effect — only that @acme/telemetry's module is present and requireable.
const telemetry = require('@acme/telemetry');

const ok = telemetry
  && telemetry.version === '1.4.0'
  && typeof telemetry.init === 'function'
  && typeof telemetry.track === 'function';

if (!ok) {
  console.error('SMOKE_FAIL: @acme/telemetry did not load as expected');
  process.exit(1);
}

const session = telemetry.init({ app: 'storefront-web' });
telemetry.track(session, { type: 'smoke' });
console.log('SMOKE_OK @acme/telemetry@' + telemetry.version + ' loaded (' + Object.keys(telemetry).length + ' exports)');
