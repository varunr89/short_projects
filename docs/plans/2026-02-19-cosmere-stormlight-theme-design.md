# Cosmere Knowledge Graph -- Stormlight Archive Theme Redesign

**Date:** 2026-02-19
**Status:** Approved
**Project:** sanderson-lore-visualization

## Overview

Full visual overhaul of the Cosmere Knowledge Graph (Words of Brandon) interactive D3.js visualization, themed around the Knight Radiant gemstone system from Brandon Sanderson's Stormlight Archive.

## Design Decisions

- **Theme:** Gemstone/Knight Radiant Orders -- each entity type maps to a Radiant gemstone
- **Depth:** Full overhaul -- animated background, custom loading screen, reimagined panel, gemstone nodes, title header
- **No layout changes to interaction model** -- focus/unfocus, search, filters, drill-down all stay the same

---

## 1. Color System & Typography

### Gemstone Palette

| Entity    | Gemstone  | Node Fill  | Glow       | CSS Variable      |
|-----------|-----------|------------|------------|--------------------|
| Character | Sapphire  | `#2E5BA8`  | `#4A8BDF`  | `--gem-sapphire`   |
| World     | Emerald   | `#2D8B57`  | `#3FBF7F`  | `--gem-emerald`    |
| Magic     | Amethyst  | `#7B4BAA`  | `#A66ED8`  | `--gem-amethyst`   |
| Shard     | Heliodor  | `#C49A2A`  | `#E8C44A`  | `--gem-heliodor`   |
| Concept   | Ruby      | `#B03A3A`  | `#D45A5A`  | `--gem-ruby`       |

### Background

- Deep blue-black: `#080C14`
- Radial gradient to dark navy at edges: `#0E1524`
- Vibe: looking into a gemheart cavern

### Typography

- **Title/Headers:** Cormorant Garamond (Google Fonts) -- fantasy chapter-heading feel
- **Body/UI text:** system-ui -- clean and readable for data-heavy panels
- **Node labels:** sans-serif for legibility at small sizes

### Accent Colors

- Stormlight white-blue: `#C8DFFF` (text highlights)
- Crem stone grey: `#2A2F3A` (borders/dividers)
- Frost: `rgba(200, 220, 255, 0.05)` (glass panel surfaces)

---

## 2. Animated Stormlight Background

Canvas layer behind the SVG graph:

- **Particles:** ~60-80 small soft circles, gaussian blur, white-blue (`#C8DFFF`) at 10-15% opacity
- **Drift:** Slow upward with gentle sine-wave wobble. Respawn at bottom when leaving top.
- **Depth layers:** 2 layers at different speeds (slow background, faster foreground) for parallax
- **Performance:** Separate canvas, `requestAnimationFrame`, particle pool. Pauses when tab hidden.
- **Interaction:** Purely decorative. When a node is focused, nearby particles subtly shift to that node's gemstone hue.

---

## 3. Gemstone Nodes & Graph Rendering

### Node Shape

- Hexagonal/octagonal SVG path (faceted gemstone silhouette)
- Small nodes: simple hexagons. Large nodes: more facets.
- Inner highlight to suggest a cut facet.

### Node Glow

- SVG `<filter>` with `feGaussianBlur` behind each node
- Glow color matches gemstone type
- Larger nodes glow brighter/wider
- Focused nodes: glow intensifies (freshly infused sphere)

### Node Sizing

- Same sqrt scale, range `4` to `26`

### Edges

- Gradient stroke between two connected gemstone colors
- Rest opacity: `0.15`
- Focus: connected edges brighten and pulse once (CSS animation) -- Stormlight flowing along a Connection

### Focus Behavior

- Focused gemstone scales up 1.3x, glow intensifies
- Connected nodes keep full opacity with softer glow boost
- Unconnected fade to ~5%
- Camera zooms/pans to center

### Labels

- Threshold: entryCount >= 30
- Color: Stormlight white-blue (`#C8DFFF`)
- Faint text-shadow glow matching node's gemstone color

---

## 4. Loading Screen

- **Background:** Same cavern background, particle system already running
- **Center:** Bridge Four glyph as SVG, drawn via `stroke-dasharray`/`stroke-dashoffset` over ~2 seconds in Stormlight white-blue with glow
- **Text:** "Connecting the Cosmere..." in Cormorant Garamond, fades in after glyph draws, pulsing opacity
- **Transition:** Glyph/text fade out over 500ms, graph fades in. Particles persist.
- **Minimum display:** 2 seconds (let animation finish even if data loads fast)

---

## 5. Title Header

Pinned top-left, replaces current search-box area:

- **Title:** "Cosmere Knowledge Graph" in Cormorant Garamond, ~20px, Stormlight white-blue
- **Subtitle:** "Words of Brandon" in system-ui, ~12px, muted grey
- **Search:** Below title, crem-stone border, gemstone-blue focus glow
- **Divider:** Faint horizontal line with gradient through gemstone colors
- Frosted glass treatment, compact

---

## 6. Reimagined Side Panel

### Panel Surface

- Dark frosted glass: `rgba(10, 14, 24, 0.92)`, `backdrop-filter: blur(20px)`
- Left border glows the focused entity's gemstone color

### Header

- Entity name in Cormorant Garamond, ~24px, gemstone hue
- Type badge as gemstone-shaped pill with inner glow
- Entry count in muted Stormlight white-blue
- Horizontal divider: gemstone color fading to transparent

### Connections List

- Section headers: Cormorant Garamond, gemstone color
- Each row: tiny gemstone dot indicator on left
- Weight badges: rounded pills with faint glow
- Hover: row background tints to connected entity's gemstone color

### WoB Entries

- Cards: subtle left-border accent in focused node's gemstone color
- Brandon's lines: Stormlight white-blue
- Questioner lines: muted grey
- Event/date: small decorative dot before it
- Tags: tiny muted gemstone pills

### Animation

- Slide in from right with content fade-in
- Gemstone glow border animates dim to full over 300ms
- Close button glows on hover in panel's gemstone color
