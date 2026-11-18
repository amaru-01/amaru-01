---
name: Paul Kimaru Portfolio
description: A whole practice raised from one line, set as numbered plates on cotton paper.
colors:
  paper: "#f2efe6"
  paper-hi: "#fbfaf6"
  ink: "#1c1c1c"
  graphite: "#5f5e5a"
  shade-mid: "#a8a8a8"
  shade-lt: "#d6d4cc"
  rule-soft: "#cfccc2"
  shell-hi: "#fcfbf7"
  shell-lo: "#dcd8cd"
  shell-edge: "#c2bdb0"
  shell-rim: "#b9b4a7"
  fold-mid: "#8d8a82"
  fold-dark: "#4f4e4a"
  paper-night: "#1b1a18"
  paper-hi-night: "#24231f"
  ink-night: "#ece8dd"
  graphite-night: "#a9a59a"
  shade-mid-night: "#6f6c64"
  shade-lt-night: "#3a3833"
  rule-soft-night: "#3d3b36"
  shell-hi-night: "#7a766b"
  shell-lo-night: "#4a4740"
  shell-edge-night: "#33312c"
  shell-rim-night: "#a29d90"
  fold-mid-night: "#2c2a26"
  fold-dark-night: "#0c0c0b"
typography:
  display:
    fontFamily: "Bodoni Moda Variable, Bodoni 72, Didot, serif"
    fontSize: "clamp(4rem, 10vw, 8.75rem)"
    fontWeight: 400
    lineHeight: 0.86
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Bodoni Moda Variable, Bodoni 72, Didot, serif"
    fontSize: "clamp(3.25rem, 9vw, 7rem)"
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Bodoni Moda Variable, Bodoni 72, Didot, serif"
    fontSize: "clamp(2.1rem, 4vw, 3.25rem)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.02em"
  lead:
    fontFamily: "Source Serif 4 Variable, Georgia, serif"
    fontSize: "1.3rem"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "Source Serif 4 Variable, Georgia, serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Bodoni Moda Variable, Bodoni 72, Didot, serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    letterSpacing: "0.01em"
rounded:
  none: "0"
  arch: "50% 50% 0 0 / 1.1rem 1.1rem 0 0"
  circle: "50%"
spacing:
  gutter-narrow: "1.25rem"
  gutter: "2.5rem"
  plate-inset: "2rem"
  section: "3.5rem"
  footer-gap: "6rem"
  container: "84rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.arch}"
    padding: "0.95rem 2rem 0.55rem"
    height: "3rem"
  button-primary-hover:
    backgroundColor: "{colors.graphite}"
    textColor: "{colors.paper}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.arch}"
    padding: "0.95rem 2rem 0.55rem"
    height: "3rem"
  button-secondary-hover:
    backgroundColor: "{colors.paper-hi}"
    textColor: "{colors.ink}"
  nav-link:
    textColor: "{colors.graphite}"
    typography: "{typography.label}"
  nav-link-active:
    textColor: "{colors.ink}"
  menu-toggle:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.circle}"
    size: "2.75rem"
  plate:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "1.75rem 0 2.25rem"
  figure-framed:
    backgroundColor: "transparent"
    rounded: "{rounded.none}"
    padding: "0.75rem 0.75rem 0.6rem"
---

# Design System: Paul Kimaru Portfolio

## Overview

**Creative North Star: "The Curved Crease Shell"**

Every page is one flat sheet of cream cotton paper ruled by a single sweeping charcoal crease, and the work is set along it as numbered plates. On the home page the line enters from the top of the sheet, becomes the crease, and the paper lifts into a shell beside the name; everywhere else the same line returns as a curved hairline under page titles, between panels and above the footer. The system is drawn, not built: depth comes from the folded paper, structure comes from hairlines, and colour is held to paper, ink and graphite.

Density is generous and editorial. Display type is a high-contrast inclined serif set very large; reading text is a calm optical-size serif at 18px. Nothing floats: there are no cards, no glass, no tinted panels. Work is shown as plates (a hairline above, an italic "Pl. n" number beside) and images keep their native proportions inside optional hairline frames. The dark scheme is the same sheet in graphite with cream ink, not an inverted theme.

This world replaced an earlier glassmorphism look; glass, blobs, gradient text and pill shapes are confirmed rejections.

**Key Characteristics:**
- One charcoal crease line per page, drawn once on load; curved hairlines rule every major division.
- Two type voices only: Bodoni Moda italic for display, labels and numbers; Source Serif 4 roman for reading.
- Arched buttons: a paper strip with one curved top edge, square at the base.
- Hairline-ruled plates numbered "Pl. n", never cards.
- Images never cropped; native aspect ratio, optional 1px soft frame.
- Monochrome warm neutrals in both schemes; no accent hue.

## Colors

A warm achromatic palette: cotton paper, soft-black ink and a ladder of graphite greys, re-cut for a graphite-paper dark scheme.

### Primary
- **Crease Ink** (ink): the one working colour. Body text, display type, the crease line, rules between plates, the primary button fill, focus outline and text selection. In the dark scheme it becomes cream ink (ink-night). The `--rule` token is an alias of ink in both schemes.

### Neutral
- **Cotton Paper** (paper): the ground of every page, overlaid with a fixed SVG fibre-noise texture (grain opacity 0.35 light, 0.18 dark, screen-blended in dark). Also the text colour on the primary button.
- **Highlight Paper** (paper-hi): the lifted sheet; used only as the secondary button's hover fill.
- **Graphite** (graphite): secondary text, labels, nav links at rest, figure captions, stack lists, plate numbers, and the primary button's hover fill. 5.6:1 on paper; 7:1 for graphite-night on night paper.
- **Soft Rule** (rule-soft): hairlines inside a group (list rows, fact lists, figure frames, the curved panel dividers on the home band).
- **Mid Shade** (shade-mid): resting underline colour on text links and the scrollbar thumb.
- **Light Shade** (shade-lt): placeholder fill behind images while they load.
- **Shell tones** (shell-hi, shell-lo, shell-edge, shell-rim, fold-mid, fold-dark): reserved for the authored paper-shell illustration: the lit face, its falloff, the rim light, and the turned-away fold. Not for UI chrome.

### Named Rules
**The Paper And Ink Rule.** The palette is paper, ink and graphite. There is no accent hue; emphasis comes from type size, italic voice and the crease, never from colour.

**The Shell Tones Stay In The Shell Rule.** The shell-* and fold-* tokens exist to light the folded sheet illustration. UI surfaces, buttons and text never use them.

## Typography

**Display Font:** Bodoni Moda Variable, italic only (with Bodoni 72, Didot, serif)
**Body Font:** Source Serif 4 Variable, optical sizing on (with Georgia, serif)

**Character:** An inclined, hairline-contrast Didone carries every voice that names or numbers something; a sturdy transitional text serif carries everything that is read. The pairing is all-serif and all-paper: engraved title page against a clean book page.

### Hierarchy
- **Display** (400 italic, clamp(4rem, 10vw, 8.75rem), 0.86): the name on the home page only.
- **Headline** (400 italic, clamp(3.25rem, 9vw, 7rem), 0.95): page titles; project detail and 404 titles run a step smaller (clamp to 6.5rem / 6rem).
- **Title** (400 italic, clamp(2.1rem, 4vw, 3.25rem), 1): plate titles, section headings and the "Next" link; home list titles at 1.5rem, the principle quote at clamp(1.75rem, 2.4vw, 2.25rem).
- **Lead** (400, 1.3rem, 1.45, max 44ch): one-line introductions under page titles; hero lede runs clamp(1.15rem, 1.6vw, 1.4rem) at 34ch.
- **Body** (400, 1.125rem, 1.6, max 65ch): reading text; about prose at 1.25rem.
- **Label** (400 italic, 0.9375rem, 0.01em, graphite): section labels, definition-list terms, status, the brand subtitle, the footer colophon. Nav links use the same italic voice at 1.05rem.

### Named Rules
**The Two Voices Rule.** Italic Bodoni names and numbers (titles, labels, nav, plate numbers, buttons); roman Source Serif is read. Never set reading text in the display face, never set a label in the text face, never use a sans or mono.

**The Lining Numbers Rule.** Plate numbers ("Pl. 1", "1", "404") are Bodoni italic in graphite with lining figures.

## Layout

A single centered sheet: 84rem maximum width with 1.25rem gutters, widening to 2.5rem from 640px. Pages open with a large italic title, an optional lead, and a full-width curved hairline arc (72px tall, rising left to right) before content. The home hero is a 5fr / 6fr split from 1024px (name and actions left, the shell right); below 1024px the shell shrinks to a 12.5rem corner piece and the crease enters from the sheet's top edge instead of the page.

Content is set as vertical runs of plates rather than grids of equal boxes. The project index uses a three-track plate (5rem number, fluid body, 13rem side column for status and links) from 900px. The home band is three panels (1.25fr / 1fr / 1fr) separated by curved soft-rule dividers, as panels of one folded sheet. Design work uses a staggered 12-column layout (7, 5 offset down 6rem, 7 inset); photography uses a two-column masonry wall from 900px. Vertical rhythm leans on large gaps: 3.5rem under page headings, 3 to 5rem between sections, 6rem above the footer.

The footer is ruled by a shallow curved hairline (a convex arc) and carries the wordmark, plain text links and an italic colophon.

## Elevation & Depth

The interface is flat. No UI element has a drop shadow, blur or backdrop; separation is by hairline and whitespace. All depth in the system lives in one authored illustration, the paper shell, where SVG radial and linear gradients light the face and fold, a feTurbulence grain textures the sheet, and two blurred shapes cast its shadow and contact point onto the page. The secondary button's 1px inset outline is a stroke, not elevation.

### Named Rules
**The Only Depth Is Paper Rule.** Shading, gradients and soft shadows belong to the folded sheet illustration and nowhere else. Buttons, plates, figures and nav stay flat on the page.

## Shapes

The form language is the crease: long, single-weight curves drawn as 1px non-scaling SVG strokes (1.4px for the hero crease). Curved hairlines replace straight rules at every major division (page-heading arc, home band rule, project-detail rule, footer fold, curved panel dividers). Within groups, rules are straight 1px lines.

Corners are square everywhere except two shapes: the arch (buttons, a strip with an elliptical top edge, 50% across and 1.1rem deep, square base) and the circle (the brand mark, the menu toggle, the arrow marker). The focus outline takes a 2px radius only so it does not read as a box.

### Named Rules
**The One Line Rule.** Every page carries one sweeping curved hairline; it is drawn once and never doubled, thickened or coloured.

## Components

### Buttons
Arched paper strips: tactile, quiet, unmistakably this world.
- **Shape:** curved top edge, square base (rounded.arch); minimum height 3rem; asymmetric padding (0.95rem top, 0.55rem bottom) so the italic sits low in the strip.
- **Primary:** ink fill, paper text, Bodoni italic 1.15rem. Hover shifts fill to graphite.
- **Secondary:** transparent with a 1px ink outline (inset), ink text. Hover fills with highlight paper.
- **Active:** presses down 1px. Transitions: transform 0.35s on the ease-out curve, colour 0.2s.
- **With marker:** outbound buttons carry the circle-arrow marker at 1rem after the label.
- **Text actions** beside buttons ("Download CV", "Ask me about this project") are underlined label-voice links, not a third button style.

### Links
- **Style:** inherit colour; 1px underline at 0.22em offset in mid shade, darkening to ink on hover.
- **Title links** (plate titles, list titles, "Next" link) rest without underline and gain a 1px underline on hover.

### Plates (cards)
- **Corner Style:** square (rounded.none).
- **Background:** none; the plate sits on the paper.
- **Shadow Strategy:** none (see Elevation).
- **Border:** 1px ink rule on top; the last plate in a run closes with a bottom rule. Inner lists use soft rules.
- **Number:** "Pl. n" in graphite Bodoni italic at 1.5rem, in its own leading column.
- **Internal Padding:** 1.75rem above, 2.25rem below; no side padding.

### Figures
- **Style:** image at its native aspect ratio (width 100%, height auto), never cropped or forced to a ratio; light-shade fill while loading.
- **Framed variant:** 1px soft-rule frame with 0.75rem inset, sized to the image (fit-content).
- **Caption:** 0.95rem graphite, prefixed by "Pl. n" with the title in ink Bodoni italic. Linked figures open the full-size image and dim to 0.92 opacity on hover.

### Navigation
- **Style:** brand mark (circle cut by a curved crease, 34px) plus the nickname in display italic 2rem; full name and city as a label from 1024px.
- **Links:** Bodoni italic 1.05rem in graphite, ink on hover; current page is ink with a 1px underline at 0.35em.
- **Mobile (below 768px):** a 2.75rem circular outlined toggle opens a list of ink links at 1.5rem, each row a 3.25rem soft-ruled line under an ink top rule. Escape and outside-click close it; without JavaScript the inline nav wraps instead.

### Definition Lists
- **Style:** label-voice terms over or beside body-voice values, each row separated by a soft rule (contact uses a 9rem term column). Used for project spec, about facts and contact channels.

### Circle-Arrow Marker
The world's only icon: a 1.1px hairline circle carrying a straight arrow (right) or a diagonal arrow (out), drawn in currentColor and sized in em. Used after outbound and "next" link text.

### Crease And Shell (signature)
The paper-shell SVG: a circular sheet lifted along one curved crease, lit face, graphite fold, rim light, fibre grain and a cast shadow. The crease line draws in once on load (1.8s on the ease-out curve, 0.15s delay) and the hero actions rise 12px into place (1.1s, 0.5s delay). Scrolling the first 80% of the viewport swings the fold's inner edge outward so the fold deepens. With reduced motion, or without JavaScript, everything renders in its settled state and the scroll response is off. Page-heading arcs reuse the same one-time draw.

## Do's and Don'ts

### Do:
- **Do** set every page on cotton paper with the fibre texture, and switch to graphite paper with cream ink for the dark scheme using the -night tokens.
- **Do** rule major divisions with a single 1px curved hairline (non-scaling stroke) and divisions inside a group with straight soft rules.
- **Do** use the arched strip for every button: ink fill for the one primary action, ink outline for the secondary.
- **Do** present work as numbered plates ("Pl. n", Bodoni italic, graphite) under a 1px ink rule.
- **Do** show images at their native proportions; frame with a 1px soft rule when an image sits among text.
- **Do** use the circle-arrow marker for outbound and next links.
- **Do** draw the crease once and render the settled state under prefers-reduced-motion.
- **Do** hide missing content (CV, screenshots, empty sections) rather than filling it with placeholders.

### Don't:
- **Don't** use glass, frosted panels, backdrop blur or translucent overlays.
- **Don't** use blobs, organic gradient shapes or gradient text.
- **Don't** use pill shapes or fully rounded rectangles; the only curves are the arch and the circle.
- **Don't** put drop shadows on UI; gradients and soft shadow belong only to the shell illustration.
- **Don't** place eyebrows or kickers above headings; a plate number is the only small text allowed beside a title.
- **Don't** use unicode arrows or glyph icons; use the circle-arrow SVG marker.
- **Don't** introduce an accent colour, a sans-serif or a monospace face.
- **Don't** crop images to a fixed ratio or tile work as equal cards in a grid.
