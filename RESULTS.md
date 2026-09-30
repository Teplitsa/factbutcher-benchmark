[English](RESULTS.md) · [Русский](RESULTS.ru.md)

# How FactButcher used the dataset: benchmark results

In July 2026 we used this dataset to choose a model and settings for fact-checking
in [FactButcher.com](https://factbutcher.com). This page describes what we
compared, how, and what we found.

## What we compared

The check is simple: one request to the model per claim. The model searches
the web itself and returns a verdict, a short explanation, and links to
sources. Every model got the same prompt. We did not compare multi-step
fact-checking systems.

A configuration is a model together with two settings:

- **reasoning**: how much the model "thinks" before answering (off, low,
  medium, high);
- **search**: for OpenAI, the amount of retrieved web text the model receives
  (narrow, medium, wide); for Anthropic, a cap on the number of searches per
  claim. Google and Perplexity build search into the model, and it can barely
  be configured.

One model can appear in several configurations.

Price limit: we aimed for no more than $0.05 per check and dropped
configurations above $0.10 right away.

## How we selected

| Stage | Claims | Configurations | What we looked at |
|---|---:|---:|---|
| Short test | 10 | 15 | Price of one check |
| Mid test | 100 | 9 | Price and quality together |
| Finals | 423 | 5 | Share of accepted answers and explanation quality |

After the finals we checked for answer leakage. While checking, the finalists
visited provereno.media, so they could simply read the published fact-check.
We re-ran the Provereno.Media claims where this happened with that site
blocked. First place did not change; second and third swapped. All numbers
below are after this correction.

Outside the main selection:

- GPT-5.6 Luna arrived later. It was run on the same 100 mid-test claims and
  made it to the finals.
- Claude Sonnet 5 was run as a control, directly on 100 claims. It did not
  beat the cheaper finalists.
- GPT-5.4, GPT-5.5, and Claude Sonnet 4.6 were tried briefly. All three cost
  more than $0.10 per check.

## Models we tested

| Company | Models (API identifier) | Furthest stage |
|---|---|---|
| OpenAI | GPT-5.4-mini (`gpt-5.4-mini`), GPT-5.6 Luna (`gpt-5.6-luna`), GPT-5.4 (`gpt-5.4`), GPT-5.5 (`gpt-5.5`) | GPT-5.4-mini and GPT-5.6 Luna: finals |
| Anthropic | Claude Haiku 4.5 (`claude-haiku-4-5`), Claude Sonnet 5 (`claude-sonnet-5`), Claude Sonnet 4.6 (`claude-sonnet-4-6`) | Claude Haiku 4.5: finals |
| Google | Gemini Flash (`gemini-3.5-flash`), Gemini Pro (`gemini-3.1-pro-preview`), Gemini Flash Lite (`gemini-3.1-flash-lite`) | Gemini Flash and Gemini Pro: mid test |
| Perplexity | Sonar Reasoning Pro (`sonar-reasoning-pro`), Sonar Pro (`sonar-pro`), Sonar (`sonar`) | Sonar Reasoning Pro: finals |

## Final results

| Configuration | Accepted answers | Verdict follows from explanation | Price per check |
|---|---:|---:|---:|
| GPT-5.4-mini: low reasoning, narrow search | 81.6% | 83.2% | $0.072 |
| Sonar Reasoning Pro: built-in reasoning, deep search | 80.6% | 92.7% | $0.028 |
| Claude Haiku 4.5: reasoning on, up to 2 searches | 79.9% | 85.1% | $0.054 |
| GPT-5.6 Luna: low reasoning, medium search | 78.7% | 92.2% | $0.046 ¹ |
| GPT-5.4-mini: default settings (no reasoning, medium search); how FactButcher ran during the test | 72.8% | 79.7% | $0.022 |

- **Accepted answers**: the share of the 423 claims where the model's answer
  is in `acceptable_verdicts`.
- **Verdict follows from explanation**: the share of answers where the verdict
  logically follows from the model's own explanation. A separate language
  model (OpenAI GPT-5.6 Sol) graded this without seeing which model answered or
  the reference verdict. Computed over 423 answers per model.
- **Price**: one check in the short test, one request at a time, at July 2026
  rates. ¹ For GPT-5.6 Luna the price was measured in the mid test.

## What this means

1. **There is no clear winner.** The difference between the top three in
   accepted answers is not statistically significant (paired test). Choosing
   among them depends on price and on how much the explanations matter.
2. **Settings mattered more than the model.** The best result and FactButcher's
   default configuration use the same model, GPT-5.4-mini. Low reasoning and
   narrow search added 8.8 percentage points (81.6% against 72.8%).
3. **Sonar Reasoning Pro is the cheapest of the top three**, and its verdict
   follows from its explanation most often. But about 11% of the links in its
   answers did not open.
4. **GPT-5.6 Luna is cautious.** It rarely confuses "true" with "false";
   almost all of its errors are "partly true" or "not enough evidence" answers
   where the reference verdict is definite.
5. **Only one explanation check clearly separates the models**: whether the
   verdict follows from the explanation. Other checks, such as whether the
   model's reasoning matches the Provereno.Media fact-check, do not tell the
   models apart.

## Why Google Gemini models were dropped

In the mid test, Gemini Flash and Gemini Pro had a high share of correct
verdicts, but they barely used search. Gemini Flash actually searched the web
in only 9 answers out of 100 and cited made-up sources in the rest. That does
not work for FactButcher: users must be able to open a link and check for
themselves.

We tried requiring search explicitly in the instructions. Real searches
dropped to zero, and the model started faking link addresses.

After it was dropped, we ran Gemini Flash separately on all 423 claims. That
result cannot be placed next to the finalists: it was not re-run with
provereno.media blocked.

## Caveats

- All numbers come from one prompt and one check design (one request per
  claim). A different prompt may give different results. Our prompt is not
  published yet, so these numbers are a reference point, not a result you can
  reproduce exactly.
- Prices are at July 2026 rates and may have changed since.
- For 174 claims from user requests, the reference verdicts were mostly
  assigned by language models; for the other 100, a person relied on their
  checks (see [`METHODOLOGY.md`](METHODOLOGY.md)).
  Mistakes shared by those models and a tested model may go unnoticed.
