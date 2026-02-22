# The Car Wash Test -- Design Document

**Date:** 2026-02-15
**Project directory:** `the-car-wash-test/`
**Status:** Design approved

## Concept

A blog post analyzing the viral "car wash" adversarial reasoning test across frontier AI models. The meme: you ask an AI "I need to wash my car, the car wash is 100 meters away, should I walk or drive?" and most models recommend walking -- missing that the car itself needs to be at the car wash.

## Angle

Mix of technical analysis and structured benchmark comparison. Layered depth: accessible first, then a deeper technical section. First-person, opinionated, irreverent tone but respectful -- framed as "testing the edges to make AI better."

## Structure

### 1. The Hook (~200 words)
- Lead with the contrast: GPT 5.2 Pro recently made news for a quantum physics breakthrough. The same model failed a question a five-year-old could answer.
- Introduce the meme and what it tests.
- Frame motivation: is this universal, or do some models handle it? Tested 9 model configurations across three frontier AI companies.

### 2. The Test and Results (~300 words)
- **Methodology:** Same prompt, clean session, no priming, first-shot only.
- **Models tested:** OpenAI (ChatGPT 5.2 Instant, Thinking, Pro), Google (Gemini 3 Fast, Thinking, Pro), Anthropic (Claude Haiku 4.5, Sonnet 4.5, Opus 4.6).

**Results table:**

| Provider | Model | Result | Notes |
|----------|-------|--------|-------|
| OpenAI | ChatGPT 5.2 Instant | Fail | Confidently says "Walk." |
| OpenAI | ChatGPT 5.2 Thinking | Fail | Same answer, recovers only when challenged |
| OpenAI | ChatGPT 5.2 Pro | Fail | Thought 2m 45s, lists correct answer as "exception" but still says walk |
| Google | Gemini 3 Fast | Pass | Correct with humor |
| Google | Gemini 3 Thinking | Pass | Snarky, playful, correct |
| Google | Gemini 3 Pro | Pass | Clean two-sentence answer |
| Anthropic | Claude Haiku 4.5 | Fail | Same failure pattern as smaller models |
| Anthropic | Claude Sonnet 4.5 | Pass | Correct, acknowledges the irony |
| Anthropic | Claude Opus 4.6 | Pass | Instant, no hesitation |

**Key callouts:**
- OpenAI swept: 0/3. Even the most powerful reasoning model failed.
- Google swept: 3/3. Even the smallest model got it.
- Anthropic split: larger models passed, smallest failed.
- The 5.2 Pro case is the most fascinating -- it identified the correct logic in its exceptions list but still chose "walk."

**Visual:** Screenshot collage showing all 9 model responses side by side.

### 3. Accessible Analysis: "What Went Wrong?" (~300 words)
- Most internet text about "walk or drive 100 meters" says walk. The statistical prior overwhelmingly favors "walk."
- The model answers the question it thinks you're asking, not the one you actually asked.
- The car isn't just transport -- it's the object being serviced. Recognizing this requires overriding the pattern match.
- Call out the 5.2 Pro paradox: the reasoning was there, the conclusion wasn't.

### 4. Deeper Layer: "Pre-training vs. Reasoning" (~300 words)
- Tension between pre-training distributions and RL-trained reasoning.
- RL/chain-of-thought should override strong priors when they conflict with logic, but this test shows the override doesn't always work.
- The prior is very strong (almost all "short distance walk or drive" content says walk) and the logical step is subtle (re-interpreting what the "object" in the scenario is).
- Brief speculation on why Gemini swept (training data mix, RLHF tuning for practical/physical reasoning).

### 5. "The Car Wash Test Isn't Alone" (~200 words)
- Place in a family of adversarial reasoning tests:
  - "How many R's in strawberry?" (tokenization blind spot)
  - "Is 9.11 greater than 9.9?" (integer vs. decimal confusion)
- Common thread: trivially easy for humans, but the obvious pattern-match answer is wrong.

### 6. Closing: "Testing the Edges" (~150 words)
- Not about dunking on AI -- about understanding where it breaks.
- Same model that failed this contributed to quantum breakthroughs. These models are powerful but have blind spots.
- Finding edges makes the next generation better.
- End: the best way to trust AI more is to understand precisely where it fails.

## Assets

**Screenshots (from `AI idiocy/` folder):**
- ChatGPT 5.2 Instant: `Screenshot 2026-02-15 at 3.14.47 PM.png`
- ChatGPT 5.2 Thinking (multi-turn): `Screenshot 2026-02-15 at 3.16.15 PM.png`
- ChatGPT 5.2 Thinking (single): `Screenshot 2026-02-15 at 3.16.33 PM.png`
- Gemini 3 Fast: `Screenshot 2026-02-15 at 3.17.51 PM.png`
- ChatGPT 5.2 Pro: `Screenshot 2026-02-15 at 3.19.59 PM.png`
- Claude Haiku 4.5: `Screenshot 2026-02-15 at 3.20.40 PM.png`
- Claude Sonnet 4.5: `Screenshot 2026-02-15 at 3.21.09 PM.png`
- Claude Opus 4.6: `Screenshot 2026-02-15 at 3.21.30 PM.png`
- Gemini 3 Thinking: `Screenshot 2026-02-15 at 3.29.48 PM.png`
- Gemini 3 Pro: `Screenshot 2026-02-15 at 3.30.29 PM.png`
- Screen recording (Gemini): `Screen Recording 2026-02-15 at 3.19.15 PM.mov`

## Tone
- First-person, opinionated, a bit irreverent
- Respectful: AI has blind spots, not "AI is dumb"
- Testing edges to make AI better, not to mock it
- The author genuinely believes in AI's potential to improve humanity
