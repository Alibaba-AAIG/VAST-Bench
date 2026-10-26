#!/usr/bin/env node
'use strict';

// logfmt CLI: turn --key value flags into a single logfmt line.
//   $ logfmt --level info --msg "hello world" --service api
//   level=info msg="hello world" service=api
const parseArgs = require('minimist');
const { formatRecord } = require('../lib/format');

const argv = parseArgs(process.argv.slice(2));
delete argv._;
process.stdout.write(formatRecord(argv) + '\n');
