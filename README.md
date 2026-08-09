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

This dataset contains 423 claims in Russian and the results of checking them.
Some claims are true, some are false, and some allow more than one defensible
answer.

You can see what kinds of claims people bring to fact-checkers, investigate a
few of them yourself, or use the complete collection to compare different
fact-checking tools.

## A few examples

| Claim | Result | Origin |
|---|---|---|
| Слоны боятся мышей | False (`FALSE`) | Request to FactButcher |
| На западе Китая в чай кладут соль | True (`TRUE`) | Request to FactButcher |
| Микеланджело говорил, что берет глыбу мрамора и отсекает от нее все лишнее. | False (`FALSE`) | [Provereno.Media](https://provereno.media/blog/2026/05/24/govoril-li-mikelandzhelo-chto-beryot-glybu-mramora-i-otsekaet-ot-neyo-vsyo-lishnee/) |

These are actual rows from the dataset. In the data files, the statement is
stored in `claim` and its main reviewed result is stored in `gold_verdict`.

## View all claims

Open the [`CSV file`](data/factbutcher_benchmark_v1.csv) in your browser, or
download it and use Excel, Google Sheets, LibreOffice, or another spreadsheet
program. Each row contains one claim and the result of checking it.

If you want to investigate a claim before seeing the answer, hide the
`gold_verdict` and `acceptable_verdicts` columns. Provereno.Media rows include
a published fact-check in `source_url`. For claims that depend on time,
`reference_date` shows the date against which the verdict was assigned.

## Where the data came from

The dataset has two parts:

| Part | Contents | Rows |
|---|---|---:|
| FactButcher Human Benchmark | Claims taken from real requests to the FactButcher Telegram product | 274 |
| Provereno.Media | Claims taken from published professional fact-checks | 149 |
| **Total** |  | **423** |

An LLM was used to extract factual claims from the FactButcher requests. The
claims were then edited into short, self-contained statements, checked, and
reviewed by a person. The published statements are not verbatim user messages;
the original messages are not included in the dataset.

The Provereno.Media rows were adapted from published articles. Each row links
to the original fact-check. The 149 rows point to 146 pages because two
articles contribute more than one separate claim.

The collection, checking, and labeling process is described in
[`METHODOLOGY.md`](METHODOLOGY.md).

## Test a model or service

You can use the dataset as a shared collection of questions with reviewed
answers. To do this:

1. send each `claim` to the model, service, or fact-checking script you want
   to test;
2. save its verdict together with the corresponding `claim_id`;
3. map the answers to `TRUE`, `FALSE`, `MIXED`, or
   `INSUFFICIENT_EVIDENCE`;
4. compare them with the reference answers in the dataset.

How claims are sent depends on the tool you choose. An API-based tool will
require its own small connecting script and access settings. This repository
contains the claims and reference answers.

For a comparable result, run all 423 rows under the same conditions and report
the model, prompt, and web-search settings. Also state whether
`provereno.media` was accessible: a tool with web search may find the
published fact-check there.

The dataset has one split, `test`. Do not use these rows to train or tune a
system and then publish its result as an independent evaluation.

## How the verdicts work

`gold_verdict` is the main reviewed result:

- `TRUE` — the claim is supported;
- `FALSE` — the claim is contradicted;
- `MIXED` — important parts of the claim have different truth values, or
  reliable sources do not support one unambiguous answer.

In some cases, two neighboring verdicts are defensible. They are listed in
`acceptable_verdicts`. This supports two ways of scoring results:

- **acceptable accuracy:** the system's answer appears in
  `acceptable_verdicts`;
- **strict accuracy:** the system's answer equals `gold_verdict`.

`INSUFFICIENT_EVIDENCE` can appear among the accepted answers, but it is not
used as the main verdict.

| Main verdict | Rows |
|---|---:|
| `TRUE` | 189 |
| `FALSE` | 152 |
| `MIXED` | 82 |

There are 120 rows with more than one accepted verdict.

## Data files

- [`data/factbutcher_benchmark_v1.csv`](data/factbutcher_benchmark_v1.csv) is
  intended for spreadsheets. Multiple accepted verdicts are separated by
  `|`.
- [`data/factbutcher_benchmark_v1.jsonl`](data/factbutcher_benchmark_v1.jsonl)
  is the main typed version for software. Each line contains one JSON object.

Load the JSONL file with standard Python:

```python
import json

with open("data/factbutcher_benchmark_v1.jsonl", encoding="utf-8") as file:
    rows = [json.loads(line) for line in file]
```

Or use the Hugging Face `datasets` library:

```python
from datasets import load_dataset

dataset = load_dataset(
    "json",
    data_files={"test": "data/factbutcher_benchmark_v1.jsonl"},
)
```

## Fields

| Field | Contents |
|---|---|
| `claim_id` | Unique identifier for the claim |
| `claim` | Claim to be checked |
| `gold_verdict` | Main reviewed verdict |
| `acceptable_verdicts` | All verdicts accepted when scoring the row |
| `benchmark_component` | Human Benchmark or Provereno.Media part |
| `reference_date` | Evaluation date for a time-sensitive claim, when known |
| `source_name` | Origin of the row |
| `source_url` | Provereno.Media article; empty for the Human Benchmark |
| `source_license` | License of adapted source material, when applicable |
| `source_license_url` | Link to the source-material license |

The full machine-readable field specification is in
[`metadata/schema.json`](metadata/schema.json).

## Limitations

- This is a relatively small Russian-language collection.
- It reflects FactButcher requests and selected Provereno.Media coverage, not
  every possible fact-checking topic.
- Topics and verdicts occur naturally rather than in equal proportions.
- Some claims depend on time.
- Even a human-reviewed verdict can be contestable. Multiple accepted labels
  represent some, but not all, ambiguity.
- Human Benchmark rows do not include a complete evidence bundle or written
  fact-check. Provereno.Media rows link to the published article.

## Privacy

The dataset does not contain original Telegram messages, user identifiers, or
private FactButcher operational data. It publishes only the prepared claims
and the fields needed to use them.

## License and citation

The dataset is available under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Every Provereno.Media row links to its original article and includes source
license information. See [`NOTICE.md`](NOTICE.md) for details. Citation
metadata is available in [`CITATION.cff`](CITATION.cff).

## File validation

This command is intended for maintainers and people who mirror or repackage
the dataset. It checks that the data, metadata, and checksums agree. You do not
need to run it simply to browse the dataset.

```bash
python scripts/validate_dataset.py
```
