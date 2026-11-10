# Paul Kimaru (Amaru): Portfolio Website

A fast, responsive personal portfolio covering **computer science**, **2D and 3D design**, and **photography**. The public site is statically generated. New design and photography work is added through a private content dashboard (Sanity Studio), with no code changes needed.

| | |
|---|---|
| **Live site** | https://paul-kimaru-portfolio.netlify.app |
| **Content dashboard (Studio)** | https://paul-kimaru.sanity.studio/ (sign-in required) |
| **Photography site (separate project)** | https://tcoaphotography.netlify.app |
| **Source** | https://github.com/amaru-01/amaru-01 (website is in `portfolio/`) |

---

## 1. What was built

- **Home**: hero, three discipline cards, and a Featured work section fed by the CMS.
- **Computer Science**: five projects (problem, role, tech stack, demo/source links), kept as source-controlled Markdown files.
- **Design**: separate 2D and 3D sections, image-led cards, managed in the CMS.
- **Photography**: CMS-managed previews plus a prominent link to the full photography site.
- **About** and **Contact**: bio, email, GitHub and LinkedIn (icon links), photography link.
- **Custom 404 page**, sitemap, `robots.txt`, canonical links and social-preview cards.

### Design
- Glassmorphism, Apple-inspired: frosted translucent cards, soft blur, animated gradient background, generous spacing.
- Automatic light and dark mode (follows the device setting).
- Self-hosted **Inter** font, so type looks the same on every device.
- Compact mobile menu (brand plus menu button and dropdown); full inline nav on larger screens.
- Accessibility: semantic headings, visible keyboard focus, skip-to-content link, alt text required in the CMS, reduced-motion support, 44-48px touch targets.

---

## 2. Tools and technologies

| Layer | Tool | Why |
|---|---|---|
| Framework | **Astro 6** + TypeScript | Static-first, fast, almost no client-side JavaScript |
| Styling | **Tailwind CSS 4** + custom CSS | Design tokens and utility classes; custom CSS for the glass effects |
| Build tooling | **Vite 7** (pinned to 7.3.8) | Astro 6's bundler; pinned because Tailwind's plugin otherwise pulled in Vite 8 and broke the build |
| CMS | **Sanity** (hosted; Studio on React 19) | Structured content and hosted image storage without running a database or server |
| CMS client | `@sanity/client`, `@sanity/image-url` | Fetch published content at build time; generate resized, WebP-optimised images |
| Local content | Astro **content collections** (Markdown + typed schema) | CS projects that rarely change |
| SEO | `@astrojs/sitemap` | Sitemap generation |
| Font | `@fontsource-variable/inter` | Self-hosted, no third-party font requests |
| Hosting | **Netlify** | Continuous deployment from GitHub, deploy previews |
| Source control | **Git + GitHub** | Branch, PR, merge workflow |
| Runtime | **Node 22** | Pinned in `.nvmrc` and `netlify.toml` |

---

## 3. How it fits together

```
   You (Studio, any device)                       GitHub (main)
          |                                             |
          |  publish / update / delete                  |  push / merge
          v                                             v
   Sanity (content + images) --webhook--> Netlify build hook --> Netlify build
          ^                                                         |
          |  fetch published content at build time                  |
          +---------------------------------------------------------+
                                                                    v
                                              Static site (HTML/CSS/images)
                                              https://paul-kimaru-portfolio.netlify.app
```

- Visitors only receive pre-built static files. No server or database runs on request.
- Editing content in the Studio triggers a rebuild, and the site updates when the deploy finishes (typically about a minute).
- The build reads **published** content only, so drafts never reach the public site.
- Images are served from Sanity's CDN, resized per card, with the focal point you set in the Studio.

---

## 4. Deployment process

### One-time setup (completed)
1. **Sanity:** created the project (`amaru_portfolio`, dataset `production`, public dataset since the content is public anyway).
2. **Studio:** `cd portfolio/studio && npm run deploy` published it at `paul-kimaru.sanity.studio`.
3. **Netlify:** imported `amaru-01/amaru-01` from GitHub with
   - Base directory: `portfolio`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Environment variables: `SANITY_PROJECT_ID`, `SANITY_DATASET`
4. **Rebuild on publish:** created a Netlify **build hook**, then a Sanity **webhook** (dataset `production`, trigger on create/update/delete, filter `_type == "project"`, POST) pointing at it.
5. **Secrets scan:** Netlify flagged the public dataset name as a "secret"; `SECRETS_SCAN_OMIT_KEYS` in `netlify.toml` exempts the two public Sanity IDs.

### Everyday workflows

| I want to... | Do this |
|---|---|
| Add or edit design/photo work | Open the Studio, create or edit a **Project**, add alt text, **Publish**. The site rebuilds automatically. |
| Feature something on the home page | Tick **Featured** on the project (the first three are shown) |
| Hide or remove work | Unpublish or delete it in the Studio. The site rebuilds without it. |
| Change text, links, layout or CS projects | Edit the code or `src/content/cs-projects/*.md`, commit on a branch, open a PR, merge to `main`. Netlify deploys it. |
| Change the CMS fields | Edit `studio/schemaTypes/project.ts`, then run `npm run deploy` in `studio/` |

### Git workflow
Work on a branch, open a pull request, merge into `main`. Netlify builds and publishes `main`. Never commit `.env` files.

---

## 5. Project structure

```
portfolio/
├── src/
│   ├── pages/            index, computer-science, design, photography, about, contact, 404
│   ├── components/       Header (mobile menu), Footer, ProjectCard, PageHeading, SocialIcon
│   ├── layouts/Base.astro  page shell, SEO and social meta tags
│   ├── lib/
│   │   ├── site.ts       name, email, links, nav (edit personal details here)
│   │   └── sanity.ts     read-only CMS client, queries, image URL helper
│   ├── content/cs-projects/   one Markdown file per CS project
│   ├── content.config.ts      typed schema for the CS projects
│   └── styles/global.css      design tokens and glass styles
├── studio/               Sanity Studio (separate package, deployed separately)
├── public/               favicon, og.png (social preview), robots.txt
├── astro.config.mjs      site URL, sitemap, Tailwind
├── netlify.toml          build settings, Node version, secrets-scan exemption
├── SETUP.md              CMS and Netlify setup steps
├── PROGRESS.md           done / remaining checklist
└── PLACEHOLDERS.md       items still to review
```

---

## 6. Running it locally

```bash
cd portfolio
npm install
cp .env.example .env     # set SANITY_PROJECT_ID (see SETUP.md)
npm run dev              # http://localhost:4321
npm run build            # production build into dist/
npm run check            # type-check Astro files

cd studio
npm install
npm run dev              # local Studio at http://localhost:3333
```

Requires Node 22 or newer.

---

## 7. Configuration and security

| Variable | Where | Secret? |
|---|---|---|
| `SANITY_PROJECT_ID` | Netlify env, `portfolio/.env` | No (public identifier) |
| `SANITY_DATASET` | Netlify env, `portfolio/.env` | No |
| `SANITY_READ_TOKEN` | Only if the dataset is ever made private | **Yes**. Keep in Netlify env only, never in the repo |
| `SANITY_STUDIO_PROJECT_ID` / `_DATASET` | `studio/.env` | No |
| Netlify **build hook URL** | Only inside the Sanity webhook | **Yes**. Treat like a password |

- `.env` files are git-ignored; only `.env.example` templates are committed.
- The Studio requires sign-in. Only people invited under sanity.io/manage → Members can edit.
- The public site has no admin routes, database, or custom authentication.
- **Never** add a real token to `SECRETS_SCAN_OMIT_KEYS`; the scan should keep catching genuine secrets.
- Personal details left off the site on purpose: phone number and resume referees.

---

## 8. Decisions and lessons learned

- **Astro 6 instead of 7:** Astro 7 needs a newer Node than the development machine had; Astro 6 works on Node 22.16.
- **Vite pinned to 7.3.8:** a duplicate Vite 8 install broke the Tailwind plugin. Both the dependency and the `overrides` entry use the exact version, because npm could not resolve a `$vite` reference.
- **CMS returns `null` for unset lists.** The query now uses `coalesce(...)` and the card component guards against `null`. Real data exposed this bug; an empty CMS did not.
- **Netlify secrets scan false positive:** the dataset is named `production`, a common word that appears across the repo. Fixed with `SECRETS_SCAN_OMIT_KEYS` for the two public IDs.
- **CS projects stay in the repo** rather than the CMS because they change rarely; this can be changed later.
- **Roles on CS projects** are set to "Personal project: design and development" except the RPS game (taken from the resume). Edit them in `src/content/cs-projects/` if you want more detail.

---

## 9. Known limitations and next steps

- Deleting or unpublishing an entry should remove it after the rebuild, but that direction has not yet been tested end to end (publishing has).
- The mobile layout was checked from a phone screenshot and desktop-sized browser screenshots, not on a range of devices.
- The "Powered by Netlify" badge seen on phones is injected by Netlify, not by this code; check Netlify's site settings.
- Upload real photography and 2D/3D work through the Studio (with alt text), and review the drafted About bio and home intro.
- Optional: a custom domain (then update `site` in `astro.config.mjs`, `public/robots.txt`, and the URL text in `public/og.png`), a detail page per project, and moving CS projects into the CMS.

See `PROGRESS.md` for the full checklist.
