import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { getCollection, type CollectionEntry } from 'astro:content';
import { parseFeatured, mergeProjects, type CaseStudy, type CodeProject, type FeaturedEntry } from './featured';

export type CaseStudyEntry = CaseStudy & { entry: CollectionEntry<'cs-projects'> };
export type CodeProjectItem = CodeProject<CaseStudyEntry>;

// The README sits at the repo root, one level above the Astro project (cwd is portfolio/ in dev, CI and Workers Builds).
const README = resolve(process.cwd(), '../README.md');

async function readFeatured(): Promise<FeaturedEntry[]> {
  let text: string;
  try {
    text = await readFile(README, 'utf8');
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code !== 'ENOENT') throw e;
    console.warn('[featured] README.md not found; using case studies only');
    return [];
  }
  return parseFeatured(text) ?? [];
}

let cached: Promise<CodeProjectItem[]> | undefined;

/** Code projects in display order: README featured list first, then the remaining case studies. */
export function getCodeProjects(): Promise<CodeProjectItem[]> {
  cached ??= (async () => {
    const [featured, entries] = await Promise.all([readFeatured(), getCollection('cs-projects')]);
    const cases = entries.map((entry): CaseStudyEntry => ({
      id: entry.id, title: entry.data.title, summary: entry.data.summary, tech: entry.data.tech,
      demo: entry.data.demo, order: entry.data.order, entry,
    }));
    return mergeProjects(featured, cases);
  })();
  return cached;
}
