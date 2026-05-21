# Political Text Analysis of Parliamentary Speeches

An end-to-end NLP pipeline for analysing publicly available Bundestag
Plenarprotokolle (German parliamentary plenary transcripts).

**Status:** Initial prototype complete — pipeline runs end-to-end on
demonstration data matching the official Bundestag XML format.

---

## Research question

Can standard NLP methods — TF-IDF feature extraction and NMF topic modelling —
recover meaningful thematic structure from German parliamentary speech transcripts,
and how consistently do speeches cluster by policy domain rather than party
affiliation?

---

## Data

**Source:** German Bundestag Plenarprotokolle (20th Bundestag, 2021–present)  
**Format:** Official XML format (DTD v1.0.2, 2023-09-05)  
**Access:** Bundestag DIP REST API — <https://dip.bundestag.de/über-dip/hilfe/api>  
**Licence:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0)

The prototype uses three synthetic XML sessions (sessions 180, 185, 190)
that are structurally identical to real Bundestag protocols. Topics covered:
Bundeshaushalt 2024, Digitalisierung & KI, Klimaschutz & Sozialpolitik.

See [`data/README.md`](data/README.md) for instructions on downloading real data
via the DIP API.

---

## Methods

| Step | Method | Library |
|------|--------|---------|
| XML parsing | lxml / DTD-compliant element traversal | lxml |
| Text cleaning | Regex, German stopword removal, NFKC normalisation | — |
| Feature extraction | TF-IDF (max 500 features, unigrams + bigrams, sublinear TF) | scikit-learn |
| Topic modelling | NMF (k=5, NNDSVDA init) | scikit-learn |
| Classification | Logistic regression (multinomial, stratified CV) | scikit-learn |
| Visualisation | Publication-quality static figures | matplotlib, seaborn |

---

## Results (prototype)

Running on 3 sessions (17 speeches, 5 parliamentary groups):

**Corpus statistics:**
- 17 speeches | 3 sessions | 6 unique speakers | 5 Fraktionen
- Vocabulary after preprocessing: 894 unique tokens
- Mean clean speech length: 74 tokens (range: 41–85)

**Top TF-IDF terms** (corpus-level mean):
`digitale`, `deutschland`, `digitalisierung`, `mittel`, `fordern`,
`unternehmen`, `klimaschutz`, `öffentlichen`, `verwaltung`

**NMF topics** (5 topics, top terms):

| Topic | Dominant terms | Interpretation |
|-------|---------------|----------------|
| 1 | klimaschutz, energiewende, wasserstoff, treibhausgasemissionen | Climate & energy |
| 2 | digitale verwaltung, digitalisierung, gigabit | Digital policy |
| 3 | investitionen, bildung, schulen, mittel | Education & investment |
| 4 | unternehmen, bürokratieabbau, onlinezugangsgesetz | Business & regulation |
| 5 | rente, pflege, altersarmut, menschen | Social policy |

Topic labels are interpretive — they describe the dominant vocabulary cluster,
not a ground truth classification.

---

## How to reproduce

```bash
# 1. Clone and install
git clone https://github.com/JonathanGoedeke98/JonathanGoedeke98.github.io
cd projects/parliamentary-text-analysis
pip install -r requirements.txt

# 2. Run the full pipeline (sample data, no API key needed)
python scripts/01_fetch_data.py       # lists sample XML files
python scripts/02_parse_xml.py        # extracts corpus_raw.csv
python scripts/03_preprocess.py       # produces corpus_clean.csv
python scripts/04_analyse.py          # TF-IDF + NMF
python scripts/05_visualise.py        # generates figures in outputs/figures/

# 3. Optional: download real data via DIP API
export BT_API_KEY="your-key-here"
python scripts/01_fetch_data.py --mode api --start 2024-01-01 --end 2024-06-30
# Then re-run steps 2–5 (the parser auto-detects real data in data/raw_xml/)
```

All outputs are written to `outputs/tables/` (CSV) and `outputs/figures/` (PNG).
Scripts are numbered and can be run individually or in sequence.

---

## Limitations

- **Corpus size:** The prototype uses 3 synthetic sessions. NMF topics and
  TF-IDF scores are illustrative, not statistically robust. Meaningful topic
  inference requires at least several hundred speeches.
- **Party classification:** With fewer than 5 speeches per party, cross-validated
  accuracy scores are noisy and should not be over-interpreted.
- **Synthetic data:** The sample XML files contain structured but representative
  German parliamentary language, not verbatim transcripts. Results on real data
  will differ.
- **Preprocessing:** The German stopword list covers common function words and
  parliamentary procedural markers but may not capture all domain-specific noise.
- **Compound words:** German compound splitting is not applied; multi-word
  compounds are treated as unigrams.

---

## Ethical and data-use note

This project uses public parliamentary speech data published by the German
Bundestag under an open-data licence. It is a methodological demonstration of
text preprocessing, topic exploration, and transparent visualisation. It does
not involve private data, operational analysis, or profiling of private
individuals. All data sources are official public records. No political claims
or partisan interpretations are drawn from the analysis results.

---

## Project structure

```
parliamentary-text-analysis/
├── data/
│   ├── README.md              Data source documentation
│   └── sample_xml/            Synthetic XML sessions (3 files)
├── scripts/
│   ├── 01_fetch_data.py       Data acquisition (sample or API mode)
│   ├── 02_parse_xml.py        XML parser → corpus_raw.csv
│   ├── 03_preprocess.py       Text cleaning → corpus_clean.csv
│   ├── 04_analyse.py          TF-IDF + NMF + optional classification
│   └── 05_visualise.py        Figure generation
├── src/
│   └── stopwords_de.py        German stopword list
├── outputs/
│   ├── figures/               Generated PNG figures
│   └── tables/                Generated CSV tables
├── requirements.txt
└── README.md
```
