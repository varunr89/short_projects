# The Integral Problem: Why AI Isn't Moving the Productivity Needle

## TL;DR

- **The problem**: Lab studies show 14-40% individual productivity gains from AI. Aggregate economic impact: 0.01 percentage points. A gap of roughly 1,000x.
- **The hypothesis**: AI adoption and potential gain are inversely correlated. The people who would benefit most aren't using the tools; the people using them most need them least.
- **What to do**: Mandate the AI path with patience, replace demos with team-specific training, invest in agentic interfaces, and build guardrails instead of gates.

---

I believe deeply that AI will improve the human condition. Many people disagree. That's fine -- I've spent two and a half years testing every major AI model release, not through demos but by integrating each one into real work. Customer communications, data analysis, code generation, product planning. I subscribe to every frontier AI service and test them end-to-end.

And I'm frustrated, because the tools work and almost nobody is using them.

Last week, Apollo's chief economist Torsten Slok wrote: "AI is everywhere except in the incoming macroeconomic data" -- invoking Robert Solow's 1987 observation that "you can see the computer age everywhere but in the productivity statistics." GPT-5.2 just derived an original result in theoretical physics. Penn Wharton measured AI's actual aggregate impact: 0.01 percentage points. One curve is practically vertical. The other is flat.

In every team I worked with at a large tech company, at most 1 in 20 engineers had truly adopted AI into their daily workflow. Not across the company -- among core engineering and product teams. Young, tech-savvy people who build software for a living. The people who should have been first.

That ratio is not an anecdote. Once I started looking at the research, I found it everywhere.

## The mismatch

In my teams, the engineers who were already the most productive -- writing the cleanest code, holding the strongest mental models -- were the ones experimenting with AI. The junior engineers who would have benefited most from an AI that could explain unfamiliar code or suggest patterns they hadn't learned? They barely touched the tools.

![The Mismatch: AI adoption rate vs. productivity gain by employee percentile](../charts/01_the_mismatch.png)
*Sources: Brynjolfsson, Li & Raymond (2023); Bick, Blandin & Deming (2024)*

The research confirms exactly what I saw. Brynjolfsson studied 5,179 customer support agents: the bottom quintile improved 35%, the top quintile roughly zero. Bick found a 2:1 education gradient in who actually uses AI. The mismatch is almost perfectly inverted -- the workers who gain 35% adopt at half the rate of workers who gain close to zero.

> *The people standing to gain the most from these tools are the ones who aren't using them, and the people using them the most are the ones who need them least.*

This is the thesis that makes everything else click. It's not just that adoption is low. It's that adoption and potential gain are inversely correlated.

## The integral problem

I think about organizational productivity as an integral -- the area under a curve where the y-axis is each employee's output and the x-axis is their percentile. The total productivity of the organization is that area.

![The Integral Problem: realized vs. unrealized productivity gains](../charts/02_the_integral_problem.png)
*Sources: Brynjolfsson et al. (2023); BCG-Harvard (2023); Bick et al. (2024)*

The chart tells the story. The red dashed line shows what we'd gain if everyone adopted AI -- huge lifts at the bottom, tapering toward the top. The blue line shows what we're actually capturing: almost nothing, because only the top few percent are using the tools. The red shaded area is unrealized potential. It's enormous.

*Realized Gain(x) = Individual Gain(x) x Adoption Rate(x)*

You're multiplying big numbers by small numbers everywhere. Lab studies find 14-40% individual gains. Penn Wharton measured 0.01 percentage points of aggregate impact. A gap of roughly 1,000x. The Anthropic Economic Index found AI usage has a Gini coefficient of 0.84 to 0.86 -- more concentrated than income inequality in the most unequal country on Earth.

### Amdahl's Law

Even among the people who do use AI, the gains disappoint. I spend maybe 11% of my time writing code -- a Microsoft study of 484 developers found the same number. The rest is meetings, debugging, architecture, code review. If AI makes coding 3x faster, the theoretical maximum improvement is 15%. Even if coding became instant -- zero time -- the max is 25%.

Amdahl's Law: *Speedup = 1 / ((1 - p) + p/s)*. You can only speed up the fraction of work AI touches.

METR ran the most rigorous test to date: sixteen experienced developers were randomized to use or not use AI tools on 246 tasks. The AI group was 19% *slower*. But they believed they'd sped up by 20%.

### The organizational multiplier

When 1 in 20 on my team used AI effectively, the other 19 still set the pace. It didn't matter that my best engineer wrote code twice as fast if the bottleneck was design review, QA, or the deployment pipeline.

This is Michael Kremer's O-Ring theory: production is multiplicative. One broken link degrades the whole chain. Google's Project Aristotle confirmed it -- studying 180 teams, they found that how people interact matters more than who's on the team.

Most organizational work isn't breakthrough discovery. It's execution. Delivery. The integral under the full curve determines what ships. And right now, that integral barely moves.

## The capability-adoption gap

![The Capability-Adoption Gap: AI milestones vs. enterprise adoption](../charts/03_capability_adoption_gap.png)
*Source: Compiled from public announcements and benchmark data*

Look at this chart. In March 2023, GPT-4 passed the bar exam. By late 2024, reasoning models hit PhD levels. By early 2025, autonomous coding agents shipped. By February 2026, GPT-5.2 contributed original physics. The capability curve is vertical.

Adoption? Flat. Lucidworks found 42% of companies abandoned most AI initiatives in 2025, up from 17% in 2024. Companies aren't ramping up -- they're giving up.

The exceptions prove the rule. Shopify mandated AI as a baseline expectation. JPMorgan went from banning ChatGPT to deploying LLM Suite to 200,000 employees in eight months. The gap isn't between companies that have AI and those that don't. It's between companies that enabled it broadly and those still running pilots.

## Why the gap exists

I've watched this up close for over two years. Five problems keep surfacing.

### The learning curve is real

Even for me, getting truly productive with AI required significant effort. I got lucky -- during paternity leave, I had unstructured time to experiment. I'd hold my son in one arm and voice-transcribe prompts with the other. That gave me something almost no working professional gets: hours of low-stakes experimentation.

Most employees get maybe 30 minutes to try a new tool before the next Slack message pulls them away. That's not enough. Humlum and Vestergaard confirmed this: even when researchers told 18,000 workers that AI could halve their task time, it had zero effect on usage. Information doesn't drive adoption. Friction does.

### The belief deficit

People's impression of AI is shaped by two misleading forces. On one side: Google's AI Overview telling users to eat rocks, or GPT-5.2 Pro spending nearly three minutes reasoning through whether to walk or drive to the car wash -- noting that "the wash requires the vehicle to be present" -- and still concluding I should walk.

On the other: $8 million Super Bowl ads where 23% featured AI, including Google's Gemini ad that hallucinated a fact about Gouda cheese on national television. Only 32% of Americans trust AI. Can you blame them?

The irony is that the tools that actually work -- terminal-based coding agents, agentic workflows -- succeed precisely because they target constrained domains where outputs are immediately verifiable. But they aren't flashy enough for a Super Bowl ad. BCG found that leadership support alone swings positive AI sentiment from 15% to 55%.

### Corporate training has not evolved

Every AI training I attended was a marketing person demoing integrations nobody asked for, or an executive showing tools employees aren't allowed to use. The audience nods politely. Nothing changes.

BCG's data: employees with 5+ hours of training become regular AI users at 79% vs. 67% with less. Twelve percentage points from actually investing in training. Real training means capstone projects -- each team builds a workflow for their own use case, not watching a slide deck.

### Enterprise tools aren't ready

Companies shove half-baked AI wrappers down employees' throats. "Use our internal copilot. It's approved by security." It's a thin wrapper around a rate-limited API with a model two generations behind.

Meanwhile, the tools that actually work are blocked. So 78% of AI users bring their own tools to work. JPMorgan figured this out: they went from banning ChatGPT to deploying LLM Suite to 200,000 employees, solving compliance at the infrastructure level. Build guardrails, not gates.

### Productivity is deeply personal

The way I write code is different from how you write code. There is no single AI workflow that fits everyone. Enterprise tools pretend otherwise.

The Anthropic Gini data (0.84-0.86) isn't measuring adoption rate. It's measuring how personal productivity is. Power users invested time to build workflows for their specific work. You can't copy-paste that across a thousand people. BCG's "silicon ceiling" data confirms it: frontline adoption stalled at 51% in 2023 and hasn't moved since.

## The agentic interface

AI is in its pre-browser moment. By the early 1990s, the internet was extraordinary -- but using it meant memorizing terminal commands and configuring network settings. Then the browser shipped. The technology didn't change. The interface did.

The most powerful AI tooling today lives in the terminal -- Claude Code, Codex CLI, Aider. That's structural, not incidental. CLI tools have full access to your machine: read files, write code, run tests, chain tools together. You can't do this from a chat window.

Two years ago, I ran a customer outreach program at a large tech company. It was slow and imprecise -- generic messages, hoping they landed. Today, with agentic tools, the same campaign can be surgical: pulling data from a CSV, looking up contacts through browser automation, drafting tailored emails, sending through authenticated APIs. All from one interface. But it took real effort to build.

Claude Code crossed $1 billion in annualized revenue faster than ChatGPT. Cursor hit $1 billion ARR. Developers aren't waiting for enterprise tooling. They're building their own workflows now.

## What to do Monday morning

### Mandate the AI path, with patience

Default to the AI-assisted approach for new projects. But budget for a temporary productivity dip -- you can't mandate AI and penalize people for being slower while they learn.

### Invest in applied training, not demos

Stop demo-driven training. Each team builds a tool for their own use case, with coaching from AI-fluent colleagues. I became fluent during paternity leave because I had unstructured time. Create that expectation: if it can be done with AI, do it with AI.

### Embrace agentic interfaces

The productivity unlock isn't the enterprise chat wrapper. It's tools that integrate into real workflows -- pulling data, automating actions, chaining operations. Give teams budget and permission to explore them.

### Accept that productivity is personal

Stop prescribing one-size-fits-all. Give people time and permission to find their own use cases. The goal is to move the whole distribution rightward, not force everyone through the same door.

### Enable, don't gate

Stop battling shadow AI. You will lose. If 78% of users bring their own tools, the problem is your approved tools. Solve security at the platform level. Trust your employees.

## The bottom line

The gap between AI capability and AI impact is organizational, not technological. The mismatch means the people who'd benefit most aren't using the tools. Amdahl's Law means even among those who do, the gains are bounded. The integral barely moves.

Nearly 90% of 6,000 executives in the NBER study said AI has had no impact on productivity. Yet they forecast 1.4% growth over the next three years. The belief is there. The results aren't. That's the Solow paradox, playing out again.

The integral only changes when the whole curve moves. Not just the tail.
