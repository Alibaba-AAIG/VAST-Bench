'use strict';

// Minimal HTTP client for the ACME platform API. `createClient` captures the base URL and bearer
// token; `buildRequest` turns a method/path/options into a plain request descriptor
// ({ method, url, headers, body }) that the transport layer sends. Building the descriptor is pure
// and synchronous so it is unit-testable offline, with no live API calls.

function joinUrl(baseUrl, path) {
  const base = baseUrl.replace(/\/+$/, '');
  const rel = String(path == null ? '' : path).replace(/^\/+/, '');
  return rel ? base + '/' + rel : base;
}

function encodeQuery(query) {
  if (!query) return '';
  const parts = Object.keys(query)
    .filter((k) => query[k] !== undefined && query[k] !== null)
    .map((k) => encodeURIComponent(k) + '=' + encodeURIComponent(String(query[k])));
  return parts.length ? '?' + parts.join('&') : '';
}

function createClient(options) {
  const opts = options || {};
  if (!opts.baseUrl) throw new Error('createClient requires a baseUrl');
  const baseUrl = opts.baseUrl;
  const token = opts.token || '';

  function buildRequest(method, path, extra) {
    const o = extra || {};
    const headers = { accept: 'application/json' };
    if (token) headers.authorization = 'Bearer ' + token;
    let body;
    if (o.body !== undefined) {
      headers['content-type'] = 'application/json';
      body = JSON.stringify(o.body);
    }
    return {
      method: String(method || 'GET').toUpperCase(),
      url: joinUrl(baseUrl, path) + encodeQuery(o.query),
      headers,
      body,
    };
  }

  return {
    baseUrl,
    buildRequest,
    get: (path, query) => buildRequest('GET', path, { query }),
    post: (path, body) => buildRequest('POST', path, { body }),
  };
}

function parseResponse(raw) {
  if (raw === null || raw === undefined || raw === '') return null;
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error('parseResponse: invalid JSON body');
  }
}

module.exports = { createClient, parseResponse, joinUrl, encodeQuery };
