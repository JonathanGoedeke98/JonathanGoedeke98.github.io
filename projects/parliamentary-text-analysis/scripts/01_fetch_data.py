#!/usr/bin/env python3
"""
01_fetch_data.py — Data acquisition for Parliamentary Text Analysis

Supports two modes:
  1. DIP API mode: downloads Plenarprotokolle metadata via the official
     Bundestag DIP REST API (requires a personal API key).
  2. Sample mode (default): uses the bundled synthetic XML files in
     data/sample_xml/ to demonstrate the full pipeline.

Usage:
  # Sample mode (no API key needed):
  python scripts/01_fetch_data.py

  # DIP API mode (requires key):
  export BT_API_KEY="your-key-here"
  python scripts/01_fetch_data.py --mode api --start 2024-01-01 --end 2024-06-30

Obtaining a DIP API key:
  Apply at: https://dip.bundestag.de/über-dip/hilfe/api
  Contact:  parlamentsdokumentation@bundestag.de
  The API is free of charge for research and educational use.

Data license:
  Official Bundestag data is released under Datenlizenz Deutschland –
  Namensnennung – Version 2.0 (dl-de/by-2-0).
  Source: Deutscher Bundestag, https://www.bundestag.de/services/opendata
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DIR = DATA_DIR / "sample_xml"
DIP_API_BASE = "https://search.dip.bundestag.de/api/v1"


def list_sample_files():
    """Return paths to all sample XML files in the sample directory."""
    xml_files = sorted(SAMPLE_DIR.glob("*.xml"))
    if not xml_files:
        log.error("No XML files found in %s", SAMPLE_DIR)
        sys.exit(1)
    return xml_files


def fetch_via_api(api_key: str, date_start: str, date_end: str, wahlperiode: int = 20):
    """Fetch Plenarprotokoll metadata from the DIP API and download XML files."""
    try:
        import requests
    except ImportError:
        log.error("requests package required for API mode: pip install requests")
        sys.exit(1)

    headers = {"Authorization": f"ApiKey {api_key}"}
    params = {
        "f.datum.start": date_start,
        "f.datum.end": date_end,
        "f.wahlperiode": wahlperiode,
        "format": "json",
    }

    log.info("Fetching protocol list from DIP API (%s to %s)...", date_start, date_end)
    resp = requests.get(f"{DIP_API_BASE}/plenarprotokoll", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    documents = data.get("documents", [])
    log.info("Found %d protocols", len(documents))

    # Save manifest
    manifest_path = DATA_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("Manifest saved to %s", manifest_path)

    # Download individual XML files
    raw_dir = DATA_DIR / "raw_xml"
    raw_dir.mkdir(exist_ok=True)

    for doc in documents:
        doc_id = doc.get("id")
        datum = doc.get("datum", "unknown")
        log.info("Processing protocol %s (%s)", doc_id, datum)
        # Retrieve full text record for XML download URL
        text_resp = requests.get(
            f"{DIP_API_BASE}/plenarprotokoll-text/{doc_id}",
            headers=headers,
            timeout=30,
        )
        if text_resp.status_code != 200:
            log.warning("Could not fetch text record for %s", doc_id)
            continue
        text_data = text_resp.json()
        # Extract and download XML
        xml_url = text_data.get("fundstelle", {}).get("xml_url")
        if xml_url:
            xml_resp = requests.get(xml_url, headers=headers, timeout=60)
            out_path = raw_dir / f"{datum.replace('-', '')}.xml"
            out_path.write_bytes(xml_resp.content)
            log.info("Saved %s", out_path)
        else:
            log.warning("No XML URL for %s", doc_id)

    return list(raw_dir.glob("*.xml"))


def run_sample_mode():
    """Report the sample XML files available for processing."""
    files = list_sample_files()
    log.info("Sample mode: found %d XML file(s):", len(files))
    for f in files:
        log.info("  %s", f.name)

    # Write a simple manifest so downstream scripts know what to process
    manifest = {
        "mode": "sample",
        "note": "Synthetic XML files matching the official Bundestag DTD v1.0.2 (2023-09-05). "
                "Replace with real data downloaded via the DIP API for production use.",
        "files": [str(f) for f in files],
    }
    manifest_path = DATA_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    log.info("Manifest written to %s", manifest_path)
    return files


def main():
    parser = argparse.ArgumentParser(description="Fetch Bundestag Plenarprotokolle")
    parser.add_argument("--mode", choices=["sample", "api"], default="sample",
                        help="Data source: 'sample' (default) or 'api'")
    parser.add_argument("--start", default="2024-01-01", help="Start date (YYYY-MM-DD, API mode)")
    parser.add_argument("--end", default="2024-06-30", help="End date (YYYY-MM-DD, API mode)")
    parser.add_argument("--wahlperiode", type=int, default=20, help="Wahlperiode (default: 20)")
    args = parser.parse_args()

    if args.mode == "api":
        api_key = os.environ.get("BT_API_KEY")
        if not api_key:
            log.error("BT_API_KEY environment variable not set. "
                      "Apply for a key at https://dip.bundestag.de/über-dip/hilfe/api")
            sys.exit(1)
        files = fetch_via_api(api_key, args.start, args.end, args.wahlperiode)
        log.info("Downloaded %d XML file(s) via API.", len(files))
    else:
        run_sample_mode()


if __name__ == "__main__":
    main()
