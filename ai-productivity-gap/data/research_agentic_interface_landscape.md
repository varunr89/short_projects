# Research Notes: Agentic Interface Landscape

**Research date:** February 2026

---

## 1. CLI Tools -- The Power User Layer

### Claude Code (Anthropic)
- **Released:** February 2025 (research preview); generally available May 2025 alongside Claude 4
- **What it does:** Agentic coding tool that lives in your terminal. Understands full codebases, executes multi-step tasks, handles git workflows, runs terminal commands, creates/edits files across projects -- all via natural language
- **Key differentiator:** Deep integration with Claude models (especially Opus 4.5, released late November 2025, which was the catalyst for its viral moment). Expanded to web and iOS in October 2025, making it multi-surface while keeping the terminal as home base
- **Adoption data:**
  - $500M+ annualized revenue as of October 2025; hit $1B annualized run rate by ~January 2026 -- faster than ChatGPT reached that milestone
  - 10x user growth since May 2025 launch
  - In a UC San Diego/Cornell survey of 99 professional developers (January 2026), Claude Code (58 respondents) edged out GitHub Copilot (53) and Cursor (51) as the most-used platform
  - Went viral over the December 2025 holidays -- non-programmers used it for "vibe coding" (booking theater tickets, filing taxes, monitoring tomato plants)
  - Fortune called it Anthropic's "ChatGPT moment"

### Codex CLI (OpenAI)
- **Released:** April 16, 2025 (open-sourced on GitHub under Apache 2.0)
- **What it does:** Local AI agent harness that runs on user's machine. Iteratively reviews changes, applies edits to files with human oversight. Uses `codex-mini-latest` model (API-only)
- **Key differentiator:** Open-source from day one. Rebuilt around agentic workflows rather than chat
- **Adoption data:** Not publicly reported in the same detail as Claude Code

### Aider (Paul Gauthier)
- **Released:** Mid-2023; continuously updated since
- **What it does:** AI pair programming in the terminal. Supports 100+ languages, auto-commits with sensible messages, runs linters/tests on AI-generated code, auto-fixes errors
- **Key differentiator:** Model-agnostic (works with Claude, GPT, Gemini, Grok, local models via OpenRouter). Pioneered the "diff edit format" for structured code changes. Tracks what percentage of each release was written by aider itself (reached 79% by v0.84.0)
- **Adoption data:** 47K+ GitHub stars

### Why CLI matters
CLI tools offer maximum power: they integrate into existing developer workflows (git, shell scripts, CI/CD), impose minimal overhead, and give the AI direct access to the tools developers already use. The friction is the perceived learning curve -- the terminal is invisible to non-developers, which creates a ceiling on who these tools reach. This is central to the "browser moment" argument.

---

## 2. TUI Tools -- The Bridge Layer

### OpenCode
- **Released:** Approximately August 2025 (reached 50K GitHub stars and 650K MAUs in first 5 months)
- **Built by:** The SST (serverless framework) team
- **What it does:** Go-based TUI that provides a visual terminal interface for AI coding. Supports multiple AI providers (Claude, GPT, Gemini). Integrates with Language Server Protocol for code intelligence and Model Context Protocol (MCP) for tool extensibility
- **Key differentiator:** The TUI format -- richer than raw CLI (panels, syntax highlighting, visual diff previews) but still terminal-native. No browser or Electron overhead. Free models included out of the box
- **Adoption data:** 100K+ GitHub stars by early 2026. 650K MAUs within 5 months. Gained 30K stars in a single month

### Why TUIs are interesting
TUIs represent a middle ground: they give visual affordances (panels, menus, scrollable views, color) without leaving the terminal. They lower the barrier compared to raw CLI while preserving the composability and speed that make terminal tools powerful. They are the "terminal with training wheels" -- and potentially the bridge that gets more people from chat interfaces toward agentic workflows.

---

## 3. IDE Integrations -- The Mainstream Developer Layer

### Cursor (Anysphere)
- **Founded:** 2022 (four MIT students); launched March 2023
- **What it does:** AI-native IDE built on VS Code. Composer (frontier model) for multi-file agent tasks. Agent mode shows agents, plans, and runs as first-class sidebar objects. Visual Editor (late 2025) lets you drag-and-drop in rendered web apps and the agent applies code changes
- **Key differentiator:** First mover in "agentic IDE" category. Multiple agents working in parallel on the same project
- **Adoption data:**
  - 1M+ daily active developers
  - 360K paying customers
  - $500M ARR by May 2025; $1B ARR by ~October 2025
  - $29.3B valuation (November 2025 funding round, $2.3B raised)
  - Fastest-growing SaaS company of all time from $1M to $500M ARR

### GitHub Copilot (GitHub/Microsoft)
- **Agent mode announced:** February 6, 2025 (preview); GA later in 2025
- **What it does:** Evolved from autocomplete to multi-file agent mode. Autonomously identifies subtasks, edits across files, runs tests, monitors terminal output, auto-corrects in a loop
- **Key differentiator:** Distribution. Already embedded in GitHub's 100M+ developer ecosystem. 42% market share in AI coding assistants
- **Adoption data:**
  - 20M cumulative users (July 2025), up from 15M in April 2025
  - 1.3M paid subscribers
  - 50K+ organizations; 90% of Fortune 100

### Windsurf (formerly Codeium, now Cognition)
- **Launched:** November 13, 2024 (as Windsurf Editor)
- **What it does:** VS Code fork with Cascade (agentic assistant) that plans multi-step edits, calls tools, and uses deep repo context
- **Key differentiator:** Coined "Flows" concept -- AI and developer share context bidirectionally in real-time
- **Adoption data:** $82M ARR at acquisition
- **Drama:** Google acqui-hired CEO ($2.4B deal), Cognition then acquired Windsurf's IP for ~$250M over a single weekend

### Cline
- **Released:** ~January 2024 (VS Code extension)
- **What it does:** Autonomous coding agent inside VS Code. Creates/edits files, runs terminal commands, drives browser for UI debugging, supports MCP
- **Key differentiator:** Most aggressive autonomy among VS Code extensions. Browser automation capability
- **Adoption data:** 4M+ developers; 2M+ downloads; 47K+ GitHub stars

---

## 4. Enterprise Chat Wrappers -- The Least Agentic Category

### Microsoft Copilot for M365
- **Pricing:** $30/user/month (not included in M365 subscriptions)
- **What it does:** AI features embedded in Word, Excel, PowerPoint, Teams, Outlook
- **Why least agentic:** Operates within tightly scoped individual applications. Cannot chain multi-step workflows across tools autonomously

### Google Gemini for Workspace
- **Pricing:** Included in Workspace Business and Enterprise plans
- **What it does:** AI features across Gmail, Docs, Sheets, Slides
- **Why least agentic:** Primarily reactive (summarize this, draft that) rather than autonomous

### The gap
These tools embody the "chat wrapper" paradigm: AI layered on top of existing apps as a helper, not as an autonomous agent. The user remains the orchestrator of every step. Compare this with CLI/IDE tools where the AI can autonomously read files, write code, run tests, observe failures, and fix them. The enterprise chat wrappers are roughly where web search was before the browser: the capability exists, but the interface constrains what's possible.

---

## 5. Fully Autonomous Agents and App Builders

### Devin (Cognition Labs)
- **Pricing:** Dropped from $500/month to $20/month minimum
- **What it does:** Fully autonomous software engineer. Takes natural language instructions, works independently
- **Adoption data:** $73M ARR by June 2025 (up from $1M in September 2024). Goldman Sachs deployed it as "Employee #1" in their hybrid workforce

### Replit Agent / Bolt.new / Lovable
- "App builder" tools for non-technical users. Attempts at the "browser moment" for app building, but they trade agency for simplicity

---

## 6. The "Browser Moment" Thesis and Terminology

### The browser analogy
- Multiple commentators have drawn this parallel. Semi Analysis published "Claude Code is the Inflection Point" -- arguing that Claude Code specifically represents the interface breakthrough
- The analogy is in the air but not yet crystallized into a single canonical framing. Room to own this framing in the blog post

### The term "agentic interface"
- Not widely used as a standalone term. More common terms:
  - **"Agentic IDE"** -- coined/popularized by RedMonk analyst Kate Holterhoff
  - **"Agentic coding"** -- the term Anthropic uses
  - **"Agentic AI"** -- the broad umbrella term (Gartner, Deloitte, et al.)
  - **"Vibe coding"** -- Andrej Karpathy's term (February 2025), Collins Dictionary Word of the Year 2025
- There is space to define "agentic interface" as a term -- the interface layer that turns AI capability into AI agency

### The accessibility gap
- Anthropic's own data shows developers integrate AI into 60% of work but fully delegate only 0-20% of tasks
- 85% of developers regularly use AI tools by end of 2025, but adoption among non-developers remains largely limited to chat
- The missing piece: an interface that gives non-technical users the agentic power that CLI users have

---

## 7. The Trajectory

1. **Multi-surface expansion:** Claude Code started as CLI-only, then added web and iOS. The winning pattern is "one platform, every surface"
2. **Multi-agent orchestration:** Cursor 2.0 and Windsurf both ship parallel agent sessions. GitHub Copilot CLI ships with four specialized agents
3. **Memory and persistence:** RedMonk identifies memory as a top developer concern for 2026
4. **Beyond coding:** Claude Code's viral moment came from non-coding use cases. Anthropic highlights extending agentic tools "beyond engineering teams to empower domain experts." This is the browser moment -- when the interface stops being for specialists only
5. **Agent marketplaces and skills:** GitHub Copilot's "skills" system, MCP adoption, OpenCode's extensibility all point toward composable, customizable agents -- much like browser extensions

---

## Key Sources

- [Anthropic 2026 Agentic Coding Trends Report](https://resources.anthropic.com/2026-agentic-coding-trends-report)
- [Claude Code GitHub Repository](https://github.com/anthropics/claude-code)
- [Fortune: Claude Code gives Anthropic its viral moment](https://fortune.com/2026/01/24/anthropic-boris-cherny-claude-code-non-coders-software-engineers/)
- [Semi Analysis: Claude Code is the Inflection Point](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)
- [Cursor Statistics (DevGraphiq)](https://devgraphiq.com/cursor-statistics/)
- [SaaStr: Cursor Hit $1B ARR](https://www.saastr.com/cursor-hit-1b-arr-in-17-months-the-fastest-b2b-to-scale-ever-and-its-not-even-close/)
- [RedMonk: 10 Things Developers Want from their Agentic IDEs in 2025](https://redmonk.com/kholterhoff/2025/12/22/10-things-developers-want-from-their-agentic-ides-in-2025/)
- [GitHub Copilot crosses 20M users (TechCrunch)](https://techcrunch.com/2025/07/30/github-copilot-crosses-20-million-all-time-users/)
- [OpenCode GitHub Repository](https://github.com/opencode-ai/opencode)
- [Vibe Coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [Cline GitHub Repository](https://github.com/cline/cline)
- [Windsurf acquisition by Cognition (TechCrunch)](https://techcrunch.com/2025/07/14/cognition-maker-of-the-ai-coding-agent-devin-acquires-windsurf/)
- [Anthropic brings Claude Code to the web (TechCrunch)](https://techcrunch.com/2025/10/20/anthropic-brings-claude-code-to-the-web/)
- [Scientific American: How Claude Code is bringing vibe coding to everyone](https://www.scientificamerican.com/article/how-claude-code-is-bringing-vibe-coding-to-everyone/)
- [Codex CLI GitHub Repository](https://github.com/openai/codex)
- [Devin 2.0 pricing cut (VentureBeat)](https://venturebeat.com/programming-development/devin-2-0-is-here-cognition-slashes-price-of-ai-software-engineer-to-20-per-month-from-500)
