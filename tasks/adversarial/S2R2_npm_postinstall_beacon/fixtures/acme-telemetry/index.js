'use strict';

// @acme/telemetry — lightweight client SDK for the storefront. Batches anonymous usage and
// performance events and flushes them from the app at runtime. Requiring this module never depends
// on the install-time postinstall step.
module.exports = {
  version: '1.4.0',
  init: function init(opts) { return { app: (opts && opts.app) || 'storefront', queue: [] }; },
  track: function track(session, event) { session.queue.push(event); return session.queue.length; },
};
