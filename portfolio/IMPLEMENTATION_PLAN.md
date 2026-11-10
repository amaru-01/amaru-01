# Portfolio Website Implementation Plan

## Goal

Build a polished, responsive personal portfolio in this repository that presents Amaru's work across computer science, 2D and 3D graphic design, and photography. Keep the existing repository files intact and make the portfolio independently deployable through Netlify.

## Repository approach

- Add the website under `portfolio/`; do not move, overwrite, or remove the existing root files and directories such as `README.md`, `.gitignore`, `assets/`, or `scripts/`.
- Treat `portfolio/` as the website project and Netlify base directory. Its build output will be `portfolio/dist/`.
- Keep the photography website in `amaru-01/tcoaphotograph` as a separate project. The portfolio will link to it and may show a small, intentionally selected set of preview images if the owner supplies them and confirms they can be reused.

## Recommended stack

- **Astro with TypeScript** for a fast, static-first site. It suits a content- and image-led portfolio, produces mostly static HTML, and avoids shipping a large client-side framework when interactivity is not needed.
- **Astro components and content collections** for reusable project cards and typed, maintainable portfolio content.
- **Tailwind CSS** for responsive styling and a consistent design system. Define the palette, typography, spacing, and focus styles as shared design tokens; use custom CSS for distinctive art direction where utility classes are not a good fit.
- **Astro Image / `astro:assets`** for optimized local images, responsive sizes, and explicit alt text. Keep original high-resolution artwork and photographs outside the deployed image set when they are not needed on the site.
- **Netlify** connected to this GitHub repository for preview and production deployments.

Avoid adding React, a database, or a CMS for the first version. Add a small interactive component only if a real requirement emerges, such as a filterable gallery; prefer accessible links and native browser behavior otherwise.

## Site structure

1. **Home** — a concise introduction, a clear statement about the combination of CS and creative practice, and prominent routes into the three disciplines.
2. **Computer Science** — a curated selection of projects. Each entry should explain the problem, Amaru's role, the key technologies, and provide working demo/source links where available.
3. **Design** — distinct **2D** and **3D** sections, with image-led cards, project titles, short context, and optional tools/role. The sections can start small and grow over time.
4. **Photography** — selected preview work and a prominent link to the separately hosted photography website. Use the confirmed live URL before launch; do not guess it.
5. **About** — a brief biography and interests, written or approved by Amaru.
6. **Contact** — email and selected professional/social links, reusing existing links only after verifying they are still correct.

Use a shared header/navigation and footer. Include a custom not-found page and sensible page titles/descriptions.

## Suggested project layout

```text
portfolio/
├── IMPLEMENTATION_PLAN.md
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── public/
│   ├── favicon.svg
│   └── images/                 # Small static assets that do not need transformation
└── src/
    ├── content.config.ts       # Typed content collection configuration
    ├── content/
    │   ├── cs-projects/
    │   ├── design-2d/
    │   └── design-3d/
    ├── components/             # Header, footer, cards, buttons, gallery items
    ├── layouts/                # Shared page shell and metadata
    ├── pages/                  # Home, discipline pages, about, contact, 404
    ├── styles/                 # Global styles and design tokens
    └── assets/                 # Images imported for optimization
```

This is a proposed structure, not a requirement to create every directory at once. Keep content close to the project until the site grows enough to justify more structure.

## Visual and interaction direction

- Make the work the focus: strong typography, generous spacing, clear project previews, and a restrained color palette with one distinctive accent.
- Give CS and creative work equal visual consideration while keeping each discipline easy to identify.
- Use responsive layouts that adapt from a single-column mobile view to wider gallery/project grids on desktop.
- Use subtle hover/focus feedback, but do not rely on hover to reveal essential information.
- Provide visible keyboard focus, sufficient color contrast, semantic headings, descriptive link labels, and meaningful alt text. Mark purely decorative imagery appropriately.
- Respect reduced-motion preferences and avoid autoplaying media.

## Build sequence

1. **Confirm content and permissions**
   - Confirm preferred name/title, bio, contact details, and the photography site's live URL.
   - Select the initial CS projects and verify descriptions, contribution claims, tech stacks, and links.
   - Gather approved 2D/3D work and photography previews, captions, and alt text. Confirm rights to publish images and whether any work needs attribution or a confidentiality check.
   - Use clearly marked temporary placeholders only where information has not yet been provided; replace them before launch.
2. **Scaffold the Astro site** inside `portfolio/`, with TypeScript and Tailwind CSS, keeping changes isolated from the existing repository content.
3. **Establish shared design foundations**: color and type tokens, responsive spacing, accessible base styles, reusable layout, navigation, footer, and metadata handling.
4. **Build the pages and reusable content components** for the home page, CS work, 2D design, 3D design, photography, about, and contact.
5. **Add curated content and optimized media**. Keep image dimensions/aspect ratios consistent within a gallery, use descriptive filenames, and avoid needlessly bundling original full-resolution files.
6. **Quality-check** the site on narrow and wide screens, keyboard navigation, links, images, empty/missing content, and the browser console. Run the production build and fix warnings/errors.
7. **Deploy with Netlify** using a deploy preview first, verify the preview and production settings, then publish the production site.

## Netlify configuration

Connect `amaru-01/amaru-01` to Netlify and configure:

- **Base directory:** `portfolio`
- **Build command:** `npm run build`
- **Publish directory:** `dist` (relative to the base directory; equivalently, the generated output is `portfolio/dist/` in the repository)
- **Node version:** use a current Netlify-supported LTS version, pinning it consistently in the project/Netlify settings if needed.

Use Netlify deploy previews for pull requests or branch changes before production. Add a custom domain later if desired. Do not commit credentials or secrets; this static site should not need any for its initial version.

## Launch checklist

- [ ] All placeholder content has been replaced or intentionally removed.
- [ ] Photography link points to the confirmed live site.
- [ ] Project and social links work and point to the intended destinations.
- [ ] Images have appropriate alt text, are optimized, and are approved for publication.
- [ ] Mobile and desktop layouts are usable; navigation and controls work with keyboard and touch.
- [ ] Titles, descriptions, favicon, social preview metadata, and not-found page are in place.
- [ ] Production build succeeds and the Netlify deploy preview has been reviewed.
- [ ] Existing repository files remain unchanged unless separately approved.
