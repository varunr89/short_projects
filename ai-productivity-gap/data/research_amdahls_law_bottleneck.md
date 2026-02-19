# Research Notes: Amdahl's Law, Bottleneck Shifting, and the AI Coding Productivity Paradox

**Research date:** February 2026

---

## 1. Amdahl's Law Applied to AI Workflows

### The Formula

Amdahl's Law (1967) states that the overall speedup of a system is limited by the fraction of the task that cannot be improved:

```
Speedup = 1 / ((1 - p) + (p / s))
```

Where:
- `p` = fraction of the task that can be improved (e.g., coding)
- `s` = speedup factor for that fraction (e.g., 2x with AI)
- `(1 - p)` = the serial/unimprovable fraction (design, review, testing, meetings, coordination)

### Applied to Software Development

If coding is 20% of a developer's time and AI makes coding 2x faster:

```
Speedup = 1 / ((1 - 0.20) + (0.20 / 2))
        = 1 / (0.80 + 0.10)
        = 1 / 0.90
        = 1.11x (11% overall improvement)
```

If coding is 30% of a developer's time and AI makes coding 2x faster:

```
Speedup = 1 / ((1 - 0.30) + (0.30 / 2))
        = 1 / (0.70 + 0.15)
        = 1 / 0.85
        = 1.18x (18% overall improvement)
```

Even if AI makes coding **infinitely fast** (s = infinity), the maximum speedup is:

```
Max speedup = 1 / (1 - p)
```

- If coding is 20% of time: max speedup = 1 / 0.80 = **1.25x (25%)**
- If coding is 30% of time: max speedup = 1 / 0.70 = **1.43x (43%)**

**The implication is stark.** Even a magical AI that writes code instantaneously can only improve overall developer productivity by 25-43%, because 70-80% of the work isn't coding.

### Explicit Amdahl's Law + AI Commentary

**AmazingCTO (Stephan Schmidt):** "Amdahl's Law, from 1967, perfectly describes everything about AI productivity and explains why some people think productivity is way up and some see negligible impact." The author experienced a 2-3x speed increase in the "idea to code" portion when using Cursor AI, but found that "the time between AI usage -- thinking and deciding -- is limiting my productivity gain." The bottleneck shifts to task planning, decision-making, and maintaining TODO lists. The insight: teams need to minimize time spent on non-AI tasks to realize gains.

Source: [AmazingCTO](https://www.amazingcto.com/amdahls-law-and-ai-productivity/)

**Pullflow / The Great AI Productivity Paradox:** "AI-driven coding gains evaporate when review bottlenecks, brittle testing, and slow release pipelines can't match the new velocity -- a reality captured by Amdahl's Law: a system moves only as fast as its slowest link."

Source: [Pullflow](https://pullflow.com/blog/the-great-ai-productivity-paradox-are-we-actually-coding-faster)

**Semi Engineering:** Published "Amdahl Limits on AI" discussing how the theoretical speedup is always limited by the non-parallelizable portion, a concept directly applicable to knowledge work where only certain tasks can be AI-assisted.

Source: [Semi Engineering](https://semiengineering.com/amdahl-limits-on-ai/)

---

## 2. How Developers Actually Spend Their Time

Multiple studies converge on the same finding: coding is a minority of developer time.

### Microsoft "Time Warp" Study (2024)

- **Sample:** 484 Microsoft developers surveyed June-July 2024
- **Published:** February 2025 (arXiv)

**Actual time allocation:**
| Activity | % of Workweek |
|----------|--------------|
| Communication & Meetings | ~12% |
| Coding | ~11% |
| Debugging | ~9% |
| Architecting & designing | ~6% |
| Pull requests / Code review | ~5% |
| Other (testing, compliance, monitoring, etc.) | ~57% |

**Ideal (preferred) time allocation:**
- Coding: ~20% (vs. 11% actual)
- Architecting & design: ~15% (vs. 6% actual)

Key finding: "Developers want to spend more time on core activities such as 'Coding' and 'Architecting and designing new systems,' and less time on 'Communication', 'Addressing Customer Support Tickets', and 'Security & Compliance.'"

**Implication for Amdahl's Law:** If coding is only 11% of developer time, even a 10x improvement via AI yields:
```
Speedup = 1 / ((1 - 0.11) + (0.11 / 10)) = 1 / (0.89 + 0.011) = 1 / 0.901 = 1.11x (11%)
```

Source: [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/11/Time-Warp-Developer-Productivity-Study.pdf) | [arXiv](https://arxiv.org/html/2502.15287v1)

### Tidelift / New Stack Survey (2019, ~400 developers)

| Activity | % of Time |
|----------|----------|
| Writing new code or improving existing code | 32% |
| Code maintenance | 19% |
| Testing | 12% |
| Responding to security issues | 4% |
| Meetings & management/operational tasks | 23% |
| Other | 10% |

Source: [Tidelift Blog](https://blog.tidelift.com/how-much-time-do-developers-spend-actually-writing-code) | [The New Stack](https://thenewstack.io/how-much-time-do-developers-spend-actually-writing-code/)

### AWS Internal Data

Referenced in industry discussions: "An average AWS engineer only spends 20% of their time coding." The remaining 80% goes to code review, meetings, design, deployment, and operational work.

Source: [Quora discussion](https://www.quora.com/Are-you-surprised-that-an-average-AWS-engineer-only-spends-20-of-their-time-coding) (primary source unclear)

### Harness State of Developer Experience (2024)

Surveyed 500 engineering leaders and practitioners. Key findings:
- 97% of developers context switch throughout the day
- 45% say they don't have enough time for learning and development
- The report highlights "developer toil" -- repetitive, manual, low-value tasks that consume significant time

Source: [Harness](https://www.harness.io/state-of-developer-experience)

### Summary of Time Allocation Across Studies

The range across studies:
- **Writing new code: 11-32%** (Microsoft on the low end, Tidelift on the high end)
- A reasonable consensus estimate: **20-25% of developer time is spent writing code**
- The remaining 70-80% is spent on meetings, code review, debugging, testing, maintenance, design, coordination, context switching, and operational tasks

---

## 3. PR Volume vs. Feature Quality: The Productivity Paradox

### GitHub Octoverse 2025 (covering Sep 2024 - Aug 2025)

- Developers pushed **nearly 1 billion commits** in 2025, a **25.1% increase** year-over-year
- Monthly pull request merges averaged **43.2 million**, a **23% increase** from the prior year
- Developers merged a record **518.7 million pull requests**, a **29% increase** year-over-year
- Over **10.5 billion GitHub Actions minutes** used in 2024, a **30% increase**
- 80% of new developers on GitHub used Copilot within their first week
- A new developer joined GitHub every second

Source: [GitHub Octoverse](https://octoverse.github.com/)

### Faros AI Research Report (July 2025) -- 10,000+ developers, 1,255 teams

**More activity, but not more output:**
- Developers with high AI adoption complete **21% more tasks** and merge **98% more pull requests**
- Teams interact with **9% more tasks** and **47% more pull requests per day**
- BUT: PR review time **increases 91%**
- Average PR size **grows 154%**
- **9% increase in bugs** per developer
- **"No significant correlation between AI adoption and improvements at the company level"**
- Gains observed in team behavior **"do not scale when aggregated"**
- No measurable improvements across overall throughput, DORA metrics, or quality KPIs

Source: [Faros AI](https://www.faros.ai/blog/ai-software-engineering)

### The Enterprise Trial That Found Zero Feature Improvement

"In one large enterprise trial, AI-assisted teams produced 18% more commits in a quarter, but review cycles lengthened, merge times slowed, and no additional features were delivered."

Source: [Mo Zaman, Medium](https://medium.com/@mozaman/the-productivity-paradox-of-ai-why-commits-and-prs-dont-tell-the-story-ceb68a453f54)

### METR Randomized Controlled Trial (July 2025)

The most rigorous study to date on AI developer productivity:
- **16 experienced open-source developers**, average 5 years experience on their repos
- **246 tasks** completed, randomized to allow or disallow AI
- **AI tools used:** Cursor Pro with Claude 3.5/3.7 Sonnet (frontier models at time of study)
- **Result:** Developers took **19% longer** with AI tools
- **Perception gap:** Developers expected AI to speed them up by **24%**, and even after the slowdown, still believed AI had helped by **20%**
- Compensation: $150/hour
- Repos averaged 22k+ stars, 1M+ lines of code

Source: [METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | [arXiv](https://arxiv.org/abs/2507.09089)

### DORA Report 2025 (Google)

- AI adoption among software development professionals surged to **90%**, up 14% from prior year
- Developers typically dedicate a **median of 2 hours daily** to working with AI
- AI adoption is linked to **higher software delivery throughput** (positive reversal from 2024)
- BUT: AI adoption continues to have a **negative relationship with software delivery stability**
- **7.2% decrease in delivery stability** for every 25% increase in AI adoption
- Central finding: "AI doesn't fix a team; it amplifies what's already there"

Source: [DORA](https://dora.dev/research/2025/dora-report/) | [Faros AI summary](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)

### Stack Overflow 2025 Developer Survey

- Only **16.3%** reported AI made them "more productive to a great extent"
- **41.4%** said AI had "little or no effect" on productivity
- **66%** cited code being "almost right, but not quite" as the main frustration
- **45.2%** spent significant time debugging AI-generated code

Source: [Stack Overflow 2025](https://survey.stackoverflow.co/2025/) (via Cerbos analysis)

---

## 4. GitClear Code Quality Data: More Code, Worse Code

### GitClear 2025 AI Code Quality Research

**Dataset:** 211 million changed lines of code, January 2020 through December 2024. Data from repositories owned by Google, Microsoft, Meta, and enterprise corporations.

**Key metrics (2020 vs. 2024):**

| Metric | 2020 | 2024 | Change |
|--------|------|------|--------|
| New code added (% of changes) | 39% | 46% | +7pp |
| Copy/pasted (cloned) lines | 8.3% | 12.3% | +48% relative |
| Refactored (moved) lines | 24.1% | 9.5% | -14.6pp (-60% relative) |
| Code revised within 2 weeks | 3.1% | 5.7% | +84% relative |
| All new code revised within 2 weeks | 5.5% | 7.9% | +44% relative |
| Code revised over 1 month old | 30% | 20% | -10pp |

**Headline findings:**
- **4x growth in code clones** compared to pre-AI trends
- Duplicated code blocks (5+ duplicated lines) increased **8x** during 2024
- **2024 was the first year** where copy/pasted lines exceeded refactored (moved) lines -- a historic first in GitClear's dataset
- **39.9% decrease** in the number of moved (refactored) lines
- Refactoring dropped from **25% of changed lines in 2021** to **less than 10% in 2024**

**Why this matters:** Code that gets copy-pasted instead of properly refactored creates technical debt. A 2023 study found that **57.1% of co-changed cloned code was involved in bugs**. More code is being written, but less of it is being written well.

Source: [GitClear 2025 Report](https://www.gitclear.com/ai_assistant_code_quality_2025_research) | [Report Summary](https://www.jonas.rs/2025/02/09/report-summary-gitclear-ai-code-quality-research-2025.html)

### CodeRabbit "State of AI vs Human Code Generation" (December 2025)

**Dataset:** 470 open-source GitHub pull requests (320 AI-coauthored, 150 human-only)

**AI-generated code creates 1.7x more issues** per PR:
- AI PRs: **10.83 issues per PR**
- Human PRs: **6.45 issues per PR**

**Category breakdown:**
- Logic and correctness issues: **+75%** in AI code
- Security vulnerabilities: **1.5-2x higher** in AI code
- Code readability problems: **3x higher** in AI code
- Performance inefficiencies (e.g., excessive I/O): **nearly 8x higher** in AI code

Source: [CodeRabbit](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) | [BusinessWire](https://www.businesswire.com/news/home/20251217666881/en/)

### Apiiro Security Research (2024)

Analysis of AI-generated code security:
- **322% more** privilege escalation paths
- **153% more** design flaws compared to human-written code
- **40% increase** in secrets exposure
- **2.5x higher** rate of critical vulnerabilities (CVSS 7.0+)
- AI commits merged to production **4x faster**, bypassing review cycles
- **60% more** reviewer comments needed on security issues

Source: Apiiro 2024 (via Cerbos analysis)

---

## 5. Bottleneck Shifting: Coding Was Never the Primary Bottleneck

### The Theory of Constraints (Goldratt) Applied to Software

Eliyahu Goldratt's Theory of Constraints (1984) states: "Any improvement not at the constraint is an illusion." In software development, multiple practitioners and researchers have identified that the constraint is rarely coding itself:

- **Deployment is often the constraint**, not coding. Tasks accumulate in the "Deployment to Production" column, not in the "Development" column.
- Lack of coordination between Dev and Ops teams creates wait times, complex deployments, manual processes, and large batches.
- The constraint moves: once one bottleneck is relieved, the next one becomes visible.

Source: [Theory of Constraints in Software Development](https://mikecarruego.medium.com/the-theory-of-constraints-in-software-development-7e37cb0911db) | [The Agile Mindset](https://www.theagilemindset.co.uk/2025/10/07/the-theory-of-constraints-in-software-development-finding-and-fixing-the-real-bottleneck/)

### Brooks's Law and Coordination Costs

Fred Brooks (The Mythical Man-Month, 1975, revised 1995): "Adding manpower to a late software project makes it later."

The mechanism: communication paths grow as n(n-1)/2 where n = team size. A team of 5 has 10 communication paths. A team of 10 has 45. A team of 20 has 190. The coordination overhead eventually exceeds the productive capacity of each additional person.

**The parallel to AI:** AI doesn't add people, but it increases the volume of code flowing through the same coordination channels (code review, testing, deployment, integration). The bottleneck shifts from code generation to code review and integration -- the same bottleneck-shifting dynamic that Brooks described, just triggered differently.

Source: [Brooks's Law - DevIQ](https://deviq.com/laws/brooks-law/) | [CodeScene](https://codescene.com/blog/visualize-brooks-law/)

### The Review Bottleneck Is Already Visible

The Faros AI data quantifies this precisely:
- AI-using developers merge **98% more PRs**
- But PR review time **increases 91%**
- PR size grows **154%**

The throughput of the code generation stage has roughly doubled. The throughput of the code review stage has not changed (same number of reviewers, same hours in the day). By Amdahl's Law and the Theory of Constraints, the bottleneck has simply shifted downstream.

### The Cerbos Analysis Framing

"The productivity paradox of AI is not that it fails to generate more code, but that in generating more, it risks drowning organizations in the very work it promised to accelerate." Human oversight and review processes simply cannot keep pace with AI's code generation velocity.

Source: [Cerbos](https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants)

---

## 6. Synthesis: The Amdahl's Law Argument for the Blog

### The Core Calculation

Using the Microsoft Time Warp data (11% of time coding) and a generous 3x AI speedup:

```
Speedup = 1 / ((1 - 0.11) + (0.11 / 3))
        = 1 / (0.89 + 0.037)
        = 1 / 0.927
        = 1.08x (8% overall improvement)
```

Using the Tidelift data (32% of time coding) and a generous 3x AI speedup:

```
Speedup = 1 / ((1 - 0.32) + (0.32 / 3))
        = 1 / (0.68 + 0.107)
        = 1 / 0.787
        = 1.27x (27% overall improvement)
```

The theoretical bound ranges from **8% to 27%** depending on what you count as "coding" and how much AI speeds it up.

### Why Reality Is Even Worse Than the Theory

Amdahl's Law assumes that speeding up one part doesn't slow down other parts. But the evidence shows the opposite:

1. **More code creates more review burden.** PR review time increases 91% with AI adoption (Faros AI). The bottleneck doesn't just stay the same -- it gets worse.

2. **More code creates more bugs.** AI-generated code has 1.7x more issues (CodeRabbit), 9% more bugs per developer (Faros AI), and 2.5x more critical security vulnerabilities (Apiiro). These bugs consume downstream time in debugging, testing, and incident response.

3. **More code creates more technical debt.** Refactoring dropped from 24.1% to 9.5% of changes (GitClear). Copy-pasted code rose 48%. The 8x increase in duplicated code blocks means future maintenance costs are being deferred.

4. **The perception gap distorts investment.** Developers believe they are 20% faster with AI even when they are 19% slower (METR). This creates a feedback loop where organizations invest more in AI coding tools while the actual bottleneck -- review, testing, design, coordination -- remains under-resourced.

### The Punchline

The organizations that will benefit most from AI coding tools are not the ones that invest most in AI coding tools. They're the ones that invest in the 70-80% of developer time that isn't coding: better review processes, faster testing pipelines, reduced meeting overhead, streamlined deployment, and clearer design specifications. Speeding up the part that was already relatively fast is the exact mistake Amdahl warned about in 1967.

---

## Key Quotes for the Blog

> "Any improvement not at the constraint is an illusion." -- Eliyahu Goldratt

> "Amdahl's Law, from 1967, perfectly describes everything about AI productivity." -- Stephan Schmidt, AmazingCTO

> "AI-driven coding gains evaporate when review bottlenecks, brittle testing, and slow release pipelines can't match the new velocity." -- Pullflow

> "The productivity paradox of AI is not that it fails to generate more code, but that in generating more, it risks drowning organizations in the very work it promised to accelerate." -- Cerbos

> "AI doesn't fix a team; it amplifies what's already there." -- DORA Report 2025

> "Developers took 19% longer when using AI tools... yet believed AI had sped them up by 20%." -- METR

---

## Sources Index

1. **Amdahl's Law + AI:** [AmazingCTO](https://www.amazingcto.com/amdahls-law-and-ai-productivity/)
2. **Microsoft Time Warp Study:** [arXiv](https://arxiv.org/html/2502.15287v1) | [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/11/Time-Warp-Developer-Productivity-Study.pdf)
3. **Tidelift/New Stack Survey:** [Blog](https://blog.tidelift.com/how-much-time-do-developers-spend-actually-writing-code) | [The New Stack](https://thenewstack.io/how-much-time-do-developers-spend-actually-writing-code/)
4. **GitClear 2025 Report:** [Report](https://www.gitclear.com/ai_assistant_code_quality_2025_research) | [Summary](https://www.jonas.rs/2025/02/09/report-summary-gitclear-ai-code-quality-research-2025.html)
5. **CodeRabbit Report (Dec 2025):** [Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) | [BusinessWire](https://www.businesswire.com/news/home/20251217666881/en/)
6. **Faros AI Research (Jul 2025):** [Report](https://www.faros.ai/blog/ai-software-engineering)
7. **METR RCT (Jul 2025):** [Blog](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | [arXiv](https://arxiv.org/abs/2507.09089)
8. **DORA Report 2025:** [DORA](https://dora.dev/research/2025/dora-report/) | [Faros Summary](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)
9. **GitHub Octoverse 2025:** [Octoverse](https://octoverse.github.com/)
10. **Cerbos Analysis:** [Blog](https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants)
11. **Pullflow Analysis:** [Blog](https://pullflow.com/blog/the-great-ai-productivity-paradox-are-we-actually-coding-faster)
12. **Theory of Constraints in Software:** [Medium](https://mikecarruego.medium.com/the-theory-of-constraints-in-software-development-7e37cb0911db) | [Agile Mindset](https://www.theagilemindset.co.uk/2025/10/07/the-theory-of-constraints-in-software-development-finding-and-fixing-the-real-bottleneck/)
13. **Brooks's Law:** [DevIQ](https://deviq.com/laws/brooks-law/)
14. **Harness 2024:** [Report](https://www.harness.io/state-of-developer-experience)
15. **Apiiro Security Research:** via [Cerbos](https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants)
