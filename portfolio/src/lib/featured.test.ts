import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseFeatured, mergeProjects, type CaseStudy } from './featured.ts';

test('parses the real README', () => {
  const readme = readFileSync(new URL('../../../README.md', import.meta.url), 'utf8');
  const entries = parseFeatured(readme)!;
  assert.equal(entries.length, 4);
  assert.deepEqual(entries.map((e) => e.title), ['FundiSwift', 'Apex Heights Suites', 'VeriDose', 'Chronicles of the Signal']);
  assert.equal(entries[0].url, 'https://fundiswift.co.ke');
  assert.equal(entries[3].url, undefined);
  assert.deepEqual(entries[2].tech, ['Next.js', 'React', 'TypeScript', 'Firebase']);
  assert.equal(entries[0].summary, 'Service marketplace connecting customers with skilled professionals.');
});

test('returns null without the section', () => {
  assert.equal(parseFeatured('# Hi\n## Tech Stack\n'), null);
});

test('throws on empty section', () => {
  assert.throws(() => parseFeatured('## Featured Projects\n\nnothing\n## Tech'), /README\.md/);
});

test('throws on a malformed bullet instead of dropping it', () => {
  const md = '## Featured Projects\n- **[A](https://a.app)** — Ok.\n- **[B](https://b.app)** Missing dash.\n## Next';
  assert.throws(() => parseFeatured(md), /README\.md.*line 3/);
});

test('handles CRLF, en dash, hyphen and missing tech line', () => {
  const md = '## Featured Projects\r\n- **[A](https://a.app/)** – Alpha.  \r\n- **B** - Beta.\r\n  `x` · `y`\r\n## Next';
  const entries = parseFeatured(md)!;
  assert.deepEqual(entries.map(({ title, url, summary, tech }) => ({ title, url, summary, tech })), [
    { title: 'A', url: 'https://a.app/', summary: 'Alpha.', tech: [] },
    { title: 'B', url: undefined, summary: 'Beta.', tech: ['x', 'y'] },
  ]);
});

test('shows only README projects when the README lists any', () => {
  const c = (id: string, title: string, order: number, demo?: string): CaseStudy => ({ id, title, summary: '', tech: [], demo, order });
  const merged = mergeProjects([{ title: 'RPS', summary: '', tech: [] }], [c('inv', 'Invoice', 1), c('rps', 'RPS', 5)]);
  assert.deepEqual(merged.map((p) => p.caseStudy?.id), ['rps']);
});

test('falls back to all case studies by order when the README lists none', () => {
  const c = (id: string, title: string, order: number): CaseStudy => ({ id, title, summary: '', tech: [], order });
  const merged = mergeProjects([], [c('rps', 'RPS', 5), c('inv', 'Invoice', 1)]);
  assert.deepEqual(merged.map((p) => p.caseStudy?.id), ['inv', 'rps']);
  assert.deepEqual(merged.map((p) => p.featured), [false, false]);
});

test('merges by url then title', () => {
  const c = (id: string, title: string, order: number, demo?: string): CaseStudy => ({ id, title, summary: '', tech: [], demo, order });
  const cases = [
    c('qr', 'Prescription QR Scanner', 2, 'https://v.app'),
    c('cos', 'Chronicles of the Signal', 3),
    c('inv', 'Invoice', 1),
    c('rps', 'RPS', 5),
  ];
  const featured = [
    { title: 'F', url: 'https://f.ke', summary: '', tech: [] },
    { title: 'VeriDose', url: 'http://v.app/', summary: '', tech: [] },
    { title: 'Chronicles of the Signal', summary: '', tech: [] },
  ];
  const merged = mergeProjects(featured, cases);
  assert.deepEqual(merged.map((p) => p.title), ['F', 'VeriDose', 'Chronicles of the Signal']);
  assert.deepEqual(merged.map((p) => p.caseStudy?.id), [undefined, 'qr', 'cos']);
  assert.deepEqual(merged.map((p) => p.featured), [true, true, true]);
  assert.equal(merged[1].demo, 'http://v.app/');
});
