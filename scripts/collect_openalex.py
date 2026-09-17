#!/usr/bin/env python3
"""Resolve journal sources and collect diverse, highly cited OpenAlex works."""
from __future__ import annotations

import csv
import json
import math
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOURNALS = ROOT / "data" / "journals.csv"
OUT = ROOT / "data" / "metadata"
RAW = ROOT / "data" / "raw"
FROM_DATE = "2016-01-01"
TO_DATE = "2025-12-31"
UA = "atmospheric-science-research-skills/0.1 (mailto:replace-with-maintainer-email@example.org)"
SOURCE_ALIASES = {
    "Earth's Future": "Earths Future",
    "Journal of Geophysical Research: Atmospheres": "Journal of Geophysical Research Atmospheres",
    "npj Climate and Atmospheric Science": "npj Climate and Atmospheric Science",
    "Tellus B: Chemical and Physical Meteorology": "Tellus B",
}


def get_json(url: str, retries: int = 5) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.load(response)
        except Exception:
            if attempt + 1 == retries:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def api(path: str, params: dict[str, str | int]) -> dict:
    return get_json(f"https://api.openalex.org/{path}?{urllib.parse.urlencode(params)}")


def normalize(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def resolve_source(title: str) -> dict:
    query = SOURCE_ALIASES.get(title, title)
    result = api("sources", {"search": query, "per-page": 10})["results"]
    if not result:
        # OpenAlex search occasionally rejects punctuation-heavy names.  A
        # conservative word-only fallback is preferable to silently skipping.
        query = " ".join(title.replace(":", " ").replace("'", " ").split())
        result = api("sources", {"search": query, "per-page": 10})["results"]
    if not result:
        raise LookupError(f"OpenAlex source not found: {title!r}")
    exact = [r for r in result if normalize(r.get("display_name", "")) == normalize(title)]
    return (exact or result)[0]


def fetch_candidates(source_id: str, limit: int = 1000) -> list[dict]:
    cursor = "*"
    rows: list[dict] = []
    source_key = source_id.rsplit("/", 1)[-1]
    while len(rows) < limit:
        payload = api(
            "works",
            {
                "filter": f"primary_location.source.id:{source_key},from_publication_date:{FROM_DATE},to_publication_date:{TO_DATE}",
                "sort": "cited_by_count:desc",
                "per-page": min(200, limit - len(rows)),
                "cursor": cursor,
                "select": "id,doi,title,publication_year,publication_date,type,cited_by_count,primary_location,best_oa_location,open_access,topics,concepts,authorships",
            },
        )
        batch = payload["results"]
        if not batch:
            break
        rows.extend(batch)
        cursor = payload["meta"].get("next_cursor")
        if not cursor:
            break
        time.sleep(0.12)
    return rows


def topic_ids(work: dict) -> list[str]:
    topics = [t.get("id", "").rsplit("/", 1)[-1] for t in work.get("topics", [])[:5]]
    if topics:
        return [t for t in topics if t]
    return [c.get("id", "").rsplit("/", 1)[-1] for c in work.get("concepts", [])[:5] if c.get("id")]


def select_diverse(rows: list[dict], n: int = 100) -> list[dict]:
    excluded = {"editorial", "erratum", "letter", "paratext"}
    pool = [r for r in rows if r.get("type") not in excluded and r.get("title")]
    selected: list[dict] = []
    covered: Counter[str] = Counter()
    remaining = list(enumerate(pool))
    while remaining and len(selected) < n:
        best_pos = 0
        best_score = -1.0
        for pos, (rank, work) in enumerate(remaining):
            citation = math.log1p(work.get("cited_by_count") or 0)
            novelty = sum(1.0 / (1 + covered[t]) for t in topic_ids(work))
            core_bonus = 5.0 if rank < 20 else 0.0
            score = 3.0 * citation + 2.0 * novelty + core_bonus - 0.006 * rank
            if score > best_score:
                best_pos, best_score = pos, score
        _, work = remaining.pop(best_pos)
        selected.append(work)
        covered.update(topic_ids(work))
    return selected


def flatten(rank: int, journal: str, work: dict) -> dict:
    loc = work.get("best_oa_location") or work.get("primary_location") or {}
    authors = []
    for a in work.get("authorships", []):
        name = (a.get("author") or {}).get("display_name")
        if name:
            authors.append(name)
    topics = [t.get("display_name") for t in work.get("topics", [])[:5] if t.get("display_name")]
    return {
        "journal_rank": rank,
        "journal": journal,
        "title": work.get("title"),
        "doi": work.get("doi"),
        "openalex_id": work.get("id"),
        "publication_date": work.get("publication_date"),
        "year": work.get("publication_year"),
        "type": work.get("type"),
        "openalex_cited_by_count": work.get("cited_by_count"),
        "authors": "; ".join(authors),
        "topics": "; ".join(topics),
        "is_oa": (work.get("open_access") or {}).get("is_oa"),
        "oa_status": (work.get("open_access") or {}).get("oa_status"),
        "landing_page_url": loc.get("landing_page_url"),
        "pdf_url": loc.get("pdf_url"),
        "wos_times_cited": "",
        "download_status": "pending",
        "local_path": "",
        "sha256": "",
        "notes": "",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    with JOURNALS.open(encoding="utf-8-sig", newline="") as handle:
        journals = list(csv.DictReader(handle))
    fieldnames = None
    all_selected = []
    for journal in journals:
        rank, title = int(journal["rank"]), journal["journal"]
        print(f"[{rank:02d}/30] resolving {title}", flush=True)
        source = resolve_source(title)
        print(f"           -> {source['display_name']} ({source['id']})", flush=True)
        journal["source_id"] = source["id"]
        journal["issn_l"] = source.get("issn_l") or ""
        journal["verification_status"] = "openalex_resolved"
        raw_path = RAW / f"{rank:02d}.json"
        if raw_path.exists():
            rows = json.loads(raw_path.read_text(encoding="utf-8"))
        else:
            rows = fetch_candidates(source["id"])
            raw_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        selected = [flatten(rank, title, w) for w in select_diverse(rows)]
        all_selected.extend(selected)
        out_path = OUT / f"{rank:02d}.csv"
        fieldnames = list(selected[0]) if selected else fieldnames
        if selected:
            with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader(); writer.writerows(selected)
    with JOURNALS.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=journals[0].keys())
        writer.writeheader(); writer.writerows(journals)
    if all_selected:
        with (OUT / "all_selected.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(all_selected[0]))
            writer.writeheader(); writer.writerows(all_selected)
    print(f"selected {len(all_selected)} records", flush=True)


if __name__ == "__main__":
    main()
