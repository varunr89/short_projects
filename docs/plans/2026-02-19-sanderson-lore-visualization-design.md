# Cosmere Knowledge Graph — Design

**Date:** 2026-02-19
**Project:** `sanderson-lore-visualization`
**Status:** Approved

## Goal

Build an interactive Cosmere knowledge graph powered by 16,282 Words of Brandon (WoB) entries. The primary experience is a relationship map — see how characters, worlds, magic systems, and Shards connect — with WoB entries as grounded citations you can drill into.

## Milestone 1: Tag Co-occurrence Graph

### Data Pipeline (Python)

1. **Load** 16K WoB entries from `words-of-brandon/wob_entries.json`
2. **Classify tags** — Use Claude API to categorize all 886 unique tags into:
   - Character (hoid, kelsier, kaladin, vin, dalinar...)
   - World/Location (roshar, scadrial, sel...)
   - Magic System (allomancy, surgebinding, awakening, feruchemy...)
   - Shard (odium, honor, preservation...)
   - Concept (investiture, cognitive realm, realmatic theory...)
   - Book (stormlight archive, warbreaker, elantris...)
   - Meta → skip (rafo, writing, favorites, inspirations, writing process...)
3. **Build co-occurrence matrix** — For every pair of non-meta tags on the same WoB entry, count shared entries. This becomes the edge weight.
4. **Output `graph.json`**:
   - `nodes`: `[{id, label, type, entryCount}]`
   - `edges`: `[{source, target, weight, entryIds}]`
5. **Output `entries.json`** — Cleaned WoB entries: strip HTML tags, keep speaker, text, tags, event name, date, entry ID.

### Frontend (Single HTML file, no build step)

**Technology:** D3.js force-directed graph, vanilla JS, inline CSS.

**Layout:**
- Full-width graph canvas
- Collapsible side panel (right)
- Search box (top-left overlay)
- Entity type filter toggles (top-right overlay)

**Graph behavior:**
- On load: full graph visible with force-directed layout. Nodes cluster naturally by connection density.
- Nodes colored by entity type, sized by entry count.
- Edges weighted by co-occurrence count (thicker = more shared entries).
- Hover: tooltip with entity name, type, entry count.

**Search & focus:**
- Type "Hoid" → graph animates to center on Hoid node.
- Connected nodes stay bright; everything else dims to ~10% opacity.
- Click any node → same focus behavior.
- Double-click node → expand one level deeper (connections of connections).
- Escape or click background → reset to full graph view.

**Filter toggles:**
- Show/hide by entity type: Character, World, Magic System, Shard, Concept, Book.

**Side panel (on node focus):**
- Header: entity name, type badge, "N entries" count.
- **Connections** grouped by entity type, sorted by edge weight.
  - e.g., "Characters: Kelsier (47), Vasher (32), Kaladin (18)..."
- Click a connection → **Entries** section shows WoB conversations where both tags co-occur.
- Entries displayed as readable Q&A threads with event name and date.
- Each entry collapsible (show first 2 lines, expand for full conversation).

**Color scheme:**
- Characters: blue
- Worlds/Locations: green
- Magic Systems: purple
- Shards: gold
- Concepts: orange
- Books: gray

### File Structure

```
sanderson-lore-visualization/
├── README.md
├── requirements.txt
├── data/
│   ├── tag_classifications.json   ← LLM output: {tag: type}
│   ├── graph.json                 ← nodes + edges
│   └── entries.json               ← cleaned WoB entries
├── notebooks/
│   ├── 01_classify_tags.py        ← Claude API tag classification
│   └── 02_build_graph.py          ← co-occurrence matrix → graph.json
├── charts/                        ← (visualizations for blog post)
└── post/
    └── draft.md
```

### Future Milestones (not in scope now)

- **Milestone 2: LLM enrichment** — Extract relationship labels ("carried", "created", "visited") and per-entity summaries from WoB text.
- **Milestone 3: Semantic search** — Embed WoB entries, allow natural language queries like "What does Brandon say about Hoid's age?"
- **Milestone 4: Blog post** — Write up the project as a blog post with static screenshots.
