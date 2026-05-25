import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const envText = readFileSync(resolve(root, ".env"), "utf8");
const env = {};

for (const rawLine of envText.split(/\r?\n/)) {
  const line = rawLine.trim();
  if (!line || line.startsWith("#") || !line.includes("=")) continue;
  const index = line.indexOf("=");
  const key = line.slice(0, index).trim();
  let value = line.slice(index + 1).trim();
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    value = value.slice(1, -1);
  }
  env[key] = value;
}

for (const key of ["SFTP_HOST", "SFTP_USERNAME", "SFTP_PASSWORD"]) {
  if (!env[key]) {
    console.error(`[fatal] missing ${key} in root .env`);
    process.exit(2);
  }
}

const batchFile = resolve(
  root,
  "npcwoods-website/scripts/deploy-affordable-arizona-2026-05-16.sftp",
);
const args = [
  "-e",
  "/usr/bin/sftp",
  "-o",
  "StrictHostKeyChecking=no",
  "-P",
  env.SFTP_PORT || "22",
  "-b",
  batchFile,
  `${env.SFTP_USERNAME}@${env.SFTP_HOST}`,
];

const result = spawnSync("/opt/homebrew/bin/sshpass", args, {
  cwd: root,
  env: { ...process.env, SSHPASS: env.SFTP_PASSWORD },
  encoding: "utf8",
});

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
process.exit(result.status ?? 1);
