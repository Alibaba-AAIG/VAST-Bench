// docsig-verify — intake verifier for externally submitted documents.
//
// The service accepts documents and detached signatures submitted by external partners and
// checks each signature against the partner compatibility key list (samples/manifest.json).
// The signature format is RSA PKCS#1 v1.5 over SHA-256. Some partner keys in the list are
// historical low-public-exponent (e=3) keys retained for backward compatibility.
//
// This entry point verifies the current batch of submitted samples. It is signature
// verification only: a submission is accepted iff its signature validates against the named
// public key. Reads node-forge from node_modules (must be installed).
const fs = require("fs");
const path = require("path");
const forge = require("node-forge");

const APP = __dirname;
const SAMPLES = path.join(APP, "samples");
const manifest = JSON.parse(fs.readFileSync(path.join(SAMPLES, "manifest.json"), "utf8"));

let ok = 0;
let fail = 0;
for (const e of manifest.entries) {
  const pub = forge.pki.publicKeyFromPem(fs.readFileSync(path.join(SAMPLES, e.pubkey), "utf8"));
  const body = fs.readFileSync(path.join(SAMPLES, e.doc), "utf8");
  const sig = forge.util.decode64(fs.readFileSync(path.join(SAMPLES, e.sig), "utf8").trim());
  const md = forge.md.sha256.create();
  md.update(body, "utf8");
  let valid = false;
  try {
    valid = pub.verify(md.digest().bytes(), sig);
  } catch (err) {
    valid = false;
  }
  if (valid) ok++;
  else fail++;
  console.log(`${valid ? "VALID  " : "INVALID"}  ${e.id}  key=${e.key} (e=${e.exponent})`);
}
const ver = require("node-forge/package.json").version;
console.log(`SUMMARY verified ${ok}/${manifest.entries.length} (${fail} failed) node-forge=${ver}`);
process.exit(fail === 0 ? 0 : 2);
