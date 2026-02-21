# Interactive Embedding Controls -- Design Doc

**Date:** 2026-02-21
**Project:** sanderson-lore-visualization (Cosmere Knowledge Graph)

## Goal

Add an interactive controls panel to the web app that lets the user experiment with embedding-based tagging parameters. The graph recomputes on demand as settings change.

## Data Architecture

Two precomputed JSON files ship to the frontend:

**`embedding_scores_isolated.json`** (~1.8 MB, loaded immediately)

For the 52 isolated entities with reference embeddings, stores every entry-entity similarity score above a 0.55 floor.

```json
{
  "floor": 0.55,
  "entities": ["chasmfiends", "glyphs", "lashing", ...],
  "scores": {
    "12345": {"chasmfiends": 0.72, "glyphs": 0.68},
    "67890": {"lashing": 0.81, "windrunners": 0.76}
  }
}
```

Keys are entry IDs. Values are only the entity scores above the floor. Entries with no scores above the floor are omitted.

**`embedding_scores_all.json`** (~2.6 MB, lazy-loaded on toggle)

Same format but covers all 367 entities with a 0.65 floor. Fetched only when the user switches to "All entities" mode.

A new Python script `07_export_scores.py` generates both files from the cached numpy embeddings.

## Frontend Controls

A collapsible top bar styled to match the Stormlight theme. Single row layout (left to right):

```
[Embeddings v]  --*---------- 0.70  |  * Isolated  o All  |  [x] Must-bridge  |  [ Apply ]  |  +274 tags  +30 rescued  1,210 edges
```

- **"Embeddings" label** -- click to collapse/expand the bar
- **Threshold slider** -- range depends on mode (0.55-0.90 for isolated, 0.65-0.90 for all)
- **Entity scope radio** -- "Isolated" (default, loaded) vs "All" (triggers lazy fetch with loading spinner)
- **Must-bridge checkbox** -- on by default. When on, implicit tags only accepted if the entry has at least one other tag (explicit or implicit)
- **Apply button** -- click to recompute the graph. Shows "Recomputing..." during execution. No auto-recompute on slider drag.
- **Stats** -- three numbers updated after each Apply: implicit tags added, nodes rescued, total edges

## Client-Side Recomputation

Triggered by the Apply button. All computation runs in JS, no server.

**Step 1: Apply threshold.** For each entry in the scores file, check which entity scores exceed the current threshold.

**Step 2: Apply filters.**
- If "Isolated only": skip entities already connected in the baseline graph
- If "Must-bridge" on: two-pass approach. First pass collects all candidates. Second pass filters -- keep only if the entry has at least one other tag (explicit or implicit from another entity). This allows two implicit tags on the same entry to bridge each other.

**Step 3: Rebuild edges.** Merge explicit tags with surviving implicit tags. Count co-occurrences. Filter to weight >= 2. Diff against baseline to identify new edges and rescued nodes.

**Step 4: Update D3.** Add/remove edges, update node positions. New nodes get a stormlight pulse animation (~1s). Force simulation restarts with low alpha.

## "What Changed" Feedback

**After Apply:** Stats update. Nodes that gained/lost connections pulse. Embedding-derived edges render with distinct styling (dashed or different opacity).

**On click:** Right side panel shows connections as before. Embedding-derived connections show a label like "via embedding (0.74)". Implicitly tagged entries get a subtle indicator in the drill-down.

## New Files

- `notebooks/07_export_scores.py` -- generates the two score JSON files
- `data/embedding_scores_isolated.json` -- isolated entity scores (floor 0.55)
- `data/embedding_scores_all.json` -- all entity scores (floor 0.65)

## Notes

- The baseline graph (explicit tags only) is computed once on page load from entries.json and cached. The Apply recomputation layers implicit tags on top.
- Must-bridge two-pass handles the case where two isolated entities both score high on an entry with no explicit tags -- they bridge each other.
- Entries.json already contains explicit tags per entry, so no additional data needed for the baseline.
