#!/usr/bin/env python3
"""Offline validation for the public FactButcher dataset package."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
JSONL_PATH = ROOT / "data" / "factbutcher_benchmark_v1.jsonl"
CSV_PATH = ROOT / "data" / "factbutcher_benchmark_v1.csv"
SCHEMA_PATH = ROOT / "metadata" / "schema.json"
MANIFEST_PATH = ROOT / "metadata" / "manifest.json"
JSONLD_PATH = ROOT / "metadata" / "dataset.jsonld"
CONFIG_PATH = ROOT / "metadata" / "release_config.json"

EXPECTED = {
    "rows": 423,
    "benchmark_components": {
        "factbutcher_human_benchmark": 274,
        "provereno_media": 149,
    },
    "primary_verdicts": {"FALSE": 152, "MIXED": 82, "TRUE": 189},
    "multiple_acceptable": 120,
    "human_benchmark_multiple_acceptable": 99,
    "provereno_urls": 149,
    "unique_provereno_urls": 146,
    "dated_rows": 323,
}

NULLABLE_FIELDS = [
    "reference_date",
    "source_url",
    "source_license",
    "source_license_url",
]

REQUIRED_PACKAGE_FILES = [
    "README.md",
    "README.ru.md",
    "METHODOLOGY.md",
    "METHODOLOGY.ru.md",
    "LICENSE",
    "NOTICE.md",
    "NOTICE.ru.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "requirements-validation.txt",
    "data/factbutcher_benchmark_v1.jsonl",
    "data/factbutcher_benchmark_v1.csv",
    "metadata/release_config.json",
    "metadata/schema.json",
    "metadata/manifest.json",
    "metadata/dataset.jsonld",
    "scripts/validate_dataset.py",
]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_number}: {exc}") from exc
    return rows


def _read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    decoded: list[dict[str, Any]] = []
    for row in rows:
        item: dict[str, Any] = dict(row)
        item["acceptable_verdicts"] = [
            part.strip()
            for part in item["acceptable_verdicts"].split("|")
            if part.strip()
        ]
        for field in NULLABLE_FIELDS:
            item[field] = item[field] or None
        decoded.append(item)
    return decoded


def _load_readme_metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("README.md has no Hugging Face YAML front matter")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("README.md YAML front matter is not an object")
    return metadata


def _add_if(condition: bool, message: str, target: list[str]) -> None:
    if condition:
        target.append(message)


def validate() -> list[str]:
    errors: list[str] = []

    missing = [path for path in REQUIRED_PACKAGE_FILES if not (ROOT / path).is_file()]
    if missing:
        return [f"Missing package files: {missing}"]

    try:
        rows = _read_jsonl(JSONL_PATH)
        csv_rows = _read_csv_rows(CSV_PATH)
        schema = _read_json(SCHEMA_PATH)
        manifest = _read_json(MANIFEST_PATH)
        jsonld = _read_json(JSONLD_PATH)
        config = _read_json(CONFIG_PATH)
        readme_metadata = _load_readme_metadata(ROOT / "README.md")
        citation_metadata = yaml.safe_load(
            (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        )
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return [str(exc)]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for index, row in enumerate(rows):
        for validation_error in validator.iter_errors(row):
            location = ".".join(str(part) for part in validation_error.path)
            errors.append(
                f"JSONL row {index + 1} schema error at {location or '<row>'}: "
                f"{validation_error.message}"
            )

    _add_if(
        len(rows) != EXPECTED["rows"],
        f"Expected 423 JSONL rows, got {len(rows)}",
        errors,
    )
    _add_if(
        len(csv_rows) != EXPECTED["rows"],
        f"Expected 423 CSV rows, got {len(csv_rows)}",
        errors,
    )
    _add_if(
        rows != csv_rows,
        "Parsed JSONL and CSV rows differ; list or Unicode round-trip failed",
        errors,
    )

    claim_ids = [row.get("claim_id") for row in rows]
    _add_if(
        len(set(claim_ids)) != len(claim_ids),
        "claim_id values are not unique",
        errors,
    )

    component_counts = dict(
        sorted(Counter(row["benchmark_component"] for row in rows).items())
    )
    verdict_counts = dict(
        sorted(Counter(row["gold_verdict"] for row in rows).items())
    )
    multiple_acceptable = sum(len(row["acceptable_verdicts"]) > 1 for row in rows)
    human_multiple = sum(
        row["benchmark_component"] == "factbutcher_human_benchmark"
        and len(row["acceptable_verdicts"]) > 1
        for row in rows
    )
    provereno_urls = sum(
        row["benchmark_component"] == "provereno_media" and bool(row["source_url"])
        for row in rows
    )
    unique_provereno_urls = len(
        {
            row["source_url"]
            for row in rows
            if row["benchmark_component"] == "provereno_media"
            and row["source_url"]
        }
    )
    dated_rows = sum(bool(row["reference_date"]) for row in rows)

    _add_if(
        component_counts != EXPECTED["benchmark_components"],
        f"Benchmark-component counts changed: {component_counts}",
        errors,
    )
    _add_if(
        verdict_counts != EXPECTED["primary_verdicts"],
        f"Primary-verdict counts changed: {verdict_counts}",
        errors,
    )
    _add_if(
        multiple_acceptable != EXPECTED["multiple_acceptable"],
        f"Expected 120 multi-acceptable rows, got {multiple_acceptable}",
        errors,
    )
    _add_if(
        human_multiple != EXPECTED["human_benchmark_multiple_acceptable"],
        f"Expected 99 Human Benchmark multi-acceptable rows, got {human_multiple}",
        errors,
    )
    _add_if(
        provereno_urls != EXPECTED["provereno_urls"],
        f"Expected 149 Provereno URLs, got {provereno_urls}",
        errors,
    )
    _add_if(
        unique_provereno_urls != EXPECTED["unique_provereno_urls"],
        f"Expected 146 unique Provereno URLs, got {unique_provereno_urls}",
        errors,
    )
    _add_if(
        dated_rows != EXPECTED["dated_rows"],
        f"Expected 323 dated rows, got {dated_rows}",
        errors,
    )

    allowed_acceptable = {"TRUE", "FALSE", "MIXED", "INSUFFICIENT_EVIDENCE"}
    for row in rows:
        if row["gold_verdict"] not in row["acceptable_verdicts"]:
            errors.append(
                f"{row['claim_id']}: primary verdict missing from acceptable_verdicts"
            )
        unknown = set(row["acceptable_verdicts"]) - allowed_acceptable
        if unknown:
            errors.append(f"{row['claim_id']}: unsupported accepted labels {unknown}")

        component = row["benchmark_component"]
        if component == "factbutcher_human_benchmark":
            _add_if(
                row["source_name"] != "FactButcher Human Benchmark",
                f"{row['claim_id']}: Human Benchmark row has wrong source name",
                errors,
            )
            _add_if(
                any(
                    row[field] is not None
                    for field in [
                        "source_url",
                        "source_license",
                        "source_license_url",
                    ]
                ),
                f"{row['claim_id']}: Human Benchmark row exposes source metadata",
                errors,
            )
        elif component == "provereno_media":
            _add_if(
                row["source_name"] != "Provereno.Media",
                f"{row['claim_id']}: Provereno row has wrong source name",
                errors,
            )
            _add_if(
                not str(row["source_url"] or "").startswith(
                    "https://provereno.media/"
                ),
                f"{row['claim_id']}: invalid Provereno source URL",
                errors,
            )
            _add_if(
                row["source_license"] != "CC BY 4.0"
                or row["source_license_url"]
                != "https://creativecommons.org/licenses/by/4.0/",
                f"{row['claim_id']}: missing Provereno CC BY 4.0 attribution",
                errors,
            )

    expected_stats = {
        "rows": len(rows),
        "unique_claim_ids": len(set(claim_ids)),
        "benchmark_components": component_counts,
        "primary_verdicts": verdict_counts,
        "rows_with_multiple_acceptable_verdicts": multiple_acceptable,
        "human_benchmark_rows_with_multiple_acceptable_verdicts": human_multiple,
        "provereno_rows_with_source_url": provereno_urls,
        "unique_provereno_source_urls": unique_provereno_urls,
    }
    _add_if(
        manifest.get("stats") != expected_stats,
        "manifest.json stats do not match parsed data",
        errors,
    )

    manifest_files = {
        item["path"]: item for item in manifest.get("files", []) if "path" in item
    }
    for relative_path, item in manifest_files.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"Manifest file is missing: {relative_path}")
            continue
        _add_if(
            path.stat().st_size != item.get("bytes"),
            f"Manifest byte count differs for {relative_path}",
            errors,
        )
        _add_if(
            _sha256(path) != item.get("sha256"),
            f"Manifest SHA-256 differs for {relative_path}",
            errors,
        )

    _add_if(
        jsonld.get("@context") != "https://schema.org/"
        or jsonld.get("@type") != "Dataset",
        "dataset.jsonld must be a Schema.org Dataset",
        errors,
    )
    required_jsonld = {
        "name",
        "description",
        "url",
        "version",
        "creator",
        "publisher",
        "license",
        "inLanguage",
        "distribution",
    }
    _add_if(
        not required_jsonld.issubset(jsonld),
        "dataset.jsonld is missing required fields: "
        f"{sorted(required_jsonld - set(jsonld))}",
        errors,
    )

    data_manifest = {
        path: manifest_files[path]
        for path in [
            "data/factbutcher_benchmark_v1.jsonl",
            "data/factbutcher_benchmark_v1.csv",
        ]
        if path in manifest_files
    }
    distribution_by_name = {
        item.get("name"): item for item in jsonld.get("distribution", [])
    }
    for relative_path, distribution_name in [
        (
            "data/factbutcher_benchmark_v1.jsonl",
            "FactButcher benchmark JSONL",
        ),
        ("data/factbutcher_benchmark_v1.csv", "FactButcher benchmark CSV"),
    ]:
        distribution = distribution_by_name.get(distribution_name)
        if distribution is None:
            errors.append(f"dataset.jsonld lacks {distribution_name}")
            continue
        _add_if(
            distribution.get("@type") != "DataDownload",
            f"{distribution_name} is not a DataDownload",
            errors,
        )
        if relative_path in data_manifest:
            _add_if(
                distribution.get("sha256")
                != data_manifest[relative_path].get("sha256"),
                f"{distribution_name} SHA-256 differs from manifest",
                errors,
            )

    expected_hf_config = [
        {
            "config_name": "default",
            "data_files": [
                {
                    "split": "test",
                    "path": "data/factbutcher_benchmark_v1.jsonl",
                }
            ],
        }
    ]
    _add_if(
        readme_metadata.get("language") != ["ru"],
        "README Hugging Face metadata must declare dataset language ru",
        errors,
    )
    _add_if(
        readme_metadata.get("license") != "cc-by-4.0",
        "README Hugging Face metadata must declare cc-by-4.0",
        errors,
    )
    _add_if(
        readme_metadata.get("configs") != expected_hf_config,
        "README Hugging Face default/test configuration is incorrect",
        errors,
    )
    _add_if(
        citation_metadata.get("license") != "CC-BY-4.0",
        "CITATION.cff must declare CC-BY-4.0",
        errors,
    )

    expected_schema_id = (
        f"{config['github_url']}/blob/main/metadata/schema.json"
        if config.get("github_url")
        else "./schema.json"
    )
    _add_if(
        schema.get("$id") != expected_schema_id,
        "schema.json $id does not match release_config.json",
        errors,
    )

    forbidden_public_terms = [
        "construction_batch",
        "origin_family",
        "human_benchmark_original",
        "human_benchmark_expansion",
        "TO-BE-CONFIRMED",
        "TO BE CONFIRMED",
        "1.0.0-draft",
        "Local publication preview",
        "After publication",
    ]
    public_text_files = [
        "README.md",
        "README.ru.md",
        "METHODOLOGY.md",
        "METHODOLOGY.ru.md",
        "NOTICE.md",
        "NOTICE.ru.md",
        "CHANGELOG.md",
        "CITATION.cff",
        "LICENSE",
        "metadata/release_config.json",
        "metadata/schema.json",
        "metadata/manifest.json",
        "metadata/dataset.jsonld",
    ]
    for relative_path in public_text_files:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for term in forbidden_public_terms:
            _add_if(
                term in text,
                f"{relative_path} exposes internal or placeholder term: {term}",
                errors,
            )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: 423 rows, bilingual docs, schema, metadata, and checksums verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
