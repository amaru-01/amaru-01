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

## 3. Cloudflare Workers (static assets)
The site deploys as a Worker that only serves static files (`wrangler.jsonc`, no adapter, no Worker code).

**First deploy from your machine:** `npx wrangler login` once, then `npm run deploy` (builds and uploads `dist/`).

**Automatic deploys (Workers Builds):**
1. Cloudflare dashboard → Workers & Pages → `paul-kimaru-portfolio` → Settings → Builds → **Connect** → GitHub → `amaru-01/amaru-01`.
2. Build settings: root directory `portfolio`, build command `npm run build`, deploy command `npx wrangler deploy`, production branch `main`. Node 22 comes from `.nvmrc`.
3. Build variables: `SANITY_PROJECT_ID`, `SANITY_DATASET` (and `SITE_URL` once a custom domain is added).
4. Settings → Builds → **Deploy Hooks** → create one for `main` and copy its URL (treat it as a secret: anyone with it can trigger builds).
5. Response headers and asset caching come from `public/_headers`; unknown paths serve `404.html`.

## 4. Rebuild on publish
In Sanity → Project → API → Webhooks → edit the existing webhook (or create one):
- URL: the Cloudflare deploy hook URL
- Dataset: `production`; Trigger on: Create, Update, Delete
- Filter: `_type == "project"`; Projection: leave empty; HTTP method POST
Publishing, updating or unpublishing a project then triggers a rebuild.

## 4b. Retire Netlify
Once the Workers site is verified: Netlify → Site configuration → **Delete site** (removes its build hook and variables). If Netlify ever held a `SANITY_READ_TOKEN`, revoke it in Sanity → API → Tokens.

## 5. Before launch
Work through `PLACEHOLDERS.md` and the launch checklist in `IMPLEMENTATION_PLAN.md`.
