# AI Tools Evolution Blog Post -- Design
Date: 2026-02-16

## Goal
Write a long-form blog post about the author's evolution using AI development tools, told through the lens of two versions of the same project: a podcast summarizer.

## Angle
All three woven together: personal growth story, technical comparison, and AI tools evolution. Long-form, chapter-style.

## Key Decisions
- **V1 access**: Deep analysis via cloned repo (at /tmp/podcast_summarizer)
- **Infrastructure story**: Include Supabase-to-Azure migration as dedicated chapter
- **Phone-a-friend**: Major feature with specific examples from consultation logs
- **Failure candor**: Very candid about production failures, debugging, over-engineering
- **First person**: Always. Never "the author" or "the user."

## Chapter Structure

### Chapter 1: The Problem (~300 words)
Too many podcasts, too few hours. Managing a kid, obligations. The lightbulb: distill podcast knowledge into daily/weekly email summaries.

### Chapter 2: V1 -- The Naive Builder (~800 words)
- Browser-based Claude/ChatGPT, then VS Code
- Timeline: March-November 2025, 30 commits over 8 months
- The "every best practice" trap:
  - 4 summarizers (LangChain, LlamaIndex, Spacy, Ensemble) -- only 1 used
  - 4 download strategies
  - Dual APIs (FastAPI + Flask) connected by Azure Service Bus
  - 50 dependencies, 30+ env vars
  - summaries.py: 5,739 lines in one file
  - Tkinter GUI test wrapper
- Concrete metrics: 80 Python files, ~10K LOC, complexity score 8/10
- It worked. It was a mess.

### Chapter 3: The Gap (~400 words)
- V1 stalled after May 2025
- What changed: discovered Claude Code, learned about distributed systems simplicity
- The decision to start fresh rather than refactor

### Chapter 4: V2 -- The Informed Builder (~1,000 words)
- Started December 18, 2025 with a design document, not code
- "Batch-first, cost-first" philosophy
- Key simplifications vs v1:
  - 1 summarizer, 1 LLM, 1 database
  - Episode-level summaries (shared, not per-user)
  - Design-first approach: 47 design docs in 5 weeks
- Velocity: 290 commits in 5 weeks, Christmas sprint (78 commits in 2 days)
- Metrics: 22K LOC production + 22K LOC tests, 86 test files

### Chapter 5: Platform Evolution -- Supabase to Azure (~600 words)
- V1: Supabase (PostgreSQL + Postgrest), Azure Service Bus, scattered cloud services
- V2: Azure-everything (SQL serverless, Blob, Container Apps, ACS Email, AI Foundry)
- Why consolidation matters for a solo developer
- Infrastructure as Code (Bicep) vs manual setup
- Cost model: ~$50-80/month

### Chapter 6: The Crisis (~600 words)
- January 5, 2026: 24 failed validations, 5 stuck jobs
- Connection pool exhaustion (QueuePool limit of 5 overflow 10)
- Root cause: N validations = N batch jobs competing for resources
- The moment of realization: even v2's "simple" architecture had a critical flaw

### Chapter 7: Phone-a-Friend (~1,000 words, expanded)
- The multi-model review pattern
- First review (Jan 6, 2:30 AM): GPT-5.2 Codex on high reasoning
  - Recommended DB lease instead of Azure SDK check
  - Identified zombie work, stuck deliveries, pool exhaustion risks
- Second review (Jan 6, 4:15 AM): Final design review
  - Found trigger race condition (check-then-trigger TOCTOU)
  - Recommended per-delivery lease with heartbeats
  - Added anti-starvation (oldest quota)
- Third review (Jan 6, 2:30 PM): Rev 4 with xhigh reasoning
  - Found CRITICAL owner ID handoff bug
  - Found premature attempt increment
  - Led to major architectural change: orchestrator becomes router-only
- 12 total phone-a-friend consultations across the project
- What this pattern teaches about AI collaboration

### Chapter 8: What I Actually Learned (~600 words)
1. AI tools changed what I could build, not just how fast
2. Over-engineering is the default failure mode when AI writes code for you
3. Design documents > code
4. Multiple AI models checking each other = having a team
5. Simpler is always better
6. The CLAUDE.md constraint list as guardrails

### Epilogue (~200 words)
The service works. Daily summaries arrive. The kid is fine.

## Data/Evidence to Include
- V1 vs V2 metrics comparison table
- Git commit timeline visualization
- Code snippets showing v1 over-engineering vs v2 simplicity
- Phone-a-friend consultation severity table
- Architecture diagrams (before/after)
- Screenshots of GitHub repos

## Estimated Length
~5,500-6,000 words
