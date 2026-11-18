import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // Canonical URLs, sitemap, robots.txt and the OG image all derive from this.
  // Set SITE_URL as a Workers Builds variable when a custom domain is added.
  site: process.env.SITE_URL ?? 'https://paul-kimaru-portfolio.pmkimaru95.workers.dev',
  integrations: [sitemap({ filter: (page) => !page.endsWith('/404/') })],
  vite: { plugins: [tailwindcss()] },
});
