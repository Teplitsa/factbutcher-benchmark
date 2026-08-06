[English](METHODOLOGY.md) · [Русский](METHODOLOGY.ru.md)

# Methodology

## Why a correct verdict is not enough

FactButcher checks factual claims with AI. A useful fact-check needs a
defensible verdict, sources that a reader can open, and an explanation that
connects the evidence to the conclusion.

This dataset provides the stable part needed for comparison: the same claims
and human-reviewed reference labels for every system. A benchmark run can then
measure verdict accuracy and, when model responses are retained, evaluate
source quality and reasoning separately.

## Dataset design

The complete benchmark contains 423 Russian-language claims in two
complementary components.

| Component | Purpose | Rows |
|---|---|---:|
| FactButcher Human Benchmark | Test systems on the kinds of claims people actually bring to the product | 274 |
| Provereno.Media | Add cases with a published professional verdict and explanation | 149 |

### FactButcher Human Benchmark

The Human Benchmark is one set of 274 claims derived from real requests sent
to the FactButcher Telegram product. Requests were collected over more than
one period so that the benchmark would cover a broader range of actual use.
Those collection periods are not separate public datasets or benchmark
components.

The source requests were used to produce short, self-contained factual claims:

1. an LLM extracted candidate claims from the requests;
2. non-factual, subjective, predictive, test, incomplete, duplicated, or
   impractically broad candidates were removed;
3. necessary context such as date or location was restored when it was
   available in the request;
4. each retained claim was checked independently with web search;
5. disagreements were adjudicated;
6. wording and reference labels received final human review.

The published claims are benchmark formulations. They are not presented as
verbatim quotations from users. The public files do not contain the raw
requests or operational identifiers.

This component keeps the benchmark close to the product’s real audience. It
reduces the risk of measuring only cases selected by researchers or
professional fact-checking editors.

### Provereno.Media

Provereno.Media is a professional Russian-language fact-checking publication.
Its articles provide both a published verdict and a detailed explanation of
how that verdict was reached.

For the benchmark:

1. one short, self-contained factual claim was selected for each benchmark
   row; most articles contribute one row, while two articles contribute
   several separate claims;
2. cases that depended on unavailable images, videos, or tables were excluded;
3. article verdicts were mapped to the benchmark label vocabulary;
4. claim wording and label mapping were independently reviewed;
5. disagreements were adjudicated and the final rows received human review.

Every Provereno.Media row links to its original article. The 149 rows point to
146 distinct article pages because two articles cover several separate claims.
The dataset does not reproduce article text or present Provereno.Media’s
reporting as FactButcher’s work.

## Reference labels

The primary label is stored in `gold_verdict`:

- `TRUE`: the central factual claim is supported;
- `FALSE`: the central factual claim is contradicted;
- `MIXED`: substantial parts have different truth values, or reliable evidence
  conflicts on the central point.

Some claims honestly allow two neighboring answers. For those cases,
`acceptable_verdicts` records every answer accepted by scoring. The primary
label remains available for strict comparisons.

The complete dataset contains:

- 189 `TRUE` primary labels;
- 152 `FALSE` primary labels;
- 82 `MIXED` primary labels;
- 120 claims with multiple acceptable verdicts:
  - 99 in the FactButcher Human Benchmark;
  - 21 in the Provereno.Media component.

`INSUFFICIENT_EVIDENCE` is not a primary gold class. It can appear as an
acceptable model answer when the available evidence does not justify a firmer
conclusion.

## What can be measured

The dataset directly supports two verdict metrics:

- **acceptable accuracy:** the model answer appears in
  `acceptable_verdicts`;
- **strict accuracy:** the model answer equals `gold_verdict`.

When a tested system also returns sources and an explanation, evaluators can
add separate checks:

| Check | Question |
|---|---|
| Source availability | Do the cited pages open? |
| Evidence support | Do those pages support the answer’s important factual statements? |
| Reasoning | Does the explanation lead logically from the evidence to the verdict? |
| Professional comparison | On Provereno.Media cases, does the answer follow the published reasoning or find another defensible route? |

Cost and latency should be reported separately. They are not evidence that a
verdict is more accurate.

## Web-search conditions

A web-enabled system may find a Provereno.Media page containing the
professional answer. This does not invalidate the row, but it changes what the
evaluation demonstrates.

Results should therefore state:

- whether web search was enabled;
- whether `provereno.media` was accessible;
- whether source and reasoning quality were evaluated in addition to verdict
  accuracy.

For a stronger independence check, run Provereno.Media rows both with ordinary
search access and with that domain excluded.

## Privacy and data minimization

The public dataset contains derived benchmark claims, not raw Telegram
requests. It excludes user IDs, trace IDs, raw request records, private review
files, and raw model transcripts.

The Human Benchmark has no per-row private source URLs. Provereno.Media rows
contain only public article URLs and source-license information.

## Known limitations

- The dataset is relatively small and Russian-language.
- It reflects FactButcher requests and selected Provereno.Media coverage, not
  every fact-checking topic.
- Topic and verdict distributions are natural rather than artificially
  balanced.
- Some claims are time-sensitive. `reference_date` records the evaluation date
  when available.
- Human-reviewed labels can still be contestable. Multiple accepted labels make
  some, but not all, ambiguity visible.
- Public source pages can change or become unavailable.
- The files provide claims, labels, and Provereno.Media links, not a complete
  evidence package for every row.

## Reproducible export

The public JSONL and CSV are generated deterministically from the frozen
canonical benchmark files. Internal file layout and collection history do not
become public dataset categories.

The build:

1. combines all final benchmark rows;
2. maps the Human Benchmark to one public component;
3. joins each Provereno.Media claim to its original article URL;
4. normalizes accepted verdicts into typed arrays;
5. writes stable component-and-ID order;
6. generates the row schema, manifest, checksums, and Schema.org metadata.

The offline validator checks 423 unique IDs, the 274/149 component totals,
label counts, Provereno.Media attribution, JSONL/CSV equality, row schema,
metadata, and SHA-256 checksums.
