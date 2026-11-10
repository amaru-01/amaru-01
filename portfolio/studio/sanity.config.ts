import { defineConfig } from 'sanity';
import { structureTool } from 'sanity/structure';
import { visionTool } from '@sanity/vision';
import { schemaTypes } from './schemaTypes';

// Fill in after creating the project at sanity.io/manage (the ID is public, not a secret).
const projectId = process.env.SANITY_STUDIO_PROJECT_ID || 'REPLACE_ME';
const dataset = process.env.SANITY_STUDIO_DATASET || 'production';

export default defineConfig({
  name: 'portfolio',
  title: 'Portfolio',
  projectId,
  dataset,
  plugins: [structureTool(), visionTool()],
  schema: { types: schemaTypes },
});
