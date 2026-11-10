# Portfolio Website Implementation Plan

## Goal

Build a polished, responsive personal portfolio in this repository that presents Amaru's work across computer science, 2D and 3D graphic design, and photography. Keep the existing repository files intact and make the portfolio independently deployable through Netlify. Support adding client and personal creative work through a private content-management dashboard rather than requiring edits to the site's source code for every new item.

## Repository approach

- Add the website under `portfolio/`; do not move, overwrite, or remove the existing root files and directories such as `README.md`, `.gitignore`, `assets/`, or `scripts/`.
- Treat `portfolio/` as the website project and Netlify base directory. Its build output will be `portfolio/dist/`.
- Keep the photography website in `amaru-01/tcoaphotograph` as a separate project. The portfolio will link to it and may show a small, intentionally selected set of preview images if the owner supplies them and confirms they can be reused.
- Keep the site statically generated. Use Sanity as a hosted CMS for frequently added portfolio entries and media; do not build a custom database or admin dashboard for the first version.

## Recommended stack

- **Astro with TypeScript** for a fast, static-first site. It suits a content- and image-led portfolio, produces mostly static HTML, and avoids shipping a large client-side framework when interactivity is not needed.
- **Astro components and content collections** for reusable project cards and typed, maintainable portfolio content. Use Astro content collections for any local, source-controlled content that does not need CMS editing.
- **Tailwind CSS** for responsive styling and a consistent design system. Define the palette, typography, spacing, and focus styles as shared design tokens; use custom CSS for distinctive art direction where utility classes are not a good fit.
- **Sanity** as a hosted headless CMS for adding/editing portfolio projects and uploading approved images through its private Studio dashboard. The CMS will store structured content and media; it removes the need to operate a custom database or admin service.
- **Sanity's Astro integration/client** to fetch published CMS content at build time. Keep the public portfolio statically generated; publishing CMS changes should trigger a Netlify rebuild so the updated content appears on the site.
- **Astro Image / `astro:assets`** for optimizing local images. For CMS-hosted images, use Sanity's image URL builder to request appropriately sized and cropped responsive variants, with explicit alt text.
- **Netlify** connected to this GitHub repository for preview and production deployments, plus a secured build hook that Sanity can call when content is published or updated.

Avoid adding React, a custom database, or custom authentication for the first version. Use the hosted Sanity Studio's access controls for content editing. A small interactive component can be added if a real requirement emerges, such as a filterable gallery; prefer accessible links and native browser behavior otherwise.

## Site structure

1. **Home** — a concise introduction, a clear statement about the combination of CS and creative practice, and prominent routes into the three disciplines.
2. **Computer Science** — a curated selection of projects. Each entry should explain the problem, Amaru's role, the key technologies, and provide working demo/source links where available. These can initially be managed as local content; move them into the CMS too if frequent non-code editing is desired.
3. **Design** — distinct **2D** and **3D** sections, with image-led cards, project titles, short context, and optional tools/role. Populate and update these from the CMS.
4. **Photography** — selected preview work managed in the CMS and a prominent link to the separately hosted photography website. Use the confirmed live URL before launch; do not guess it.
5. **About** — a brief biography and interests, written or approved by Amaru.
6. **Contact** — email and selected professional/social links, reusing existing links only after verifying they are still correct.

Use a shared header/navigation and footer. Include a custom not-found page and sensible page titles/descriptions.

## CMS content model and publishing workflow

Create a Sanity `project` document type with fields such as:

- **Title** and **slug** for display and stable routing.
- **Category**: computer science, 2D design, 3D design, or photography.
- **Summary** and optional longer description/case study.
- **Cover image** and optional gallery images, each with descriptive alt text and optional captions.
- **Tools/technologies**, optional role/contribution, and optional external demo/source links.
- **Client or attribution**, optional and only shown when approved for publication.
- **Featured** flag and **sort order** for curating the portfolio landing page.
- **Publication status** using Sanity's draft/published workflow; drafts must never appear on the public site.

Expected workflow: sign in to the private Sanity Studio, create a project, choose its category, add text and approved images, preview the entry, and publish it. Publishing or updating content triggers a secured Netlify build hook. Netlify rebuilds the static site using published Sanity content, and the change becomes public once that deployment completes. Unpublishing/removing an item should also trigger a rebuild so it disappears from the site.

Use Sanity's hosted media storage for CMS-uploaded images. Set practical upload limits and use image transformations for display; do not expose original client deliverables or unnecessarily large source files. Keep the CMS project and production dataset private to authorized editors, and grant the owner appropriate access. Do not commit Sanity write tokens, Netlify build-hook URLs, or other secrets. Use environment variables for any server/build-time credentials, restrict tokens to read-only access where the site build only needs published content, and ensure draft preview credentials are never sent to public visitors.

## Suggested project layout

```text
portfolio/
├── IMPLEMENTATION_PLAN.md
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── sanity.config.ts           # Studio configuration if using an embedded/local Studio
├── sanity.cli.ts
├── public/
│   ├── favicon.svg
│   └── images/                 # Small static assets that do not need transformation
└── src/
    ├── content.config.ts       # Typed local Astro content collections, if needed
    ├── content/
    │   └── cs-projects/        # Optional local content for CS projects
    ├── components/             # Header, footer, cards, buttons, gallery items
    ├── layouts/                # Shared page shell and metadata
    ├── lib/                    # Sanity client, queries, and image URL helpers
    ├── pages/                  # Home, discipline pages, about, contact, 404
    ├── styles/                 # Global styles and design tokens
    └── assets/                 # Images imported for optimization
```

The Sanity Studio may instead live in a separate repository or be hosted independently. Choose that approach based on the desired editor URL and deployment workflow; do not expose editing access through the public portfolio. This is a proposed structure, not a requirement to create every directory at once. Keep content close to the project until the site grows enough to justify more structure.

## Visual and interaction direction

- Make the work the focus: strong typography, generous spacing, clear project previews, and a restrained color palette with one distinctive accent.
- Give CS and creative work equal visual consideration while keeping each discipline easy to identify.
- Use responsive layouts that adapt from a single-column mobile view to wider gallery/project grids on desktop.
- Use subtle hover/focus feedback, but do not rely on hover to reveal essential information.
- Provide visible keyboard focus, sufficient color contrast, semantic headings, descriptive link labels, and meaningful alt text. Mark purely decorative imagery appropriately.
- Respect reduced-motion preferences and avoid autoplaying media.
- Ensure CMS entries with missing optional fields render gracefully; only show links, client names, captions, and credits when provided and approved.

## Build sequence

1. **Confirm content, CMS needs, and permissions**
   - Confirm preferred name/title, bio, contact details, and the photography site's live URL.
   - Select the initial CS projects and verify descriptions, contribution claims, tech stacks, and links.
   - Gather approved 2D/3D work and photography previews, captions, and alt text. Confirm rights to publish images and whether any work needs attribution or a confidentiality check; do not publish client-identifying details without permission.
   - Confirm who needs CMS access and whether CS projects also need editing through the CMS.
   - Use clearly marked temporary placeholders only where information has not yet been provided; replace them before launch.
2. **Scaffold the Astro site** inside `portfolio/`, with TypeScript and Tailwind CSS, keeping changes isolated from the existing repository content.
3. **Establish shared design foundations**: color and type tokens, responsive spacing, accessible base styles, reusable layout, navigation, footer, and metadata handling.
4. **Set up Sanity**: define the project schema, category values, draft/publish behavior, access roles, and image handling. Create a private Studio and seed it with approved initial creative entries.
5. **Integrate CMS content**: configure a read-only published-content client, queries for featured and category-specific projects, resilient empty states, image URL helpers, and metadata. Keep draft preview access separate and protected; never include privileged secrets in browser code.
6. **Build the pages and reusable content components** for the home page, CS work, 2D design, 3D design, photography, about, and contact.
7. **Configure rebuild-on-publish**: create a Netlify build hook, store it securely, and configure Sanity to call it on publish/update/unpublish. Verify the webhook only triggers deployments and that a publishing action produces a successful updated deploy.
8. **Add curated content and optimized media**. Keep image dimensions/aspect ratios consistent within a gallery, use descriptive alt text, and avoid needlessly bundling original full-resolution files.
9. **Quality-check** the site on narrow and wide screens, keyboard navigation, links, images, empty/missing content, draft exclusion, CMS publish/unpublish behavior, webhook deployment, and the browser console. Run the production build and fix warnings/errors.
10. **Deploy with Netlify** using a deploy preview first, verify the preview and production settings, then publish the production site.

## Netlify configuration

Connect `amaru-01/amaru-01` to Netlify and configure:

- **Base directory:** `portfolio`
- **Build command:** `npm run build`
- **Publish directory:** `dist` (relative to the base directory; equivalently, the generated output is `portfolio/dist/` in the repository)
- **Node version:** use a current Netlify-supported LTS version, pinning it consistently in the project/Netlify settings if needed.
- **Environment variables:** add only the CMS project/dataset configuration and any necessary read-only build-time token through Netlify's environment settings. Do not commit secrets. Prefer publicly readable published content if compatible with the dataset's privacy requirements.
- **Build hook:** generate a Netlify build hook and store its URL only in the CMS webhook configuration as a secret. Do not include it in source control or expose it in frontend code.

Use Netlify deploy previews for pull requests or branch changes before production. Add a custom domain later if desired. The public site is static; the CMS is hosted separately and there is no custom application server to maintain.

## Launch checklist

- [ ] All placeholder content has been replaced or intentionally removed.
- [ ] Photography link points to the confirmed live site.
- [ ] Project and social links work and point to the intended destinations.
- [ ] Images have appropriate alt text, are optimized, and are approved for publication.
- [ ] Client work, client names, and credits are published only with permission.
- [ ] CMS drafts are private and excluded from public pages; only authorized editors can publish.
- [ ] Publishing, updating, and unpublishing a CMS entry triggers a successful Netlify rebuild.
- [ ] CMS and Netlify secrets are stored outside source control and are not exposed to browser code.
- [ ] Mobile and desktop layouts are usable; navigation and controls work with keyboard and touch.
- [ ] Titles, descriptions, favicon, social preview metadata, and not-found page are in place.
- [ ] Production build succeeds and the Netlify deploy preview has been reviewed.
- [ ] Existing repository files remain unchanged unless separately approved.
