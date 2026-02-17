# AI Tools Evolution

**Summary:** How I went from copy-pasting ChatGPT output to orchestrating multi-model architecture reviews -- told through two versions of the same podcast summarizer.

## Data Sources

- GitHub repos: `varunr89/podcast_summarizer` (v1) and `varunr89/podcast-summarizer-v2` (v2)
- Claude Code conversation archives (episodic memory)
- Phone-a-friend consultation logs from `.claude/phone-a-friend/`
- Git commit histories and design documents

## Methodology

- Cloned v1 repo for structural analysis (file counts, LOC, dependency analysis)
- Analyzed v2 repo in-place (already local)
- Searched conversation archives for key development moments
- Read all 12 phone-a-friend consultation logs
- Compared commit timelines, design doc density, and code metrics

## Key Findings

- V1: 80 files, ~10K LOC, 50 dependencies, 4 unused summarizers, 8-month development
- V2: 290 commits in 5 weeks, 22K LOC + 22K tests, 47 design docs, proper CI/CD
- January 5 production crisis led to 4-revision redesign reviewed by GPT-5.2 Codex
- 12 phone-a-friend consultations found critical bugs that would have been production failures
