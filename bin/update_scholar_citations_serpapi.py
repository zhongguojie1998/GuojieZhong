#!/usr/bin/env python3
"""Update _data/citations.yml from a Google Scholar profile.

Backends:
  - SerpAPI (google_scholar_author engine) when SERPAPI_KEY is set.
  - scholarly (direct scraping) otherwise.

Usage:
  SERPAPI_KEY=... python bin/update_scholar_citations_serpapi.py [--force] [--backend serpapi|scholarly]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, TypedDict

import yaml

ROOT: Path = Path(__file__).resolve().parent.parent
CONFIG_FILE: Path = ROOT / "_data" / "socials.yml"
OUTPUT_FILE: Path = ROOT / "_data" / "citations.yml"
SERPAPI_URL: str = "https://serpapi.com/search.json"
PAGE_SIZE: int = 100
MAX_PAGES: int = 10
TIMEOUT_S: int = 30


class Paper(TypedDict):
    title: str
    year: str
    citations: int


Papers = dict[str, Paper]


class CitationError(RuntimeError):
    pass


def load_scholar_user_id() -> str:
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            config: dict[str, Any] = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as e:
        raise CitationError(f"Cannot read {CONFIG_FILE}: {e}") from e
    user_id = config.get("scholar_userid")
    if not isinstance(user_id, str) or not user_id.strip():
        raise CitationError(f"'scholar_userid' missing in {CONFIG_FILE}")
    return user_id.strip()


def fetch_serpapi(user_id: str, api_key: str) -> Papers:
    papers: Papers = {}
    start = 0
    for _ in range(MAX_PAGES):
        query = urllib.parse.urlencode(
            {
                "engine": "google_scholar_author",
                "author_id": user_id,
                "hl": "en",
                "sort": "pubdate",
                "num": PAGE_SIZE,
                "start": start,
                "api_key": api_key,
            }
        )
        try:
            with urllib.request.urlopen(f"{SERPAPI_URL}?{query}", timeout=TIMEOUT_S) as resp:
                data: dict[str, Any] = json.load(resp)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            raise CitationError(f"SerpAPI request failed: {e}") from e
        if "error" in data:
            raise CitationError(f"SerpAPI error: {data['error']}")

        articles: list[dict[str, Any]] = data.get("articles") or []
        for art in articles:
            pub_id = art.get("citation_id")
            if not pub_id:
                continue
            cited_by = (art.get("cited_by") or {}).get("value")
            papers[pub_id] = {
                "title": str(art.get("title", "Unknown Title")),
                "year": str(art.get("year") or "Unknown Year"),
                "citations": int(cited_by or 0),
            }

        if len(articles) < PAGE_SIZE or not (data.get("serpapi_pagination") or {}).get("next"):
            break
        start += PAGE_SIZE
    return papers


def fetch_scholarly(user_id: str) -> Papers:
    try:
        from scholarly import scholarly  # type: ignore[import-untyped]
    except ImportError as e:
        raise CitationError("scholarly not installed: pip install scholarly") from e

    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    try:
        author = scholarly.fill(scholarly.search_author_id(user_id), sections=["publications"])
    except Exception as e:  # scholarly raises assorted exception types
        raise CitationError(f"scholarly fetch failed: {e}") from e

    papers: Papers = {}
    for pub in author.get("publications", []):
        pub_id = pub.get("author_pub_id") or pub.get("pub_id")
        if not pub_id:
            continue
        bib: dict[str, Any] = pub.get("bib", {})
        papers[pub_id] = {
            "title": str(bib.get("title", "Unknown Title")),
            "year": str(bib.get("pub_year", "Unknown Year")),
            "citations": int(pub.get("num_citations") or 0),
        }
    return papers


def load_existing() -> dict[str, Any]:
    if not OUTPUT_FILE.exists():
        return {}
    try:
        with OUTPUT_FILE.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as e:
        print(f"Warning: cannot read {OUTPUT_FILE}: {e}", file=sys.stderr)
        return {}


def write_output(papers: Papers) -> None:
    payload = {"metadata": {"last_updated": date.today().isoformat()}, "papers": papers}
    tmp = OUTPUT_FILE.with_suffix(".yml.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        yaml.dump(payload, f, width=1000, sort_keys=True, allow_unicode=True)
    tmp.replace(OUTPUT_FILE)


def report_diff(old: Papers, new: Papers) -> None:
    for pid, p in sorted(new.items(), key=lambda kv: -kv[1]["citations"]):
        prev = old.get(pid)
        if prev is None:
            print(f"  + {p['citations']:>5}  {p['title'][:90]}")
        elif prev.get("citations") != p["citations"]:
            print(f"  ~ {prev.get('citations')} -> {p['citations']}  {p['title'][:90]}")
    for pid in old.keys() - new.keys():
        print(f"  - {old[pid].get('title', pid)[:90]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--backend", choices=("serpapi", "scholarly"), default=None)
    parser.add_argument("--force", action="store_true", help="rewrite even if unchanged")
    args = parser.parse_args()

    api_key = os.environ.get("SERPAPI_KEY", "").strip()
    backend: str = args.backend or ("serpapi" if api_key else "scholarly")

    try:
        user_id = load_scholar_user_id()
        print(f"Fetching citations for {user_id} via {backend}")
        if backend == "serpapi":
            if not api_key:
                raise CitationError("SERPAPI_KEY not set")
            papers = fetch_serpapi(user_id, api_key)
        else:
            papers = fetch_scholarly(user_id)
    except CitationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not papers:
        print("Error: no publications returned; keeping existing file", file=sys.stderr)
        return 1

    old: Papers = load_existing().get("papers") or {}
    if old == papers and not args.force:
        print(f"No changes ({len(papers)} papers).")
        return 0

    report_diff(old, papers)
    write_output(papers)
    print(f"Wrote {len(papers)} papers, {sum(p['citations'] for p in papers.values())} total citations -> {OUTPUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
