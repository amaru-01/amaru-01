import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const csProjects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/cs-projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      summary: z.string(),
      problem: z.string().optional(),
      role: z.string().optional(),
      tech: z.array(z.string()).default([]),
      demo: z.url().optional(),
      source: z.url().optional(),
      status: z.enum(['live', 'in development', 'prototype']).optional(),
      // Optional screenshot, e.g. cover: ./images/supermarket.png (shown only when present)
      cover: image().optional(),
      coverAlt: z.string().optional(),
      order: z.number().default(100),
    }),
});

export const collections = { 'cs-projects': csProjects };
