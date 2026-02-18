# The Integral Problem: Why AI Isn't Moving the Productivity Needle

I've spent the last two and a half years working across engineering and product teams at a large tech company, and in that time I've personally evaluated every major AI model release. I subscribe to every frontier AI service. I've tested each one end-to-end, not in sandboxed demos but on real work -- customer communications, data analysis, code generation, product planning.

The progression has been staggering. In early 2023, GPT-4 could pass the bar exam and ace the SAT, which felt like science fiction at the time. By mid-2024, models could see images and hold real-time voice conversations. By late 2024, they could autonomously control a computer desktop -- moving the mouse, clicking buttons, typing into applications. By early 2025, reasoning models were performing at PhD levels on physics and chemistry benchmarks. And just last week, GPT-5.2 derived an original result in theoretical physics -- a formula that physicists had assumed was zero for decades, discovered through a 12-hour scaffolded reasoning session and co-authored with researchers from the Institute for Advanced Study, Vanderbilt, Cambridge, and Harvard.

We went from models that could write passable haikus to autonomous agents contributing genuine scientific discoveries. In under three years.

And yet.

> In every team I worked with, at most 1 in 20 engineers had truly adopted AI into their daily workflow.

Not 1 in 20 across the whole company. Not 1 in 20 among random employees. One in twenty among core engineering and product teams at a major technology company. Young, tech-savvy people who build software for a living. The people who should have been first.

That ratio is not an anecdote. It's empirical evidence. And once I started looking at the research, I found it everywhere.

## The mismatch

Here's what makes this story more painful than a simple "people aren't adopting new technology" narrative.

![The Mismatch](../charts/01_the_mismatch.png)

The people who would gain the most from AI are the least likely to use the tools.

Brynjolfsson, Li, and Raymond studied 5,179 customer support agents at a Fortune 500 company and found that AI increased overall productivity by 14%. But the gains were wildly uneven. The bottom quintile -- the lowest-performing 20% of agents -- improved by 35%. The top quintile improved by roughly zero. The mechanism was straightforward: the AI had essentially encoded the knowledge and patterns of top performers and redistributed them downward.

Dell'Acqua and colleagues at Harvard ran a controlled study with 758 BCG consultants -- 7% of the firm's entire consulting force -- using GPT-4. Below-average consultants improved output quality by 43%. Above-average consultants improved by 17%. The performance gap between the top and bottom performers shrank from 22 percentage points to just 4.

Noy and Zhang found similar compression in a randomized writing experiment: ChatGPT reduced task completion time by 40% and increased quality by 18%, with the largest gains for the lowest performers.

The pattern is remarkably consistent across studies: AI is an equalizer. It lifts the floor far more than it raises the ceiling.

Now look at who actually uses it. Bick, Blandin, and Deming ran the first nationally representative U.S. survey on generative AI use and found a stark 2:1 education gradient -- about 40% of college-educated workers use AI at work, compared to about 20% of workers without a college degree. Pew Research confirmed the gap is widening, from 7 percentage points to 12 in a single year. Humlum and Vestergaard surveyed 18,000 Danish workers and found that higher-earning workers adopt at significantly higher rates, even controlling for experience and tenure.

The mismatch is almost perfectly inverted. The workers who gain 35-43% from AI adopt at half the rate of workers who gain 0-17%.

This is the thesis that makes everything else in this post click. It's not just that adoption is low. It's that adoption and potential gain are inversely correlated. The people standing to gain the most from these tools are the ones who aren't using them, and the people using them the most are the ones who need them least.

## The integral problem

Think about organizational productivity as a curve. On the x-axis, employees ranked by percentile. On the y-axis, output. The total productivity of the organization is the area under that curve -- the integral.

![The Integral Problem](../charts/02_the_integral_problem.png)

When only the top 5% adopt AI, only the right tail of that curve shifts upward. The shaded area between the old curve and the new one is vanishingly small. The integral barely moves.

The math is straightforward but unforgiving. Realized gain at any point on the distribution equals the individual gain at that point multiplied by the adoption rate at that point. Both factors work against us. At the bottom of the distribution, where individual gains are highest (35-43%), adoption rates are lowest (around 20%). At the top, where adoption rates are highest (40-50%), individual gains are smallest (0-17%). You're multiplying big numbers by small numbers everywhere.

The result shows up in the macro data. Lab studies consistently find 14-40% productivity gains for specific tasks. But when Penn Wharton measured AI's actual impact on aggregate total factor productivity, they found 0.01 percentage points. That's a gap of roughly 1,000x between what's measured in controlled settings and what's showing up in the economy.

You can see AI everywhere except in the productivity statistics.

The Kansas City Fed published a study just this month noting that while higher AI adoption is associated with faster productivity growth across individual industries, "it explains little of the shift in aggregate contributions." The San Francisco Fed reached the same conclusion, explicitly invoking Robert Solow's 1987 observation that "you can see the computer age everywhere but in the productivity statistics." The Fed researchers found that observation remains relevant today. Kent Smetters at Penn Wharton put it more bluntly: "It's not electricity, it's not refrigeration -- it's not that transformative."

The Anthropic Economic Index measured AI usage patterns across enterprise deployments and found a Gini coefficient of 0.84 to 0.86. To put that in plain language: if you lined up every employee in an organization by how much they use AI, the distribution would look like a hockey stick lying on its back. A tiny cluster of power users at the far end accounts for almost all the usage. A Gini of 0.85 is more concentrated than income inequality in the most unequal country on Earth. Frontier workers in their dataset sent 6x more messages than the median enterprise user.

This is where the organizational theory comes in, and it matters more than most AI discussions acknowledge. Michael Kremer's O-Ring theory -- named after the Challenger disaster, where a single faulty component destroyed the entire shuttle -- models production as a multiplicative function across tasks. If any one person in the chain fails at their task, they destroy a disproportionate fraction of the final product's value. The implication: quality enters multiplicatively, so a team of nine excellent workers and one mediocre one produces far less than ten good workers. The cost of weak links is devastating in high-value production.

Ivan Steiner's foundational taxonomy of group tasks lays out the framework. Some tasks are disjunctive -- group output depends on the best member, like a quiz bowl where one person can answer. But most real-world organizational work is conjunctive (output limited by the weakest member, like a climbing team that goes only as fast as its slowest climber) or additive (output is the sum of everyone's contributions, like tug-of-war). In conjunctive and additive work, the floor and the average matter more than the ceiling.

Anderson and Sally, analyzing over 8,000 professional soccer matches, demonstrated this vividly. Soccer is a "weak link" sport. The 8th through 11th best players on a team predict results more than the star. Improving a team's worst player from the 38th to the 48th percentile is worth 13 goals per season. Improving the best player from the 82nd to the 92nd percentile is worth only 10. The bottom of the roster has higher leverage than the top.

Swaab and colleagues found something even more striking: too much top talent actually hurts team performance in interdependent sports. In basketball and football, once the ratio of elite to non-elite players exceeded roughly 2:1, coordination broke down. More stars produced fewer assists, fewer defensive rebounds, and lower field-goal percentages. In interdependent work -- which describes most knowledge work -- there is a point where more stars actively harms output.

Google's own Project Aristotle study of 180 internal teams found that "who is on a team matters less than how the team members interact." Psychological safety, not individual brilliance, was the single strongest predictor of team performance. Woolley and colleagues published similar findings in Science: a team's collective intelligence was not correlated with the average or maximum individual intelligence of its members.

I want to be honest about the counterargument. O'Boyle and Aguinis showed convincingly that individual performance in knowledge work follows a power-law distribution, not a normal one. Stars are real. Netflix's "talent density" philosophy explicitly embraces this: in creative work, the best performers may be 10x better than their peers. And for genuinely disjunctive tasks -- making a breakthrough discovery, closing a transformative deal -- the star model applies.

But here's the key: even under a power-law distribution, the body of the distribution still produces the majority of total output. If you have 1,000 engineers and 50 are 10x performers, those 50 contribute enormously per capita. But the other 950 still produce the majority of aggregate work. Price's Law says half of all output comes from the square root of contributors -- but the other half comes from everyone else. Remove them and you've halved your total output.

Most organizational work is not disjunctive. It's execution. Delivery. Operations. The kind of work where the aggregate matters, where the integral under the full curve determines what ships and what doesn't. And right now, that integral is barely moving.

## The capability-adoption gap

The timeline makes the absurdity visible.

![The Capability-Adoption Gap](../charts/03_capability_adoption_gap.png)

In March 2023, GPT-4 passed the bar exam at the 90th percentile. Six months later, models could understand images. By May 2024, GPT-4o could hold real-time multimodal conversations with 320-millisecond voice response time. By September 2024, OpenAI's o1 was performing at PhD levels on physics and chemistry benchmarks. In October 2024, AI won a Nobel Prize. By early 2025, autonomous coding agents were shipping -- Claude Code, Codex CLI, GitHub Copilot's agent mode -- tools that could plan, write, debug, and deploy code with minimal human intervention. By mid-2025, Claude Opus 4 could sustain multi-hour autonomous work spanning thousands of steps. By late 2025, AI coding tools were achieving 77% on the SWE-bench benchmark, solving real-world software engineering problems that would challenge experienced developers.

The capability curve is practically vertical. And the adoption curve remains stubbornly flat.

McKinsey's 2025 State of AI survey found that 88% of organizations say they "use AI." But only about 7% have fully scaled it across operations. That gap between saying and doing is where productivity gains go to die.

Worklytics' 2025 AI Adoption Benchmarks found that 74% of companies show no tangible value from their AI investments. Not negative value. Just nothing measurable.

According to Lucidworks, 42% of companies abandoned most of their AI initiatives in 2025, up from 17% in 2024. Companies aren't ramping up. They're giving up.

McKinsey separately reported that over $1 trillion was spent on IT last year, yet more than 60% of companies reported no significant bottom-line impact from AI. AEI noted that roughly 80% of companies claim to use generative AI, yet just as many report no meaningful impact, with about 90% of transformative vertical use cases stuck in pilot mode.

The Solow paradox is repeating itself. Robert Solow observed in 1987 that you could see the computer age everywhere except in the productivity statistics. Here we are, nearly four decades later, and the same sentence works if you substitute "AI" for "computers." The capability exists. The tools are extraordinary. And the economic needle has barely budged.

## Why the gap exists

I've watched this play out up close for over two years. Five problems keep surfacing.

### The learning curve is real

I consider myself AI-fluent. I've been building with these tools since GPT-3. And even for me, getting truly productive with AI required significant effort.

I got lucky. During paternity leave, I had unstructured time to experiment. I'd hold my son in one arm and voice-transcribe prompts with the other. That sounds absurd, but it gave me something almost no working professional gets: hours of low-stakes experimentation. Trying things, failing, adjusting, building intuition. That's what it actually takes.

Most employees don't have that. They have meetings, deadlines, and sprint commitments. They get maybe 30 minutes to try a new tool before the next Slack message pulls them away. That's not enough to build fluency. It's barely enough to get through setup.

Humlum and Vestergaard found something that should alarm every manager trying to drive adoption. In their study of 18,000 Danish workers, even when researchers randomly informed workers that AI could halve their task time, it had no effect on usage behavior. None. Information alone doesn't drive adoption. Knowing the tool is powerful doesn't make people use it. The frictions -- lack of time, lack of training, lack of integration into existing workflows -- are causal barriers, not just correlates.

This is not an awareness problem. It's a friction problem.

### The belief deficit

Most people's impression of AI comes from public failures. The lawyer who cited fake cases. The company that shipped AI-generated slop. The chatbot that told someone to eat rocks.

Can you blame someone for not wanting to stake their reputation on a tool they associate with embarrassing output?

Here's the thing: AI slop is a human problem, not an AI problem. It comes from people who don't review output. People who copy-paste without reading. People who were never taught how to prompt well or verify results. Bad work produced faster is still bad work. This problem has existed forever. AI just makes it more visible.

But the belief deficit is fixable. BCG found that positive sentiment toward AI jumps from 15% to 55% when employees receive strong leadership support. That's a 40-percentage-point swing driven entirely by whether leadership signals that AI is a serious, supported initiative rather than a fad. Only about 25% of frontline employees currently report having that level of support.

The fix isn't a newsletter. It isn't an all-hands deck. It's managers actively using AI in their own work, showing real examples from their own domain, and making it clear that AI-assisted work done well is valued -- not suspected.

### The training is useless

Every AI training I attended was a marketing person demoing tools that employees couldn't actually use.

I'm not exaggerating. The demos are flashy. Someone shows ChatGPT writing a poem or summarizing a document. The audience nods politely. Then everyone goes back to their desks and nothing changes. Because the demo didn't teach them how to integrate AI into their workflow. It showed them what's theoretically possible in a vacuum.

The OECD published a report specifically on this problem. Most AI training is focused on AI specialists, not general workers. The prerequisites demanded for AI courses are higher than average, creating a barrier for the people who need basic literacy most. There's too much specialist training and not nearly enough general AI literacy.

BCG's numbers tell the story. Among regular AI users, 18% received no training at all. Among those who did get training, only 36% said it was enough. But here's the lever: employees who received 5 or more hours of training became regular AI users at a rate of 79%, compared to 67% for those with less. Twelve percentage points of adoption driven by the difference between serious training and token training.

Real training looks nothing like a demo. Real training means hands-on workshops where people build their own workflows with their own data. It means pairing AI-fluent employees with those who aren't. It means giving people real, protected, calendar-blocked time to experiment and fail. Not a 45-minute lunch-and-learn. Not a slide deck.

### Enterprise tools aren't ready

Companies love to shove their own half-baked AI wrappers down employees' throats. "Use our internal copilot. It's approved by security." The internal copilot is a thin wrapper around a rate-limited API with a clunky interface and a model that's two generations behind.

Meanwhile, the tools that actually work -- Claude Code, Cursor, GitHub Copilot -- are either blocked or exist in a gray area. So what happens? Shadow AI. Employees use the good tools anyway, just on their personal machines, outside the security perimeter.

Microsoft's own Work Trend Index found that 78% of AI users bring their own AI tools to work. At small and medium businesses, that number rises to 80%. This is not a compliance failure. It's a product signal. When almost four out of five people bypass your approved tools, the problem is the approved tools.

This is an own goal. If your employees are using unauthorized tools, they're telling you something important: the sanctioned tools aren't good enough. Fix the tools, don't punish the behavior.

### Productivity is deeply personal

Knowledge work is individual. The way I write code is different from how you write code. The way I draft documents, run analyses, manage projects -- all different. There is no single AI workflow that fits everyone.

Enterprise tools are designed as if one workflow works for all. It doesn't. A product manager needs AI for different things than a backend engineer, who needs it for different things than a data scientist, who needs it for different things than a marketing lead.

The Anthropic Gini data (0.84-0.86 concentration) isn't just measuring adoption rate. It's measuring the deeply personal nature of productivity. The power users aren't power users because they got a better demo. They're power users because they invested the time to build workflows that fit their specific work.

BCG's data on the "silicon ceiling" drives this home. Frontline worker adoption stalled at 51% in 2023 and hasn't moved since, despite two years of capability improvements and organizational push. The ceiling isn't a capability ceiling. It's a personalization ceiling. The tools haven't met these workers where they are.

## The agentic interface

There's a useful analogy that keeps coming to mind. Think about the early internet. By the early 1990s, the underlying capability was extraordinary -- email, file transfer, hyperlinked documents spanning the globe. But using it meant memorizing terminal commands, understanding protocols, configuring network settings manually. The capability existed, but it was locked behind an interface that excluded almost everyone.

Then the browser shipped. Mosaic, then Netscape, then the explosion. The technology didn't change. The interface did. And that interface change is what turned the internet from an academic tool into the defining infrastructure of modern life.

AI is in its pre-browser moment right now. The capability is here -- it's remarkable, it's real, and it keeps getting better. But the dominant interfaces constrain what's possible.

Let me walk through the current landscape, because I think understanding the layers matters.

At the top of the power curve, you have CLI tools. Claude Code, Codex CLI, Aider. These live in your terminal and give AI direct access to the tools developers already use -- git, file systems, shell scripts, CI/CD pipelines. They're maximally powerful. Claude Code alone has crossed $1 billion in annualized revenue, faster than ChatGPT reached that milestone. In a UC San Diego/Cornell survey of professional developers in early 2026, Claude Code was the most-used agentic platform, edging out GitHub Copilot and Cursor.

One layer down, you have IDE integrations. Cursor reinvented itself with its own purpose-built model and multi-agent architecture where multiple AI agents work on different parts of a codebase simultaneously. It reached $1 billion in annualized revenue by late 2025, making it the fastest-growing SaaS company of all time from $1M to that milestone. GitHub Copilot sits on a distribution advantage no one else can match -- 100 million developers already in the ecosystem, 20 million cumulative users, 90% of the Fortune 100.

An interesting middle layer is emerging: TUIs -- terminal user interfaces. OpenCode, built by the SST team, exploded past 100,000 GitHub stars and 650,000 monthly active users in its first five months. It provides visual affordances -- panels, syntax highlighting, diff previews -- without leaving the terminal. It's the terminal with training wheels, a bridge between the raw power of CLI tools and the accessibility of graphical interfaces.

And at the bottom of the agentic spectrum, you have enterprise chat wrappers. Microsoft Copilot for M365, Google Gemini for Workspace. These layer AI on top of existing apps as a helper, not as an autonomous agent. The user remains the orchestrator of every step. They're roughly where web search was before the browser: the answers exist, but the interface makes it tedious to find them.

The terminology itself hasn't converged yet, which tells you how early this is. People call these tools "agentic IDEs" (RedMonk's Kate Holterhoff coined that one). Others say "agentic coding." Andrej Karpathy coined "vibe coding," which became Collins Dictionary's Word of the Year for 2025. I've seen "developer-grade AI," "AI workbench," and "agentic interface" all used to describe overlapping concepts. Semi Analysis published a piece titled "Claude Code is the Inflection Point," arguing it represents the interface breakthrough. The fact that we don't even have a settled term yet is itself a signal -- this category is still forming.

Here's a concrete example of what becomes possible when the interface gets out of the way. Two years ago, I drove a customer communication program reaching out to hundreds of one-off customers at a large tech company. It was slow, imprecise, and mostly ineffective. We were crafting generic messages and hoping they landed. Fast forward to today: using agentic AI tools, the same type of campaign can be surgical and prescriptive. Tailored outreach for each customer, specific recommendations based on their usage patterns, context-aware follow-ups that adapt based on response. The same workflow, transformed.

But it wasn't easy. It took trial and error. Hours of prompt iteration. Building custom pipelines. The effort pays off, but you have to invest it. The enterprise chat wrappers that promise "AI in a box" can't deliver this level of integration.

The investment signal is unmistakable. Claude Code at $1 billion ARR. Cursor at $1 billion ARR. OpenCode at 100K+ stars in months. Developers aren't waiting for enterprise tooling to catch up. They're building their own agentic workflows now.

The call to action here is simple: invest in agentic interfaces, not just chat wrappers. The browser didn't just make the internet easier to use. It made entirely new categories of work possible. Agentic AI interfaces will do the same, if we stop treating chat wrappers as the end state.

## What to do Monday morning

I've laid out the problem. Here's what I'd actually do about it, starting this week.

### Mandate the AI path, with patience

For new projects, default to the AI-assisted approach. Don't make it optional. But hold quality to the same bar as before. The goal is not to ship faster. The goal is to ship the same quality, faster, once people are up to speed.

Here's the part most managers skip: you have to budget for a temporary productivity dip. You cannot mandate AI and then penalize people for being slower while they learn. That kills adoption dead. Humlum's research showed that even knowing about AI's benefits doesn't change behavior when friction is high. You have to actively reduce the friction, which means time and patience.

John Ousterhout from Stanford calls AI a "tactical tornado." It lets you move fast, but speed without review produces slop. The fix is active review and tight feedback loops, not pulling back from AI. Quality control isn't optional. It's the entire point. AI without review is like shipping code without tests.

### Invest in applied training, not demos

Stop doing demo-driven AI training. Today. It's worse than useless because it creates the illusion that you've invested in adoption.

BCG's data makes the case. Employees with 5 or more hours of training use AI regularly at a rate of 79%. Those with less: 67%. That 12-point gap is the difference between a team where AI is part of the workflow and a team where it's a novelty. And right now, 18% of regular AI users got no training at all -- imagine what they could do with structured support.

Real training means:
- Hands-on workshops where people build workflows with their own data
- Pairing AI-fluent employees with those who are still learning
- Dedicated, protected time for experimentation -- not squeezed into existing sprints
- Follow-up sessions to share what worked and what didn't

I became fluent during paternity leave because I had unstructured time. You can't give everyone paternity leave, but you can carve out space for the same kind of experimentation. Two hours a week. A Friday afternoon. Something.

### Embrace agentic interfaces

The real productivity unlock is not the enterprise chat wrapper your company deployed last quarter. It's the agentic tools that integrate into real workflows -- terminal-based coding agents, IDE integrations with autonomous capabilities, tools that can read your codebase, run your tests, and iterate on failures without you babysitting every step.

I know this is a harder sell than "just add AI to Outlook." But the data is clear: the tools that are growing fastest -- Claude Code, Cursor, OpenCode -- are the ones that give users genuine agency, not just an autocomplete box in a sidebar. The enterprise wrappers that promise "AI in a box" aren't where the productivity gains live.

Give teams the budget and the permission to explore agentic tools. Solve for security at the platform level so you can say "yes" to the tools that actually work.

### Accept that productivity is personal

Stop prescribing. There is no one-size-fits-all AI workflow. A mandate to "use tool X for task Y" will fail because it ignores how individual knowledge work actually is.

The Anthropic Gini coefficient of 0.84-0.86 is not just a measure of inequality. It's a measure of how personal AI productivity is. The power users found workflows that fit their specific work. You can't copy-paste that across a thousand people.

Instead: give people time and explicit permission to find their own use cases. Celebrate when someone discovers an unconventional workflow. Share wins across teams. Let adoption be organic, messy, and personal. The goal is to move the whole distribution rightward, not to force everyone through the same door.

### Enable, don't gate

Stop battling shadow AI. You will lose.

If 78% of AI users are bringing their own tools to work, that tells you something fundamental about your approved tools. Instead of locking things down further, solve for data security and let people experiment.

There's a regulatory parallel here. The countries that over-regulate AI development slow down. The same dynamic plays out inside organizations. When you make it hard to use AI, people either don't use it or use it outside your visibility. Neither outcome is what you want.

Trust your employees. Build guardrails, not gates. There's a meaningful difference. The companies that win will be the ones that figured out how to say "yes, and here's how to do it safely" instead of "no."

## The bottom line

The gap between AI capability and AI impact is not a technology problem. It's an organizational one. The tools are extraordinary. The research consistently shows 14-40% productivity gains in controlled settings. The question is why almost none of that is showing up at the organizational level.

The answer is the integral. When adoption is concentrated among the people who need it least, and absent among the people who would gain the most, the aggregate barely moves. The math doesn't care about your most productive engineer's 10x workflow. It cares about the full curve.

The integral only changes when the whole curve moves. Not just the tail.
