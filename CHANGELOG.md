# Changelog

## Documentation update — 2026-09-30

The data files are unchanged; the dataset version stays 1.0.0.

- Recorded the publication on GitHub and Hugging Face on 2026-08-10 and the
  current Hugging Face address, `teplitsa-soc-tech/factbutcher-benchmark`.
- Rewrote the English and Russian README: a plain-language overview first,
  then a short summary of FactButcher's benchmark results, then instructions
  for running the dataset yourself. Technical details moved to the
  methodology.
- Added `RESULTS.md` and `RESULTS.ru.md`: how FactButcher used the dataset to
  choose a model, the selection stages, the models tested, and the final
  results.
- Methodology: described how the reference verdicts were assigned (two
  language models, a third checker for disagreements; for 100 user-request
  claims a person set the verdict based on those checks, for the other 174 the
  models' verdicts were the main source; final human review) and how
  Provereno.Media verdicts were mapped; added a limitation about
  model-assigned labels; moved the file-validation instructions here from the
  README.

## 1.0.0 — 2026-07-28

- Prepared and locally validated the complete 423-row dataset package; external
  publication is pending.
- Included the 274-row FactButcher Human Benchmark as one public component.
- Included 149 Provereno.Media rows with original article links and
  source-license fields.
- Added matched English and Russian documentation.
- Added JSONL and CSV data, a row schema, Schema.org metadata, a manifest,
  attribution notices, citation metadata, and offline validation.
