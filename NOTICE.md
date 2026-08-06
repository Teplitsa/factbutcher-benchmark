[English](NOTICE.md) · [Русский](NOTICE.ru.md)

# Attribution and provenance notice

## Complete dataset

The 423-row FactButcher Russian Fact-Checking Benchmark is available under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

## FactButcher Human Benchmark

The FactButcher project produced 274 benchmark claims through LLM-assisted
extraction from real requests to the FactButcher Telegram product, followed by
filtering, independent fact-checking, adjudication, and human review.

The released claims are benchmark formulations, not user quotations. The
public dataset does not contain raw requests, user IDs, trace IDs, or other
operational identifiers.

## Provereno.Media component

149 claims were adapted from fact-checking articles published by
[Provereno.Media](https://provereno.media/).

Provereno.Media states that its material is available under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Its site rules are
available at [provereno.media/site-rules](https://provereno.media/site-rules/).

Every Provereno.Media row includes:

- `source_name = "Provereno.Media"`;
- the original article in `source_url`;
- `source_license = "CC BY 4.0"`;
- the license link in `source_license_url`.

Changes made by FactButcher include selecting articles, extracting one short
checkable claim, normalizing wording, mapping the published verdict to the
benchmark vocabulary, reviewing the claim and verdict, adding acceptable
alternative verdicts where justified, and packaging the result as an
evaluation dataset.

This use and attribution do not imply that Provereno.Media endorses
FactButcher, the benchmark, or downstream uses of the dataset.
