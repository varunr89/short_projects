# short_projects -- Repository Rules

This repository contains short analysis projects that each result in a blog post article.

## Repository Structure

```
short_projects/
├── README.md                  <- Repo-level overview and index of all projects
├── <project-name>/            <- One directory per project (kebab-case)
│   ├── README.md              <- Project overview: goal, data sources, key findings
│   ├── data/                  <- Raw and processed data files
│   │   └── .gitkeep
│   ├── notebooks/             <- Jupyter notebooks and analysis scripts
│   ├── charts/                <- Generated visualizations and figures
│   ├── post/                  <- Final blog post draft(s) in Markdown
│   │   └── draft.md
│   └── requirements.txt       <- Python dependencies specific to this project
└── .claude/
    └── CLAUDE.md              <- This file
```

## Rules

### Project Isolation
- Every project lives in its own top-level directory. No project files in the repo root.
- Use **kebab-case** for project directory names (e.g., `india-air-quality`, `king-county-housing-heatmap`).
- Each project is self-contained: its own data, notebooks, outputs, and dependencies.

### Graduation to Own Repo
- If a project exceeds **500 lines of code** (excluding markdown, data, and config), it has outgrown short_projects and should be promoted to its own repository under `/Users/varunr/projects/<project-name>/`.
- Move the entire project directory out, initialize a new git repo, and remove it from short_projects.
- Add a one-line entry to the root `README.md` noting the project graduated with a link to its new repo.

### Required Files per Project
- **`README.md`** -- Must include: one-line summary, data source(s), methodology overview, and key findings.
- **`post/draft.md`** -- The blog post draft. This is the primary deliverable of every project.
- **`requirements.txt`** -- Pin all Python dependencies used by the project.

### Data
- Raw data goes in `data/`. Do not commit large datasets (>10 MB) -- use `.gitignore` and document the download steps in the project README instead.
- Processed/intermediate data may also live in `data/` with a clear naming convention (e.g., `raw_sales.csv` vs `processed_sales.csv`).

### Notebooks and Scripts
- Notebooks go in `notebooks/`. Use numbered prefixes for ordering (e.g., `01_data_exploration.ipynb`, `02_analysis.ipynb`).
- Standalone Python scripts also go in `notebooks/` if they are part of the analysis pipeline.

### Visualizations
- All generated charts and figures go in `charts/`.
- Use numbered prefixes matching the notebook that generated them (e.g., `01_timeseries.png`).
- Use descriptive filenames -- no `output.png` or `fig1.png`.

### Blog Post
- Every project must produce a blog post draft in `post/draft.md`.
- The draft should be written in Markdown and be suitable for publishing.
- Reference charts using relative paths: `![description](../charts/01_timeseries.png)`.

### Blog Writing Constitution

#### Research
- Open with a personal observation or experience. Find research that supports it, not the other way around.
- 1-2 strong data points per section, preferring recent (last 5 years) tech industry sources. Expand to other years/industries only if nothing recent fits.
- Every stat needs a "so what" -- if you can't tie it back to a personal insight, cut it.

#### First Draft
- Every paragraph leads with personal experience. Research is support, never the opener.
- Write in first person. "I tested," "I saw," "when I followed up." Never "the author" or "the user."
- Target 1,500-2,500 words. Shorter is almost always better.
- Include charts early and often. Charts are personal and engaging, not decoration.

#### Editing
- Zero em-dashes. They are the single biggest tell that AI wrote it.
- Vary sentence length. Use fragments for punch. One-sentence paragraphs are fine.
- Use parentheses or periods where you'd reach for an em-dash.
- Read it out loud (or imagine reading it). If a sentence sounds like a press release, rewrite it.
- Second-person "you try it" moments make the reader lean in. Use them.

#### Formatting
- Horizontal rules before h2 sections for visual separation. h3s stay subordinate (no rules).
- Charts get descriptive alt text and italic source captions beneath them.
- Blockquotes for the one key insight per major section. Not for every quote.
- TL;DR box at the top: problem, hypothesis, what to do.

### Publishing Drafts to bhavanaai
- When a blog draft is ready for review, always create it as a **draft** in the bhavanaai repo at `/Users/varunr/projects/bhavanaai/` so it's viewable on the web via the admin layer.
- Create `src/content/blog/<project-name>.md` with frontmatter: `title`, `date`, `description`, and `draft: true`.
- Copy chart images to `public/images/blog/<project-name>/` and use absolute paths in the markdown: `![alt](/images/blog/<project-name>/filename.png)`.
- This makes the draft accessible at `me.bhavanaai.com/blog/<project-name>` for review and inline commenting from any device.

### Blog Preview and Feedback Loop
- Every project should have a `post/preview.html` that renders the blog draft as a publishable preview with full styling, embedded charts, dark mode support, a "DRAFT PREVIEW" banner, and an **inline commenting system**.
- **Whenever you read or review a blog draft (`post/draft.md`), automatically regenerate `post/preview.html` from it and open it in the browser** so the author can see exactly how it will look to readers.
- The preview uses relative image paths (`../charts/filename.png`) so it works locally without a server.
- Match the styling of the bhavanaai Astro blog: system-ui font, 42rem max-width, 1.125rem base font size, 1.7 line-height, dark mode via `prefers-color-scheme`.

#### Inline Commenting System
- The preview includes a Google Docs-style commenting UI: select text, click "Comment," type feedback, and the comment appears as a right-margin annotation.
- Comments persist in `localStorage` across page refreshes.
- "Save Feedback" button in the banner exports comments to `post/feedback.json` via the File System Access API.

#### Feedback Workflow
1. Author opens `post/preview.html` in Chrome and reads the draft.
2. Author selects text and adds inline comments on anything that needs changes.
3. Author clicks "Save Feedback" and saves to `post/feedback.json`.
4. Author tells Claude to "read my feedback" or "apply feedback."
5. Claude reads `post/feedback.json`, applies each comment's requested changes to `post/draft.md`, regenerates `post/preview.html` (preserving the commenting system), and opens it in the browser.
6. Claude summarizes what was changed for each comment.
7. Repeat until the draft is finalized.

### Python Environment
- Always use a virtual environment. Never install packages globally.
- Each project has its own `requirements.txt`.

### Git Workflow
- Develop each new project on a feature branch off `main`.
- Branch naming: `project/<project-name>` (e.g., `project/india-air-quality`).
- Merge to `main` only when the project is complete and the blog post draft is finalized.

### README Index
- When a project is merged to `main`, add it to the root `README.md` project index table with: project name (linked), one-line description, date completed, and status.
