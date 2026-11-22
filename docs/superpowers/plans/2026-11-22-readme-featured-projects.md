# README-driven Featured Projects Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The portfolio's Code page and home "Selected code" follow the root `README.md` "## Featured Projects" list.

**Architecture:** A pure parser and merger (`src/lib/featured.ts`, no Astro imports, unit-tested with Node's built-in runner) turns README text plus case-study data into one ordered list. A thin Astro-side module (`src/lib/code-projects.ts`) reads `../README.md` and the `cs-projects` collection and calls it. Three pages consume that one list.

**Tech Stack:** Astro 6, TypeScript, Node 22 `node --test --experimental-strip-types` (no new dependencies).

**Spec:** `docs/superpowers/specs/2026-11-22-readme-featured-projects-design.md`

## Global Constraints

- No new npm dependencies; no GitHub API calls.
- No source-code links rendered anywhere; external demo links use `target="_blank" rel="noopener noreferrer"` plus `<span class="sr-only"> (opens in a new tab)</span>`.
- README path at build time: `../README.md` relative to the `portfolio/` project root.
- README missing: `console.warn` and fall back to case studies only. Section present but zero entries parsed: throw `Error` whose message contains `README.md`.
- No visual changes to plates, type or layout.

## Review Focus

- Entry with no link (`- **Chronicles of the Signal** — ...`): parsed with `url` undefined, still matched to its case study by title.
- Separator variants `—`, `–`, ` - ` and trailing `  ` (markdown line-break spaces) on the summary line: summary trimmed, no trailing spaces or separator left.
- Windows CRLF line endings in README: parses the same as LF.
- URL match ignoring trailing slash and `http`/`https` difference (`https://x.app/` equals `https://x.app`).
- A README entry whose tech line is missing: `tech` is `[]`, the next bullet is not swallowed.

---

### Task 1: Parser and merger

**Files:**
- Create: `portfolio/src/lib/featured.ts`
- Test: `portfolio/src/lib/featured.test.ts`
- Modify: `portfolio/package.json` (add `"test": "node --test --experimental-strip-types src/lib/*.test.ts"`)

**Interfaces:**
- Produces:
  - `type FeaturedEntry = { title: string; url?: string; summary: string; tech: string[] }`
  - `parseFeatured(readme: string): FeaturedEntry[] | null` — `null` when no `## Featured Projects` heading; throws `Error` (message contains `README.md`) when the heading exists but zero entries parse.
  - `type CaseStudy = { id: string; title: string; summary: string; tech: string[]; demo?: string; order: number }`
  - `type CodeProject<C extends CaseStudy> = { title: string; summary: string; tech: string[]; demo?: string; featured: boolean; caseStudy?: C }`
  - `mergeProjects<C extends CaseStudy>(featured: FeaturedEntry[], cases: C[]): CodeProject<C>[]` — featured in README order (README title/summary/tech/url win; `demo` = README url ?? case demo), then unmatched cases by `order` asc with `featured: false`. Match = normalized URL equal to case `demo`, else normalized title equal (lowercase, non-alphanumerics removed). Each case matches at most once.

- [ ] **Step 1: Write failing tests** in `featured.test.ts` using `node:test` + `node:assert/strict`, importing `./featured.ts`:
  - `parses the real README`: read `../../../README.md`; expect 4 entries; titles `['FundiSwift','Apex Heights Suites','VeriDose','Chronicles of the Signal']`; `[0].url === 'https://fundiswift.co.ke'`; `[3].url === undefined`; `[2].tech` deep-equals `['Next.js','React','TypeScript','Firebase']`; `[0].summary === 'Service marketplace connecting customers with skilled professionals.'`.
  - `returns null without the section`: `parseFeatured('# Hi\n## Tech Stack\n')` is `null`.
  - `throws on empty section`: `parseFeatured('## Featured Projects\n\nnothing\n## Tech')` throws matching `/README\.md/`.
  - `handles CRLF, en dash, hyphen and missing tech line`: input `'## Featured Projects\r\n- **[A](https://a.app/)** – Alpha.  \r\n- **B** - Beta.\r\n  `x` · `y`\r\n## Next'` gives `[{title:'A',url:'https://a.app/',summary:'Alpha.',tech:[]},{title:'B',summary:'Beta.',tech:['x','y']}]` (B has no `url` key or `url` undefined).
  - `merges by url then title, leftovers by order`: cases `[{id:'qr',title:'Prescription QR Scanner',demo:'https://v.app',order:2,...},{id:'cos',title:'Chronicles of the Signal',order:3,...},{id:'inv',title:'Invoice',order:1,...},{id:'rps',title:'RPS',order:5,...}]`, featured `[{title:'F',url:'https://f.ke',...},{title:'VeriDose',url:'http://v.app/',...},{title:'Chronicles of the Signal',...}]`. Expect titles `['F','VeriDose','Chronicles of the Signal','Invoice','RPS']`; `caseStudy?.id` `[undefined,'qr','cos','inv','rps']`; `featured` `[true,true,true,false,false]`; `[1].demo === 'http://v.app/'`.

- [ ] **Step 2: Run** `npm test` in `portfolio/`. Expected: FAIL, cannot find module `./featured.ts`.

- [ ] **Step 3: Implement** `featured.ts` per Interfaces. Section = lines after the heading until the next line starting `## `. Bullet regex on each line: `^- \*\*(?:\[(.+?)\]\((.+?)\)|(.+?))\*\*\s*[—–-]\s*(.+?)\s*$`; the following line, if it is indented and contains backticks, gives tech via `/`([^`]+)`/g`. Split on `/\r?\n/`. URL normalize: lowercase, strip `^https?://`, strip trailing `/`.

- [ ] **Step 4: Run** `npm test`. Expected: all 5 tests PASS.

- [ ] **Step 5: Commit** `git add portfolio/src/lib/featured.ts portfolio/src/lib/featured.test.ts portfolio/package.json && git commit -m "feat(portfolio): parse README featured projects"`

### Task 2: Wire pages to the merged list

**Files:**
- Create: `portfolio/src/lib/code-projects.ts`
- Modify: `portfolio/src/pages/computer-science/index.astro`, `portfolio/src/pages/computer-science/[slug].astro`, `portfolio/src/pages/index.astro`, `.github/workflows/portfolio-ci.yml`

**Interfaces:**
- Consumes: `parseFeatured`, `mergeProjects`, `CodeProject` from Task 1.
- Produces: `getCodeProjects(): Promise<CodeProject<CollectionEntry<'cs-projects'> & CaseStudy-shaped>[]>` — reads `new URL('../../../README.md', import.meta.url)` with `fs.readFile`; on `ENOENT` warns `[featured] README.md not found; using case studies only` and passes `[]`; `parseFeatured` `null` also passes `[]`. Maps each collection entry to `CaseStudy` fields while keeping the entry (e.g. `{ id, ...data, entry }`) so pages can `render()` it. Memoized per build.

  Note: if `import.meta.url` resolves inside `dist/` or `.astro/` at build time, use `path.resolve(process.cwd(), '../README.md')` instead (cwd is `portfolio/` in CI and Workers Builds); verify in Step 2.

- [ ] **Step 1: Implement `getCodeProjects()`** in `code-projects.ts`.

- [ ] **Step 2: Code page** (`computer-science/index.astro`): replace the sorted collection with `getCodeProjects()`. Plate: title links to `/computer-science/${caseStudy.id}` when `caseStudy` exists, otherwise to `demo` in a new tab, otherwise plain text. Links list: "Case notes" only with `caseStudy`; "Live demo" with `demo`. Status label from `caseStudy?.data.status`; cover from `caseStudy?.data.cover`. Sanity list unchanged and numbered after.

- [ ] **Step 3: Detail page** (`[slug].astro`): `getStaticPaths` builds from `getCodeProjects()` filtered to those with `caseStudy`; `no` = index in the full merged list + 1; `next` = next project in the filtered list (wrapping). Page shows the merged `title`, `summary`, `tech`, `demo`; problem/role/status/cover/body from the case study.

- [ ] **Step 4: Home page** (`index.astro`): `lead` = first 3 of `getCodeProjects()` mapped to `{ title, href: caseStudy ? '/computer-science/'+id : demo ?? '/computer-science', tech }`; external hrefs get `target="_blank" rel="noopener noreferrer"`. Count = merged length + Sanity `cs` length. Remove the `featured.filter(p => p.category === 'cs')` lead; keep `featured` for the visual pick.

- [ ] **Step 5: CI**: add `"README.md"` to `on.pull_request.paths` in `portfolio-ci.yml`; add a `Unit tests` step `run: npm test` before `Type check`.

- [ ] **Step 6: Verify** in `portfolio/`: `npm test && npx astro check && npm run build`. Expected: tests pass, `0 errors`, build complete. Then `grep -o 'FundiSwift\|VeriDose\|Apex Heights Suites\|Chronicles of the Signal\|Supermarket Invoice App' dist/computer-science/index.html | uniq` lists them in that order; `ls dist/computer-science` shows the 5 case-study slugs; `grep -c 'Prescription QR Scanner' dist/computer-science/index.html` is `0`.

- [ ] **Step 7: Screenshot** `/computer-science` and `/` with the impeccable `shot` command at desktop and phone widths; confirm FundiSwift plate (no cover, no case notes) sits cleanly with the others.

- [ ] **Step 8: Commit** `git add -A portfolio/src .github/workflows/portfolio-ci.yml && git commit -m "feat(portfolio): Code section follows README featured projects"`
