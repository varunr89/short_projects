# Interactive Embedding Controls -- Design Doc (v2)

**Date:** 2026-02-21
**Project:** sanderson-lore-visualization (Cosmere Knowledge Graph)
**Revision:** v2 -- incorporates Codex 5.3 feedback on per-entity calibration, hub penalties, margin constraints, multi-prototype references, hypothesis layer, and review panel.

## Goal

Add an interactive controls panel to the web app that lets the user experiment with all embedding-based tagging parameters. The graph recomputes on demand as settings change. Implicit (embedding-derived) edges are visually distinct from explicit (text-matched) edges, and the user can review individual implicit tags to build a ground-truth evaluation set.

---

## 1. Algorithm Improvements

### 1a. Per-Entity Calibration

**Problem:** A single global threshold treats all entities the same. But "Hoid" (hundreds of entries, diverse topics) has a very different score distribution than "chasmfiends" (a handful of focused entries).

**Solution:** Entity-specific thresholds derived from each entity's own explicit-tag score distribution.

For each entity with reference embeddings:
1. Compute cosine similarity between the entity's reference vector and every entry that is explicitly tagged with that entity.
2. Record the distribution (mean, std, percentiles) of those scores.
3. The entity's threshold = the Nth percentile of its explicit-entry scores, where N is a user-controlled "calibration percentile."

Example: If chasmfiends' explicitly-tagged entries score [0.78, 0.74, 0.81, 0.76, 0.79], the p25 is ~0.76. Any entry scoring above 0.76 against chasmfiends is in the range where explicit entries live -- so it's likely relevant.

**Precomputed data (per entity):**
```json
{
  "chasmfiends": {
    "mean": 0.77, "std": 0.03,
    "percentiles": {"p10": 0.73, "p25": 0.76, "p50": 0.78}
  }
}
```

**UI knob:** "Calibration percentile" slider (p10 to p50). Lower = looser (more tags), higher = stricter.

### 1b. Hub Penalties (Specificity Score)

**Problem:** Broad entities like "cosmere" and "realmatic theory" score moderately against everything because their reference vectors are the average of all Cosmere content -- they are the centroid of the whole space.

**Solution:** IDF-style specificity score per entity.

```
specificity(entity) = log(total_entries / entries_above_floor)
```

Where `entries_above_floor` = number of entries scoring above a low floor (e.g., 0.40) against this entity. High specificity = niche entity (good). Low specificity = hub (suspect).

Example:
- "chasmfiends": 200 entries above floor out of 16,282 -- specificity = 4.4 (very specific)
- "cosmere": 14,000 entries above floor -- specificity = 0.15 (hub, nearly everything matches)

**Precomputed data (per entity):**
```json
{
  "chasmfiends": {"specificity": 4.4, "entries_above_floor": 200},
  "cosmere": {"specificity": 0.15, "entries_above_floor": 14000}
}
```

**UI knob:** "Min specificity" slider. Entities below the cutoff are excluded from tagging. Replaces the crude "isolated vs all" toggle -- you can include all entities but let hub penalties naturally filter the generic ones.

### 1c. Margin Constraints

**Problem:** An entry about "Roshar magic in general" scores 0.74 against fabrials, 0.72 against spren, and 0.71 against soulcasting. It's not really about any of them specifically -- it's equally mediocre against all three.

**Solution:** For each entry, require that accepted implicit tags score within a margin of the best-scoring entity for that entry.

For each candidate implicit tag on an entry:
```
if (best_score - this_score) > margin:
    reject
```

Example with margin = 0.05:
- fabrials: 0.74, gap = 0.00 -- keep
- spren: 0.72, gap = 0.02 -- keep
- soulcasting: 0.71, gap = 0.03 -- keep
- chasmfiends: 0.58, gap = 0.16 -- reject

Example with a focused entry (margin = 0.05):
- chasmfiends: 0.82, gap = 0.00 -- keep
- greatshells: 0.73, gap = 0.09 -- reject (only chasmfiends survives)

**UI knob:** "Confidence margin" slider (0.00 to 0.15). At 0.00, no margin filtering. At 0.10+, usually keeps only the single best-matching entity per entry.

### 1d. Multi-Prototype References

**Problem:** Each entity gets one reference vector (centroid of all its tagged entries). But entities that appear in diverse contexts get a mushy average. Example: Hoid appears in worldhopping lore, Stormlight scenes, and Warbreaker crossover discussions. The centroid is a blend of all three, matching none well.

**Solution:** Cluster each entity's tagged entries using k-means. Store multiple prototype vectors. Score against all prototypes and take the max.

Prototype count rules (user-adjustable):
- **3-4 entries:** 1 prototype (centroid, same as today)
- **5-9 entries:** 2 prototypes
- **10+ entries:** 3 prototypes

Example:
```
Entry about Hoid worldhopping:
  vs Hoid_proto_A (worldhopping cluster):  0.81  <- max, used as score
  vs Hoid_proto_B (Stormlight scenes):     0.69
  vs Hoid_proto_C (Warbreaker crossover):  0.64
```

**Precomputed data (per entity):** Multiple reference vectors per entity, plus cluster membership for each tagged entry.

**UI knobs:**
- "2-proto min" slider -- entry count needed for 2 prototypes (default: 5)
- "3-proto min" slider -- entry count needed for 3 prototypes (default: 10)

---

## 2. Hypothesis Layer

**Problem:** Implicit edges (from embeddings) and explicit edges (from text co-occurrence) are visually indistinguishable. Users can't tell which connections are established facts vs algorithmic suggestions.

**Solution:** Each edge carries a `type` field. The visualization renders them differently.

**Edge types:**
```json
{"source": "nicrosil", "target": "forgery", "weight": 3, "type": "implicit", "confidence": 0.78}
{"source": "kaladin", "target": "bridge-four", "weight": 47, "type": "explicit"}
```

**Visual treatment:**
- **Explicit edges:** Solid lines (current behavior)
- **Implicit edges:** Dashed lines, slightly transparent, amber/gold color (vs current gray)
- **Hover on implicit edge:** Tooltip shows "Suggested connection (confidence: 0.78) -- based on 3 entries where embedding similarity exceeded threshold"

**UI knob:** Edge layer toggle with three states:
- **Explicit only** -- baseline graph, no embedding edges
- **Both** -- both layers, visually distinct (default)
- **Implicit only** -- only embedding-discovered edges

---

## 3. Review Panel

A collapsible right-side drawer for human-in-the-loop validation of implicit tags.

**Table columns:**
```
Entity          Entry (truncated)                     Score   Status
nicrosil        "Can Identity be stored in metal..."  0.78    [ ? ]
forgery         "How does Forging interact with..."   0.76    [ ? ]
chasmfiends     "Are chasmfiends attracted to..."     0.82    [ v ]
worldspire      "When is the next Alcatraz..."        0.54    [ x ]
```

**Status values:**
- `?` -- unreviewed (default)
- `v` -- confirmed (click "keep")
- `x` -- rejected (click "reject")

**Interactions:**
- Clicking a row highlights the entry and entity in the graph
- Sort by score (lowest first to find weakest links), by entity, or by status
- Filter to unreviewed only

**Persistence:**
- "Save Reviews" exports decisions to `reviews.json`
- "Load Reviews" imports previous decisions
- Reviewed tags persist across Apply clicks -- if you change threshold and re-apply, tags that still exist keep their review status

**Why:** Over time, reviewed tags become the evaluation dataset for tuning all other knobs. Replaces ad-hoc Python sampling with systematic in-context validation.

---

## 4. UI Layout

### Top Bar (always visible)
```
[Model: v azure_openai]  [Scope: o Isolated  o All]  [Apply]  [Stats: 274 tags, 30 rescued, 12 reviewed]
```

### Tuning Panel (collapsible, below top bar)
```
Threshold ----------- [====*========] 0.70
Calibration %ile ---- [====*========] p25
Min Specificity ----- [====*========] 2.0
Confidence Margin --- [====*========] 0.05
2-Proto Min --------- [====*========] 5
3-Proto Min --------- [====*========] 10
Edge Layer ---------- o Explicit  * Both  o Implicit
Must-Bridge --------- [x]
```

### Review Panel (right drawer, toggled by button)
```
[Review Tags (274)]  [Sort: v Score]  [Filter: v Unreviewed]
---
nicrosil -> entry 54321          0.78  [v] [x]
forgery -> entry 54322           0.76  [v] [x]
...
[Save Reviews]  [Load Reviews]
```

### Graph (center stage)
- Solid lines = explicit edges
- Dashed amber lines = implicit edges
- Pulse animation on newly rescued nodes after Apply

---

## 5. Data Architecture

### Precomputed by Python (07_export_scores.py)

**`scores.json`** (~2-3 MB)

For each entity with reference embeddings, stores:
- Per-entry similarity scores (only entries above a floor of 0.30)
- Entity calibration stats (mean, std, percentiles of explicit-entry scores)
- Entity specificity score (IDF value, entries_above_floor count)
- Per-prototype scores (if multi-prototype enabled, scores against each cluster centroid)
- Prototype cluster membership (which entries belong to which cluster)

```json
{
  "meta": {
    "model": "azure_openai",
    "floor": 0.30,
    "total_entries": 16282,
    "proto_thresholds": {"two": 5, "three": 10}
  },
  "entities": {
    "chasmfiends": {
      "specificity": 4.4,
      "entries_above_floor": 200,
      "calibration": {"mean": 0.77, "std": 0.03, "p10": 0.73, "p25": 0.76, "p50": 0.78},
      "prototypes": 1,
      "scores": {
        "12345": [0.72],
        "67890": [0.68]
      }
    },
    "hoid": {
      "specificity": 2.1,
      "entries_above_floor": 1200,
      "calibration": {"mean": 0.65, "std": 0.08, "p10": 0.55, "p25": 0.60, "p50": 0.65},
      "prototypes": 3,
      "scores": {
        "11111": [0.81, 0.69, 0.64],
        "22222": [0.58, 0.77, 0.61]
      }
    }
  }
}
```

Score arrays are ordered by prototype index. Client takes `max(scores)` for the entity score (or can inspect per-prototype if desired).

**`graph.json`** (existing) -- Baseline explicit-only graph, unchanged.

**`reviews.json`** (user-generated) -- Saved review decisions, created by the review panel.

### Computed Client-Side (on Apply)

1. For each entity: compute effective threshold = calibration percentile from entity's stats
2. Filter entities by specificity >= min specificity slider
3. For each entry, for each surviving entity: take max across prototypes, compare to entity's effective threshold
4. Apply margin filter: reject tags where (best_score - this_score) > margin
5. Apply must-bridge filter: entry must have at least one other tag
6. Rebuild edges from combined explicit + implicit tags, filter to weight >= 2
7. Merge with review statuses
8. Update D3: add/remove edges, pulse new nodes, style implicit edges as dashed amber

---

## 6. New Files

- `notebooks/07_export_scores.py` -- generates scores.json from cached numpy embeddings
- `data/scores.json` -- precomputed scores, calibration stats, specificity, prototypes
- `data/reviews.json` -- user-generated review decisions (not committed)

---

## 7. Migration from v1

The v1 design had two separate score files (isolated and all) with a lazy-load toggle. The v2 design replaces this with:
- A single `scores.json` containing all entities (specificity slider replaces the isolated/all toggle)
- The "Scope" radio in the top bar is kept for backwards compatibility but could be removed once specificity filtering proves sufficient
- The floor drops from 0.55/0.65 to 0.30 to support the wider range of per-entity calibrated thresholds

---

## 8. Open Questions

- **scores.json size at floor=0.30:** May be larger than 3 MB. If so, consider a higher floor (0.40) or split by entity groups.
- **k-means stability:** With only 5 entries, k=2 clusters may be unstable. May need to run multiple seeds and pick the best silhouette score.
- **Review panel scale:** At 274 implicit tags, the table is manageable. If the user switches to "All" scope with lower thresholds, thousands of tags could appear. May need pagination or "review top-N by score" filtering.
