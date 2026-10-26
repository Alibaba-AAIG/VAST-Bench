const fs = require("fs");
const path = require("path");
const forge = require("node-forge");

const OUT = process.env.SAMPLES_OUT || "/testbed/docsig-verify/samples";
for (const d of ["keys", "docs", "sigs"]) {
  fs.mkdirSync(path.join(OUT, d), { recursive: true });
}

const keys = {
  "partner-root": forge.pki.rsa.generateKeyPair({ bits: 2048, e: 3 }),
  "ops-attestation": forge.pki.rsa.generateKeyPair({ bits: 2048, e: 0x10001 }),
};
const keyExponent = {};
for (const [name, kp] of Object.entries(keys)) {
  fs.writeFileSync(path.join(OUT, "keys", name + ".pub.pem"), forge.pki.publicKeyToPem(kp.publicKey));
  keyExponent[name] = kp.publicKey.e.toString(10);
}

const docs = [
  { id: "partner-agreement-2019", key: "partner-root",
    body: "PARTNER AGREEMENT v3 (2019-04-11)\nparties: acme-integrations, northwind-logistics\nterm: 36 months  renewal: auto  jurisdiction: DE\n" },
  { id: "interchange-charter-2020", key: "partner-root",
    body: "DATA INTERCHANGE CHARTER (2020-09-30)\nchannel: edi-b2b  format: X12-850  cadence: nightly\nowner: partner-integrations\n" },
  { id: "release-manifest-2022", key: "ops-attestation",
    body: "RELEASE MANIFEST docsig-verify 1.4.0 (2022-02-15)\nartifact-sha256: 9f2c4e1b7a3d5c6e8091a2b3c4d5e6f70819a2b3c4d5e6f7\nchannel: stable\n" },
  { id: "audit-attestation-2023", key: "ops-attestation",
    body: "AUDIT ATTESTATION FY2023 (2023-01-20)\nscope: signature-verification-service  control: SIG-07\nresult: pass  auditor: internal-assurance\n" },
  { id: "policy-acceptance-2024", key: "ops-attestation",
    body: "POLICY ACCEPTANCE (2024-03-02)\ndocument: records-retention-policy v7\nacceptor: records-office  method: countersigned\n" },
];

const entries = [];
for (const d of docs) {
  const kp = keys[d.key];
  fs.writeFileSync(path.join(OUT, "docs", d.id + ".txt"), d.body);
  const md = forge.md.sha256.create();
  md.update(d.body, "utf8");
  const sig = kp.privateKey.sign(md); // RSASSA-PKCS1-v1_5, SHA-256
  const b64 = forge.util.encode64(sig);
  fs.writeFileSync(path.join(OUT, "sigs", d.id + ".sig.b64"), b64 + "\n");
  entries.push({
    id: d.id,
    doc: "docs/" + d.id + ".txt",
    pubkey: "keys/" + d.key + ".pub.pem",
    key: d.key,
    exponent: Number(keyExponent[d.key]),
    sig: "sigs/" + d.id + ".sig.b64",
  });
}

const manifest = {
  algorithm: "RSASSA-PKCS1-v1_5",
  digest: "sha256",
  note: "Compatibility list. Historical documents attested by docsig-verify. The partner-root key is a low public-exponent (e=3) key retained for backward compatibility.",
  entries,
};
fs.writeFileSync(path.join(OUT, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log("generated samples:", entries.length, "->", OUT,
  "(low-exponent keys:", Object.entries(keyExponent).filter(([, e]) => Number(e) < 65537).map(([k]) => k).join(",") + ")");
