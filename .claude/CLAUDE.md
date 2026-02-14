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

### Blog Preview
- Every project should have a `post/preview.html` that renders the blog draft as a publishable preview with full styling, embedded charts, dark mode support, and a "DRAFT PREVIEW" banner.
- **Whenever you read or review a blog draft (`post/draft.md`), automatically regenerate `post/preview.html` from it and open it in the browser** so the author can see exactly how it will look to readers.
- The preview uses relative image paths (`../charts/filename.png`) so it works locally without a server.
- Match the styling of the bhavanaai Astro blog: system-ui font, 42rem max-width, 1.125rem base font size, 1.7 line-height, dark mode via `prefers-color-scheme`.

### Python Environment
- Always use a virtual environment. Never install packages globally.
- Each project has its own `requirements.txt`.

### Git Workflow
- Develop each new project on a feature branch off `main`.
- Branch naming: `project/<project-name>` (e.g., `project/india-air-quality`).
- Merge to `main` only when the project is complete and the blog post draft is finalized.

### README Index
- When a project is merged to `main`, add it to the root `README.md` project index table with: project name (linked), one-line description, date completed, and status.
