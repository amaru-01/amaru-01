// Featured code projects come from the "## Featured Projects" list in the repo's root README.md,
// so a project is featured in one place for both the GitHub profile and this site.
// Pure functions only (no Astro imports) so they run under `node --test`.

export interface FeaturedEntry {
  title: string;
  url?: string;
  summary: string;
  tech: string[];
}

export interface CaseStudy {
  id: string;
  title: string;
  summary: string;
  tech: string[];
  demo?: string;
  order: number;
}

export interface CodeProject<C extends CaseStudy = CaseStudy> {
  title: string;
  summary: string;
  tech: string[];
  demo?: string;
  featured: boolean;
  caseStudy?: C;
}

const HEADING = /^##\s+Featured Projects\s*$/;
// - **[Title](url)** — summary   or   - **Title** — summary  (em dash, en dash or hyphen)
const BULLET = /^-\s+\*\*(?:\[(.+?)\]\((.+?)\)|(.+?))\*\*\s*[—–-]\s*(.+?)\s*$/;

/** Returns null when the README has no Featured Projects section; throws when the section has no readable entries. */
export function parseFeatured(readme: string): FeaturedEntry[] | null {
  const lines = readme.split(/\r?\n/);
  const start = lines.findIndex((l) => HEADING.test(l));
  if (start === -1) return null;

  const entries: FeaturedEntry[] = [];
  for (let i = start + 1; i < lines.length && !lines[i].startsWith('## '); i++) {
    const m = lines[i].match(BULLET);
    if (!m) continue;
    const next = lines[i + 1] ?? '';
    const tech = /^\s+\S/.test(next) && next.includes('`') ? [...next.matchAll(/`([^`]+)`/g)].map((t) => t[1].trim()) : [];
    entries.push({ title: (m[1] ?? m[3]).trim(), url: m[2]?.trim(), summary: m[4], tech });
  }
  if (entries.length === 0) {
    throw new Error('README.md has a "## Featured Projects" section but no entry could be read. Expected lines like: - **[Title](https://…)** — Summary.');
  }
  return entries;
}

const normUrl = (u?: string) => u?.toLowerCase().replace(/^https?:\/\//, '').replace(/\/+$/, '');
const normTitle = (t: string) => t.toLowerCase().replace(/[^a-z0-9]/g, '');

/** README entries first (README wins on title, summary, tech and link), then unmatched case studies by order. */
export function mergeProjects<C extends CaseStudy>(featured: FeaturedEntry[], cases: C[]): CodeProject<C>[] {
  const remaining = [...cases];
  const take = (pred: (c: C) => boolean) => {
    const i = remaining.findIndex(pred);
    return i === -1 ? undefined : remaining.splice(i, 1)[0];
  };

  const lead = featured.map((f): CodeProject<C> => {
    const url = normUrl(f.url);
    const caseStudy = (url ? take((c) => normUrl(c.demo) === url) : undefined) ?? take((c) => normTitle(c.title) === normTitle(f.title));
    return { title: f.title, summary: f.summary, tech: f.tech, demo: f.url ?? caseStudy?.demo, featured: true, caseStudy };
  });

  const rest = remaining
    .sort((a, b) => a.order - b.order)
    .map((c): CodeProject<C> => ({ title: c.title, summary: c.summary, tech: c.tech, demo: c.demo, featured: false, caseStudy: c }));

  return [...lead, ...rest];
}
