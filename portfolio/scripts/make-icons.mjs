// Renders the favicon mark to the raster sizes browsers and phones ask for.
// Run from portfolio/: node scripts/make-icons.mjs
import sharp from 'sharp';
import { writeFileSync } from 'node:fs';

// Light-scheme mark (rasters can't switch scheme). `inset` adds padding for
// icons that the OS crops or rounds itself (Apple touch, Android maskable).
const mark = (size, { rounded = true, inset = 0 } = {}) => {
  const s = 32, pad = inset, scale = (s - pad * 2) / s;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 32 32">
  <defs><linearGradient id="f" x1="0.15" y1="0.2" x2="0.75" y2="0.95"><stop offset="0" stop-color="#1c1c1c"/><stop offset="1" stop-color="#8d8a82"/></linearGradient></defs>
  <rect width="32" height="32" rx="${rounded ? 7 : 0}" fill="#f2efe6"/>
  <g transform="translate(${pad} ${pad}) scale(${scale})">
    <path d="M7.2 10.2 Q13 15.5 18.5 26.1 A10.5 10.5 0 0 1 7.2 10.2 Z" fill="url(#f)" opacity=".9"/>
    <circle cx="16" cy="16" r="10.5" fill="none" stroke="#1c1c1c" stroke-width="1.6"/>
    <path d="M7.2 10.2 Q13 15.5 18.5 26.1" fill="none" stroke="#1c1c1c" stroke-width="2" stroke-linecap="round"/>
  </g>
</svg>`;
};

const out = 'public';
const png = (svg, file) => sharp(Buffer.from(svg), { density: 600 }).png({ palette: true, colours: 48, compressionLevel: 9, effort: 10 }).toFile(`${out}/${file}`);

await png(mark(180, { rounded: false, inset: 3 }), 'apple-touch-icon.png');
await png(mark(192), 'icon-192.png');
await png(mark(512), 'icon-512.png');
await png(mark(512, { rounded: false, inset: 5 }), 'icon-maskable-512.png');
// 256px source for favicon.ico: pack it with Pillow, e.g.
// python -c "from PIL import Image; Image.open('public/ico-source.png').save('public/favicon.ico', sizes=[(16,16),(32,32),(48,48)])"
await png(mark(256), 'ico-source.png');

writeFileSync(`${out}/site.webmanifest`, JSON.stringify({
  name: 'Paul Kimaru (Amaru)',
  short_name: 'Amaru',
  icons: [
    { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
    { src: '/icon-512.png', sizes: '512x512', type: 'image/png' },
    { src: '/icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
  ],
  theme_color: '#f2efe6',
  background_color: '#f2efe6',
  display: 'browser',
}, null, 2) + '\n');
console.log('icons written');
