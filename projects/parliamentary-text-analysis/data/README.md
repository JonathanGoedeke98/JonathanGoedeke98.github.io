# Data — Parliamentary Text Analysis

## Sample data (included)

The `sample_xml/` directory contains three **synthetic** XML files created for
pipeline demonstration. Their structure is identical to the official Bundestag
Plenarprotokoll format (DTD Version 1.0.2, published 2023-09-05).

| File       | Session | Date       | Topic                          |
|------------|---------|------------|--------------------------------|
| 20180.xml  | 180     | 2024-03-20 | Bundeshaushalt 2024            |
| 20185.xml  | 185     | 2024-04-17 | Digitalisierung & KI           |
| 20190.xml  | 190     | 2024-05-08 | Klimaschutz & Sozialpolitik    |

These files contain fictional speakers but realistic German parliamentary speech
text structured around the same policy topics that appear in the actual 20th
Bundestag. They are labelled as synthetic in the XML comments.

## Real data

Real Bundestag Plenarprotokolle for the 19th and 20th Wahlperioden are available
in the same XML format through the official DIP REST API:

- **Documentation:** <https://dip.bundestag.de/über-dip/hilfe/api>
- **API endpoint:** `https://search.dip.bundestag.de/api/v1/plenarprotokoll`
- **Key:** Free for research use; apply at `parlamentsdokumentation@bundestag.de`
- **DTD:** <https://www.bundestag.de/resource/blob/575720/dbtplenarprotokoll.dtd>

To download real data, set the `BT_API_KEY` environment variable and run:

```bash
export BT_API_KEY="your-key-here"
python scripts/01_fetch_data.py --mode api --start 2024-01-01 --end 2024-06-30
```

Downloaded files are saved to `data/raw_xml/`. All subsequent scripts will
automatically prefer `raw_xml/` over `sample_xml/` when it exists.

## Data licence

Official Bundestag data is released under **Datenlizenz Deutschland –
Namensnennung – Version 2.0 (dl-de/by-2-0)**. Attribution required:
> Quelle: Deutscher Bundestag, <https://www.bundestag.de/services/opendata>

## What is NOT in this repository

- Real plenary protocol XML files (download via API as described above)
- Any personally identifiable data beyond publicly available MdB metadata
- Any non-public or restricted-access Bundestag material
