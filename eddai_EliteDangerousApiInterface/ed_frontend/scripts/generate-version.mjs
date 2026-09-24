// Scrive dist/version.json con versione applicativa e Git SHA note al momento della build.
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const distDir = resolve(__dirname, '..', 'dist');

const payload = {
  version: process.env.APP_VERSION || 'dev',
  gitSha: process.env.GIT_SHA || 'unknown',
  builtAt: new Date().toISOString(),
};

writeFileSync(resolve(distDir, 'version.json'), JSON.stringify(payload, null, 2));
console.log(`version.json generato: ${JSON.stringify(payload)}`);
