'use strict';

// Encode a flat record { key: value } into a logfmt line: space-separated key=value pairs, where a
// value containing whitespace, '=' or '"' is double-quoted. This is the wire convention the ACME
// services use for structured logs.

function needsQuote(s) {
  return s === '' || /[\s="]/.test(s);
}

function formatValue(v) {
  if (v === null || v === undefined) return '';
  const s = String(v);
  if (!needsQuote(s)) return s;
  return '"' + s.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}

function formatRecord(record) {
  if (record === null || typeof record !== 'object') {
    throw new TypeError('formatRecord expects an object');
  }
  return Object.keys(record)
    .map((k) => k + '=' + formatValue(record[k]))
    .join(' ');
}

function parseLine(line) {
  const out = {};
  const re = /(\w+)=("(?:[^"\\]|\\.)*"|[^\s]*)/g;
  let m;
  while ((m = re.exec(line)) !== null) {
    let val = m[2];
    if (val.length >= 2 && val.startsWith('"') && val.endsWith('"')) {
      val = val.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
    }
    out[m[1]] = val;
  }
  return out;
}

module.exports = { formatRecord, parseLine, formatValue };
