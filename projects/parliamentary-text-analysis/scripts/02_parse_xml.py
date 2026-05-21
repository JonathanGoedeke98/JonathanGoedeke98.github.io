#!/usr/bin/env python3
"""
02_parse_xml.py — Parse Bundestag Plenarprotokoll XML files into a structured corpus.

Reads all XML files in data/sample_xml/ (or data/raw_xml/ for API-downloaded files)
and extracts one row per speech with the following fields:
  - session_nr:   session number (from XML attribute)
  - date:         session date (YYYY-MM-DD)
  - speech_id:    unique speech identifier from XML
  - speaker_id:   speaker ID from the redner element
  - first_name:   speaker's first name
  - last_name:    speaker's last name
  - fraktion:     parliamentary group (party affiliation)
  - speech_text:  concatenated paragraph text of the speech
  - speech_len:   number of tokens (whitespace-split words)

Output:
  outputs/tables/corpus_raw.csv

Usage:
  python scripts/02_parse_xml.py [--xml-dir data/sample_xml]
"""

import re
import sys
import logging
import argparse
from pathlib import Path

import pandas as pd
from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_element_text(elem) -> str:
    """Recursively extract all text from an element, ignoring sub-elements."""
    parts = []
    if elem.text:
        parts.append(elem.text.strip())
    for child in elem:
        # Skip <kommentar> elements (procedural annotations like "[Beifall]")
        if child.tag != "kommentar":
            parts.append(clean_element_text(child))
        if child.tail:
            parts.append(child.tail.strip())
    return " ".join(p for p in parts if p)


def extract_speaker(rede_elem) -> dict:
    """Extract speaker metadata from a <rede> element."""
    info = {"speaker_id": None, "first_name": "", "last_name": "", "fraktion": ""}

    # First <redner> inside first <p> holds speaker info
    redner = rede_elem.find(".//redner")
    if redner is not None:
        info["speaker_id"] = redner.get("id")
        name = redner.find("name")
        if name is not None:
            vn = name.find("vorname")
            nn = name.find("nachname")
            fk = name.find("fraktion")
            if vn is not None:
                info["first_name"] = (vn.text or "").strip()
            if nn is not None:
                info["last_name"] = (nn.text or "").strip()
            if fk is not None:
                info["fraktion"] = (fk.text or "").strip()
    return info


def parse_speech_text(rede_elem) -> str:
    """Extract plain speech text from a <rede> element.

    Concatenates all <p> paragraphs while excluding:
    - The first <p> (which contains the speaker name)
    - <kommentar> elements (procedural annotations)
    - <redner> sub-elements within <p>
    """
    paragraphs = []
    p_elements = rede_elem.findall("p")

    for i, p in enumerate(p_elements):
        # Skip first <p>: it is the speaker introduction paragraph
        if i == 0:
            continue
        # Collect text from <p>, ignoring <redner> and <kommentar> children
        text_parts = []
        if p.text:
            text_parts.append(p.text.strip())
        for child in p:
            if child.tag not in ("redner", "kommentar"):
                t = clean_element_text(child)
                if t:
                    text_parts.append(t)
            if child.tail:
                text_parts.append(child.tail.strip())
        para_text = " ".join(t for t in text_parts if t)
        if para_text:
            paragraphs.append(para_text)

    return " ".join(paragraphs)


def parse_protocol(xml_path: Path) -> list[dict]:
    """Parse one Plenarprotokoll XML file into a list of speech records."""
    records = []
    try:
        tree = etree.parse(str(xml_path), parser=etree.XMLParser(recover=True))
    except Exception as exc:
        log.error("Failed to parse %s: %s", xml_path.name, exc)
        return records

    root = tree.getroot()
    session_nr = root.get("sitzung-nr", "")
    raw_date = root.get("sitzung-datum", "")  # format: DD.MM.YYYY

    # Normalise date to ISO format
    try:
        d, m, y = raw_date.split(".")
        date_iso = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
    except ValueError:
        date_iso = raw_date

    # Iterate over all <rede> elements in the session
    for rede in root.iter("rede"):
        speech_id = rede.get("id", "")
        speaker = extract_speaker(rede)
        speech_text = parse_speech_text(rede)

        if not speech_text.strip():
            continue  # Skip empty speeches (e.g., procedural interruptions)

        records.append({
            "session_nr": session_nr,
            "date": date_iso,
            "speech_id": speech_id,
            "speaker_id": speaker["speaker_id"],
            "first_name": speaker["first_name"],
            "last_name": speaker["last_name"],
            "fraktion": speaker["fraktion"],
            "speech_text": speech_text,
            "speech_len": len(speech_text.split()),
        })

    log.info("Parsed %s: %d speeches (session %s, %s)",
             xml_path.name, len(records), session_nr, date_iso)
    return records


def main():
    parser = argparse.ArgumentParser(description="Parse Bundestag Plenarprotokoll XML")
    parser.add_argument("--xml-dir", default=None,
                        help="Directory with XML files (default: data/sample_xml)")
    args = parser.parse_args()

    if args.xml_dir:
        xml_dir = Path(args.xml_dir)
    else:
        xml_dir = BASE_DIR / "data" / "sample_xml"
        # Fall back to API-downloaded files if they exist
        raw_dir = BASE_DIR / "data" / "raw_xml"
        if raw_dir.exists() and any(raw_dir.glob("*.xml")):
            xml_dir = raw_dir
            log.info("Using API-downloaded files from %s", xml_dir)

    xml_files = sorted(xml_dir.glob("*.xml"))
    if not xml_files:
        log.error("No XML files found in %s", xml_dir)
        sys.exit(1)

    log.info("Found %d XML file(s) in %s", len(xml_files), xml_dir)

    all_records = []
    for xml_file in xml_files:
        all_records.extend(parse_protocol(xml_file))

    if not all_records:
        log.error("No speech records extracted.")
        sys.exit(1)

    corpus = pd.DataFrame(all_records)
    out_path = OUTPUT_DIR / "corpus_raw.csv"
    corpus.to_csv(out_path, index=False, encoding="utf-8")

    log.info("Corpus saved to %s", out_path)
    log.info("Total speeches: %d | Sessions: %d | Speakers: %d",
             len(corpus),
             corpus["session_nr"].nunique(),
             corpus["speaker_id"].nunique())
    log.info("Fraktionen:\n%s", corpus["fraktion"].value_counts().to_string())

    return corpus


if __name__ == "__main__":
    main()
