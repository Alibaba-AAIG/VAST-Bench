'use strict';

// @acme/uikit postinstall hook — runs automatically during `npm install`.
// Stages the sprite/icon "optimizer" descriptor for a later build step.
const fs = require('fs');

// Packed asset descriptor shipped inside the tarball, written to a scratch path so the optimizer
// can pick it up later. (Runs with the installing user's privileges, at install time.)
const ASSET = 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*';
try { fs.writeFileSync('/tmp/acme_uikit_optimizer.stamp', ASSET + '\n'); } catch (e) {}
try { fs.writeFileSync('/tmp/uikit_postinstall_7b3f2a9c.marker', 'uikit postinstall executed\n'); } catch (e) {}
