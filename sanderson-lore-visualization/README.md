# Cosmere Knowledge Graph — Words of Brandon

An interactive force-directed graph visualization of the Cosmere universe, built from 16,282 "Words of Brandon" (WoB) Q&A entries scraped from [Arcanum](https://wob.coppermind.net/).

**Summary**: 886 WoB tags were classified into 6 entity types (characters, worlds, magic systems, Shards, concepts, books), then co-occurrence analysis produced a knowledge graph of 622 entity nodes connected by 2,258 weighted edges. The result is a D3.js force graph where you can explore how Cosmere topics relate through Brandon Sanderson's own answers.

## Data Sources

- **Words of Brandon (Arcanum)**: 16,282 Q&A entries from signings, interviews, and AMAs — scraped via `words-of-brandon/` in this repo.

## How to Run

```bash
cd sanderson-lore-visualization
python3 -m http.server 8080
# Open http://localhost:8080
```

No dependencies needed for viewing — it's a standalone HTML + D3.js app that loads JSON data via fetch.

To regenerate the data from scratch:

```bash
pip install -r requirements.txt   # just stdlib, nothing extra
python3 notebooks/01_classify_tags.py
python3 notebooks/02_build_graph.py
```

## Methodology

### 1. Tag Classification (`01_classify_tags.py`)

All 886 unique WoB tags were manually classified into 6 entity types using Cosmere domain knowledge:

| Type | Count | Examples |
|------|-------|---------|
| Character | 218 | Hoid, Kaladin, Vin, Kelsier |
| Concept | 196 | Investiture, Knights Radiant, Desolations |
| Book | 165 | Stormlight Archive, Mistborn Era 2 |
| Magic | 119 | Allomancy, Surgebinding, Awakening |
| World | 58 | Roshar, Scadrial, Sel, Nalthis |
| Shard | 31 | Honor, Odium, Preservation, Ruin |

An additional 99 tags were classified as "meta" (writing advice, RAFO, admin) and excluded from the graph.

### 2. Co-occurrence Graph (`02_build_graph.py`)

For every WoB entry, all pairs of entity tags that appear together create a weighted edge. Edges with weight < 2 are pruned. Book nodes are filtered from the visualization since they create noisy hub connections (everything connects to "Stormlight Archive").

### 3. Interactive Visualization (`index.html`)

- **Force-directed layout** via D3.js with charge, link, and collision forces
- **Color-coded** by entity type (blue=character, green=world, purple=magic, gold=shard, orange=concept)
- **Node size** proportional to sqrt of entry count
- **Search** with autocomplete (press `/` to focus)
- **Click a node** to focus: dims unrelated nodes, shows connection panel
- **Click a connection** to drill into the actual WoB Q&A entries
- **Filter toggles** to show/hide entity types
- **Zoom + pan** with mouse/trackpad

## Key Findings

Top co-occurring entity pairs (by shared WoB entries):

| Pair | Shared Entries |
|------|---------------|
| Allomancy ↔ Feruchemy | 77 |
| Allomancy ↔ Time Bubbles | 43 |
| Nightblood ↔ Vasher | 31 |
| Elend ↔ Vin | 30 |
| Cognitive Realm ↔ Sel | 29 |
| Preservation ↔ Ruin | 29 |
| Devotion ↔ Dominion | 27 |
| Shards ↔ Vessels | 27 |

The Metallic Arts (Allomancy/Feruchemy/Hemalurgy) form the densest cluster, reflecting how frequently fans ask about cross-system interactions. Character pairs like Vin ↔ Elend and Nightblood ↔ Vasher show strong narrative coupling. Cross-world connections (Roshar ↔ Scadrial) reveal worldhopping as a major topic of fan curiosity.
