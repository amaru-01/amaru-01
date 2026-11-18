import { createClient } from '@sanity/client';
import { createImageUrlBuilder } from '@sanity/image-url';

const projectId = import.meta.env.SANITY_PROJECT_ID;
const dataset = import.meta.env.SANITY_DATASET || 'production';
const token = import.meta.env.SANITY_READ_TOKEN; // read-only; used at build time only, never sent to the browser

export const sanityConfigured = Boolean(projectId);

// 'published' perspective guarantees drafts are never returned.
export const client = sanityConfigured
  ? createClient({ projectId, dataset, apiVersion: '2025-01-01', useCdn: false, perspective: 'published', token })
  : null;

const builder = projectId ? createImageUrlBuilder({ projectId, dataset }) : null;

export interface SanityImage { asset?: unknown; alt?: string; caption?: string; }

export interface Project {
  _id: string;
  title: string;
  slug: string;
  category: '2d' | '3d' | 'photography' | 'cs';
  summary: string;
  coverImage: SanityImage;
  gallery?: SanityImage[];
  tools?: string[];
  role?: string;
  demoUrl?: string;
  sourceUrl?: string;
  client?: string;
  featured?: boolean;
}

/** Responsive image URL (WebP, width-capped). Without a height the image keeps its own proportions. */
export function imgUrl(src: SanityImage, width = 800, height?: number): string | undefined {
  if (!builder || !src?.asset) return undefined;
  let b = builder.image(src as never).width(width).auto('format').quality(80);
  if (height) b = b.height(height).fit('crop');
  return b.url();
}

const fields = `_id, title, "slug": slug.current, category, summary, coverImage, "gallery": coalesce(gallery, []), "tools": coalesce(tools, []), role, demoUrl, sourceUrl, client, featured`;

/** Returns [] when the CMS isn't configured or unreachable, so the site still builds. */
const cache = new Map<string, Promise<Project[]>>();

async function fetchProjects(filter: string, params: Record<string, string> = {}): Promise<Project[]> {
  if (!client) return [];
  try {
    return await client.fetch(`*[_type == "project" && ${filter}] | order(order asc, _createdAt desc){${fields}}`, params);
  } catch (e) {
    console.warn('[sanity] fetch failed; rendering empty state:', (e as Error).message);
    return [];
  }
}

export const getProjectsByCategory = (category: Project['category']) => {
  if (!cache.has(category)) cache.set(category, fetchProjects('category == $category', { category }));
  return cache.get(category)!;
};

/** Design appears in navigation only once there is published 2D or 3D work. */
export async function hasDesignWork(): Promise<boolean> {
  const [a, b] = await Promise.all([getProjectsByCategory('2d'), getProjectsByCategory('3d')]);
  return a.length + b.length > 0;
}

/** Native aspect ratio from a Sanity asset id like image-abc-4000x6000-jpg. */
export function imgRatio(src?: SanityImage): number | undefined {
  const ref = (src?.asset as { _ref?: string } | undefined)?._ref;
  const m = ref?.match(/-(\d+)x(\d+)-/);
  return m ? Number(m[1]) / Number(m[2]) : undefined;
}
export const getFeaturedProjects = () => fetchProjects('featured == true');
