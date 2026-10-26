'use strict';

// @acme/uikit — minimal shared component library for the checkout frontend.
// Self-contained: requiring this module never depends on the install-time postinstall step.
module.exports = {
  version: '1.2.0',
  Button: function Button(label) { return { tag: 'button', label: label }; },
  Input: function Input(name) { return { tag: 'input', name: name }; },
};
