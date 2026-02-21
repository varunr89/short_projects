# Embedding Controls Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Python export pipeline (07_export_scores.py) and interactive frontend controls so users can experiment with all embedding-based tagging parameters in the browser.

**Architecture:** A Python script precomputes per-entity similarity scores, calibration stats, specificity scores, and multi-prototype references into a single `scores.json`. The frontend loads this file and performs all filtering/tagging client-side when the user clicks Apply. Implicit edges render as dashed amber lines, distinct from solid explicit edges. A review panel lets users validate individual implicit tags.

**Tech Stack:** Python 3 (numpy, scikit-learn for k-means), pytest for backend tests, Playwright for E2E frontend tests, vanilla JS + D3.js for the frontend.

---

## Parallel Execution Strategy

Two independent tracks that converge at Task 5:

```
Track A (Python Pipeline)           Track B (Frontend Engine)
  Task 1: tests + export script       Task 3: client-side tagging engine tests + impl
  Task 2: run pipeline, verify         Task 4: UI controls tests + impl
                  \                    /
                   Task 5: Integration (hypothesis layer + review panel)
                       |
                   Task 6: E2E Playwright tests
                       |
                   Task 7: Deploy + commit
```

Tasks 1-2 and Tasks 3-4 can run in parallel. Task 5+ depends on both tracks.

---

## Task 1: Python Export Script (07_export_scores.py) with Tests

**Files:**
- Create: `sanderson-lore-visualization/notebooks/07_export_scores.py`
- Create: `sanderson-lore-visualization/tests/test_export_scores.py`

This task covers the full TDD cycle for the Python pipeline.

### Step 1: Create test file with real-data integration tests

The tests load actual cached embeddings from `data/embeddings_cache/azure_openai.npy` and `data/embeddings_cache/entry_ids.json`. No mocks.

```python
"""
Integration tests for 07_export_scores.py using real embedding data.

These tests use the actual cached Azure OpenAI embeddings (191MB .npy file)
and real WoB entries to verify the export pipeline produces correct output.
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "embeddings_cache"
SCRIPT_PATH = PROJECT_ROOT / "notebooks" / "07_export_scores.py"
WOB_PATH = PROJECT_ROOT.parent / "words-of-brandon" / "wob_entries.json"
TAG_CLASS_PATH = DATA_DIR / "tag_classifications.json"
OUTPUT_PATH = DATA_DIR / "scores.json"

# Skip all tests if real data isn't available
pytestmark = pytest.mark.skipif(
    not (CACHE_DIR / "azure_openai.npy").exists(),
    reason="Real embedding data not available",
)


@pytest.fixture(scope="module")
def run_export():
    """Run 07_export_scores.py once and return the output path."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--model", "azure_openai"],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    assert OUTPUT_PATH.exists(), "scores.json was not created"
    return OUTPUT_PATH


@pytest.fixture(scope="module")
def scores(run_export):
    """Load the generated scores.json."""
    with open(run_export) as f:
        return json.load(f)


class TestScoresJsonSchema:
    """Verify the top-level structure of scores.json matches the design doc."""

    def test_has_meta_section(self, scores):
        assert "meta" in scores
        meta = scores["meta"]
        assert meta["model"] == "azure_openai"
        assert isinstance(meta["floor"], float)
        assert meta["total_entries"] == 16282
        assert "proto_thresholds" in meta

    def test_has_entities_section(self, scores):
        assert "entities" in scores
        assert len(scores["entities"]) > 0

    def test_entity_has_required_fields(self, scores):
        """Every entity must have specificity, calibration, prototypes, and scores."""
        for name, entity in scores["entities"].items():
            assert "specificity" in entity, f"{name} missing specificity"
            assert "entries_above_floor" in entity, f"{name} missing entries_above_floor"
            assert "calibration" in entity, f"{name} missing calibration"
            assert "prototypes" in entity, f"{name} missing prototypes"
            assert "scores" in entity, f"{name} missing scores"

    def test_calibration_has_percentiles(self, scores):
        """Calibration stats must include mean, std, and percentiles."""
        for name, entity in scores["entities"].items():
            cal = entity["calibration"]
            assert "mean" in cal, f"{name} calibration missing mean"
            assert "std" in cal, f"{name} calibration missing std"
            assert "p10" in cal, f"{name} calibration missing p10"
            assert "p25" in cal, f"{name} calibration missing p25"
            assert "p50" in cal, f"{name} calibration missing p50"

    def test_scores_are_arrays(self, scores):
        """Each entry's scores should be a list with length == prototypes."""
        sample_entity = list(scores["entities"].values())[0]
        n_proto = sample_entity["prototypes"]
        for eid, score_list in sample_entity["scores"].items():
            assert isinstance(score_list, list)
            assert len(score_list) == n_proto, (
                f"Entry {eid} has {len(score_list)} scores but entity has {n_proto} prototypes"
            )


class TestCalibrationValues:
    """Verify calibration stats are numerically reasonable using real data."""

    def test_kaladin_calibration(self, scores):
        """Kaladin has 100+ entries -- calibration stats should be well-defined."""
        if "kaladin" not in scores["entities"]:
            pytest.skip("kaladin not in scores")
        cal = scores["entities"]["kaladin"]["calibration"]
        # Percentiles should be ordered: p10 <= p25 <= p50
        assert cal["p10"] <= cal["p25"] <= cal["p50"]
        # Mean should be positive and less than 1.0
        assert 0.0 < cal["mean"] < 1.0
        assert cal["std"] > 0.0

    def test_percentile_ordering_all_entities(self, scores):
        """For every entity, p10 <= p25 <= p50."""
        for name, entity in scores["entities"].items():
            cal = entity["calibration"]
            assert cal["p10"] <= cal["p25"] + 1e-6, f"{name}: p10 > p25"
            assert cal["p25"] <= cal["p50"] + 1e-6, f"{name}: p25 > p50"


class TestSpecificityScores:
    """Verify specificity (IDF) scores separate hubs from niche entities."""

    def test_cosmere_is_low_specificity(self, scores):
        """'cosmere' tags nearly everything -- should have very low specificity."""
        if "cosmere" not in scores["entities"]:
            pytest.skip("cosmere not in scores")
        spec = scores["entities"]["cosmere"]["specificity"]
        assert spec < 1.0, f"cosmere specificity {spec} is too high for a hub"

    def test_niche_entity_is_high_specificity(self, scores):
        """A niche entity should have specificity > 2.0."""
        # Find any entity with < 500 entries_above_floor
        niche = None
        for name, entity in scores["entities"].items():
            if entity["entries_above_floor"] < 500:
                niche = (name, entity)
                break
        if niche is None:
            pytest.skip("No niche entity found")
        name, entity = niche
        assert entity["specificity"] > 2.0, (
            f"{name} with {entity['entries_above_floor']} entries has specificity {entity['specificity']}"
        )

    def test_specificity_is_positive(self, scores):
        """All specificity scores should be positive."""
        for name, entity in scores["entities"].items():
            assert entity["specificity"] > 0, f"{name} has non-positive specificity"


class TestMultiPrototype:
    """Verify k-means clustering produces correct number of prototypes."""

    def test_small_entity_single_prototype(self, scores):
        """Entities with 3-4 tagged entries should have 1 prototype."""
        for name, entity in scores["entities"].items():
            # We can't directly know how many tagged entries from scores.json alone,
            # but entities with prototypes=1 should have score arrays of length 1
            if entity["prototypes"] == 1:
                for eid, s in entity["scores"].items():
                    assert len(s) == 1, f"{name} proto=1 but scores length={len(s)}"

    def test_multi_prototype_scores_length(self, scores):
        """Entities with 2+ prototypes should have matching score array lengths."""
        for name, entity in scores["entities"].items():
            n = entity["prototypes"]
            for eid, s in entity["scores"].items():
                assert len(s) == n, f"{name} proto={n} but entry {eid} has {len(s)} scores"

    def test_at_least_some_multi_prototype(self, scores):
        """With default thresholds (2-proto=5, 3-proto=10), some entities should have multiple prototypes."""
        multi = [n for n, e in scores["entities"].items() if e["prototypes"] > 1]
        assert len(multi) > 0, "No entities have multiple prototypes"


class TestScoreValues:
    """Verify the actual similarity scores are numerically reasonable."""

    def test_scores_in_valid_range(self, scores):
        """All scores should be between -1.0 and 1.0 (cosine similarity)."""
        for name, entity in scores["entities"].items():
            for eid, score_list in entity["scores"].items():
                for s in score_list:
                    assert -1.0 <= s <= 1.0, (
                        f"{name} entry {eid} has out-of-range score {s}"
                    )

    def test_scores_above_floor(self, scores):
        """All stored scores should be above the floor."""
        floor = scores["meta"]["floor"]
        for name, entity in scores["entities"].items():
            for eid, score_list in entity["scores"].items():
                max_score = max(score_list)
                assert max_score >= floor - 1e-6, (
                    f"{name} entry {eid} max score {max_score} is below floor {floor}"
                )

    def test_explicit_entries_have_high_scores(self, scores):
        """
        Entries explicitly tagged with an entity should generally score high
        against that entity. Check kaladin as a well-known case.
        """
        if "kaladin" not in scores["entities"]:
            pytest.skip("kaladin not in scores")
        # Load explicit tags
        with open(WOB_PATH) as f:
            raw = json.load(f)
        with open(TAG_CLASS_PATH) as f:
            tc = json.load(f)
        entity_tags = {t for t, info in tc.items() if info["type"] not in {"meta", "book"}}

        kaladin_explicit_eids = set()
        for e in raw:
            if "kaladin" in e["tags"] and "kaladin" in entity_tags:
                kaladin_explicit_eids.add(str(e["id"]))

        kaladin_scores = scores["entities"]["kaladin"]["scores"]
        # Check that explicit entries are present and score reasonably
        found = 0
        for eid in kaladin_explicit_eids:
            if eid in kaladin_scores:
                max_s = max(kaladin_scores[eid])
                assert max_s > 0.5, f"Kaladin explicit entry {eid} scores only {max_s}"
                found += 1
        assert found > 10, f"Only {found} kaladin explicit entries found in scores"


class TestOutputFileSize:
    """Verify scores.json isn't too large for browser loading."""

    def test_file_under_10mb(self, run_export):
        size_mb = run_export.stat().st_size / (1024 * 1024)
        assert size_mb < 10, f"scores.json is {size_mb:.1f} MB, should be under 10 MB"
```

**Step 2: Run tests to verify they fail**

Run: `cd sanderson-lore-visualization && source venv/bin/activate && python -m pytest tests/test_export_scores.py -v`
Expected: FAIL -- 07_export_scores.py doesn't exist yet, subprocess call will fail.

### Step 3: Implement 07_export_scores.py

```python
"""
Export precomputed embedding scores for the interactive frontend.

Generates scores.json containing:
- Per-entity similarity scores (entries above floor)
- Calibration stats (mean, std, percentiles of explicit-entry scores)
- Specificity scores (IDF-style hub detection)
- Multi-prototype reference vectors (k-means clustering)

Usage:
    python 07_export_scores.py
    python 07_export_scores.py --model azure_openai --floor 0.30
    python 07_export_scores.py --two-proto-min 5 --three-proto-min 10
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans

# -- Paths -------------------------------------------------------------------

project_root = Path(__file__).parent.parent
data_dir = project_root / "data"
cache_dir = data_dir / "embeddings_cache"
wob_path = project_root.parent / "words-of-brandon" / "wob_entries.json"

# -- CLI ---------------------------------------------------------------------

ALL_MODELS = ["azure_openai", "azure_cohere", "azure_mistral", "gemini", "voyage"]

parser = argparse.ArgumentParser(description="Export embedding scores for frontend")
parser.add_argument("--model", choices=ALL_MODELS, default="azure_openai")
parser.add_argument("--floor", type=float, default=0.30,
                    help="Minimum score to include in output (default: 0.30)")
parser.add_argument("--two-proto-min", type=int, default=5,
                    help="Min entries for 2 prototypes (default: 5)")
parser.add_argument("--three-proto-min", type=int, default=10,
                    help="Min entries for 3 prototypes (default: 10)")
args = parser.parse_args()

MIN_ENTRIES_FOR_REF = 3  # Minimum entries to create any reference embedding

# -- Load data ---------------------------------------------------------------

npy_path = cache_dir / f"{args.model}.npy"
ids_path = cache_dir / "entry_ids.json"

embeddings = np.load(npy_path)
with open(ids_path) as f:
    entry_ids = json.load(f)

assert embeddings.shape[0] == len(entry_ids)
eid_to_idx = {eid: idx for idx, eid in enumerate(entry_ids)}

with open(wob_path) as f:
    raw_entries = json.load(f)

with open(data_dir / "tag_classifications.json") as f:
    tag_class = json.load(f)

EXCLUDE_TYPES = {"meta", "book"}
entity_tags = {t for t, info in tag_class.items() if info["type"] not in EXCLUDE_TYPES}

# Build explicit tags per entry
entry_explicit_tags = {}
for e in raw_entries:
    eid = e["id"]
    explicit = [t for t in e["tags"] if t in entity_tags]
    if explicit:
        entry_explicit_tags[eid] = set(explicit)

print(f"Model: {args.model} ({embeddings.shape[1]}-dim)")
print(f"Entries: {len(entry_ids)}")
print(f"Entity tags: {len(entity_tags)}")

# -- L2-normalize entries ----------------------------------------------------

norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
zero_mask = (norms.squeeze() == 0)
norms = np.where(norms == 0, 1.0, norms)
entries_norm = embeddings / norms
entries_norm[zero_mask] = 0.0

# -- Build entity data -------------------------------------------------------

output = {
    "meta": {
        "model": args.model,
        "floor": args.floor,
        "total_entries": len(entry_ids),
        "proto_thresholds": {"two": args.two_proto_min, "three": args.three_proto_min},
    },
    "entities": {},
}

for tag in sorted(entity_tags):
    # Find explicitly tagged entries
    tag_eids = [
        eid for eid, tags in entry_explicit_tags.items()
        if tag in tags and eid in eid_to_idx
    ]
    if len(tag_eids) < MIN_ENTRIES_FOR_REF:
        continue

    indices = [eid_to_idx[eid] for eid in tag_eids]
    tag_embeddings = entries_norm[indices]  # Already L2-normalized

    # -- Determine number of prototypes --------------------------------------
    n_entries = len(tag_eids)
    if n_entries >= args.three_proto_min:
        n_proto = 3
    elif n_entries >= args.two_proto_min:
        n_proto = 2
    else:
        n_proto = 1

    # -- Compute prototype reference vectors ---------------------------------
    if n_proto == 1:
        ref = tag_embeddings.mean(axis=0)
        norm = np.linalg.norm(ref)
        if norm > 0:
            ref = ref / norm
        proto_refs = [ref]
    else:
        # k-means clustering
        kmeans = KMeans(n_clusters=n_proto, n_init=10, random_state=42)
        kmeans.fit(tag_embeddings)
        proto_refs = []
        for center in kmeans.cluster_centers_:
            norm = np.linalg.norm(center)
            if norm > 0:
                center = center / norm
            proto_refs.append(center)

    proto_matrix = np.array(proto_refs, dtype=np.float32)  # (n_proto, dims)

    # -- Compute similarity scores for all entries ---------------------------
    # sim_matrix: (n_entries, n_proto)
    sim_matrix = entries_norm @ proto_matrix.T
    sim_matrix = np.nan_to_num(sim_matrix, nan=0.0, posinf=0.0, neginf=0.0)

    # Keep entries where max score across prototypes >= floor
    max_scores = sim_matrix.max(axis=1)
    above_floor_mask = max_scores >= args.floor

    # -- Calibration stats from explicit entries -----------------------------
    explicit_indices = np.array(indices)
    explicit_max_scores = sim_matrix[explicit_indices].max(axis=1)

    calibration = {
        "mean": round(float(np.mean(explicit_max_scores)), 4),
        "std": round(float(np.std(explicit_max_scores)), 4),
        "p10": round(float(np.percentile(explicit_max_scores, 10)), 4),
        "p25": round(float(np.percentile(explicit_max_scores, 25)), 4),
        "p50": round(float(np.percentile(explicit_max_scores, 50)), 4),
    }

    # -- Specificity score ---------------------------------------------------
    entries_above_floor = int(above_floor_mask.sum())
    if entries_above_floor > 0:
        specificity = round(float(np.log(len(entry_ids) / entries_above_floor)), 4)
    else:
        specificity = round(float(np.log(len(entry_ids))), 4)

    # -- Build scores dict (only entries above floor) ------------------------
    entry_scores = {}
    above_indices = np.where(above_floor_mask)[0]
    for idx in above_indices:
        eid = entry_ids[idx]
        scores_list = [round(float(s), 4) for s in sim_matrix[idx]]
        entry_scores[str(eid)] = scores_list

    output["entities"][tag] = {
        "specificity": specificity,
        "entries_above_floor": entries_above_floor,
        "calibration": calibration,
        "prototypes": n_proto,
        "scores": entry_scores,
    }

    print(f"  {tag}: spec={specificity:.2f}, proto={n_proto}, "
          f"above_floor={entries_above_floor}, cal_mean={calibration['mean']:.3f}")

# -- Save --------------------------------------------------------------------

output_path = data_dir / "scores.json"
with open(output_path, "w") as f:
    json.dump(output, f)

size_mb = output_path.stat().st_size / (1024 * 1024)
print(f"\nSaved {output_path} ({size_mb:.1f} MB)")
print(f"Entities exported: {len(output['entities'])}")
```

**Step 4: Run tests to verify they pass**

Run: `cd sanderson-lore-visualization && source venv/bin/activate && pip install scikit-learn && python -m pytest tests/test_export_scores.py -v`
Expected: All tests PASS.

**Step 5: Commit**

```bash
git add sanderson-lore-visualization/notebooks/07_export_scores.py sanderson-lore-visualization/tests/test_export_scores.py
git commit -m "feat: add 07_export_scores.py with multi-prototype, calibration, and specificity"
```

---

## Task 2: Run Pipeline and Verify Output

**Files:**
- Read: `sanderson-lore-visualization/data/scores.json` (generated by Task 1)

### Step 1: Run the export script with real data

Run: `cd sanderson-lore-visualization && source venv/bin/activate && python notebooks/07_export_scores.py --model azure_openai`

### Step 2: Verify output size and basic stats

Run: `ls -lh data/scores.json`
Expected: Under 10 MB.

Run: `python -c "import json; d=json.load(open('data/scores.json')); print(f'Entities: {len(d[\"entities\"])}'); print(f'Model: {d[\"meta\"][\"model\"]}')"`

### Step 3: Check if scores.json needs to be gitignored

If scores.json is over 5 MB, add it to .gitignore and document download steps. Otherwise commit it.

### Step 4: Commit data

```bash
git add sanderson-lore-visualization/data/scores.json
git commit -m "data: add precomputed scores.json for interactive embedding controls"
```

---

## Task 3: Client-Side Tagging Engine (JS Module + Tests)

**Files:**
- Create: `sanderson-lore-visualization/tests/test_tagging_engine.html` (standalone test page)
- Will be embedded in: `sanderson-lore-visualization/index.html` (later in Task 4)

This task builds and tests the pure-logic recomputation engine that runs in the browser. The test page loads real scores.json and entries.json and runs assertions.

### Step 1: Write the test page

Create `tests/test_tagging_engine.html` -- a standalone HTML page that loads the real data files and runs assertions against the tagging engine functions. This is a "poor man's test runner" that works without Node/npm.

The test page should:
- Load `../data/scores.json` and `../data/entries.json` and `../data/graph.json`
- Import the tagging engine functions (inlined in the test page initially)
- Run tests that verify:
  - `computeImplicitTags()` returns tags above threshold
  - Calibration filtering narrows tags per entity
  - Specificity filtering removes hub entities
  - Margin filtering removes weakly-differentiated tags
  - Must-bridge filtering removes orphan tags
  - Edge rebuilding produces correct co-occurrence counts
- Display PASS/FAIL results in the page

### Step 2: Run via Playwright to verify tests fail

Run: `cd sanderson-lore-visualization && npx playwright test tests/test_tagging_engine.spec.js`
Expected: FAIL -- functions not implemented yet.

### Step 3: Implement the tagging engine

The tagging engine is a set of pure functions (no DOM dependency) that will be embedded in index.html:

```javascript
// -- Tagging Engine (pure functions) --

function computeEffectiveThreshold(entity, calibrationPercentile) {
    // Returns the threshold for this entity based on its calibration stats
    const cal = entity.calibration;
    const key = 'p' + calibrationPercentile;
    return cal[key] || cal.p25;  // fallback to p25
}

function filterBySpecificity(entities, minSpecificity) {
    // Returns entity names that pass the specificity filter
    const result = {};
    for (const [name, entity] of Object.entries(entities)) {
        if (entity.specificity >= minSpecificity) {
            result[name] = entity;
        }
    }
    return result;
}

function computeImplicitTags(params) {
    // params: { scores, entries, baselineGraph, settings }
    // settings: { calibrationPercentile, minSpecificity, confidenceMargin,
    //             mustBridge, twoProtoMin, threeProtoMin }
    // Returns: { implicitTags: [{entity, entryId, score}], stats: {...} }
}

function applyMarginFilter(candidateTags, margin) {
    // For each entry, reject tags where (best_score - this_score) > margin
}

function applyMustBridgeFilter(implicitTags, explicitTags) {
    // Only keep implicit tags on entries that have at least one other tag
}

function rebuildEdges(explicitTags, implicitTags, minEdgeWeight) {
    // Build co-occurrence edges from combined tags, return {edges, stats}
}
```

### Step 4: Run tests to verify they pass

Run: `npx playwright test tests/test_tagging_engine.spec.js`
Expected: All assertions pass.

### Step 5: Commit

```bash
git add sanderson-lore-visualization/tests/
git commit -m "feat: implement client-side tagging engine with real-data tests"
```

---

## Task 4: Frontend UI Controls

**Files:**
- Modify: `sanderson-lore-visualization/index.html`

### Step 1: Write Playwright test for controls existence

Create `tests/test_controls.spec.js` that verifies:
- Top bar renders with model selector, scope toggle, Apply button, stats
- Tuning panel expands/collapses
- All 8 sliders/controls exist
- Apply button triggers recomputation (stats update)

### Step 2: Run tests to verify they fail

### Step 3: Implement the controls UI in index.html

Add to `index.html`:
1. **CSS** for top bar, tuning panel, and slider styles (matching Stormlight theme)
2. **HTML** for the control elements (inserted between `#header` and `#graph-container`)
3. **JS** to wire up controls:
   - Load scores.json on page load
   - Apply button calls `computeImplicitTags()` and updates the graph
   - Stats display updates after each Apply
   - Sliders show their current values

Controls:
- Threshold slider (0.30 - 0.90, step 0.01, default 0.70)
- Calibration percentile slider (10 - 50, step 5, default 25)
- Min Specificity slider (0.0 - 5.0, step 0.1, default 2.0)
- Confidence Margin slider (0.00 - 0.15, step 0.01, default 0.05)
- 2-Proto Min slider (3 - 20, step 1, default 5)
- 3-Proto Min slider (5 - 50, step 1, default 10)
- Edge Layer radio (Explicit / Both / Implicit)
- Must-Bridge checkbox (default: checked)

### Step 4: Run tests to verify they pass

### Step 5: Commit

```bash
git add sanderson-lore-visualization/index.html sanderson-lore-visualization/tests/test_controls.spec.js
git commit -m "feat: add interactive embedding controls UI with all tuning sliders"
```

---

## Task 5: Hypothesis Layer + Review Panel

**Files:**
- Modify: `sanderson-lore-visualization/index.html`

### Step 1: Write tests for hypothesis layer and review panel

Playwright tests that verify:
- After clicking Apply, implicit edges render as dashed amber lines
- Explicit edges remain solid
- Edge layer toggle switches between explicit/both/implicit views
- Review panel drawer opens when toggled
- Review panel lists implicit tags with entity, entry, score
- Clicking confirm/reject updates the tag status
- Save Reviews generates downloadable JSON

### Step 2: Run tests to verify they fail

### Step 3: Implement hypothesis layer

In the D3 graph rendering:
- When rebuilding edges after Apply, annotate each edge with `type: "implicit"` or `type: "explicit"`
- Implicit edges: `stroke-dasharray: "6,4"`, `stroke: var(--gem-heliodor-glow)`, `stroke-opacity: 0.4`
- Explicit edges: solid lines (current behavior)
- Edge layer radio filters which edges are visible
- Tooltip on implicit edge hover shows confidence score

### Step 4: Implement review panel

- Right-side drawer (matches existing panel styling)
- Table of all implicit tags from the most recent Apply
- Each row: entity name, entry text (truncated), score, confirm/reject buttons
- Sorting: by score (asc/desc), by entity, by status
- Filter: unreviewed only
- Save/Load Reviews using File System Access API (same pattern as blog preview)
- Review status persists across Apply clicks (matched by entity+entryId key)

### Step 5: Run tests to verify they pass

### Step 6: Commit

```bash
git add sanderson-lore-visualization/index.html sanderson-lore-visualization/tests/
git commit -m "feat: add hypothesis layer (dashed implicit edges) and review panel"
```

---

## Task 6: End-to-End Integration Tests

**Files:**
- Create: `sanderson-lore-visualization/tests/test_e2e.spec.js`

### Step 1: Write comprehensive E2E test

Playwright test that exercises the full workflow with real data:

1. Open index.html, wait for graph to load
2. Verify baseline graph has no implicit edges
3. Click Apply with default settings
4. Verify implicit edges appear (dashed, amber)
5. Verify stats show tag count > 0
6. Change threshold slider to 0.90, click Apply
7. Verify tag count decreased
8. Change min specificity to 5.0, click Apply
9. Verify even fewer tags (hubs excluded)
10. Toggle edge layer to "Implicit only"
11. Verify only dashed edges visible
12. Open review panel
13. Verify it lists the implicit tags
14. Click reject on first tag
15. Verify status updates to rejected
16. Toggle edge layer back to "Both"

### Step 2: Run the test

Run: `cd sanderson-lore-visualization && npx playwright test tests/test_e2e.spec.js --headed`
Expected: All steps pass.

### Step 3: Commit

```bash
git add sanderson-lore-visualization/tests/test_e2e.spec.js
git commit -m "test: add E2E integration tests for embedding controls workflow"
```

---

## Task 7: Deploy and Final Commit

**Files:**
- Modify: `sanderson-lore-visualization/requirements.txt` (add scikit-learn)

### Step 1: Update requirements.txt

Add `scikit-learn` to requirements.txt (needed for k-means in 07_export_scores.py).

### Step 2: Run all tests

Run: `cd sanderson-lore-visualization && source venv/bin/activate && python -m pytest tests/ -v && npx playwright test tests/`
Expected: All tests pass.

### Step 3: Deploy to GitHub Pages

Copy updated files to `/tmp/cosmere-graph/` and push to `varunr89/cosmere-graph`.
Make sure to include `data/scores.json` in the deploy.

### Step 4: Final commit

```bash
git add -A sanderson-lore-visualization/
git commit -m "feat: complete interactive embedding controls with hypothesis layer and review panel"
```

---

## Implementation Notes

### Real Data Locations
- Embeddings: `data/embeddings_cache/azure_openai.npy` (191 MB, 16282 x 3072)
- Entry IDs: `data/embeddings_cache/entry_ids.json`
- Raw WoB: `../../words-of-brandon/wob_entries.json` (16,282 entries)
- Tag classifications: `data/tag_classifications.json`
- Current graph: `data/graph.json`
- Current entries: `data/entries.json`

### Virtual Environment
- Location: `sanderson-lore-visualization/venv/`
- Activate: `source sanderson-lore-visualization/venv/bin/activate`

### Key Constraints
- scores.json must be under 10 MB for reasonable browser loading
- The floor (0.30) determines file size -- higher floor = smaller file
- k-means with k=2 on 5 entries may be unstable; use n_init=10 and random_state=42
- All frontend computation must complete in < 2 seconds for good UX
- D3 force simulation should restart with low alpha after Apply to avoid jarring layout changes
