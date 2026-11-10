import { defineField, defineType } from 'sanity';

export const categories = [
  { title: '2D Design', value: '2d' },
  { title: '3D Design', value: '3d' },
  { title: 'Photography', value: 'photography' },
  { title: 'Computer Science', value: 'cs' },
];

export const project = defineType({
  name: 'project',
  title: 'Project',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string', validation: (r) => r.required() }),
    defineField({
      name: 'slug', type: 'slug', options: { source: 'title', maxLength: 96 },
      validation: (r) => r.required(),
    }),
    defineField({
      name: 'category', type: 'string', options: { list: categories, layout: 'radio' },
      validation: (r) => r.required(),
    }),
    defineField({ name: 'summary', type: 'text', rows: 3, validation: (r) => r.required().max(240) }),
    defineField({ name: 'description', title: 'Longer description / case study', type: 'array', of: [{ type: 'block' }] }),
    defineField({
      name: 'coverImage', type: 'image', options: { hotspot: true },
      fields: [defineField({ name: 'alt', type: 'string', title: 'Alt text', validation: (r) => r.required() })],
      validation: (r) => r.required(),
    }),
    defineField({
      name: 'gallery', type: 'array',
      of: [{
        type: 'image', options: { hotspot: true },
        fields: [
          defineField({ name: 'alt', type: 'string', title: 'Alt text', validation: (r) => r.required() }),
          defineField({ name: 'caption', type: 'string' }),
        ],
      }],
    }),
    defineField({ name: 'tools', title: 'Tools / technologies', type: 'array', of: [{ type: 'string' }], options: { layout: 'tags' } }),
    defineField({ name: 'role', type: 'string' }),
    defineField({ name: 'demoUrl', type: 'url' }),
    defineField({ name: 'sourceUrl', type: 'url' }),
    defineField({
      name: 'client', title: 'Client / attribution', type: 'string',
      description: 'Only fill in when you have permission to publish it.',
    }),
    defineField({ name: 'featured', type: 'boolean', initialValue: false }),
    defineField({ name: 'order', title: 'Sort order', type: 'number', initialValue: 100, description: 'Lower numbers appear first.' }),
  ],
  orderings: [{ title: 'Sort order', name: 'order', by: [{ field: 'order', direction: 'asc' }] }],
  preview: { select: { title: 'title', subtitle: 'category', media: 'coverImage' } },
});
