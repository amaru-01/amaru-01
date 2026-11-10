// Central site config. Every [PLACEHOLDER] must be replaced before launch (see PLACEHOLDERS.md).
export const site = {
  name: '[PLACEHOLDER] Amaru',
  title: '[PLACEHOLDER] Computer Science, Design & Photography',
  description:
    '[PLACEHOLDER] Portfolio of computer science projects, 2D and 3D design, and photography.',
  email: '[PLACEHOLDER] hello@example.com',
  // Source repo for now; swap for the live Netlify URL once the photography site is hosted.
  photographyUrl: 'https://github.com/amaru-01/tcoaphotograph',
  github: 'https://github.com/amaru-01',
};

export const nav = [
  { href: '/computer-science', label: 'Code' },
  { href: '/design', label: 'Design' },
  { href: '/photography', label: 'Photography' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];
