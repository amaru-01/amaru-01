# Setup: CMS and deployment (steps only you can do)

## 1. Create the Sanity project
1. Sign in at https://www.sanity.io/manage and create a project (dataset: `production`).
2. Copy the **Project ID** (public, not a secret).
3. In `studio/`: copy `.env.example` to `.env`, set `SANITY_STUDIO_PROJECT_ID`.
4. `cd studio && npm run dev` to edit locally. The hosted Studio is at **https://paul-kimaru.sanity.studio/** (sign-in required; add editors under Project → Members). To update it after schema changes, run `npm run deploy` in `studio/`.
5. Create a few `Project` documents. Every image needs alt text. Click **Publish**: drafts never reach the site.

## 2. Site environment variables
Locally: copy `.env.example` to `.env` in `portfolio/` and set `SANITY_PROJECT_ID` (and `SANITY_DATASET`).
Only set `SANITY_READ_TOKEN` (a **Viewer**-role token from Project → API → Tokens) if you make the dataset private. Never commit `.env`.

## 3. Cloudflare Pages
1. Cloudflare dashboard → Workers & Pages → Create → Pages → **Connect to Git** → pick `amaru-01/amaru-01`.
2. Project name `paul-kimaru-portfolio` (gives `https://paul-kimaru-portfolio.pages.dev`; if you pick another name, set `SITE_URL` in step 4).
3. Build settings: framework preset **Astro**, root directory `portfolio`, build command `npm run build`, output directory `dist`, production branch `main`. Node 22 is picked up from `.nvmrc`.
4. Settings → Variables and Secrets: add `SANITY_PROJECT_ID` and `SANITY_DATASET` (and `SITE_URL` only for a custom domain or a different project name).
5. Settings → Builds → **Deploy hooks** → add one for branch `main` and copy its URL (treat as a secret).
6. Response headers and asset caching come from `public/_headers`.

## 4. Rebuild on publish
In Sanity → Project → API → Webhooks → edit the existing webhook (or create one):
- URL: the Cloudflare deploy hook URL
- Dataset: `production`; Trigger on: Create, Update, Delete
- Filter: `_type == "project"`; Projection: leave empty; HTTP method POST
Publishing, updating or unpublishing a project then triggers a rebuild.

## 4b. Retire Netlify (after the Cloudflare site is verified)
1. Netlify → Site configuration → delete the site (or unlink the repo) so `main` stops deploying twice.
2. Delete `portfolio/netlify.toml`.

## 5. Before launch
Work through `PLACEHOLDERS.md` and the launch checklist in `IMPLEMENTATION_PLAN.md`.
