# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary: people hiring developers.** Recruiters, hiring managers and tech leads skimming in under a minute, usually on a laptop, sometimes on a phone from a LinkedIn or CV link. Their job: decide whether Paul can build real software and is worth an interview.
- **Secondary: design and photography clients.** They want to see range and taste in 2D/3D design; full photography work lives on T.C.O.A Photography (separate site), and this site shows a strong selection and sends them there.

## Product Purpose

Personal portfolio of Mwangi Paul Kimaru ("Amaru"), a University of Nairobi Computer Science graduate based in Nairobi, Kenya. It proves engineering ability first (full-stack web and mobile, AI integration, data) and shows visual craft (graphic design, 3D, photography) as range. Success: a hiring visitor reaches a concrete project, its proof (demo, source, screenshots) and a way to contact him or get his CV within seconds.

## Positioning

A developer who is also a working designer and photographer: the projects are engineered and visually considered by the same person. The site itself should be the proof of that combination.

## Operating Context

- Static Astro 6 site, Tailwind 4; Code projects are local Markdown in `src/content/cs-projects/`; 2D, 3D, photography and featured work come from Sanity CMS (published only), rebuilt on publish via a deploy hook.
- Hosting is moving from Netlify to Cloudflare Pages (`paul-kimaru-portfolio.pages.dev`).
- Visitors arrive from GitHub (`github.com/amaru-01`), LinkedIn and a CV.

## Capabilities and Constraints

- Pages: Home, Code (computer science), Design (2D and 3D), Photography (selection + link to T.C.O.A), About, Contact, 404.
- Must keep: Sanity content pipeline, light and dark support, keyboard and screen-reader access, reduced-motion support, SEO metadata.
- Phone number and referees are never published. Company projects (FundiSwift, MkulimaMdogo, Adept chatbots) are not listed without employer permission.
- Undecided: per-project case-study pages (wanted), CV file (owner to provide), custom domain.

## Brand Commitments

- Name: Paul Kimaru, nickname Amaru. Photography brand: T.C.O.A Photography (tcoaphotography.netlify.app).
- The owner chose a "quiet gallery" register for the redesign: the work at large scale on a neutral ground with almost no interface around it. Explicitly rejected: glassmorphism, blurred colour blobs, gradient text, generic SaaS-landing look.

## Evidence on Hand

- Five Code projects with real stacks and links: Supermarket Invoice App (Next.js, Neon Postgres), Prescription QR Scanner (Next.js, Firestore; live demo), Chronicles of the Signal (Godot 4 cyberpunk RPG, in progress), WebAR Real Estate Preview, Rock Paper Scissors AI (Python, OpenCV, MediaPipe).
- Two photographs in Sanity (graduation portrait, dog portrait). No 2D/3D design pieces yet; the owner will upload 4-6. No project screenshots, portrait of Paul or CV yet. Do not fabricate testimonials, clients, metrics or employers.

## Product Principles

1. Proof before claims: every project shows what it is and links to demo or source.
2. The work leads; the interface recedes.
3. Engineering first for hiring visitors, visual craft as visible range, never an equal three-way split.
4. Content must be addable from the CMS without code changes.
5. Honest empty states: a section without work is hidden, never shown as a placeholder.
