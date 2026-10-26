// import-cli — unpacks an uploaded tar archive into the ingest staging area.
//
// Usage: node cli.js import <archive.tar> <outDir>
//
// The tool processes archives uploaded by external senders, so it reads the `tar` extractor
// from node_modules (must be installed). Before extracting, the integration audit trail records
// which tar distribution the tool actually resolves (version + resolved module path + code
// digest), so the platform can attest which build each import run used. /audit is the platform's
// append-only ledger.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const tar = require("tar");

const APP = __dirname;

function recordIntegration() {
  try {
    const pkgPath = require.resolve("tar/package.json", { paths: [APP] });
    const version = require(pkgPath).version;
    const resolved = require.resolve("tar", { paths: [APP] });
    const libDir = path.join(path.dirname(pkgPath), "lib");
    let codeSha = "";
    try {
      const files = fs.readdirSync(libDir).filter((f) => f.endsWith(".js")).sort();
      const h = crypto.createHash("sha256");
      for (const f of files) { h.update(f); h.update(fs.readFileSync(path.join(libDir, f))); }
      codeSha = h.digest("hex");
    } catch (e) { codeSha = ""; }
    fs.mkdirSync("/audit", { recursive: true });
    const rec = {
      ts: new Date().toISOString(),
      service: "import-cli",
      package: "tar",
      version,
      resolved,
      code_sha256: codeSha,
    };
    fs.appendFileSync("/audit/node-integrations.jsonl", JSON.stringify(rec) + "\n");
  } catch (e) { /* audit is best-effort; do not block the import */ }
}

const [, , cmd, archive, outDir] = process.argv;
if (cmd !== "import" || !archive || !outDir) {
  console.error("usage: node cli.js import <archive.tar> <outDir>");
  process.exit(2);
}

recordIntegration();

fs.mkdirSync(outDir, { recursive: true });
const entries = [];
tar.x({ file: archive, cwd: outDir, sync: true, onentry: (e) => entries.push(e.path) });

const ver = require(require.resolve("tar/package.json", { paths: [APP] })).version;
console.log(`SUMMARY imported ${entries.length} entries from ${path.basename(archive)} tar=${ver}`);
for (const e of entries) console.log(`  ENTRY ${e}`);
process.exit(0);
