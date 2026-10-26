const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const OUT = process.env.REGISTRY_OUT || "/srv/npm-registry";
const REGHOST = process.env.REGISTRY_HOST || "http://npm.internal";
const KEEP = ["7.5.10"];
const LATEST = "7.5.10";

(async () => {
  const tarDir = path.join(OUT, "tarballs");
  fs.mkdirSync(tarDir, { recursive: true });

  cp.execSync(`npm pack ws@${KEEP[0]} --pack-destination ${tarDir}`, {
    stdio: "inherit",
  });

  const full = await (await fetch("https://registry.npmjs.org/ws")).json();
  const versions = {};
  for (const v of KEEP) {
    const meta = JSON.parse(JSON.stringify(full.versions[v]));
    meta.dist.tarball = `${REGHOST}/tarballs/ws-${v}.tgz`;
    versions[v] = meta;
  }
  const packument = {
    _id: "ws",
    name: "ws",
    "dist-tags": { latest: LATEST },
    versions,
    time: {
      modified: full.time.modified,
      created: full.time.created,
      "7.5.9": full.time["7.5.9"],
      "7.5.10": full.time["7.5.10"],
    },
  };
  fs.writeFileSync(path.join(OUT, "ws"), JSON.stringify(packument));
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
