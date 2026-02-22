# Embedding Pipeline Design -- Cosmere Knowledge Graph

**Date:** 2026-02-20
**Status:** Approved
**Project:** sanderson-lore-visualization

## Problem

The text-matching pipeline (03_text_matching.py) introduced false positives by matching
common English words against Cosmere entity names. For example, "rock" matches both the
Horneater character Rock and any geological reference. 124 of 783 entity names are
ambiguous English words (honor, ruin, lift, stick, marsh, focus, color, etc.).

We need an approach that:
1. Fixes false positive tags from text matching (entity disambiguation)
2. Connects remaining 92 isolated nodes via semantic similarity
3. Adds a "similar entities" feature to the visualization side panel
4. Discovers hidden connections -- entries that reference entities without naming them

## Architecture Decisions

- **Deployment: fully static.** All computation happens offline in the pipeline. The site
  ships precomputed JSON files to GitHub Pages. No server, no inference at query time.
- **Embedding-first tagging.** Embeddings replace regex text matching entirely. Instead of
  matching entity names in text, we compute semantic similarity between entries and entity
  reference embeddings.
- **Multi-model cache.** We embed all entries with 5 models and cache all results. We do
  not pick a single winner upfront. Different models may find different hidden connections.
  The pipeline accepts a `--model` flag to generate the graph from any cached model.
- **Embed all entries.** All 16,282 raw WoB entries get embedded, not just the 12,562 that
  have explicit tags. Untagged entries may reference entities without being tagged for them.

## Models (5)

| Model                        | Provider         | Dims | Strength                              |
|------------------------------|------------------|------|---------------------------------------|
| text-embedding-3-large       | Azure OpenAI     | 3072 | High dimensionality, wide ecosystem   |
| Cohere embed-v4              | Azure AI Foundry | 1024 | Reranking-optimized paradigm          |
| Mistral-embed                | Azure AI Foundry | 1024 | LLM-based, deepest semantic grasp     |
| Gemini embedding-001         | GCP Vertex AI    | 3072 | MTEB overall champion                 |
| Voyage-4                     | Voyage AI direct | 1024 | MoE architecture, hard-negative training |

Total one-time cost: ~$3-4 across all 5 models for 16K entries. All embeddings cached to
disk for reuse.

## Pipeline

### Scripts

1. **`04_embed_entries.py`** -- Embeds all 16,282 entries with all 5 models. Caches
   embeddings to `data/embeddings_cache/<model_name>.npy` (numpy arrays). Idempotent:
   skips models that are already cached.

2. **`05_build_graph.py --model <name>`** -- Takes a model flag. Computes entity reference
   embeddings, runs embedding-first tagging, builds the co-occurrence graph, and generates
   similarity lists. Outputs `graph.json`, `entries.json`, `similarity.json`.

3. **`06_compare_models.py`** -- Runs evaluation tests across all 5 models, prints
   comparison results to terminal and saves a summary file.

### Data Flow

```
Raw WoB entries (16,282)
        |
        v
[04_embed_entries.py]
  Embed all entries with 5 models
  Cache to data/embeddings_cache/
        |
        v
[05_build_graph.py --model <name>]
  1. Load cached embeddings for chosen model
  2. Compute entity reference embeddings
     (average of explicitly-tagged entries, min 5 entries per entity)
  3. Embedding-first tagging:
     For each entry, compute cosine similarity against all entity
     reference embeddings. Tag entry with entities above threshold.
  4. Build co-occurrence graph from explicit + predicted tags
  5. Build similarity.json: top-K similar entities per node
        |
        v
Output: graph.json, entries.json, similarity.json
  (static files shipped to GitHub Pages)
```

### Embedding-First Tagging (detail)

For each of the 16,282 entries:
- Compute cosine similarity between the entry embedding and every entity reference
  embedding (~783 entities with 5+ explicit entries)
- If similarity exceeds threshold, add that entity as an implicit tag
- The entry's explicit Arcanum tags are always preserved (curator-verified)
- Implicit tags from embeddings supplement, never override, explicit tags

This replaces the regex text-matching step entirely. No more `\brock\b` matching --
instead, the embedding knows from context whether "rock" refers to the character or
the geological thing.

### Entity Reference Embeddings

For each entity with 5+ explicitly-tagged entries:
- Collect all entry embeddings where that entity appears as an explicit Arcanum tag
- Average those embeddings to produce a single entity reference vector
- This "clean" reference represents what discussions about that entity actually sound like

Entities with fewer than 5 explicit entries get no reference embedding and rely solely
on their explicit tags.

### Similarity Lists (similarity.json)

For each entity, compute cosine similarity against all other entity reference embeddings.
Store the top-K (e.g., K=10) most similar entities with their scores. This powers the
"Similar Entities" section in the visualization side panel.

## Evaluation (06_compare_models.py)

Three tests, run across all 5 models:

### Test 1: Disambiguation Accuracy
Hand-label ~30 entries for ambiguous entities as ground truth:
- 10 entries where "rock" = character vs. geology
- 10 entries where "honor" = Shard vs. English word
- 10 entries where "lift" = Edgedancer vs. verb

Check each model's precision on accepting/rejecting these.

### Test 2: Similarity Quality
For 10 well-known entities (Kaladin, Hoid, Kelsier, Allomancy, Roshar, Shallan, Honor,
Vin, Stormfather, Hemalurgy), print each model's top-5 most similar entities side-by-side.
Qualitative assessment of which rankings make Cosmere sense.

### Test 3: Discovery Power
Check what new entity-entry connections each model finds beyond explicit tags. For entries
known to be about an entity (e.g., mentions "Bridge Four" and "Windrunner" but not
"Kaladin"), does the model correctly tag them?

## Provider Configuration

### Azure (3 models)
- OpenAI text-embedding-3-large via Azure OpenAI endpoint
- Cohere embed-v4 via Azure AI Foundry unified embeddings API
- Mistral-embed via Azure AI Foundry unified embeddings API

### GCP (1 model)
- Gemini embedding-001 via Vertex AI / google-genai SDK

### Voyage AI Direct (1 model)
- Voyage-4 via Voyage AI API (free tier)

### Dependencies
- `azure-ai-inference` -- Azure AI Foundry unified SDK
- `openai` -- Azure OpenAI SDK
- `google-genai` -- Google Gen AI SDK
- `voyageai` -- Voyage AI SDK
- `numpy` -- Vector operations and caching

## Frontend Changes

### Side Panel: "Similar Entities" Section
When a node is focused, the side panel shows a new section below connections:

```
Similar Entities
  Szeth          0.89
  Dalinar        0.85
  Syl            0.83
  Bridge Four    0.81
  Windrunner     0.79
```

Each entry is clickable (focuses that node). Similarity scores displayed as subtle
secondary text. Data sourced from precomputed similarity.json.

## What This Replaces

- **03_text_matching.py** -- Fully replaced by the embedding pipeline. The regex-based
  text matching with its skip list and false positive problems is no longer needed.
- The co-occurrence graph building logic moves into 05_build_graph.py.
- 02_build_graph.py remains as the baseline (explicit tags only) for comparison.
