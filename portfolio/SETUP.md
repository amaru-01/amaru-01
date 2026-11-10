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

## 3. Netlify
1. New site → import `amaru-01/amaru-01`.
2. Base directory `portfolio`, build command `npm run build`, publish directory `dist`.
3. Add the env vars above in Site settings → Environment variables.
4. Site settings → Build & deploy → Build hooks → create one and copy its URL (treat as a secret).

## 4. Rebuild on publish
In Sanity → Project → API → Webhooks → Create:
- URL: the Netlify build hook URL
- Dataset: `production`; Trigger on: Create, Update, Delete
- Filter: `_type == "project"`; Projection: leave empty; HTTP method POST
Publishing, updating or unpublishing a project then triggers a rebuild.

## 5. Before launch
Work through `PLACEHOLDERS.md` and the launch checklist in `IMPLEMENTATION_PLAN.md`.
