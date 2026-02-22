# The Car Wash Test -- Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a blog post analyzing the viral "car wash" adversarial reasoning test across 9 frontier AI models.

**Architecture:** Content project with screenshots, a Markdown blog draft, and an HTML preview with inline commenting. No code/analysis -- this is a writing project with asset management.

**Tech Stack:** Markdown, HTML/CSS/JS (preview template from ai-productivity-gap project)

---

### Task 1: Set up project directory structure

**Files:**
- Create: `the-car-wash-test/README.md`
- Create: `the-car-wash-test/data/.gitkeep`
- Create: `the-car-wash-test/notebooks/.gitkeep`
- Create: `the-car-wash-test/charts/` (will be populated in Task 2)
- Create: `the-car-wash-test/post/` (will be populated in Task 3)
- Create: `the-car-wash-test/requirements.txt`

**Step 1: Create directory structure**

```bash
mkdir -p the-car-wash-test/{data,notebooks,charts,post}
touch the-car-wash-test/data/.gitkeep
touch the-car-wash-test/notebooks/.gitkeep
touch the-car-wash-test/requirements.txt
```

**Step 2: Write project README**

Create `the-car-wash-test/README.md` with:

```markdown
# The Car Wash Test

**Summary:** Which frontier AI models can figure out that you need to drive your car to the car wash?

## Data Sources

- Direct testing of 9 model configurations across OpenAI, Google, and Anthropic (February 2026)
- Screenshots of each model's response

## Methodology

Same prompt ("I need to wash my car. The car wash is only 100 meters away. Should I walk or take my car there?"), clean session, no priming, first-shot evaluation across:
- OpenAI: ChatGPT 5.2 Instant, Thinking, Pro
- Google: Gemini 3 Fast, Thinking, Pro
- Anthropic: Claude Haiku 4.5, Sonnet 4.5, Opus 4.6

## Key Findings

- OpenAI: 0/3 passed (all recommend walking, even after 2m 45s of reasoning)
- Google: 3/3 passed (all correctly identify the car must be present)
- Anthropic: 2/3 passed (Haiku fails, Sonnet and Opus pass)
```

**Step 3: Commit**

```bash
git add the-car-wash-test/
git commit -m "feat: scaffold the-car-wash-test project structure"
```

---

### Task 2: Move and rename screenshots

**Files:**
- Move from: `AI idiocy/*.png` and `AI idiocy/*.mov`
- Move to: `the-car-wash-test/charts/` with descriptive names

**Step 1: Copy and rename screenshots**

Map each screenshot to a descriptive filename:

| Source | Destination |
|--------|-------------|
| `Screenshot 2026-02-15 at 3.14.47 PM.png` | `01_chatgpt_52_instant.png` |
| `Screenshot 2026-02-15 at 3.16.15 PM.png` | `02_chatgpt_52_thinking_followup.png` |
| `Screenshot 2026-02-15 at 3.16.33 PM.png` | `03_chatgpt_52_thinking.png` |
| `Screenshot 2026-02-15 at 3.17.51 PM.png` | `04_gemini_3_fast.png` |
| `Screenshot 2026-02-15 at 3.19.59 PM.png` | `05_chatgpt_52_pro.png` |
| `Screenshot 2026-02-15 at 3.20.40 PM.png` | `06_claude_haiku_45.png` |
| `Screenshot 2026-02-15 at 3.21.09 PM.png` | `07_claude_sonnet_45.png` |
| `Screenshot 2026-02-15 at 3.21.30 PM.png` | `08_claude_opus_46.png` |
| `Screenshot 2026-02-15 at 3.29.48 PM.png` | `09_gemini_3_thinking.png` |
| `Screenshot 2026-02-15 at 3.30.29 PM.png` | `10_gemini_3_pro.png` |
| `Screen Recording 2026-02-15 at 3.19.15 PM.mov` | `gemini_screen_recording.mov` |

```bash
cp "AI idiocy/Screenshot 2026-02-15 at 3.14.47 PM.png" the-car-wash-test/charts/01_chatgpt_52_instant.png
cp "AI idiocy/Screenshot 2026-02-15 at 3.16.15 PM.png" the-car-wash-test/charts/02_chatgpt_52_thinking_followup.png
# ... etc for all files
```

**Step 2: Commit**

```bash
git add the-car-wash-test/charts/
git commit -m "feat: add model response screenshots to the-car-wash-test"
```

---

### Task 3: Write the blog post draft

**Files:**
- Create: `the-car-wash-test/post/draft.md`

**Step 1: Write the full blog draft**

Follow the structure from the design document (`docs/plans/2026-02-15-the-car-wash-test-design.md`):

1. **Hook** (~200 words): GPT 5.2 Pro quantum breakthrough contrast. Introduce the meme. Frame the test.
2. **The Test** (~300 words): Methodology, results table (pass/fail with notes), key callouts (OpenAI 0/3, Google 3/3, Anthropic 2/3). Reference screenshots.
3. **Accessible Analysis** (~300 words): Pre-training bias intuition, pattern-match vs. contextual reasoning, the 5.2 Pro paradox.
4. **Deeper Layer** (~300 words): Pre-training distributions vs. RL reasoning, why chain-of-thought fails here, speculation on Gemini's success.
5. **Broader Pattern** (~200 words): Strawberry counting, 9.11 vs 9.9, common thread of adversarial reasoning.
6. **Closing** (~150 words): Testing edges makes AI better, the author believes in AI's potential, end with "the best way to trust AI more is to understand where it fails."

Tone: First-person, opinionated, irreverent but respectful. No em-dashes (per CLAUDE.md rules).

Reference all screenshots using relative paths: `![description](../charts/filename.png)`

**Step 2: Commit**

```bash
git add the-car-wash-test/post/draft.md
git commit -m "feat: write car wash test blog draft"
```

---

### Task 4: Generate the preview HTML

**Files:**
- Create: `the-car-wash-test/post/preview.html`
- Reference: `ai-productivity-gap/post/preview.html` (template source)

**Step 1: Generate preview.html**

Convert `post/draft.md` to HTML and wrap it in the preview template from `ai-productivity-gap/post/preview.html`. This includes:

- Full CSS styling (system-ui font, 42rem max-width, dark mode, etc.)
- DRAFT PREVIEW banner with Save Feedback and Clear All Comments buttons
- Page layout with comments column
- Full commenting system JavaScript
- All images referenced with relative paths (`../charts/filename.png`)
- Table styling for the results table

Adapt the template title, date, and content. Keep all commenting system code intact.

**Step 2: Open preview in browser**

```bash
open the-car-wash-test/post/preview.html
```

**Step 3: Commit**

```bash
git add the-car-wash-test/post/preview.html
git commit -m "feat: add preview HTML for car wash test blog"
```

---

### Task 5: Clean up source directory

**Files:**
- Remove: `AI idiocy/` (original unorganized screenshots)

**Step 1: Verify all files were copied**

Confirm all 11 files from `AI idiocy/` exist in `the-car-wash-test/charts/` with correct names.

**Step 2: Remove original directory**

```bash
rm -rf "AI idiocy/"
```

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove original AI idiocy directory after migration"
```
