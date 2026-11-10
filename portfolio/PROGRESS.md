# Portfolio Progress Checklist

_Last updated: 2026-11-10_

**Live site:** https://paul-kimaru-portfolio.netlify.app
**Studio (CMS):** https://paul-kimaru.sanity.studio/
**Photography site:** https://tcoaphotography.netlify.app
**Repo:** https://github.com/amaru-01/amaru-01 (website lives in `portfolio/`)

---

## Done

### Foundation
- [x] Astro 6 + TypeScript + Tailwind CSS 4 project in `portfolio/` (existing repo files untouched)
- [x] Pinned Vite to 7.3.8 (Astro 6 compatibility); Astro 6 chosen because Astro 7 needs a newer Node than installed
- [x] `netlify.toml` (build command, publish dir, Node 22, secrets-scan exemption for public Sanity IDs)
- [x] `.env.example` files; real `.env` files are git-ignored

### Design
- [x] Glassmorphism / Apple-style design system: frosted glass cards, gradient background, light + dark mode
- [x] Self-hosted Inter font (renders the same on every device, no external font requests)
- [x] Reduced-motion support, visible focus rings, skip-to-content link
- [x] Compact mobile menu (brand + menu button, dropdown, Escape/outside-click close, works without JS)

### Pages
- [x] Home (hero, discipline cards, Featured work from CMS)
- [x] Computer Science (5 projects from local content files)
- [x] Design (separate 2D and 3D sections, CMS-driven, empty states)
- [x] Photography (CMS previews + link to the photography site)
- [x] About, Contact (email, GitHub, LinkedIn, photography), custom 404

### Content
- [x] Name "Paul Kimaru" (nickname Amaru), email, GitHub, LinkedIn
- [x] CS projects: Supermarket Invoice App, Prescription QR Scanner, Chronicles of the Signal, WebAR Real Estate Preview, Rock Paper Scissors AI
- [x] Roles filled in (RPS from resume; others "Personal project: design and development")
- [x] Phone number and referees intentionally NOT published

### CMS (Sanity)
- [x] Sanity project created (`amaru_portfolio`, dataset `production`)
- [x] `project` schema: title, slug, category (2D / 3D / Photography / CS), summary, description, cover image + gallery with required alt text, tools, role, demo/source links, optional client, featured flag, sort order
- [x] Site reads published content only (drafts never appear); builds fine with empty CMS
- [x] Fixed null-array bug found during real-data testing
- [x] Studio deployed and hosted

### Deployment
- [x] Netlify connected (base dir `portfolio`, deploys from `main`)
- [x] Fixed Netlify secrets-scan false positive
- [x] Netlify build hook + Sanity webhook: publishing in the Studio rebuilds the site (verified with a real entry appearing under Featured work)

### SEO and quality
- [x] Site URL, canonical links, sitemap (404 excluded), `robots.txt`
- [x] Open Graph / Twitter card tags + 1200x630 social preview image
- [x] One `h1` per page, titles and meta descriptions, alt text on every image
- [x] `astro check`: 0 errors, 0 warnings; production build passes
- [x] Live site checked: pages, links, sitemap, robots, canonical and OG tags all serving correctly

---

## Remaining

### You
- [ ] Test the Studio from your phone: publish a small entry, confirm the Netlify rebuild, then delete it
- [ ] Confirm **deleting/unpublishing** an entry removes it from the site after the rebuild (publish direction is verified; delete is not yet)
- [ ] Upload real work in the Studio, each with alt text:
  - [ ] 3-6 photography entries
  - [ ] 2-4 each of 2D and 3D design
  - [ ] Mark about 3 best pieces as **Featured**
  - [ ] Only upload work you have rights to publish; leave **Client** empty unless you have permission
- [ ] Remove or rename the leftover test entry ("My photography images")
- [ ] Read and edit the **About bio** and home intro (drafted from your resume): `src/pages/about.astro`, `src/pages/index.astro`
- [ ] Decide whether to list company projects from your resume (FundiSwift, MkulimaMdogo, Adept chatbots); only with the employers' OK
- [ ] Check the "Powered by Netlify" badge in Netlify site settings (it is not in the code)
- [ ] Optional: add `appId` to `studio/sanity.cli.ts` (copy it from the deploy output) so future deploys don't prompt

### Me, once your content is in
- [ ] Review Design and Photography pages with real content (image crops, ordering, captions)
- [ ] Mobile and keyboard pass on the real site; fix anything you report from your phone
- [ ] Walk through the full launch checklist in `IMPLEMENTATION_PLAN.md`

### Optional later
- [ ] Custom domain (then update `site` in `astro.config.mjs`, `public/robots.txt`, and the OG image URL text)
- [ ] Move CS projects into the CMS if you want to edit them without touching code
- [ ] Add a gallery/case-study detail page per project
- [ ] Unpushed local commit `6a7228f` (records the Studio URL in `SETUP.md`): push and merge when convenient

---

## Where things live

| What | Where |
|---|---|
| Name, email, links, photography URL | `src/lib/site.ts` |
| CS projects | `src/content/cs-projects/*.md` |
| 2D / 3D / photography / featured work | Sanity Studio (no code needed) |
| CMS schema | `studio/schemaTypes/project.ts` |
| Setup steps for CMS and Netlify | `SETUP.md` |
| Placeholders still to review | `PLACEHOLDERS.md` |
