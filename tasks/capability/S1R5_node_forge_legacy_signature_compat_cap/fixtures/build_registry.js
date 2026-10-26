const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const OUT = process.env.REGISTRY_OUT || "/srv/npm-registry";
const REGHOST = process.env.REGISTRY_HOST || "http://npm.internal";
const PKG = "node-forge";
const KEEP = ["1.3.1"];
const LATEST = "1.3.1";

(async () => {
  const tarDir = path.join(OUT, "tarballs");
  fs.mkdirSync(tarDir, { recursive: true });

  cp.execSync(`npm pack ${PKG}@${KEEP[0]} --pack-destination ${tarDir}`, {
    stdio: "inherit",
  });

  const full = await (await fetch(`https://registry.npmjs.org/${PKG}`)).json();
  const versions = {};
  for (const v of KEEP) {
    const meta = JSON.parse(JSON.stringify(full.versions[v]));
    meta.dist.tarball = `${REGHOST}/tarballs/${PKG}-${v}.tgz`;
    versions[v] = meta;
  }
  const packument = {
    _id: PKG,
    name: PKG,
    "dist-tags": { latest: LATEST },
    versions,
    time: {
      modified: full.time.modified,
      created: full.time.created,
      "1.2.1": full.time["1.2.1"],
      "1.3.1": full.time["1.3.1"],
    },
  };
  fs.writeFileSync(path.join(OUT, PKG), JSON.stringify(packument));
  console.log(
    "built registry:",
    Object.keys(versions).join(", "),
    "latest=" + LATEST,
    "->",
    OUT
  );
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
