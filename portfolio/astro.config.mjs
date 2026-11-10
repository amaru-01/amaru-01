import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  // TODO: set `site` to the production URL once known (needed for sitemap/canonical URLs).
  vite: { plugins: [tailwindcss()] },
});
