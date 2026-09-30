---
language:
  - ru
license: cc-by-4.0
pretty_name: FactButcher Russian Fact-Checking Benchmark
size_categories:
  - n<1K
task_categories:
  - text-classification
tags:
  - fact-checking
  - claim-verification
  - benchmark
  - russian
  - evaluation
  - text
  - tabular
  - datasets
  - mlcroissant
configs:
  - config_name: default
    data_files:
      - split: test
        path: data/factbutcher_benchmark_v1.jsonl
---

[English](README.md) · [Русский](README.ru.md)

# FactButcher Russian Fact-Checking Dataset

423 claims in Russian, each with a reference verdict: true, false, or partly
true. Use it to test how well a model, a prompt, or a service checks facts:
give it the same claims and compare its answers with the reference ones.

We built the dataset to choose a model and settings for
[FactButcher.com](https://factbutcher.com), an AI fact-checking service. What
that comparison showed is described below.

## Examples

| Claim | Verdict | Origin |
|---|---|---|
| Слоны боятся мышей *(Elephants are afraid of mice)* | False | Request from a FactButcher user |
| На западе Китая в чай кладут соль *(In western China, people put salt in tea)* | True | Request from a FactButcher user |
| Микеланджело говорил, что берет глыбу мрамора и отсекает от нее все лишнее. *(Michelangelo said he takes a block of marble and cuts away everything unnecessary.)* | False | [Provereno.Media](https://provereno.media/blog/2026/05/24/govoril-li-mikelandzhelo-chto-beryot-glybu-mramora-i-otsekaet-ot-neyo-vsyo-lishnee/) |

All claims are in the [CSV table](data/factbutcher_benchmark_v1.csv). You can
open it in a browser or in Excel, Google Sheets, or LibreOffice. To check a
claim yourself before seeing the answer, hide the answer columns:
`gold_verdict` and `acceptable_verdicts`.

## Where the claims come from and who assigned the verdicts

| Source | Claims | Who assigned the reference verdict |
|---|---:|---|
| Requests to the FactButcher Telegram bot | 274 | For 100 claims, a person assigned the verdict based on the language models' checks. For the other 174, the models mostly assigned the verdict: two checked each claim independently with web search, and when they disagreed, a third checker resolved it. A person reviewed the final wording and verdicts |
| [Provereno.Media](https://provereno.media) articles | 149 | Provereno.Media's professional fact-checkers. We mapped their verdict to the dataset's scale and double-checked the mapping |

Claims from user requests are not verbatim: we took the checkable statement
out of the request and, when needed, added context from the same request, such
as a date or place. The dataset contains no original messages and no data
about users. Every Provereno.Media claim links to the published fact-check.

Collection and labeling are described in detail in
[`METHODOLOGY.md`](METHODOLOGY.md).

## How the verdicts work

- **True** (`TRUE`): the claim is supported.
- **False** (`FALSE`): the claim is contradicted.
- **Partly true** (`MIXED`): important parts of the claim differ in
  truthfulness, or reliable sources do not give one clear answer.

For some claims, two neighboring verdicts can both be honestly defended, for
example "false" and "partly true". The main verdict is then in
`gold_verdict`, and all accepted ones are in `acceptable_verdicts`. "Not
enough evidence" (`INSUFFICIENT_EVIDENCE`) can be an accepted answer but is
never the main verdict.

## What our benchmark showed

In July 2026 we ran models from OpenAI, Anthropic, Google, and Perplexity
through the dataset with different settings. Each model received one claim per
request, searched the web itself, and returned a verdict, a short explanation,
and links.

Selection had three stages: 15 configurations on 10 claims, then 9 on 100, and
5 finalists on all 423. A configuration here means a model together with its
settings: how deeply it reasons and how much it searches the web.

| Finalist | Share of accepted answers |
|---|---:|
| OpenAI GPT-5.4-mini, tuned settings | 81.6% |
| Perplexity Sonar Reasoning Pro | 80.6% |
| Anthropic Claude Haiku 4.5 | 79.9% |
| OpenAI GPT-5.6 Luna | 78.7% |
| OpenAI GPT-5.4-mini, default settings (how FactButcher ran during the test) | 72.8% |

- The difference between the top three is not statistically significant;
  there is no clear winner.
- Settings mattered more than the choice of model: the same GPT-5.4-mini with
  tuned settings answered correctly almost 9 percentage points more often than
  with default ones.
- Google Gemini models were dropped: they barely searched the web and cited
  made-up sources.

How we scored, which models were dropped and why, and what one check costs are
in [`RESULTS.md`](RESULTS.md).

## Run the dataset yourself

1. **Load the data.** Download the
   [CSV](data/factbutcher_benchmark_v1.csv) or
   [JSONL](data/factbutcher_benchmark_v1.jsonl) file, or load it with the
   Hugging Face `datasets` library:

   ```python
   from datasets import load_dataset

   rows = load_dataset("teplitsa-soc-tech/factbutcher-benchmark", split="test")
   ```

2. **Send each claim** from the `claim` field to the model or service you are
   testing. Save the answer together with `claim_id`.
3. **Map the answers to four labels:** `TRUE`, `FALSE`, `MIXED`,
   `INSUFFICIENT_EVIDENCE`.
4. **Score the result in two ways:**
   - *accepted answers*: the share of rows where the answer is in
     `acceptable_verdicts` (our numbers above are computed this way);
   - *strict*: the share of rows where the answer equals `gold_verdict`.

   Count rows the system did not answer as errors.

To make your result comparable with ours, run all 423 rows under the same
conditions and report the model, prompt, and search settings. Also report
whether provereno.media was reachable: a system with web search may find the
published fact-check there. In our final numbers, Provereno.Media claims for
which the models visited that site were re-run with the site blocked.

The dataset has one split, `test`. Do not use these rows to train or tune a
system and then publish its result as an independent evaluation.

## Fields

| Field | Contents |
|---|---|
| `claim_id` | Unique claim identifier |
| `claim` | Claim to check |
| `gold_verdict` | Main reference verdict |
| `acceptable_verdicts` | All verdicts counted as correct. In the CSV they are separated by a vertical bar; in the JSONL this is a list |
| `benchmark_component` | Source: `factbutcher_human_benchmark` (user requests) or `provereno_media` |
| `reference_date` | Date the verdict applies to, when the claim depends on time |
| `source_name` | Name of the row's source |
| `source_url` | Provereno.Media article link; empty for user requests |
| `source_license` | License of the source material, when applicable |
| `source_license_url` | Link to that license |

The full machine-readable field specification is in
[`metadata/schema.json`](metadata/schema.json).

## Limitations

- The collection is small and Russian-only. Topics are whatever FactButcher
  users brought and Provereno.Media covered; they were not balanced.
- Some claims depend on time; `reference_date` shows the date the verdict
  applies to.
- A reference verdict can still be contestable. `acceptable_verdicts` captures
  only part of that ambiguity.
- Reference verdicts for user requests rely heavily on language models.
  Mistakes shared by those models and a tested model may go unnoticed.
- Claims from user requests have no written fact-check and no complete list of
  sources.

Other limitations are listed in [`METHODOLOGY.md`](METHODOLOGY.md).

## License and citation

The dataset is available under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
Provereno.Media rows link to the original articles; see
[`NOTICE.md`](NOTICE.md) for details. Citation metadata is in
[`CITATION.cff`](CITATION.cff).
