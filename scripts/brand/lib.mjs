// Shared helpers for Brizo asset generation.
// Pure Node + pinned npm packages (see package.json). No system tools required.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';
import opentype from 'opentype.js';

export const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = path.resolve(HERE, '..', '..');

// ---------------------------------------------------------------------------
// Brand palette — primary values are owner-approved and MUST NOT change.
// ---------------------------------------------------------------------------
export const PALETTE = Object.freeze({
  lightSail: '#6FBCEB', // Light Sail Blue — rear sail
  primary: '#1684D1', // Primary Blue — front sail
  deepOcean: '#174EA4', // Deep Ocean Blue — hull
  bgLight: '#F4F8FC',
  bgDark: '#0B1220',
  border: '#D8E5F3',
  white: '#FFFFFF',
  text: '#0F172A',
});
export const PRIMARY_COLORS = [PALETTE.lightSail, PALETTE.primary, PALETTE.deepOcean];

// ---------------------------------------------------------------------------
// Fonts — Inter (SIL OFL 1.1) via @fontsource/inter. Text is converted to
// outlined paths so GitHub / any viewer renders it identically without
// loading fonts.
// ---------------------------------------------------------------------------
const fontCache = new Map();
export function font(weight = 700) {
  if (!fontCache.has(weight)) {
    const file = path.join(HERE, 'node_modules/@fontsource/inter/files', `inter-latin-${weight}-normal.woff`);
    const buf = fs.readFileSync(file);
    fontCache.set(weight, opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)));
  }
  return fontCache.get(weight);
}

/** Outline `text`; returns { d, width, height(cap), x1,y1,x2,y2 } with the baseline at y=0. */
export function textPath(text, { weight = 700, size = 48, tracking = 0 } = {}) {
  const f = font(weight);
  const scale = size / f.unitsPerEm;
  let x = 0;
  const parts = [];
  const glyphs = f.stringToGlyphs(text);
  glyphs.forEach((g, i) => {
    const p = g.getPath(x, 0, size);
    parts.push(p.toPathData(2));
    x += g.advanceWidth * scale;
    if (i < glyphs.length - 1) {
      x += f.getKerningValue(g, glyphs[i + 1]) * scale + tracking;
    }
  });
  const capH = (f.tables.os2.sCapHeight || f.ascender * 0.7) * scale;
  return { d: parts.join(''), width: x, capHeight: capH };
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------
export function renderPNG(svg, width, opts = {}) {
  const r = new Resvg(svg, {
    fitTo: { mode: 'width', value: width },
    background: opts.background, // undefined => transparent
    shapeRendering: 2,
    font: { loadSystemFonts: false },
  });
  const img = r.render();
  return { png: img.asPng(), pixels: img.pixels, width: img.width, height: img.height };
}

/** Bounding box of rendered geometry in user units. */
export function svgBBox(svg) {
  const r = new Resvg(svg, { font: { loadSystemFonts: false } });
  const b = r.getBBox();
  return { x: b.x, y: b.y, width: b.width, height: b.height };
}

// ---------------------------------------------------------------------------
// File helpers
// ---------------------------------------------------------------------------
export function write(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
}

export function fmt(n) {
  return Number(n.toFixed(2)).toString();
}

// ---------------------------------------------------------------------------
// Container encoders (ICO / ICNS / BMP) — tiny, dependency-free.
// ---------------------------------------------------------------------------

/** ICO with PNG-compressed entries (supported since Windows Vista). */
export function encodeICO(entries /* [{size, png}] */) {
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(entries.length, 4);
  const dir = Buffer.alloc(16 * entries.length);
  let offset = 6 + dir.length;
  entries.forEach((e, i) => {
    const o = i * 16;
    dir.writeUInt8(e.size >= 256 ? 0 : e.size, o);
    dir.writeUInt8(e.size >= 256 ? 0 : e.size, o + 1);
    dir.writeUInt8(0, o + 2);
    dir.writeUInt8(0, o + 3);
    dir.writeUInt16LE(1, o + 4);
    dir.writeUInt16LE(32, o + 6);
    dir.writeUInt32LE(e.png.length, o + 8);
    dir.writeUInt32LE(offset, o + 12);
    offset += e.png.length;
  });
  return Buffer.concat([header, dir, ...entries.map((e) => e.png)]);
}

/** ICNS with PNG payloads. `entries`: [{type:'ic10', png}] */
export function encodeICNS(entries) {
  const chunks = entries.map((e) => {
    const h = Buffer.alloc(8);
    h.write(e.type, 0, 'ascii');
    h.writeUInt32BE(8 + e.png.length, 4);
    return Buffer.concat([h, e.png]);
  });
  const body = Buffer.concat(chunks);
  const h = Buffer.alloc(8);
  h.write('icns', 0, 'ascii');
  h.writeUInt32BE(8 + body.length, 4);
  return Buffer.concat([h, body]);
}
export const ICNS_TYPES = [
  // [type, pixel size]
  ['icp4', 16], ['icp5', 32], ['icp6', 64], ['ic07', 128], ['ic08', 256],
  ['ic09', 512], ['ic10', 1024], ['ic11', 32], ['ic12', 64], ['ic13', 256], ['ic14', 512],
];

/** 24-bit BMP (bottom-up) from RGBA pixels, flattened onto `bg` (hex). Used for NSIS installer bitmaps. */
export function encodeBMP24(rgba, w, h, bg = '#FFFFFF') {
  const [br, bgc, bb] = [1, 3, 5].map((i) => parseInt(bg.slice(i, i + 2), 16));
  const rowSize = Math.ceil((w * 3) / 4) * 4;
  const data = Buffer.alloc(rowSize * h);
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const s = (y * w + x) * 4;
      const a = rgba[s + 3] / 255;
      const d = (h - 1 - y) * rowSize + x * 3;
      data[d] = Math.round(rgba[s + 2] * a + bb * (1 - a));
      data[d + 1] = Math.round(rgba[s + 1] * a + bgc * (1 - a));
      data[d + 2] = Math.round(rgba[s] * a + br * (1 - a));
    }
  }
  const file = Buffer.alloc(14 + 40);
  file.write('BM', 0, 'ascii');
  file.writeUInt32LE(54 + data.length, 2);
  file.writeUInt32LE(54, 10);
  file.writeUInt32LE(40, 14);
  file.writeInt32LE(w, 18);
  file.writeInt32LE(h, 22);
  file.writeUInt16LE(1, 26);
  file.writeUInt16LE(24, 28);
  file.writeUInt32LE(data.length, 34);
  file.writeInt32LE(2835, 38);
  file.writeInt32LE(2835, 42);
  return Buffer.concat([file, data]);
}

// ---------------------------------------------------------------------------
// PNG inspection (for validation) — decode IHDR + pixels via zlib.
// ---------------------------------------------------------------------------
export function pngInfo(buf) {
  if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('not a PNG');
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20), bitDepth: buf[24], colorType: buf[25] };
}

/** Decode 8-bit RGBA non-interlaced PNG (what resvg emits) to raw RGBA. */
export function decodePNG(buf) {
  const { width, height, bitDepth, colorType } = pngInfo(buf);
  if (bitDepth !== 8 || colorType !== 6) throw new Error(`unsupported PNG ${bitDepth}/${colorType}`);
  const idat = [];
  let p = 8;
  while (p < buf.length) {
    const len = buf.readUInt32BE(p);
    const type = buf.toString('ascii', p + 4, p + 8);
    if (type === 'IDAT') idat.push(buf.subarray(p + 8, p + 8 + len));
    p += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const bpp = 4, stride = width * bpp;
  const out = Buffer.alloc(stride * height);
  for (let y = 0; y < height; y++) {
    const f = raw[y * (stride + 1)];
    const src = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? out[y * stride + x - bpp] : 0;
      const b = y > 0 ? out[(y - 1) * stride + x] : 0;
      const c = x >= bpp && y > 0 ? out[(y - 1) * stride + x - bpp] : 0;
      let v = src[x];
      if (f === 1) v += a;
      else if (f === 2) v += b;
      else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) {
        const pp = a + b - c, pa = Math.abs(pp - a), pb = Math.abs(pp - b), pc = Math.abs(pp - c);
        v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      }
      out[y * stride + x] = v & 0xff;
    }
  }
  return { width, height, data: out };
}
