# The Integral Problem -- Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the `ai-productivity-gap/` project: two charts and a blog post arguing that AI adoption follows a power law, so organizational productivity barely moves.

**Architecture:** Python scripts generate two matplotlib charts. A markdown blog post references them. No notebooks needed -- the charts are illustrative, not exploratory.

**Tech Stack:** Python 3, matplotlib, numpy. Minimal dependencies.

**Design doc:** `docs/plans/2026-02-14-ai-productivity-gap-design.md`

---

### Task 1: Scaffold the project directory

**Files:**
- Create: `ai-productivity-gap/README.md`
- Create: `ai-productivity-gap/requirements.txt`
- Create: `ai-productivity-gap/data/.gitkeep`
- Create: `ai-productivity-gap/notebooks/.gitkeep`
- Create: `ai-productivity-gap/charts/.gitkeep`
- Create: `ai-productivity-gap/post/.gitkeep`

**Step 1: Create the directory structure**

```bash
cd /Users/varunr/projects/short_projects
mkdir -p ai-productivity-gap/{data,notebooks,charts,post}
touch ai-productivity-gap/data/.gitkeep ai-productivity-gap/notebooks/.gitkeep ai-productivity-gap/charts/.gitkeep
```

**Step 2: Write requirements.txt**

```
matplotlib>=3.7
numpy>=1.24
```

**Step 3: Write README.md**

```markdown
# The Integral Problem: Why AI Isn't Moving the Productivity Needle

A study on why enterprise AI adoption hasn't translated to broad productivity gains, despite an explosion of capable AI tools.

## Data Sources

- McKinsey State of AI Survey (2024, 2025)
- Anthropic Economic Index (September 2025)
- GitHub Copilot usage statistics
- Stack Overflow Developer Survey 2024
- Worklytics 2025 AI Adoption Benchmarks

## Key Findings

- 88% of organizations say they "use AI," but only 7% have fully scaled it
- AI usage follows a power law: Gini coefficients of 0.84-0.86 (Anthropic data)
- Frontier workers send 6x more messages than median enterprise users
- 74% of companies show no tangible value from AI investments
- The gap between AI capability and enterprise adoption is widening

## Methodology

Conceptual/illustrative charts built from survey data and firsthand observation. This is an argument piece, not a statistical study.
```

**Step 4: Set up virtual environment and install deps**

```bash
cd /Users/varunr/projects/short_projects/ai-productivity-gap
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Step 5: Commit**

```bash
git add ai-productivity-gap/
git commit -m "scaffold: ai-productivity-gap project structure"
```

---

### Task 2: Build Chart 1 -- The Productivity Curve

**Files:**
- Create: `ai-productivity-gap/notebooks/01_productivity_curve.py`
- Output: `ai-productivity-gap/charts/01_productivity_curve.png`

**Step 1: Write the chart script**

Create `ai-productivity-gap/notebooks/01_productivity_curve.py`:

The chart must show:
- X-axis: Employee percentile (0 to 100)
- Y-axis: Productivity (arbitrary units, no numbers needed)
- Curve 1 ("Before AI"): A smooth, slightly concave-up curve rising from left to right. This represents the baseline distribution -- most employees cluster in the middle, top performers at the right.
- Curve 2 ("After AI"): Nearly identical to Curve 1 for the first ~90% of the x-axis, then lifts noticeably above it for the top ~10%. This shows only top-percentile employees gaining from AI.
- Shaded area between the two curves, labeled "Net organizational productivity gain" -- visually small.
- Clean, minimal style. No gridlines. Light gray background or white. Two distinct colors for the curves.
- Legend in upper left.
- Title: "The Integral Problem"
- Subtitle or annotation: "Organizational output = area under the curve. If only the top 5% adopt AI, the total area barely changes."

Use a mathematical approach:
- Before AI: `y = x^1.5` (or similar convex curve, normalized)
- After AI: same curve but add a bump for x > 90th percentile (e.g., multiply by a logistic function that kicks in at x=90)

Style reference: clean, modern, magazine-quality. Use Helvetica/Arial fonts if available. Tight layout, no wasted space. Save at 300 DPI, 10x6 inches.

**Step 2: Run the script and verify output**

```bash
cd /Users/varunr/projects/short_projects/ai-productivity-gap
source .venv/bin/activate
python notebooks/01_productivity_curve.py
open charts/01_productivity_curve.png
```

Verify: Two curves that are nearly identical except at the far right. Small shaded area. Clean styling.

**Step 3: Iterate on the chart if needed**

Adjust curve parameters, colors, fonts, label positions until the visual punchline is immediate: the shaded area is tiny.

**Step 4: Commit**

```bash
git add notebooks/01_productivity_curve.py charts/01_productivity_curve.png
git commit -m "feat: add productivity curve chart (the integral problem)"
```

---

### Task 3: Build Chart 2 -- The Capability-Adoption Gap

**Files:**
- Create: `ai-productivity-gap/notebooks/02_capability_adoption_gap.py`
- Output: `ai-productivity-gap/charts/02_capability_adoption_gap.png`

**Step 1: Write the chart script**

Create `ai-productivity-gap/notebooks/02_capability_adoption_gap.py`:

This chart needs real dates on the x-axis with model release markers. Here are the key dates:

**AI Model/Tool Releases (capability milestones):**
- 2023-03-14: GPT-4
- 2023-06-29: GitHub Copilot Chat (beta)
- 2023-07-06: ChatGPT Code Interpreter
- 2023-12-06: Gemini 1.0 Pro
- 2024-02-15: Gemini 1.5 Pro (preview)
- 2024-03-04: Claude 3 Opus
- 2024-05-13: GPT-4o
- 2024-06-20: Claude 3.5 Sonnet
- 2024-12-11: Gemini 2.0 Flash
- 2025-02-24: Claude Code (preview)
- 2025-02-27: GPT-4.5
- 2025-03-25: Gemini 2.5 Pro
- 2025-04-16: OpenAI Codex CLI
- 2025-05-22: Claude Opus 4
- 2026-02-05: Claude Opus 4.6

Not all of these need labels -- pick ~8-10 that are the most significant to avoid clutter. Must include at least one from each provider (OpenAI, Anthropic, Google) and the CLI/agentic tools.

**Adoption data points (approximate, from research):**
- Mid-2023: ~55% of orgs say they use AI (McKinsey 2023)
- Early 2024: ~65% regularly using gen AI (McKinsey 2024)
- Mid-2024: ~62% of developers using AI tools (Stack Overflow)
- Early 2025: ~78-88% of orgs claim AI use, but only 7% fully scaled (McKinsey 2025)
- 2025: Only 31% of employees use AI regularly (Worklytics)
- 2025: 74% of companies show no tangible value (Worklytics)

The chart must show:
- X-axis: Timeline from March 2023 to February 2026
- Y-axis: Qualitative scale (no numbers) -- "Low" to "High"
- Line 1 ("AI Capability"): Steep upward curve with markers at major releases. Color-code markers by provider (e.g., OpenAI = green, Anthropic = orange, Google = blue).
- Line 2 ("Enterprise Adoption"): Nearly flat, slight upward drift. Anchored by the adoption data points above.
- Shaded area between the lines, labeled "Unrealized productivity"
- The gap should clearly widen over time

Style: Match Chart 1's visual language. Same fonts, similar color palette, 300 DPI, 10x6 inches.

**Step 2: Run the script and verify**

```bash
cd /Users/varunr/projects/short_projects/ai-productivity-gap
source .venv/bin/activate
python notebooks/02_capability_adoption_gap.py
open charts/02_capability_adoption_gap.png
```

Verify: Clear widening gap. Model releases legible but not cluttered. Provider colors distinguishable.

**Step 3: Iterate on readability**

Label placement is the hardest part. May need to alternate label positions (above/below), use smaller font for dates, or reduce to fewer markers if cluttered.

**Step 4: Commit**

```bash
git add notebooks/02_capability_adoption_gap.py charts/02_capability_adoption_gap.png
git commit -m "feat: add capability-adoption gap timeline chart"
```

---

### Task 4: Write the blog post draft

**Files:**
- Create: `ai-productivity-gap/post/draft.md`

**Step 1: Write the full draft**

Create `ai-productivity-gap/post/draft.md` following the structure from the design doc (`docs/plans/2026-02-14-ai-productivity-gap-design.md`).

Key writing rules:
- **No em-dashes.** Use commas, periods, or parentheses instead.
- **First person throughout.** "I've seen this." Not "organizations should consider."
- **Raw, not polished.** Short sentences. Some fragments. Frustration should come through.
- **No hedging.** Not "AI might help." Say "AI works, and we're squandering it."
- **Specific over abstract.** Ground every claim in an observation or data point.
- **No AI buzzwords.** No "revolutionize," "transform," "unlock potential."
- **Anonymized.** "A large tech company" -- never name the employer.
- **Lead GitHub Copilot CLI** when listing terminal tools, then Claude Code, Codex CLI, etc.

Structure (from design doc):

1. **Opening hook** -- The 1-in-20 observation. Set the scene: the AI boom, the tools shipped, and the reality on the ground.

2. **The Integral Problem** -- Introduce the productivity curve chart. Explain the math: org output = integral of the productivity distribution. If only the right tail moves, the area barely changes.
   - Reference Chart 1: `![The Integral Problem](../charts/01_productivity_curve.png)`

3. **The Capability-Adoption Gap** -- Introduce the timeline chart. Model after model ships, adoption stays flat.
   - Reference Chart 2: `![The Capability-Adoption Gap](../charts/02_capability_adoption_gap.png)`
   - Weave in key data: 88% "use AI" but 7% fully scaled. 74% show no tangible value. Gini coefficient of 0.84-0.86.

4. **Why the gap exists** -- Five reasons, each a short subsection:
   - Learning curve is real (paternity leave anecdote)
   - Belief deficit (AI slop is a human problem, not an AI problem)
   - Bad training ("every training was a marketing demo")
   - Enterprise gatekeeping (shadow AI)
   - Productivity is personal

5. **What to do Monday morning** -- Five CTAs:
   - CTA 1: Mandate the AI path with patience (tactical tornado, review loops, belief)
   - CTA 2: Invest in applied training, not demos
   - CTA 3: Embrace CLI-level tools (customer campaign anecdote)
   - CTA 4: Accept that productivity is personal
   - CTA 5: Enable, don't gate (regulation parallel)

6. **Close** -- Generational opportunity. The bottleneck is organizational. Here's what to do.

**Step 2: Review the draft**

Read through for:
- No em-dashes anywhere
- Raw, honest tone throughout
- Charts referenced with correct relative paths
- Data points cited inline (source name, not URLs)
- No named employer
- GitHub Copilot CLI listed first among terminal tools

**Step 3: Commit**

```bash
git add ai-productivity-gap/post/draft.md
git commit -m "feat: add blog post draft -- The Integral Problem"
```

---

### Task 5: Final review and README update

**Files:**
- Modify: `README.md` (root)
- Review: all files in `ai-productivity-gap/`

**Step 1: Add project to root README index**

Add a row to the project index table in `/Users/varunr/projects/short_projects/README.md`:

```markdown
| [ai-productivity-gap](ai-productivity-gap/) | Why AI isn't moving the enterprise productivity needle | In progress |
```

**Step 2: Final review pass**

- Read `post/draft.md` end to end
- Verify both charts render and look correct when referenced from the post
- Check no em-dashes slipped in
- Verify tone is raw and first-person throughout

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add ai-productivity-gap to project index"
```
