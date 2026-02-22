# The Car Wash Test

**Summary:** Which frontier AI models can figure out that you need to drive your car to the car wash?

## Data Sources

- Direct testing of 9 model configurations across OpenAI, Google, and Anthropic (February 2026)
- Screenshots of each model's response

## Methodology

Same prompt ("I need to wash my car. The car wash is only 100 meters away. Should I walk or take my car there?"), clean session, no priming, first-shot evaluation across:
- OpenAI: ChatGPT 5.2 Instant, Thinking, Pro
- Google: Gemini 3 Fast, Thinking, Pro
- Anthropic: Claude Haiku 4.5, Sonnet 4.5, Opus 4.6

## Key Findings

- OpenAI: 0/3 passed (all recommend walking, even after 2m 45s of reasoning)
- Google: 3/3 passed (all correctly identify the car must be present)
- Anthropic: 2/3 passed (Haiku fails, Sonnet and Opus pass)
