# README-driven featured projects on the Code section

## Intent

Paul picks his featured projects in the repo's root `README.md` ("## Featured Projects"). The portfolio's Code section and the home page's "Selected code" should follow that list, so a project is featured in one place and the site and the GitHub profile stay in sync. Today the two lists have drifted: the README says VeriDose and Apex Heights Suites, the site still says Prescription QR Scanner and WebAR Real Estate Preview, and FundiSwift is missing from the site.

## Goals

- The README's Featured Projects list sets which projects lead the Code page and in what order.
- The README's title, link, summary and tech tags are what the site shows for those projects.
- Projects not in the README (Supermarket Invoice App, Rock, Paper, Scissors AI) stay on the Code page, below the featured ones, in their existing `order`.
- Editing the README and pushing to `main` updates the site with no other step.

## Non-goals

- No GitHub API, tokens or scheduled rebuilds.
- No change to Sanity or the studio schema.
- No visual redesign of the Code page; same plates, same type.

## Anti-goals

- A README typo must not silently ship a site with the featured projects missing.
- Source-code links must not come back (owner shows live demos only).

## Constraints

- The README and portfolio share one repo; `portfolio/` is the Astro root, so the file is `../README.md` at build time (present in CI checkout and Cloudflare Workers Builds clone).
- Demo links open in a new tab (already done).
- FundiSwift: owner confirmed permission to list it.

## Approaches

- **A. Parse `README.md` at build time (picked).** Same repo, no network, rebuild happens on push.
- B. Fetch README from the GitHub API on a schedule. Adds a token, rate limits and a cron rebuild for a file already on disk.
- C. Generate the README from portfolio content. Wrong direction: the owner edits the README.

## Design

**Parser** (`portfolio/src/lib/featured.ts`): read `../README.md`, take the lines between `## Featured Projects` and the next `## ` heading. Each entry is a bullet `- **[Title](url)** — summary` or `- **Title** — summary` (no link), followed by an indented line of backtick tags separated by ` · `. Accept `—`, `–` or `-` as the separator. Returns `{ title, url?, summary, tech[] }[]` in README order.

**Merge** (same module, used by all three pages): each README entry is matched to a local case study in `src/content/cs-projects/` when the URLs are equal (README link vs `demo`) or the normalized titles are equal. The merged project takes title, summary, tech and demo link from the README, and problem, role, status, cover and case-note body from the case study. Unmatched README entries (FundiSwift) show with their live link and no case notes. Then the unmatched case studies follow by `order`. Sanity `cs` projects stay last, as now.

**Pages:** `computer-science/index.astro`, `computer-science/[slug].astro` (plate numbers and "Next" follow the merged order; detail pages exist only for projects with a case study) and `index.astro` ("Selected code" = first 3 of the merged list; Sanity-featured `cs` projects no longer jump ahead, the README is the one place to feature).

**Failure:** if the README file is missing, warn and fall back to case studies only. If the section exists but no entry parses, fail the build with a message naming the README, so CI catches it before deploy.

**Deploy:** confirm in Cloudflare Workers Builds that build watch paths include `README.md` (or are unrestricted); otherwise README-only pushes won't rebuild. CI path filter in `.github/workflows/portfolio-ci.yml` gets `README.md` added.

## Left to the builder

- Exact title normalization (lowercase, strip punctuation).
- Unit tests for the parser against the current README plus a malformed sample.
