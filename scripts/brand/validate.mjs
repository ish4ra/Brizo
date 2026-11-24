#!/usr/bin/env node
// Repository validation for Task-001-era content. Exit code 1 on any failure.
//   node validate.mjs
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { Resvg } from '@resvg/resvg-js';
import { PALETTE, PRIMARY_COLORS, REPO, decodePNG, pngInfo, ICNS_TYPES } from './lib.mjs';

const errors = [];
const notes = [];
const fail = (m) => errors.push(m);
const ok = (m) => notes.push(m);
const rel = (p) => path.relative(REPO, p);

const tracked = execSync('git ls-files -co --exclude-standard', { cwd: REPO, encoding: 'utf8' })
  .split('\n').filter(Boolean).filter((f) => !f.includes('node_modules/'));

// 1. Fixed palette must never drift.
const expected = { lightSail: '#6FBCEB', primary: '#1684D1', deepOcean: '#174EA4', bgLight: '#F4F8FC', bgDark: '#0B1220', border: '#D8E5F3', white: '#FFFFFF', text: '#0F172A' };
for (const [k, v] of Object.entries(expected)) if (PALETTE[k] !== v) fail(`palette ${k} is ${PALETTE[k]}, expected ${v}`);
ok('brand palette constants match the approved values');

// 2. Public SVGs: parse, safety, palette.
const ALLOWED = new Set([...Object.values(PALETTE), '#111A2E', '#1E2B44', '#475569', '#A9B8CC', '#C7D9EE', '#24344F'].map((c) => c.toUpperCase()));
const svgs = tracked.filter((f) => f.endsWith('.svg'));
for (const f of svgs) {
  const abs = path.join(REPO, f);
  const src = fs.readFileSync(abs, 'utf8');
  try { new Resvg(src); } catch (e) { fail(`${f}: SVG does not parse (${e.message})`); continue; }
  if (/<script|\son[a-z]+\s*=|javascript:/i.test(src)) fail(`${f}: contains script or event handler`);
  if (/(?:href|src)\s*=\s*"(?:https?:)?\/\//i.test(src) || /@import|url\(\s*['"]?https?:/i.test(src)) fail(`${f}: references external resources`);
  if (/<text[\s>]/.test(src)) fail(`${f}: contains live <text>; outline text for consistent GitHub rendering`);
  for (const c of src.match(/#[0-9a-fA-F]{6}\b/g) ?? []) if (!ALLOWED.has(c.toUpperCase())) fail(`${f}: colour ${c} is not in the brand system`);
  if (f.startsWith('assets/readme/') && src.includes('@keyframes') && !src.includes('prefers-reduced-motion')) fail(`${f}: animated without reduced-motion fallback`);
  // static fallback present and sized like the viewBox
  if (f.startsWith('assets/readme/')) {
    const png = path.join(REPO, 'assets/readme/static', path.basename(f).replace('.svg', '.png'));
    if (!fs.existsSync(png)) fail(`${f}: missing static fallback ${rel(png)}`);
    else {
      const [, w, h] = src.match(/viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/);
      const i = pngInfo(fs.readFileSync(png));
      if (i.width !== Math.round(+w) || i.height !== Math.round(+h)) fail(`${rel(png)}: ${i.width}×${i.height}, expected ${w}×${h}`);
    }
  }
}
ok(`${svgs.length} tracked SVGs parsed, safe, on-palette`);

// 3. Logo geometry must not leak into tracked files while provenance is unresolved.
const master = path.join(REPO, 'branding-private/source/brizo-mark.svg');
if (fs.existsSync(master)) {
  const ds = [...fs.readFileSync(master, 'utf8').matchAll(/\sd="([^"]{40,})"/g)].map((m) => m[1].slice(0, 40));
  for (const f of tracked) {
    if (/\.(png|ico|icns|bmp|webp|woff2?)$/.test(f)) continue;
    const s = fs.readFileSync(path.join(REPO, f), 'utf8');
    for (const d of ds) if (s.includes(d)) fail(`${f}: contains private logo geometry`);
  }
  ok('no private logo geometry in tracked files');
} else ok('private logo master not present (skipped leak check against geometry)');
for (const f of tracked) if (f.startsWith('branding-private/')) fail(`${f}: private branding file is tracked`);
for (const f of tracked) if (/\.(webp|icns|ico|bmp)$/i.test(f)) fail(`${f}: logo-type binary in tracked files`);

// 4. Markdown links & anchors.
const slug = (h) => h.trim().toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/\s/g, '-');
const mds = tracked.filter((f) => f.endsWith('.md'));
let links = 0;
for (const f of mds) {
  const src = fs.readFileSync(path.join(REPO, f), 'utf8').replace(/```[\s\S]*?```/g, '');
  const targets = [...src.matchAll(/\]\(([^)\s]+)\)/g), ...src.matchAll(/(?:src|srcset|href)="([^"]+)"/g)].map((m) => m[1]);
  for (const t of targets) {
    if (/^(https?:|mailto:)/.test(t)) continue;
    links++;
    const [p, anchor] = t.split('#');
    const file = p ? path.resolve(path.dirname(path.join(REPO, f)), decodeURI(p)) : path.join(REPO, f);
    if (!fs.existsSync(file)) { fail(`${f}: broken link ${t}`); continue; }
    if (anchor && file.endsWith('.md')) {
      const heads = [...fs.readFileSync(file, 'utf8').matchAll(/^#{1,6}\s+(.+)$/gm)].map((m) => slug(m[1]));
      if (!heads.includes(anchor)) fail(`${f}: missing anchor #${anchor}`);
    }
  }
}
ok(`${mds.length} Markdown files, ${links} local links/anchors resolved`);

// 5. Honesty guard: no release/download claims in the README.
const readme = fs.readFileSync(path.join(REPO, 'README.md'), 'utf8');
for (const bad of [/releases\/latest/i, /img\.shields\.io\/github\/(downloads|stars)/i, /\/actions\/workflows\/.*badge/i]) if (bad.test(readme)) fail(`README: forbidden pattern ${bad}`);
if (!readme.includes('Early Development')) fail('README: status "Early Development" missing');
ok('README honesty checks passed');

// 6. Secrets scan.
const SECRET = /(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9]{32,})/;
for (const f of tracked) {
  if (/\.(png|ico|icns|bmp|webp)$/.test(f)) continue;
  if (SECRET.test(fs.readFileSync(path.join(REPO, f), 'utf8'))) fail(`${f}: possible secret`);
}
ok('no secrets detected');

// 7. Private exports (only when present locally).
const EXP = path.join(REPO, 'branding-private/exports');
if (fs.existsSync(EXP)) {
  for (const s of [16, 24, 32, 48, 64, 128, 256, 512, 1024]) {
    const p = path.join(EXP, `png/brizo-mark-${s}.png`);
    const img = decodePNG(fs.readFileSync(p));
    if (img.width !== s || img.height !== s) fail(`${rel(p)}: wrong size`);
    const a = (x, y) => img.data[(y * s + x) * 4 + 3];
    if (a(0, 0) || a(s - 1, 0) || a(0, s - 1) || a(s - 1, s - 1)) fail(`${rel(p)}: corners not transparent`);
  }
  // exact primary colours present in the large render
  const big = decodePNG(fs.readFileSync(path.join(EXP, 'png/brizo-mark-1024.png')));
  const seen = new Set();
  for (let i = 0; i < big.data.length; i += 4) if (big.data[i + 3] === 255) seen.add('#' + [0, 1, 2].map((k) => big.data[i + k].toString(16).padStart(2, '0')).join('').toUpperCase());
  for (const c of PRIMARY_COLORS) if (!seen.has(c)) fail(`brizo-mark-1024.png: exact colour ${c} not found`);
  // ICO / ICNS structure
  const ico = fs.readFileSync(path.join(EXP, 'icons/windows/brizo.ico'));
  if (ico.readUInt16LE(2) !== 1 || ico.readUInt16LE(4) !== 8) fail('brizo.ico: bad header');
  const icns = fs.readFileSync(path.join(EXP, 'icons/macos/brizo.icns'));
  if (icns.toString('ascii', 0, 4) !== 'icns' || icns.readUInt32BE(4) !== icns.length) fail('brizo.icns: bad header');
  let p = 8, n = 0;
  while (p < icns.length) { const len = icns.readUInt32BE(p + 4); pngInfo(icns.subarray(p + 8, p + len)); p += len; n++; }
  if (n !== ICNS_TYPES.length) fail(`brizo.icns: ${n} entries`);
  const bmp = fs.readFileSync(path.join(EXP, 'installer/windows-nsis/welcome-sidebar.bmp'));
  if (bmp.readInt32LE(18) !== 164 || bmp.readInt32LE(22) !== 314) fail('welcome-sidebar.bmp: wrong size');
  ok('private exports: sizes, transparency, exact colours, ICO/ICNS/BMP structure');
} else ok('private exports not present (skipped)');

for (const n of notes) console.log(`  ✓ ${n}`);
if (errors.length) {
  for (const e of errors) console.error(`  ✗ ${e}`);
  console.error(`\n${errors.length} problem(s) found.`);
  process.exit(1);
}
console.log('\nAll checks passed.');
