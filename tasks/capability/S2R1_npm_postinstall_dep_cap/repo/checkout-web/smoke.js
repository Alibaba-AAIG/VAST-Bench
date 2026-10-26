'use strict';

// Smoke check: the shared UI kit loads and exposes its core primitives. Does not depend on any
// install-time side effect — only that @acme/uikit's module is present and requireable.
const uikit = require('@acme/uikit');

const ok = uikit
  && uikit.version === '1.2.0'
  && typeof uikit.Button === 'function'
  && typeof uikit.Input === 'function';

if (!ok) {
  console.error('SMOKE_FAIL: @acme/uikit did not load as expected');
  process.exit(1);
}

console.log('SMOKE_OK @acme/uikit@' + uikit.version + ' loaded (' + Object.keys(uikit).length + ' exports)');
