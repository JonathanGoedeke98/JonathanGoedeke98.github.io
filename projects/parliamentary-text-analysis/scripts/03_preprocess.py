#!/usr/bin/env python3
"""
03_preprocess.py — Text preprocessing for parliamentary speech corpus.

Steps applied:
  1. Remove procedural markers: (Beifall ...), (Lachen), [Zuruf], etc.
  2. Lowercase and Unicode normalisation
  3. Remove punctuation and digits
  4. Tokenise on whitespace
  5. Remove German stopwords (see src/stopwords_de.py)
  6. Remove very short tokens (len < 3) and very long tokens (len > 40)

Input:  outputs/tables/corpus_raw.csv
Output: outputs/tables/corpus_clean.csv
        outputs/tables/vocab_stats.csv (token frequency table)

Usage:
  python scripts/03_preprocess.py
"""

import re
import sys
import logging
import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
from src.stopwords_de import STOPWORDS_DE, PROCEDURAL_PATTERN

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

INPUT_PATH = BASE_DIR / "outputs" / "tables" / "corpus_raw.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"


def remove_procedural(text: str) -> str:
    """Remove inline procedural annotations like (Beifall bei der SPD)."""
    text = re.sub(PROCEDURAL_PATTERN, " ", text)
    # Also remove square-bracket interjections: [Zuruf], [Unruhe]
    text = re.sub(r"\[[^\]]{1,60}\]", " ", text)
    return text


def normalise_unicode(text: str) -> str:
    """NFKC normalisation — resolves ligatures and compatibility characters."""
    return unicodedata.normalize("NFKC", text)


def tokenise(text: str) -> list[str]:
    """Lowercase, remove punctuation/digits, split on whitespace."""
    text = text.lower()
    # Replace hyphens within compound words with space so we keep sub-parts
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)
    # Remove everything that isn't a letter or whitespace (incl. digits)
    text = re.sub(r"[^a-zäöüß\s]", " ", text)
    return text.split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [
        t for t in tokens
        if t not in STOPWORDS_DE and 3 <= len(t) <= 40
    ]


def preprocess(text: str) -> tuple[list[str], str]:
    """Full preprocessing pipeline. Returns (token_list, joined_clean_text)."""
    text = remove_procedural(text)
    text = normalise_unicode(text)
    tokens = tokenise(text)
    tokens = remove_stopwords(tokens)
    return tokens, " ".join(tokens)


def main():
    if not INPUT_PATH.exists():
        log.error("Raw corpus not found at %s. Run 02_parse_xml.py first.", INPUT_PATH)
        sys.exit(1)

    corpus = pd.read_csv(INPUT_PATH, encoding="utf-8")
    log.info("Loaded %d speeches from %s", len(corpus), INPUT_PATH)

    # Apply preprocessing
    results = corpus["speech_text"].apply(preprocess)
    corpus["tokens"] = results.apply(lambda x: x[0])
    corpus["clean_text"] = results.apply(lambda x: x[1])
    corpus["clean_len"] = corpus["tokens"].apply(len)

    # Save cleaned corpus
    out_path = OUTPUT_DIR / "corpus_clean.csv"
    corpus.to_csv(out_path, index=False, encoding="utf-8")
    log.info("Cleaned corpus saved to %s", out_path)

    # Token frequency table
    from collections import Counter
    all_tokens = [t for tokens in corpus["tokens"] for t in tokens]
    freq = Counter(all_tokens)
    vocab_df = pd.DataFrame(freq.most_common(), columns=["token", "count"])
    vocab_path = OUTPUT_DIR / "vocab_stats.csv"
    vocab_df.to_csv(vocab_path, index=False, encoding="utf-8")
    log.info("Vocabulary: %d unique tokens. Top 10:", len(vocab_df))
    log.info("\n%s", vocab_df.head(10).to_string(index=False))

    # Summary statistics
    log.info("\nClean speech length statistics:")
    log.info(corpus["clean_len"].describe().to_string())

    return corpus, vocab_df


if __name__ == "__main__":
    main()
