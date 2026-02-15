# Research Notes: Who Is Actually Adopting AI at Work?

**Research date:** February 2026
**Hypothesis:** AI is currently being adopted primarily by top performers / highly skilled workers, while the bottom of the distribution isn't using it yet -- meaning the biggest potential gains (for low-skill workers) are going unrealized.

**Verdict:** The hypothesis is strongly supported by the evidence, with important nuances.

---

## 1. Adoption Rates by Skill / Education Level

### Bick, Blandin & Deming (2024) -- "The Rapid Adoption of Generative AI" (NBER WP 32966)
- First nationally representative U.S. survey on GenAI use (Real-Time Population Survey, 10,000+ respondents, Aug & Nov 2024)
- **~40% of workers with a bachelor's degree or more** use generative AI at work
- **~20% of workers without a college degree** use generative AI at work
- This is a **2:1 education gradient** -- college-educated workers adopt at double the rate
- The pattern is "strikingly similar" to early PC adoption (42% vs 20% by education, 3 years after mass-market launch)
- By college major: **46% of STEM majors** use GenAI at work, vs **40% business/econ/comms**, vs **22% all other majors**
- By gender: 32% of men vs 23% of women use GenAI at work
- By age: ~34% for workers under 40, declining to ~17% for workers 50+
- Overall: 39.6% of U.S. adults 18-64 use GenAI; 23% of employed respondents used it for work in the past week; 9% use it daily

### Pew Research Center (Oct 2025) -- "21% of US workers use AI on the job"
- 21% of U.S. workers say at least some of their work is done with AI, up from 16% a year prior
- **28% of workers with at least a bachelor's degree** say some of their work is done with AI (up from 20%)
- **16% of workers with some college or less** say some of their work is done with AI (up from 13%)
- The education gap **widened** from 7pp to 12pp in one year
- AI adopters more likely to live in urban areas and have a bachelor's degree (51% vs 39% among non-adopters)
- Most common use cases: information seeking (57%), editing (52%), drafting content (47%)

### Humlum & Vestergaard (PNAS, Jan 2025) -- "The Unequal Adoption of ChatGPT"
- 18,000 workers surveyed across 11 "AI-exposed" occupations in Denmark, linked to register data
- 41% of workers in exposed occupations have used ChatGPT for work
- Adoption ranges from **65% (marketing professionals)** to **12% (financial advisors)**
- **Women are 16 percentage points less likely** to have used ChatGPT for work (same occupations, similar tasks)
- **Higher-earning workers adopt more**, even controlling for experience and tenure
- Younger, less experienced workers more likely to adopt (each additional year of age = -0.7pp adoption)
- Key finding: "Users of ChatGPT earned slightly more already before its arrival"

### Key Stat for the Blog
> The education gradient for AI adoption is roughly 2:1. About 40% of college-educated workers use GenAI at work, vs about 20% of non-college workers. This gap has been *widening* over time, not closing.

---

## 2. Adoption by Job Role / Seniority

### BCG AI at Work Survey (2025, 3rd annual) -- 10,635 employees across 11 nations
- **72% of leaders, managers, and frontline workers** are regular GenAI users overall
- But this masks a steep seniority gradient:
  - **Leaders: ~75-78%** regular use
  - **Managers: 78%** regular use (up from 64% in 2023, 46% in 2018)
  - **Frontline employees: 51%** regular use (**stalled** -- down 1pp from 2023)
- Frontline workers have hit a **"silicon ceiling"** -- adoption plateaued despite 7 years of growth (20% in 2018 to 52% in 2023, then stuck)
- Only **25% of frontline employees** say they receive strong leadership support for AI
- Only **28% of frontline employees** have been trained on how AI will change their jobs (vs 50% of leaders)
- 79% of those with 5+ hours of training are regular users vs 67% with less training

### McKinsey "Superagency" Report (Jan 2025) -- 3,613 employees + 238 C-suite
- Employees are **3x more likely to be using GenAI** than their leaders think
- 4% of C-suite estimate employees use GenAI for >30% of daily tasks; **13% of employees self-report** this
- The biggest barrier to success is **leadership**, not employee readiness
- 88% of organizations report AI use in at least one function (up from 78% prior year)
- But only ~1/3 have begun to scale AI programs

### Microsoft Work Trend Index (2024-2025)
- 75% of global knowledge workers report using GenAI (2024 WTI, 31,000 respondents)
- 78% of AI users bring their own AI tools to work (BYOAI), even more at SMBs (80%)
- **73% of leaders** are familiar/extremely familiar with AI agents, vs **45% of employees**
- Engineering teams show highest adoption rates
- 142x increase in LinkedIn members adding AI skills
- Writers, designers, marketers lead AI skill-building
- Sales, operations, finance becoming "agent-first" functions

### Bick et al. -- Occupation-Level Data
- **Computer/mathematical occupations: 49.6%** adoption
- **Management occupations: 49.0%** adoption
- Legal occupations: ~20%
- Office/administrative occupations: ~20%
- Construction, food/accommodation: lowest adoption
- Information systems and finance: highest industry adoption rates

### Key Stat for the Blog
> BCG found that 78% of managers use GenAI regularly, but frontline worker adoption has **stalled at 51%** -- unchanged in two years. The "silicon ceiling" is real.

---

## 3. The Productivity Paradox of AI Adoption

### The Core Paradox
AI helps low-skill workers the most (+34-43%), but high-skill workers are the ones adopting it (+7-17% gains). This mismatch means the aggregate productivity impact is far below its potential.

### Brynjolfsson, Li & Raymond (2023/2025) -- "Generative AI at Work" (QJE)
- Study of 5,179 customer support agents at a Fortune 500 company
- Average productivity increase: **14% (issues resolved per hour)**
- **Bottom quintile (lowest-performing 20%): +35% improvement**
- **Top quintile (highest-performing 20%): ~0% improvement** (small or slightly negative)
- Mechanism: AI essentially encodes knowledge of top performers and distributes it to less-skilled workers
- Within 2 months, AI users resolved 2.5 chats/hour vs 1.7 for non-users (who took 8 months to reach that level)
- Caveat: Top workers' adherence to AI recommendations may reduce the quality of future AI training data

### Noy & Zhang (2023) -- "Experimental Evidence on the Productivity Effects of GenAI" (Science)
- 453 college-educated professionals, randomized experiment with writing tasks
- ChatGPT reduced task-completion time by **~40%** and increased output quality by **~18%**
- **Lower-performing workers saw the largest gains**
- Variance in output quality **decreased** -- AI compressed the distribution
- "Treated workers completed tasks 0.8 SD faster and produced output rated 0.4 SD higher"

### Dell'Acqua et al. (2023) -- "Navigating the Jagged Technological Frontier" (Harvard/BCG)
- 758 BCG consultants (7% of BCG's consulting force), GPT-4
- For tasks within AI's capability frontier:
  - **12.2% more tasks** completed, **25.1% faster**, **40% higher quality**
  - **Below-average consultants: +43% quality improvement**
  - **Above-average consultants: +17% quality improvement**
  - Performance gap between top and bottom performers shrank from **22% to 4%**
- For tasks outside the frontier: **19 percentage points worse** performance with AI
- "People kind of switch off their brains and follow what AI recommends"

### Merali (2024) -- Translation Study
- Lower-skilled translators experienced gains **roughly 4x larger** than higher-skilled counterparts
- 12.3% reduction in completion time, 0.18 SD quality improvement, 16.1% earnings increase

### The Mismatch Quantified
If we combine the adoption data with the productivity data:
- **High-skill workers**: ~40% adoption rate, ~7-17% productivity gain = modest aggregate impact
- **Low-skill workers**: ~20% adoption rate, ~34-43% productivity gain = much larger *potential* impact, but mostly unrealized
- The workers who would benefit most are half as likely to be using the tools

### Key Stat for the Blog
> In the BCG study, below-average consultants improved quality by 43% with AI, while above-average improved by only 17%. The gap between top and bottom performers shrank from 22% to just 4%. But in the real world, it's the top performers who are actually using AI.

---

## 4. The Counterargument: AI as Skill-Divider (Not Just Leveler)

### Otis et al. (2024) -- "The Uneven Impact of GenAI on Entrepreneurial Performance" (HBS)
- Field experiment with 640 Kenyan entrepreneurs, GPT-4-powered WhatsApp assistant, 5 months
- **No average effect** on business performance
- But strong heterogeneity:
  - **High-performing entrepreneurs: +15%** revenue/profit improvement
  - **Low-performing entrepreneurs: -8 to -10%** (they got worse)
- Why? Low performers sought help on "much more challenging business tasks" -- open-ended, unstructured problems where AI is less reliable
- Key distinction: **Narrowly defined tasks** (writing, customer support) = AI levels the playing field. **Open-ended, unstructured tasks** (running a business) = AI may widen the gap.

### Dropbox Research (2025) -- Top Performers and AI
- **73% of top-performing developers** use AI daily vs **59% of other developers**
- 84% of top performers say it's easy to understand/modify their code vs 62% of peers
- 69% of top performers have time for deep, focused work vs 51% of peers
- BUT: "AI use alone doesn't explain who's thriving" -- human skills (curiosity, focus, initiative) matter more
- Dropbox reached 90% engineering AI adoption (vs ~50% industry average) through intentional leadership and culture

### The Long-Run Worry
Matthew Call argues that superstars are "most likely to be pushing the boundaries of what's possible with AI," potentially accelerating their advantage over time. The compression effect seen in controlled experiments may not persist as top performers learn to use AI for increasingly complex tasks.

---

## 5. Barriers to Adoption for Lower-Skill Workers

### From Humlum & Vestergaard (PNAS, 2025) -- Barriers data from 18,000 Danish workers
- **Lack of training: 42%** cited as primary barrier
- **Company restrictions on use: 32%** (82% in financial sector specifically)
- **Fear of job loss: only 8%** (much lower than expected)
- Critical finding: Even when workers believe ChatGPT can halve task time, **only 23% plan to use it within 2 weeks**
- When researchers randomly informed workers about time savings, **it had no effect on usage behavior** -- information alone doesn't drive adoption
- Frictions are **causal barriers**, not just correlates

### BCG (2025) -- Training and Support Gaps
- Only 30% of managers and 28% of frontline employees trained on how AI will change their jobs (vs 50% of leaders)
- Only 36% of employees believe their training is "enough"
- **18% of regular AI users received NO training at all**
- Employees with 5+ hours of training: 79% are regular users
- Employees with <5 hours: 67% are regular users
- Positive sentiment toward AI rises from 15% to 55% **with strong leadership support**
- Only ~25% of frontline employees report strong leadership support

### OECD (2025) -- "Bridging the AI Skills Gap"
- Most AI training is focused on **AI professionals**, not general workers
- Training prerequisites demanded for AI courses are higher than average -- creating a barrier for lower-skill adults
- The vast majority of workers only need **general AI literacy**, not specialized AI skills
- Current training supply is mismatched: too much specialist training, not enough basic AI literacy

### McKinsey (2025/2026) -- Frontline Worker Analysis
- Manufacturing COOs list "cultural shift" and "reskilling" as top barriers
- Only 1/3 of companies have scaled any AI solutions across their networks
- Only 2% say AI is fully embedded across all operations
- "Too few workers with the capabilities needed to collaborate effectively with AI"
- **$1 trillion+ spent on IT** last year, yet **60%+ of companies report no significant bottom-line impact from AI**

### UNESCO/ILO/WEF (2024-2025) -- Global Digital Divide
- 52% of adults globally report being **nervous** about AI (vs 54% excited)
- Fear overshadows natural curiosity
- Much AI content is in English, creating barriers for non-English speakers
- Cross-country AI adoption gaps widened from 2%-16% range in 2021 to 4%-28% in 2024

### Summary of Barriers (Ranked by Evidence)
1. **Lack of training** (42% cite this; training quality matters enormously)
2. **Employer restrictions** (32% cite this; especially in regulated industries)
3. **No leadership support** (75% of frontline workers lack it)
4. **Digital literacy/comfort gap** (CLI tools and technical workflows are intimidating)
5. **Job design mismatch** (AI tools designed for knowledge workers, not frontline roles)
6. **Fear of job loss** (only 8% cite this -- smaller barrier than commonly assumed)

### Key Stat for the Blog
> In Denmark, 42% of non-adopters cite lack of training as the main barrier. And even when workers are told AI could halve their task time, it doesn't change their behavior. Information isn't the bottleneck -- organizational friction is.

---

## 6. Adoption by Performance Percentile (Within Roles)

### Direct Evidence
No large-scale study has directly measured AI adoption rates by performance percentile within the same role. The closest data:

1. **Brynjolfsson et al. (2023)**: Showed that *after* AI was deployed to all agents, the **bottom quintile** gained the most. But this was mandatory deployment, not voluntary adoption -- it doesn't tell us who would have chosen to adopt.

2. **Dropbox (2025)**: Among developers, **73% of top performers** use AI daily vs **59% of others**. This is the closest to measuring adoption by performance tier within a role. The gap is 14 percentage points.

3. **Dell'Acqua et al. / BCG (2023)**: The study assigned AI access randomly, so it doesn't measure voluntary adoption by performance tier. But it shows that *when given access*, below-average performers benefit far more.

4. **Otis et al. (2024)**: In the Kenya entrepreneurship study, both high and low performers used the AI assistant. But high performers implemented the advice more effectively, while low performers asked for help on harder problems and got worse results.

### Indirect Evidence
- The Anthropic Economic Index found Gini coefficients of 0.84-0.86 for AI usage in enterprise deployments, meaning a tiny fraction of users account for most usage
- Microsoft's data shows "power users" (top 5% of Teams users) are massively more active with AI features
- BCG's "silicon ceiling" data suggests performance and seniority correlate with adoption

### The Gap in the Literature
**This is an important research gap.** No one has published a study that:
1. Measures individual workers' pre-AI performance (baseline)
2. Gives them access to AI (without mandating use)
3. Tracks who voluntarily adopts vs doesn't
4. Correlates adoption with baseline performance quartile

The Humlum & Vestergaard PNAS study comes closest by linking adoption to earnings data, finding that higher-earning workers adopt more. But earnings are a noisy proxy for within-role performance.

---

## 7. The Self-Selection Problem in AI Studies

### The Core Issue
Most influential AI productivity studies have one of two designs:
1. **Randomized access, mandatory use** (Brynjolfsson, Noy & Zhang, Dell'Acqua) -- measures what happens when everyone gets AI, not who would choose to use it
2. **Observational/voluntary adoption** (real-world surveys) -- measures who adopts, but the adopters are self-selected and likely more motivated/skilled

Neither design answers both questions simultaneously: "Who adopts?" AND "What would the gains be for everyone?"

### Specific Biases in the Literature

**Novelty Effect / Hawthorne Effect:**
- Workers in experiments know they're being studied
- Perceived productivity gains may reflect excitement, not real output
- Self-reported time savings (e.g., the 33% per-hour-of-use figure from Bick et al.) may be inflated

**Survivorship Bias in Enterprise Reports:**
- S&P Global 2025: 42% of companies abandoned most AI initiatives (up from 17% in 2024)
- ~80% of AI projects never reach production (per MIT estimates)
- 95% of GenAI investments produce no measurable financial returns
- Reports of positive ROI typically come from the surviving, successful deployments

**Self-Selection in Voluntary Studies:**
- Humlum & Vestergaard showed that even *informing* workers about AI's benefits doesn't change adoption
- This means non-adopters aren't just uninformed -- they face real friction
- Voluntary adoption studies capture results from the most motivated, tech-savvy users
- Census Bureau research notes: "even when voluntary, technology adoption does not guarantee productivity gains"

**Macro-Micro Disconnect:**
- Micro studies show 14-40% productivity gains in specific tasks
- But AI's macro impact on TFP: only **0.01 percentage points** as of 2025 (Penn Wharton)
- St. Louis Fed: self-reported time savings translate to only **1.1-1.3% aggregate productivity increase**
- Kent Smetters (PWBM): "It's not electricity, it's not refrigeration -- it's not that transformative"
- Workers may take time savings as on-the-job leisure rather than additional output

**The Controlled-Setting Fallacy:**
- In experiments, participants are instructed to use AI and given training
- Real-world workers face friction: unclear permissions, no training, tool restrictions
- "Workers in real-world settings may face frictions in adoption and may not know how to use the tools effectively"

### Key Stat for the Blog
> Micro-level studies show 14-40% productivity gains. But Penn Wharton estimates AI's actual impact on aggregate productivity growth is 0.01 percentage points as of 2025. That's a 1,000x gap between what's measured in labs and what's showing up in the economy.

---

## 8. Synthesis: The Adoption-Impact Mismatch

### The Central Finding
There is a profound mismatch in AI adoption:

| Dimension | Who Benefits Most | Who Adopts Most |
|-----------|------------------|-----------------|
| Skill level | Low-skill workers (+34-43%) | High-skill workers (40% vs 20%) |
| Performance tier | Bottom performers (+35-43%) | Top performers (73% vs 59% daily use) |
| Seniority | Junior/less experienced | Leaders and managers (78% vs 51%) |
| Education | Non-college-educated | College-educated (28% vs 16%) |
| Income | Lower-earning | Higher-earning |
| Gender | (No clear differential in gains) | Men (32% vs 23%) |

### Why This Matters for Aggregate Productivity
- The workers who gain the most from AI are the **least likely to use it**
- The workers who use AI the most see the **smallest marginal gains**
- This means aggregate productivity impact is a fraction of what's theoretically possible
- The "integral" barely moves because the bottom of the distribution -- where the biggest gains are -- remains mostly unshifted

### The Unrealized Potential
If the bottom half of workers adopted AI at the same rate as the top half:
- Customer support: instead of ~7% aggregate gains (14% avg * ~50% adoption), you'd see closer to 14%
- Consulting work: instead of modest quality improvements for the 40% who adopt, you'd see the full 43% quality boost for below-average workers across the board
- The aggregate curve would shift dramatically -- the integral would change

### What Would Close the Gap
Based on the evidence:
1. **Mandatory/default deployment** (not optional) -- the studies with the biggest gains gave everyone access
2. **5+ hours of structured training** (not demos) -- jumps regular use from 67% to 79%
3. **Active leadership support** -- jumps positive sentiment from 15% to 55%
4. **Removing employer restrictions** where possible -- 32% of non-adopters cite this
5. **Designing AI tools for non-technical users** -- CLI tools exclude most frontline workers

---

## Key Sources

1. Bick, Blandin & Deming (2024). "The Rapid Adoption of Generative AI." NBER WP 32966.
   https://www.nber.org/papers/w32966

2. Pew Research Center (Oct 2025). "21% of US workers use AI on the job."
   https://www.pewresearch.org/short-reads/2025/10/06/about-1-in-5-us-workers-now-use-ai-in-their-job-up-since-last-year/

3. Pew Research Center (Feb 2025). "Workers' views of AI use in the workplace."
   https://www.pewresearch.org/social-trends/2025/02/25/workers-views-of-ai-use-in-the-workplace/

4. Humlum & Vestergaard (PNAS, Jan 2025). "The unequal adoption of ChatGPT exacerbates existing inequalities among workers."
   https://www.pnas.org/doi/10.1073/pnas.2414972121

5. BCG (2025). "AI at Work 2025: Momentum Builds, but Gaps Remain."
   https://www.bcg.com/publications/2025/ai-at-work-momentum-builds-but-gaps-remain

6. McKinsey (2025). "Superagency in the Workplace."
   https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/superagency-in-the-workplace-empowering-people-to-unlock-ais-full-potential-at-work

7. McKinsey (2026). "A US productivity unlock: Investing in frontline workers' AI skills."
   https://www.mckinsey.com/capabilities/operations/our-insights/a-us-productivity-unlock-investing-in-frontline-workers-ai-skills

8. Microsoft Work Trend Index (2024/2025).
   https://www.microsoft.com/en-us/worklab/work-trend-index

9. Brynjolfsson, Li & Raymond (2023/2025). "Generative AI at Work." QJE.
   https://academic.oup.com/qje/article/140/2/889/7990658

10. Noy & Zhang (2023). "Experimental Evidence on the Productivity Effects of Generative AI." Science.
    https://www.science.org/doi/10.1126/science.adh2586

11. Dell'Acqua et al. (2023). "Navigating the Jagged Technological Frontier." HBS WP 24-013.
    https://www.hbs.edu/faculty/Pages/item.aspx?num=65159

12. Otis et al. (2024). "The Uneven Impact of Generative AI on Entrepreneurial Performance." HBS WP 24-042.
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4671369

13. Dropbox (2025). "Research: How top performers stand out in the age of AI."
    https://blog.dropbox.com/topics/company/research-how-top-performers-stand-out-in-the-age-of-ai

14. Penn Wharton Budget Model (Sep 2025). "The Projected Impact of Generative AI on Future Productivity Growth."
    https://budgetmodel.wharton.upenn.edu/issues/2025/9/8/projected-impact-of-generative-ai-on-future-productivity-growth

15. St. Louis Fed (Nov 2025). "The State of Generative AI Adoption in 2025."
    https://www.stlouisfed.org/on-the-economy/2025/nov/state-generative-ai-adoption-2025

16. OECD (2025). "Bridging the AI Skills Gap: Is Training Keeping Up?"
    https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/04/bridging-the-ai-skills-gap_b43c7c4a/66d0702e-en.pdf

17. World Economic Forum (2025). "Beyond the desk: How AI is transforming the frontline workforce."
    https://www.weforum.org/stories/2025/10/ai-frontline-workforce/

18. Census Bureau (2025). "The Rise of Industrial AI in America."
    https://www2.census.gov/library/working-papers/2025/adrm/ces/CES-WP-25-27.pdf
