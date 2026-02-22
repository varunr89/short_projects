# Embedding Pipeline Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a multi-model embedding pipeline that replaces regex text matching with semantic similarity for entity disambiguation, hidden connection discovery, and a "similar entities" UI feature.

**Architecture:** Embed all 16,282 WoB entries with 5 embedding models (Azure OpenAI, Azure AI Foundry Cohere/Mistral, GCP Gemini, Voyage AI). Cache all embeddings to disk. A graph-building script uses any cached model to compute entity reference embeddings, run embedding-first tagging, build the co-occurrence graph, and generate similarity lists. A comparison script evaluates all 5 models side-by-side.

**Tech Stack:** Python 3, numpy, azure-ai-inference, openai, google-genai, voyageai

**Design doc:** `docs/plans/2026-02-20-embedding-pipeline-design.md`

---

### Task 1: Set up virtual environment and dependencies

**Files:**
- Modify: `sanderson-lore-visualization/requirements.txt`

**Step 1: Create venv and install dependencies**

```bash
cd /Users/varunr/projects/short_projects/sanderson-lore-visualization
python3 -m venv venv
source venv/bin/activate
pip install numpy openai azure-ai-inference google-genai voyageai python-dotenv
```

**Step 2: Update requirements.txt**

```bash
pip freeze > requirements.txt
```

**Step 3: Create .env file for API keys**

Create `sanderson-lore-visualization/.env` with placeholders:

```
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=

# Azure AI Foundry (Cohere, Mistral)
AZURE_AI_ENDPOINT=https://<project>.models.ai.azure.com/
AZURE_AI_API_KEY=

# Google (Gemini)
GOOGLE_API_KEY=

# Voyage AI
VOYAGE_API_KEY=
```

**Step 4: Verify .gitignore excludes .env and venv**

Check that `.env`, `venv/`, and `data/embeddings_cache/` are in `.gitignore`. Add them if missing.

**Step 5: Commit**

```bash
git add requirements.txt .gitignore
git commit -m "chore: add embedding pipeline dependencies"
```

---

### Task 2: Build the embedding script (04_embed_entries.py)

**Files:**
- Create: `sanderson-lore-visualization/notebooks/04_embed_entries.py`

This script embeds all 16,282 raw WoB entries with all 5 models. It caches results to
`data/embeddings_cache/<model_name>.npy` as numpy arrays. It is idempotent -- it skips
any model whose cache file already exists.

**Step 1: Write the embedding script**

The script must:

1. Load all 16,282 entries from `words-of-brandon/wob_entries.json`
2. For each entry, build the text to embed: concatenate all `lines[].text` (HTML-stripped)
   plus `note` field. Store the entry ID order in a separate `entry_ids.json` so we can
   map numpy array rows back to entry IDs.
3. Define 5 embedding provider functions, each taking a list of texts and returning a
   numpy array of shape `(n, dims)`:
   - `embed_azure_openai(texts)` -- uses `openai.AzureOpenAI` client with
     model `text-embedding-3-large`. Batch in chunks of 2048 (API limit).
   - `embed_azure_cohere(texts)` -- uses `azure.ai.inference.EmbeddingsClient`
     pointed at the Cohere embed-v4 endpoint. Batch in chunks of 96.
   - `embed_azure_mistral(texts)` -- uses `azure.ai.inference.EmbeddingsClient`
     pointed at the Mistral-embed endpoint. Batch in chunks of 96.
   - `embed_gemini(texts)` -- uses `google.genai.Client` with
     `models.embed_content(model='gemini-embedding-001', ...)`. Batch in chunks of 100.
   - `embed_voyage(texts)` -- uses `voyageai.Client` with `client.embed(texts,
     model='voyage-4')`. Batch in chunks of 128.
4. Each provider function should print progress (e.g., "Embedding batch 3/17...").
5. For each model, check if `data/embeddings_cache/<model>.npy` exists. If yes, skip.
   If no, call the provider function, save the result as a `.npy` file.
6. Also save `data/embeddings_cache/entry_ids.json` -- the ordered list of entry IDs
   corresponding to rows in the numpy arrays.

**Key details:**
- The raw WoB file is at: `../../words-of-brandon/wob_entries.json` (relative to
  the notebooks dir), or absolute:
  `/Users/varunr/projects/short_projects/words-of-brandon/wob_entries.json`
- Strip HTML from entry text before embedding using the same `strip_html()` function
  from `02_build_graph.py`.
- Truncate very long entries to ~8000 tokens (~32000 chars) to avoid API limits.
  Most entries are short (median 406 chars) so this only affects a handful.
- Load API keys from `.env` using `python-dotenv`.
- Create `data/embeddings_cache/` directory if it does not exist.

**Expected output files:**
```
data/embeddings_cache/
  entry_ids.json             # [1356, 1357, ...] -- 16282 entry IDs
  azure_openai.npy           # shape (16282, 3072), float32
  azure_cohere.npy           # shape (16282, 1024), float32
  azure_mistral.npy          # shape (16282, 1024), float32
  gemini.npy                 # shape (16282, 3072), float32
  voyage.npy                 # shape (16282, 1024), float32
```

**Step 2: Test with one model first**

Run the script with only Voyage (free tier) to verify the pipeline works end-to-end
before spending money on the other 4. To do this, temporarily comment out the other
models or add a `--models` CLI flag.

```bash
cd /Users/varunr/projects/short_projects/sanderson-lore-visualization
source venv/bin/activate
python notebooks/04_embed_entries.py --models voyage
```

Expected: Creates `data/embeddings_cache/voyage.npy` and `entry_ids.json`.
Verify shape:

```bash
python -c "import numpy as np; a = np.load('data/embeddings_cache/voyage.npy'); print(a.shape, a.dtype)"
```

Expected output: `(16282, 1024) float32`

**Step 3: Run all 5 models**

```bash
python notebooks/04_embed_entries.py
```

This calls all 5 providers. Each skips if its cache file exists. Expected ~2-5 min
per model depending on API speed.

**Step 4: Commit**

```bash
git add notebooks/04_embed_entries.py
git commit -m "feat: add multi-model embedding script for WoB entries"
```

Note: Do NOT commit the .npy files or .env. They should be in .gitignore.

---

### Task 3: Build the graph generation script (05_build_graph.py)

**Files:**
- Create: `sanderson-lore-visualization/notebooks/05_build_graph.py`

This script takes a `--model` flag, loads the cached embeddings for that model, and
produces `graph.json`, `entries.json`, and `similarity.json`.

**Step 1: Write the graph generation script**

The script must:

1. Accept `--model` argument (choices: azure_openai, azure_cohere, azure_mistral,
   gemini, voyage). Default: voyage.
2. Accept `--threshold` argument (float, default 0.5). This is the cosine similarity
   threshold for embedding-first tagging.
3. Load:
   - `data/embeddings_cache/<model>.npy` -- the entry embeddings matrix
   - `data/embeddings_cache/entry_ids.json` -- maps row index to entry ID
   - `data/tag_classifications.json` -- entity types
   - Raw WoB entries from `words-of-brandon/wob_entries.json` -- for explicit tags
4. Build a mapping: `entry_id -> row_index` for fast lookup.
5. **Compute entity reference embeddings:**
   - For each entity tag in `tag_classifications.json` (type != "meta"):
     - Find all raw WoB entries where this tag appears in explicit `tags` list
     - Collect their embedding row indices
     - If fewer than 5 entries, skip (entity gets no reference embedding)
     - Average those entry embeddings to produce one reference vector
     - L2-normalize the reference vector
   - Store as a numpy matrix `entity_refs` of shape `(n_entities, dims)` with a
     parallel list `entity_ids` mapping row to entity name.
6. **Embedding-first tagging:**
   - L2-normalize all entry embeddings.
   - Compute cosine similarity matrix: `sim = entries_norm @ entity_refs.T`
     Shape: `(16282, n_entities)`.
   - For each entry, find all entities where `sim > threshold`.
   - Merge with explicit tags (explicit tags always kept).
   - This produces `entry_all_tags`: dict of `entry_id -> set of entity tags`.
7. **Build co-occurrence graph** (same logic as `02_build_graph.py`):
   - For each entry's combined tags, create edges for all tag pairs.
   - Filter edges with weight >= 2.
   - Build nodes list with entry counts.
8. **Build similarity.json:**
   - Compute `entity_refs @ entity_refs.T` -- pairwise entity similarity matrix.
   - For each entity, take top-10 most similar other entities (excluding self).
   - Output format: `{ "kaladin": [{"id": "szeth", "score": 0.89}, ...], ... }`
9. **Save outputs:**
   - `data/graph.json`
   - `data/entries.json` (cleaned entries with combined tags)
   - `data/similarity.json`
10. **Print summary stats:**
    - Nodes, edges, isolated nodes
    - Comparison with baseline (02_build_graph.py output: 787 nodes, 2258 edges)
    - Number of new implicit tags added
    - Top 10 entities by number of new implicit tags

**Step 2: Run with Voyage embeddings**

```bash
python notebooks/05_build_graph.py --model voyage --threshold 0.5
```

Inspect output: check that "rock" entries about geology are NOT tagged with the
Rock character. Check that isolated node count decreased.

**Step 3: Tune the threshold**

Run with different thresholds (0.4, 0.5, 0.6, 0.7) and compare:
- How many implicit tags are added?
- How many false positives appear for known ambiguous entities?
- How many isolated nodes remain?

Print a summary table for each threshold.

**Step 4: Commit**

```bash
git add notebooks/05_build_graph.py
git commit -m "feat: add embedding-based graph builder with disambiguation"
```

---

### Task 4: Build the model comparison script (06_compare_models.py)

**Files:**
- Create: `sanderson-lore-visualization/notebooks/06_compare_models.py`

**Step 1: Write the comparison script**

The script runs all 3 evaluation tests across all cached models.

**Test 1: Disambiguation accuracy**

Define a ground truth dict of ~30 manually labeled entries:

```python
# Format: entry_id -> {entity_name: True/False}
# True = this entry IS about that entity, False = it is NOT
GROUND_TRUTH = {
    # "rock" the character vs. geology
    <entry_id>: {"rock": True},   # entry about Rock the Horneater
    <entry_id>: {"rock": False},  # entry about rock formations
    ...
    # "honor" the Shard vs. English word
    <entry_id>: {"honor": True},  # entry about Honor the Shard
    <entry_id>: {"honor": False}, # entry using "honor" as English word
    ...
}
```

To populate this, the script should first find candidate entries by searching
entry text for the ambiguous words, then you manually label them. Alternatively,
ship a pre-labeled `data/disambiguation_ground_truth.json`.

For each model + threshold combo:
- Run the tagging logic
- Check precision/recall on the ground truth entries
- Print results as a table

**Test 2: Similarity quality**

For 10 well-known entities, print each model's top-5 similar entities:

```
Entity: Kaladin
  azure_openai:  szeth (0.91), dalinar (0.88), syl (0.85), bridge four (0.83), windrunner (0.82)
  azure_cohere:  ...
  azure_mistral: ...
  gemini:        ...
  voyage:        ...
```

**Test 3: Discovery power**

Count new implicit tags per model. Show entities that gained the most new
connections. Print overall stats:
- Total new tags per model
- Entries newly tagged (were untagged, now have tags)
- Isolated nodes per model

**Step 2: Run comparison**

```bash
python notebooks/06_compare_models.py
```

Review output. This is where we see which model(s) produce the best results.

**Step 3: Commit**

```bash
git add notebooks/06_compare_models.py
git commit -m "feat: add multi-model comparison script"
```

---

### Task 5: Add "Similar Entities" to the visualization

**Files:**
- Modify: `sanderson-lore-visualization/index.html`

**Step 1: Load similarity.json in the frontend**

In `index.html` around line 794, add a third fetch for `similarity.json`:

```javascript
const [graphResp, entriesResp, similarityResp] = await Promise.all([
  fetch(basePath + '/data/graph.json').then(function(r) { return r.json(); }),
  fetch(basePath + '/data/entries.json').then(function(r) { return r.json(); }),
  fetch(basePath + '/data/similarity.json').then(function(r) { return r.json(); }),
]);
graph = graphResp;
entries = entriesResp;
var similarity = similarityResp;
```

Make `similarity` accessible globally (declare `var similarity = {};` at the top
alongside `var graph, entries;`).

**Step 2: Add "Similar Entities" section to showPanel()**

In the `showPanel()` function (line 1127), after appending `connSection` to `content`
(line 1233) and before creating `entriesSection`, add:

```javascript
// Similar Entities section
var simData = similarity[nodeId];
if (simData && simData.length > 0) {
  var simDivider = document.createElement('div');
  simDivider.className = 'panel-divider';
  content.appendChild(simDivider);

  var simSection = document.createElement('div');
  simSection.className = 'similar-section';

  var simH3 = document.createElement('h3');
  simH3.style.color = 'var(--stormlight)';
  simH3.textContent = 'Similar Entities';
  simSection.appendChild(simH3);

  simData.forEach(function(s) {
    var simNode = graph.nodes.find(function(n) { return n.id === s.id; });
    if (!simNode || !activeFilters.has(simNode.type)) return;

    var item = document.createElement('div');
    item.className = 'connection-item';

    var left = document.createElement('div');
    left.className = 'conn-left';

    var gem = document.createElement('span');
    gem.className = 'conn-gem';
    gem.style.background = GEM_COLORS[simNode.type];
    left.appendChild(gem);

    var nameSpan = document.createElement('span');
    nameSpan.style.color = GEM_GLOW[simNode.type];
    nameSpan.textContent = simNode.label;
    left.appendChild(nameSpan);

    var score = document.createElement('span');
    score.className = 'connection-weight';
    score.style.background = 'rgba(200, 220, 255, 0.08)';
    score.style.color = 'var(--stormlight)';
    score.textContent = (s.score * 100).toFixed(0) + '%';

    item.appendChild(left);
    item.appendChild(score);
    item.addEventListener('click', function() {
      focusNode(s.id);
    });
    simSection.appendChild(item);
  });

  content.appendChild(simSection);
}
```

**Step 3: Add CSS for similar section**

Add a subtle visual distinction so "Similar Entities" looks different from
"Connections" -- e.g., slightly dimmer, or with a different header style.
Use the existing `.connections-section` styles as a base.

**Step 4: Test locally**

Start the local server and verify:
- Side panel shows "Similar Entities" below connections
- Clicking a similar entity focuses it
- Similarity scores display correctly

**Step 5: Commit**

```bash
git add sanderson-lore-visualization/index.html
git commit -m "feat: add similar entities section to side panel"
```

---

### Task 6: Deploy to GitHub Pages

**Files:**
- Modify: files in `/tmp/cosmere-graph/` (deployment repo)

**Step 1: Copy updated files to deployment repo**

```bash
cp sanderson-lore-visualization/index.html /tmp/cosmere-graph/
cp sanderson-lore-visualization/data/graph.json /tmp/cosmere-graph/data/
cp sanderson-lore-visualization/data/entries.json /tmp/cosmere-graph/data/
cp sanderson-lore-visualization/data/similarity.json /tmp/cosmere-graph/data/
```

**Step 2: Commit and push**

```bash
cd /tmp/cosmere-graph
git add -A
git commit -m "feat: embedding-based graph with similar entities"
git push
```

**Step 3: Verify deployment**

Wait for GitHub Pages build, then check https://varunr89.github.io/cosmere-graph/

**Step 4: Commit source changes to short_projects**

```bash
cd /Users/varunr/projects/short_projects
git add sanderson-lore-visualization/
git commit -m "feat: embedding pipeline for Cosmere knowledge graph"
```

---

### Task 7: Create ground truth labels for disambiguation test

**Files:**
- Create: `sanderson-lore-visualization/data/disambiguation_ground_truth.json`

**Step 1: Find candidate entries for labeling**

Write a small helper that searches raw WoB entries for ambiguous entity names
(rock, honor, lift, stick, ruin, focus, color, marsh) and prints entry ID + text
snippet for manual labeling. Pick ~5 entries per ambiguous entity (mix of true
positives and true negatives).

**Step 2: Create the ground truth JSON**

Format:
```json
{
  "entries": {
    "1234": {"rock": true},
    "5678": {"rock": false},
    ...
  },
  "entities_tested": ["rock", "honor", "lift", "stick", "ruin"]
}
```

**Step 3: Commit**

```bash
git add data/disambiguation_ground_truth.json
git commit -m "data: add disambiguation ground truth labels"
```

---

## Execution Order

Tasks 1-4 are sequential (each depends on the previous).
Task 5 (frontend) can run in parallel with Task 4 (comparison).
Task 6 (deploy) depends on Tasks 4 and 5.
Task 7 (ground truth) should run before Task 4 but can be done alongside Task 2-3.

Recommended order: 1 -> 2 -> 7 -> 3 -> 4 + 5 (parallel) -> 6
