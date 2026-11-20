// Leonida Legend — GTA VI trophy guide entry (Node 22, standard library only).
// The app is the app/ folder beside this file: plain static files a browser opens
// at app/index.html, fully offline. This program hands the entry in: it copies
// app/ and screenshots/ to the output directory and writes dossier.json with the
// vendored make.fun library, under the scorer's caps (text 160 KiB, at most 4
// screenshots of 256 KiB, at most 993 files / 48 MiB under app/).
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { cpSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildDossier } from './vendor/makefun-frontend.ts';

const root = fileURLToPath(new URL('.', import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(out, { recursive: true });
cpSync(join(root, 'app'), join(out, 'app'), { recursive: true });

const shotsDir = join(root, 'screenshots');
mkdirSync(join(out, 'screenshots'), { recursive: true });
if (existsSync(shotsDir)) {
  cpSync(shotsDir, join(out, 'screenshots'), { recursive: true });
}

writeFileSync(
  join(out, 'dossier.json'),
  buildDossier(out, {
    text_max_bytes: 163840,
    screenshots: { max: 4, max_bytes: 262144 },
    app_max_files: 993,
    app_max_bytes: 50331648,
  }),
);
