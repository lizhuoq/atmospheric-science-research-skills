#!/usr/bin/env python3
"""Build deterministic topic assignments and leakage-resistant corpus splits."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
DERIVED = ROOT / "data" / "derived" / "paper_topics.csv"
SPLITS = ROOT / "data" / "splits" / "paper_splits.csv"
MANIFEST = ROOT / "data" / "splits" / "manifest.json"
SEED = "atmospheric-skills-m1-v1"

# The initial vocabulary is intentionally inspectable. Counts in the generated
# report determine which candidates become separate skills; labels are not skills.
TAXONOMY: dict[str, tuple[str, ...]] = {
    "dynamics-weather-systems": ("cyclone", "convection", "monsoon", "circulation", "dynamics", "storm", "front", "blocking", "wave"),
    "forecasting-predictability": ("forecast", "predictability", "prediction", "ensemble", "nowcast"),
    "boundary-layer-turbulence": ("boundary layer", "turbulence", "surface layer", "eddy covariance", "large-eddy"),
    "cloud-precipitation-microphysics": ("cloud", "precipitation", "rainfall", "microphysics", "snowfall", "ice nucleation"),
    "atmospheric-radiation": ("radiation", "radiative", "albedo", "shortwave", "longwave"),
    "atmospheric-chemistry": ("chemistry", "chemical", "ozone", "reactive", "oxidation", "trace gas", "methane"),
    "aerosols": ("aerosol", "particulate", "black carbon", "dust", "organic carbon"),
    "air-quality-exposure": ("air quality", "air pollution", "exposure", "mortality", "pm2.5", "health"),
    "remote-sensing-retrieval": ("remote sensing", "satellite", "retrieval", "radar", "lidar", "radiometer"),
    "observations-instruments": ("measurement", "instrument", "observation", "network", "sensor", "campaign"),
    "numerical-weather-prediction": ("numerical weather", "weather model", "data assimilation", "wrf", "forecast model"),
    "climate-variability-change": ("climate change", "climate variability", "warming", "teleconnection", "enso", "anthropogenic"),
    "extremes": ("extreme", "heatwave", "drought", "flood", "compound event", "heavy precipitation"),
    "hydrometeorology": ("hydrometeorology", "hydrolog", "water cycle", "soil moisture", "runoff", "evapotranspiration"),
    "land-atmosphere": ("land-atmosphere", "land surface", "soil", "vegetation", "urban", "biosphere"),
    "ocean-atmosphere": ("ocean-atmosphere", "air-sea", "sea surface", "marine", "ocean coupling"),
    "paleoclimate": ("paleoclimate", "palaeoclimate", "proxy", "holocene", "last glacial", "ice core"),
    "earth-system-models": ("earth system model", "esm", "coupled model", "cmip", "carbon cycle"),
    "model-evaluation-downscaling": ("model evaluation", "model bias", "bias correction", "downscal", "regional climate", "parameterization"),
    "statistics-causal-ml": ("machine learning", "deep learning", "neural network", "causal", "statistical", "random forest", "artificial intelligence"),
    "quality-control-uncertainty": ("quality control", "uncertainty", "error", "validation", "intercomparison", "benchmark"),
    "research-integrity-writing": ("reproducib", "peer review", "research integrity", "open science", "reporting guideline"),
}

METHODS: dict[str, tuple[str, ...]] = {
    "observation": ("observation", "measurement", "station", "campaign", "instrument"),
    "remote_sensing": ("satellite", "radar", "lidar", "retrieval", "remote sensing"),
    "numerical_modeling": ("model", "simulation", "wrf", "cmip", "ensemble"),
    "reanalysis": ("reanalysis", "era5", "merra", "jra-55"),
    "statistical_ml": ("statistical", "regression", "machine learning", "neural network", "causal"),
    "review_synthesis": ("review", "assessment", "synthesis", "perspective"),
}


def normalized_doi(value: str) -> str:
    return value.strip().lower().removeprefix("https://doi.org/").removeprefix("http://doi.org/")


def classify(row: dict[str, str]) -> tuple[list[str], list[str]]:
    text = f"{row.get('title', '')} {row.get('topics', '')}".lower()
    themes = [name for name, terms in TAXONOMY.items() if any(term in text for term in terms)]
    methods = [name for name, terms in METHODS.items() if any(term in text for term in terms)]
    return themes or ["unclassified"], methods or ["unspecified"]


def stable_hash(value: str) -> str:
    return hashlib.sha256(f"{SEED}|{value}".encode()).hexdigest()


def assign_splits(records: list[dict]) -> dict[str, str]:
    """Year-quota stratification with greedy theme/journal balancing."""
    targets = {"train": 0.70, "development": 0.15, "blind_test": 0.15}
    totals = Counter()
    labels_by_doi: dict[str, set[str]] = {}
    for r in records:
        labels = {f"theme:{t}" for t in r["themes"]}
        labels.add(f"journal:{r['journal_rank']}")
        labels_by_doi[r["doi_norm"]] = labels
        totals.update(labels)
    assigned_counts = {s: Counter() for s in targets}
    result: dict[str, str] = {}
    by_year: dict[int, list[dict]] = defaultdict(list)
    for record in records:
        by_year[record["year"]].append(record)
    for year in sorted(by_year):
        group = by_year[year]
        n = len(group)
        development = max(1, round(n * targets["development"])) if n >= 3 else 0
        blind = max(1, round(n * targets["blind_test"])) if n >= 3 else 0
        quotas = {"development": development, "blind_test": blind, "train": n - development - blind}
        ordered = sorted(group, key=lambda r: (min(totals[x] for x in labels_by_doi[r["doi_norm"]]), stable_hash(r["doi_norm"])))
        year_counts = Counter()
        for r in ordered:
            labels = labels_by_doi[r["doi_norm"]]
            allowed = [s for s in targets if year_counts[s] < quotas[s]]
            scores = {}
            for split in allowed:
                label_need = sum(max(0.0, totals[x] * targets[split] - assigned_counts[split][x]) / max(1, totals[x]) for x in labels)
                quota_need = (quotas[split] - year_counts[split]) / max(1, quotas[split])
                scores[split] = label_need + quota_need
            split = max(allowed, key=lambda s: (scores[s], stable_hash(r["doi_norm"] + s)))
            result[r["doi_norm"]] = split
            assigned_counts[split].update(labels)
            year_counts[split] += 1
    return result


def build() -> tuple[list[dict], dict]:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    seen: set[str] = set()
    records = []
    for row in rows:
        doi = normalized_doi(row["doi"])
        if not doi or doi in seen:
            raise ValueError(f"missing or duplicate DOI: {doi!r}")
        seen.add(doi)
        themes, methods = classify(row)
        records.append({
            "doi_norm": doi,
            "doi": row["doi"],
            "title": row["title"],
            "year": int(row["year"]),
            "journal": row["journal"],
            "journal_rank": int(row["journal_rank"]),
            "themes": themes,
            "methods": methods,
            "has_local_fulltext": row["download_status"].startswith("downloaded") and bool(row["local_path"]),
        })
    split_by_doi = assign_splits(records)
    for record in records:
        record["split"] = split_by_doi[record["doi_norm"]]
    counts = Counter(r["split"] for r in records)
    topic_counts = Counter(t for r in records for t in r["themes"])
    method_counts = Counter(m for r in records for m in r["methods"])
    manifest = {
        "schema": "atmospheric-corpus-split/1.0",
        "seed": SEED,
        "algorithm": "deterministic hard quotas within publication year, with greedy multi-label balancing over theme and journal",
        "ratios": {"train": 0.70, "development": 0.15, "blind_test": 0.15},
        "records": len(records),
        "counts": dict(sorted(counts.items())),
        "leakage_policy": {
            "train": "rule extraction and examples allowed",
            "development": "workflow tuning and error analysis only; not rule extraction",
            "blind_test": "final evaluation only; never inspect full text while authoring rules"
        },
        "taxonomy_version": "candidate-keywords/1.0",
        "topic_counts": dict(topic_counts.most_common()),
        "method_counts": dict(method_counts.most_common()),
        "input_sha256": hashlib.sha256(MASTER.read_bytes()).hexdigest(),
    }
    return records, manifest


def render_csv(records: list[dict], split_only: bool = False) -> str:
    from io import StringIO
    out = StringIO(newline="")
    if split_only:
        fields = ["doi", "split", "year", "journal_rank", "primary_theme", "has_local_fulltext"]
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for r in sorted(records, key=lambda x: x["doi_norm"]):
            writer.writerow({"doi": r["doi"], "split": r["split"], "year": r["year"], "journal_rank": r["journal_rank"], "primary_theme": r["themes"][0], "has_local_fulltext": str(r["has_local_fulltext"]).lower()})
    else:
        fields = ["doi", "title", "year", "journal", "themes", "methods", "has_local_fulltext"]
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for r in sorted(records, key=lambda x: x["doi_norm"]):
            writer.writerow({"doi": r["doi"], "title": r["title"], "year": r["year"], "journal": r["journal"], "themes": ";".join(r["themes"]), "methods": ";".join(r["methods"]), "has_local_fulltext": str(r["has_local_fulltext"]).lower()})
    return out.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed derived outputs are stale")
    args = parser.parse_args()
    records, manifest = build()
    outputs = {
        DERIVED: render_csv(records),
        SPLITS: render_csv(records, split_only=True),
        MANIFEST: json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    }
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, content in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != content]
        if stale:
            raise SystemExit("stale generated outputs: " + ", ".join(stale))
    else:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        print(json.dumps(manifest["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
