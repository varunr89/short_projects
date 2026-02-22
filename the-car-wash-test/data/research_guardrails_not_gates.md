# Research Notes: Companies Choosing "Guardrails, Not Gates" for AI Adoption

Compiled: 2026-02-19

---

## 1. Shopify's AI-First Mandate

### Timeline
- **Late 2021**: VP & Head of Engineering Farhan Thawar brought GitHub Copilot to Shopify -- before ChatGPT even launched. Copilot adoption reached 80% within engineering.
- **April 7, 2025**: CEO Tobi Lutke publicly shared an internal memo on X (Twitter) after learning it was being leaked. The memo declared "reflexive AI usage is now a baseline expectation at Shopify."
- The memo sparked similar announcements from Box, Fiverr, and even Canada's Prime Minister within weeks. The "AI-first CEO memo" became a genre.

### Specific Policies Implemented

1. **AI usage is a performance metric.** Shopify added "AI native" and "AI reflexive" ratings to 360-degree performance reviews. Before you get headcount, you have to demonstrate why the job cannot be done by AI.

2. **Universal access, no budget limits.** Thawar ordered 1,500 Cursor licenses, then rapidly needed 1,500 more. No token quotas exist. Thawar tracks value through an internal leaderboard of highest token spenders. His framing: "If engineers spend $1,000 monthly for 10% productivity gains, that's too cheap."

3. **Legal team adopted "default to yes."** Instead of blocking, leadership asked: "We're likely going to do this. How can we do it safely?" Legal worked to find safe implementation paths rather than restricting.

4. **"MCP everything."** Built internal MCP (Model Context Protocol) servers connecting all internal data systems -- Slack, Salesforce, GSuite Drive, GitHub. Thawar: "We make every single piece of data inside the company available... ready for people to interrogate and figure out their own workflows."

5. **LLM Proxy infrastructure.** Internal tool enabling access to multiple models with instant updates to latest versions. A "one-stop shop" of agents already created by others for anyone to use.

### Measurable Results
- **Non-engineering teams became fastest-growing AI users.** Support and revenue teams adopted faster than expected -- contradicting assumptions about where AI value emerges.
- **A non-technical sales rep** used Cursor to build an automated site audit tool that generates performance comparisons between prospects' sites and Shopify benchmarks, complete with talking points.
- **50% of AI-generated project updates proceed unmodified**, demonstrating high contextual accuracy.
- **Intern hiring expanded dramatically.** Thawar initially estimated supporting 75 interns; revised to 1,000. Interns are "AI centaurs" who naturally embrace new tools.
- **Roast framework**: Open-source AI orchestration tool for code review that shows AI reasoning at each step, built with Claude Code.

### Key Quotes
- Lutke: "Using AI effectively is now a fundamental expectation of everyone at Shopify."
- Lutke on opting out: "You're welcome to try, but I cannot see this working out today, and definitely not tomorrow. Stagnation is almost certain, and stagnation is slow-motion failure."
- Lutke on hiring: "There are an infinite number of bad solutions and probably 10,000 good ones. Your job is finding the best solution among 10,000, not stopping at the first working one."

### Sources
- [Tobi Lutke's X post (April 2025)](https://x.com/tobi/status/1909251946235437514)
- [First Round: From Memo to Movement -- Shopify's Cultural Adoption of AI](https://www.firstround.com/ai/shopify)
- [MIT CDO: Shopify CEO on AI as fundamental expectation](https://cdo.mit.edu/blog/2025/04/11/shopify-ceo-tobi-lutke-ai-is-now-a-fundamental-expectation-for-employeeslutke-says-managers-asking-for-new-human-talent-will-have-to-explain-why-the-job-cant-be-done-by-ai/)
- [Pragmatic Engineer: How AI is changing software engineering at Shopify](https://newsletter.pragmaticengineer.com/p/how-ai-is-changing-software-engineering)

---

## 2. Anthropic's Internal AI Usage

### Key Statistics (August 2025 survey)
- **59% of daily work** now involves Claude (up from 28% a year prior -- more than 2x increase)
- **50% average productivity boost** (up from +20% previously)
- **14% of respondents** report productivity increases exceeding 100%
- **27% of Claude-assisted tasks** wouldn't have been done otherwise (new work that AI made feasible)
- **70-90% of company-wide code** is written by AI (per Anthropic spokesperson)
- **Claude Code itself**: about 90% of its code is written by Claude Code

### Survey Methodology
- 132 engineers and researchers surveyed
- 53 in-depth qualitative interviews
- 200,000 internal Claude Code transcripts analyzed (Feb-Aug 2025)

### Usage Patterns
- Debugging: 55% use Claude daily
- Code understanding: 42% daily
- Implementing new features: 37% daily
- 8.6% of Claude Code tasks involve "papercut" quality-of-life fixes that wouldn't have been worth doing manually

### Autonomy Metrics (6-month trend)
- Maximum consecutive tool calls: 9.8 to 21.2 (+116%)
- Human turns per interaction: 6.2 to 4.1 (-33%)
- Task complexity: 3.2 to 3.8 on 5-point scale

### What This Means for the Blog
Anthropic is a company that dogfoods its own AI tools and publishes transparent data on outcomes. The "27% of work wouldn't have been done otherwise" statistic is powerful -- AI is not just replacing existing work, it is enabling new work that was previously too expensive to justify.

### Sources
- [Anthropic: How AI Is Transforming Work at Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- [Anthropic: How teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- [Fortune: Top engineers at Anthropic, OpenAI say AI now writes 100% of their code](https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/)

---

## 3. JPMorgan Chase: From Ban to Broad Enablement

### The Arc
- **February 2023**: JPMorgan restricted ChatGPT usage across the firm, citing compliance with third-party software regulations.
- **August 2024**: Launched "LLM Suite" -- an internal AI assistant powered by OpenAI and Anthropic models.
- **Within 8 months**: 200,000 employees onboarded (driven partly by employee demand).
- **By late 2025**: ~250,000 employees have access (entire workforce except branch/call center staff). Half use it roughly every day.
- **2025**: Won American Banker's "Innovation of the Year" award for LLM Suite.

### Strategy
- $18 billion technology investment for 2025, with AI as central component.
- 450+ identified AI use cases across the firm.
- 10-20% productivity increase reported for employees using code creation and conversion through LLMs.
- Major training initiative to equip global workforce with AI skills.

### What This Means for the Blog
JPMorgan is the clearest example of a company that went from "ban" to "broad enablement." They didn't just unban ChatGPT -- they built their own secure platform, solved for compliance at the infrastructure level, and then made it available to nearly everyone. The result: 125,000+ daily active users.

### Sources
- [CNBC: JPMorgan giving employees AI assistant](https://www.cnbc.com/2024/08/09/jpmorgan-chase-ai-artificial-intelligence-assistant-chatgpt-openai.html)
- [Tearsheet: JPMorgan's 450 use cases](https://tearsheet.co/artificial-intelligence/jpmorgan-chases-gen-ai-implementation-450-use-cases-and-lessons-learned/)
- [CNBC: JPMorgan's blueprint for fully AI-powered megabank](https://www.cnbc.com/2025/09/30/jpmorgan-chase-fully-ai-connected-megabank.html)
- [JPMorgan: LLM Suite wins Innovation of the Year](https://www.jpmorganchase.com/about/technology/news/llmsuite-ab-award)

---

## 4. Other Companies with Broad AI Enablement

### Morgan Stanley
- Deployed "AI @ Morgan Stanley Assistant" to financial advisors in September 2023 -- a GPT-4-powered chatbot that answers questions by drawing on ~100,000 research reports.
- In 2024, added "AskResearchGPT" for institutional securities division.
- Approach: provide advisors with a secure, curated AI tool rather than blocking consumer AI.

### Goldman Sachs
- Launched internal AI assistant "OneGS 3.0" for employees.
- Focus areas: sales processes, client onboarding, lending workflows, regulatory reporting, vendor management.
- Expanding banker/trader copilots across divisions.

### GitHub Copilot Adoption (as a proxy for enterprise AI enablement)
- 90% of Fortune 100 companies use GitHub Copilot (as of 2025).
- 20+ million all-time users by July 2025.
- Developers complete coding tasks 55% faster.
- Pull request time dropped from 9.6 days to 2.4 days (75% reduction).
- Copilot contributes an average of 46% of all code written by active users (up from 27% at launch).
- 81.4% of developers install the IDE extension the same day they receive access.
- AI coding tools market: $7.37 billion in 2025; Copilot holds 42% market share.

### Sources
- [Fortune: Employees banned from ChatGPT (2023)](https://fortune.com/2023/05/19/chatgpt-banned-workplace-apple-goldman-risk-privacy/)
- [GitHub Copilot statistics](https://www.secondtalent.com/resources/github-copilot-statistics/)
- [Morgan Stanley AI in wealth management](https://www.morganstanley.com/insights/articles/ai-workplace-outlook-2H-2025)

---

## 5. The Anti-Patterns: Over-Restriction and Its Consequences

### Samsung: The Canonical Cautionary Tale
- **May 2023**: Engineers pasted proprietary source code into ChatGPT for debugging. Samsung banned all generative AI tools on company-owned devices and internal networks.
- **Aftermath**: Samsung developed internal "Gauss AI" and confined employees to it.
- **2024-2025**: Eventually reversed course, reinstating ChatGPT access under new security protocols. Implemented "Safe Harbor" policies for vetted external tool access.
- **Lesson**: The ban was a reflexive response that drove usage underground before the company eventually built the guardrails it should have started with.

### The 2023 Ban Wave
Multiple major companies banned ChatGPT in early-to-mid 2023:
- **JPMorgan Chase** (reversed -- see above)
- **Bank of America**
- **Citigroup** (added to standard third-party software restrictions)
- **Deutsche Bank** (disabled access for staff)
- **Goldman Sachs** (reversed -- built internal tools)
- **Wells Fargo**
- **Apple** (restricted ChatGPT and GitHub Copilot; built internal LLM instead)
- **Amazon** (recommended internal CodeWhisperer over ChatGPT, but didn't fully ban)
- **Verizon** (blocked on corporate systems)

### Shadow AI: The Cost of Over-Restriction

**The fundamental problem**: Banning AI tools does not stop employees from using them. It just makes the usage invisible and ungovernable.

Key statistics:
- **69% of organizations** suspect or have evidence employees are using prohibited GenAI tools (Gartner survey of 302 cybersecurity leaders, March-May 2025).
- **71% of UK employees** admitted to using unapproved AI tools at work; 51% do so at least weekly (Microsoft research).
- **Over 90% of employees** use personal AI accounts despite official bans (from "The Samsung Effect" analysis).
- **Only 40% of companies** have purchased enterprise AI licenses -- leaving most employees to fend for themselves.
- **Even 68% of security leaders** admit using unauthorized AI tools.
- **48% of employees** said they wouldn't stop using AI even if banned.

**Financial cost of shadow AI (IBM 2025 Cost of a Data Breach Report)**:
- Organizations with high shadow AI usage paid **$670,000 more per breach** than those with low/no shadow AI.
- Shadow AI incidents account for **20% of all breaches**.
- Average cost of shadow-AI-associated breaches: **$4.63 million** vs $3.96 million for standard breaches.
- **63% of breached organizations** lack AI governance policies entirely.
- Among AI-related breaches, **97% lacked proper access controls**.

**Gartner prediction**: By 2030, more than 40% of enterprises will experience security or compliance incidents linked to unauthorized shadow AI.

### Sources
- [CNBC: Samsung bans ChatGPT after data leak (May 2023)](https://www.cnbc.com/2023/05/02/samsung-bans-use-of-ai-like-chatgpt-for-staff-after-misuse-of-chatbot.html)
- [SammyGuru: Samsung reinstates ChatGPT under new security rules](https://sammyguru.com/samsung-reinstates-chatgpt-use-for-employees-under-new-security-rules/)
- [Gartner: Shadow AI security breaches prediction](https://www.fortra.com/blog/shadow-ai-security-breaches-will-hit-40-companies-2030-warns-gartner)
- [Gartner: Critical GenAI blind spots for CIOs](https://www.gartner.com/en/newsroom/press-releases/2025-11-19-gartner-identifies-critical-genai-blind-spots-that-cios-must-urgently-address0)
- [IBM 2025 Cost of a Data Breach Report: Shadow AI](https://www.kiteworks.com/cybersecurity-risk-management/ibm-2025-data-breach-report-ai-risks/)
- [IBM Newsroom: AI breach report](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls)
- [Bloomberg: Wall Street banks cracking down on ChatGPT (2023)](https://www.bloomberg.com/news/articles/2023-02-24/citigroup-goldman-sachs-join-chatgpt-crackdown-fn-reports)
- [The AI Hat: The Samsung Effect](https://theaihat.com/the-samsung-effect-why-banning-chatgpt-is-the-most-expensive-mistake-you-can-make/)

---

## 6. The Duolingo/Klarna Cautionary Tales (Different Anti-Pattern)

These are examples of "AI-first" gone too far in the other direction -- replacing workers rather than enabling them.

### Duolingo
- **January 2024**: Cut 10% of contractor workforce, shifting content creation to AI.
- **April 2025**: CEO announced "AI-first" strategy where AI handles content creation before humans are considered.
- **Backlash**: CEO Luis von Ahn walked back comments, clarifying "I do not see AI as replacing what our employees do."
- **September 2025**: CEO claimed AI makes employees "four or five times" as productive, with no full-time layoffs.
- **Status**: Still navigating the tension between AI efficiency and workforce messaging.

### Klarna
- Klarna CEO Sebastian Siemiatkowski positioned company as "favorite guinea pig" of OpenAI.
- Implemented hiring freeze, replacing workers with AI. AI chatbot now does the equivalent work of 700 customer service agents.
- **Reversal**: Klarna is now hiring again to ensure customers can always speak to a live representative -- suggesting quality issues with full AI replacement.

### What This Means for the Blog
These are the "gates, not guardrails" version for workers -- companies that used AI to replace rather than enable. Both faced backlash and partial reversals. The lesson: "guardrails, not gates" applies in both directions. Don't gate workers from AI tools, and don't use AI to gate workers out of their jobs.

### Sources
- [Fast Company: Going AI-first backfires on Duolingo and Klarna](https://www.fastcompany.com/91332763/going-ai-first-appears-to-be-backfiring-on-klarna-and-duolingo)
- [CNBC: Duolingo CEO on AI productivity without layoffs](https://www.cnbc.com/2025/09/17/duolingo-ceo-how-ai-makes-my-employees-more-productive-without-layoffs.html)
- [Fortune: Duolingo CEO walks back AI-first comments](https://fortune.com/2025/05/24/duolingo-ai-first-employees-ceo-luis-von-ahn/)

---

## 7. Macro Data Points for Context

### McKinsey (2025 "Superagency in the Workplace" report)
- **78% of organizations** use AI in at least one business function; 72% have adopted generative AI specifically.
- **Employees are 3x more likely** than leaders expect to be using GenAI for at least 30% of their daily work.
- **Only 1% of business leaders** describe their GenAI rollouts as "mature."
- **48% of employees** rank training as the most important factor for adoption, but nearly half report minimal or no training.

### Deloitte (2025)
- ~70% of enterprises have integrated AI into at least one business function (up from ~50% a year earlier).
- Industries embracing AI see labor productivity grow **4.8x faster** than the global average.
- 60% of executives say Responsible AI boosts ROI and efficiency.
- 55% report improved customer experience and innovation.

### Sources
- [McKinsey: Superagency in the Workplace (2025)](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/superagency-in-the-workplace-empowering-people-to-unlock-ais-full-potential-at-work)
- [Deloitte: AI trends 2025](https://www.deloitte.com/us/en/services/consulting/blogs/ai-adoption-challenges-ai-trends.html)

---

## Summary: The "Guardrails, Not Gates" Playbook

Companies that succeed at AI adoption share these traits:

1. **Solve for security at the platform level**, not by banning tools. Build or buy a secure AI gateway (JPMorgan's LLM Suite, Shopify's LLM Proxy). Then open it to everyone.

2. **Remove budget constraints on AI tooling.** Shopify has no token quotas. The cost of AI tools is trivial compared to the cost of a single engineer's time.

3. **Make AI a performance expectation**, not an optional extra. Shopify baked it into reviews. JPMorgan invested in firm-wide training.

4. **Legal defaults to "yes."** Shopify's legal team asks "how can we do this safely?" rather than "should we allow this?"

5. **Measure and celebrate usage**, not restrict it. Shopify has a leaderboard of highest token spenders. Anthropic publishes internal usage data.

6. **Enable non-technical users** -- they often adopt fastest and find the most creative applications. Shopify's sales and support teams outpaced engineering in adoption growth.

7. **Accept that banning does not work.** 69% of companies already have evidence of shadow AI. The question is not whether employees will use AI -- it is whether they'll use it with or without governance.
