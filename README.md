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

# FactButcher Russian Fact-Checking Benchmark

A 423-claim Russian-language evaluation dataset for comparing fact-checking
models, prompts, and systems on the same reference labels.

| Benchmark component | What it represents | Rows |
|---|---|---:|
| FactButcher Human Benchmark | Claims derived from real Telegram user requests, then independently checked and reviewed | 274 |
| Provereno.Media | Claims adapted from published professional fact-checks, with links to the original articles | 149 |
| **Complete benchmark** |  | **423** |

The 274 Human Benchmark claims form one dataset component. Requests were
collected over time, but collection history is not part of the public dataset
structure. The claims were extracted with an LLM and edited into
self-contained benchmark statements; they are not presented as user
quotations.

## Start here

Choose the path that matches what you want to do:

| Goal | What to use |
|---|---|
| Read, search, sort, or filter rows | The Dataset Viewer on the Hugging Face dataset page |
| Download data for code or a spreadsheet | [`JSONL`](data/factbutcher_benchmark_v1.jsonl) or [`CSV`](data/factbutcher_benchmark_v1.csv) |
| Understand how claims and labels were produced | [`METHODOLOGY.md`](METHODOLOGY.md) |
| Validate a downloaded copy | `python scripts/validate_dataset.py` |

The JSONL file is the canonical typed version. In the CSV file,
`acceptable_verdicts` uses `|` between multiple accepted labels.

Load a local clone with the Hugging Face `datasets` library:

```python
from datasets import load_dataset

dataset = load_dataset(
    "json",
    data_files={"test": "data/factbutcher_benchmark_v1.jsonl"},
)
print(dataset["test"][0])
```

Or use Python without an extra library:

```python
import json

with open("data/factbutcher_benchmark_v1.jsonl", encoding="utf-8") as file:
    rows = [json.loads(line) for line in file]
```

## Labels

`gold_verdict` is the primary reference label:

- `TRUE`: the central factual claim is supported;
- `FALSE`: the central factual claim is contradicted;
- `MIXED`: substantial parts have different truth values, or reliable evidence
  conflicts on the central point.

`acceptable_verdicts` lists all answers accepted by benchmark scoring. This
prevents a defensible neighboring label from being marked wrong on genuinely
ambiguous claims. The primary label remains available for strict scoring.

`INSUFFICIENT_EVIDENCE` can appear only as an acceptable answer. It is not a
primary gold label.

| Primary verdict | Rows |
|---|---:|
| `TRUE` | 189 |
| `FALSE` | 152 |
| `MIXED` | 82 |

There are 120 claims with more than one acceptable verdict: 99 in the
FactButcher Human Benchmark and 21 in the Provereno.Media component.

## Fields

| Field | Meaning |
|---|---|
| `claim_id` | Stable unique identifier |
| `claim` | Russian-language claim presented for verification |
| `gold_verdict` | Primary reference verdict |
| `acceptable_verdicts` | All verdicts accepted by scoring |
| `benchmark_component` | `factbutcher_human_benchmark` or `provereno_media` |
| `reference_date` | Date against which a time-sensitive claim was evaluated, when available |
| `source_name` | Human-readable provenance |
| `source_url` | Original Provereno.Media article URL; empty for the Human Benchmark |
| `source_license` | License of adapted source material, when applicable |
| `source_license_url` | Link to that source-material license |

The machine-readable field specification is in
[`metadata/schema.json`](metadata/schema.json).

## How to evaluate a system

For every row:

1. send `claim` to the system under test;
2. map its answer to `TRUE`, `FALSE`, `MIXED`, or
   `INSUFFICIENT_EVIDENCE`;
3. count it as correct when the mapped answer appears in
   `acceptable_verdicts`;
4. also report strict accuracy against `gold_verdict`;
5. report whether web search was enabled and whether `provereno.media` was
   available.

Do not train on the test rows and then report the resulting score as a
comparable evaluation. This dataset has a single `test` split.

## Methodology

The Human Benchmark is based on claims people actually brought to
FactButcher. The Provereno.Media component provides cases with published
professional fact-checks and traceable source pages.

Claims and verdicts went through independent checking, adjudication, and final
human review. Some contestable claims accept more than one verdict. See the
full process and limitations in [`METHODOLOGY.md`](METHODOLOGY.md).

The 149 Provereno.Media rows link to 146 distinct article pages; two articles
contribute more than one separate claim.

## Important limitations

- The benchmark is small and contains Russian-language claims.
- It reflects FactButcher requests and selected Provereno.Media coverage, not
  every fact-checking topic.
- Many claims are time-sensitive; use `reference_date` where provided.
- Web-enabled systems may find a Provereno.Media page that contains the
  reference answer. Report access conditions so results remain comparable.
- The dataset provides claims, labels, and Provereno source links. It does not
  provide a complete evidence bundle for every claim.

## Privacy

The dataset contains benchmark claims, not raw Telegram requests. It does not
include user IDs, trace IDs, raw request records, private review files, or raw
model transcripts.

## License and attribution

The dataset is available under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Every Provereno.Media row links to its source article and carries source-license
metadata. [`NOTICE.md`](NOTICE.md) describes attribution and the changes made
when adapting the source material.

## Citation

Use the metadata in [`CITATION.cff`](CITATION.cff).

## Files and reproducibility

- [`data/factbutcher_benchmark_v1.jsonl`](data/factbutcher_benchmark_v1.jsonl)
  — canonical data;
- [`data/factbutcher_benchmark_v1.csv`](data/factbutcher_benchmark_v1.csv)
  — spreadsheet-friendly export;
- [`metadata/schema.json`](metadata/schema.json) — row schema;
- [`metadata/dataset.jsonld`](metadata/dataset.jsonld) — Schema.org dataset
  metadata;
- [`metadata/manifest.json`](metadata/manifest.json) — counts and SHA-256
  checksums.

Validate all rows, both data formats, metadata, attribution fields, and
checksums:

```bash
python scripts/validate_dataset.py
```
