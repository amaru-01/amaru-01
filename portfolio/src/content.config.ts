import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const csProjects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/cs-projects' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    problem: z.string().optional(),
    role: z.string().optional(),
    tech: z.array(z.string()).default([]),
    demo: z.url().optional(),
    source: z.url().optional(),
    order: z.number().default(100),
  }),
});

export const collections = { 'cs-projects': csProjects };
