"""German stopword list for parliamentary text analysis.

Combines standard German function words with parliamentary procedural terms
that carry no semantic content for topic analysis.
"""

STOPWORDS_DE = {
    # Articles and determiners
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einem", "einen",
    "einer", "eines", "kein", "keine", "keinem", "keinen", "keiner", "keines",
    # Pronouns
    "ich", "du", "er", "sie", "es", "wir", "ihr", "mich", "mir", "dich", "dir",
    "ihn", "ihm", "ihr", "uns", "euch", "sich", "man", "mein", "dein", "sein",
    "unser", "euer", "meine", "deine", "seine", "unsere", "eure",
    "dieser", "diese", "dieses", "diesem", "diesen",
    # Prepositions
    "in", "an", "auf", "aus", "bei", "mit", "nach", "von", "vor", "zu", "zur",
    "zum", "im", "am", "ins", "ans", "beim", "durch", "für", "gegen", "ohne",
    "über", "unter", "zwischen", "neben", "hinter", "um", "seit", "bis",
    "ab", "als", "außer", "entlang", "gegenüber", "trotz", "während", "wegen",
    # Conjunctions
    "und", "oder", "aber", "denn", "weil", "dass", "ob", "wenn", "als",
    "damit", "obwohl", "sodass", "sowohl", "entweder", "weder", "noch",
    "jedoch", "allerdings", "sondern", "daher", "deshalb", "trotzdem",
    "dennoch", "außerdem", "zudem", "einerseits", "andererseits",
    # Adverbs
    "auch", "noch", "schon", "nicht", "nur", "sehr", "so", "mehr", "immer",
    "jetzt", "dann", "hier", "dort", "ja", "nein", "nun", "oft", "nie",
    "bereits", "gerade", "dabei", "dazu", "davon", "daran", "damit",
    "dafür", "darum", "darauf", "danach", "zwar", "eben", "doch", "mal",
    "einmal", "wieder", "weiter", "besonders", "genau", "ganz", "viel",
    "wenig", "kaum", "fast", "eher", "vor", "nach", "eigentlich",
    # Verbs (auxiliary/modal)
    "sein", "ist", "sind", "war", "waren", "wird", "werden", "wurde", "wurden",
    "haben", "hat", "hatte", "hatten", "habe", "habt", "können", "kann",
    "konnte", "müssen", "muss", "musste", "wollen", "will", "wollte",
    "sollen", "soll", "sollte", "dürfen", "darf", "durfte", "mögen", "mag",
    "mochte", "lassen", "lässt", "ließ", "worden", "worden", "geworden",
    "gemacht", "gesagt", "gegeben", "gehabt", "gewesen",
    # Parliamentary procedural terms
    "herr", "frau", "präsident", "präsidentin", "kolleginnen", "kollegen",
    "damen", "herren", "sehr", "geehrten", "geehrte", "liebe", "lieben",
    "meine", "danke", "vielen", "bitte", "jawohl", "beifall",
    "abgeordnete", "abgeordneten", "abgeordneter", "fraktion", "fraktionen",
    "bundesregierung", "bundesminister", "bundesministerin", "staatssekretär",
    "parlamentarisch", "parlamentarische", "parlamentarischen",
    "tagesordnung", "tagesordnungspunkt", "sitzung", "sitzungen",
    "drucksache", "drucksachen", "abstimmung", "abstimmungen",
    "ausschuss", "ausschüsse", "ausschusses", "ausschüssen",
    "antrag", "anträge", "antrags", "anträgen",
    "beschluss", "beschlüsse", "beschlusses", "beschlüssen",
    "beratung", "beratungen", "debatte", "debatten",
    "rede", "reden", "redner", "rednerin", "rednerinnen", "sprecher",
    "bundesrat", "bundestag", "bundestages", "bundesrates",
    "erste", "zweite", "dritte", "vierte", "fünfte",
    "lesungen", "lesung", "beratung", "beratungen",
    # Common parliamentary fillers
    "stellt", "stellen", "stelle", "geht", "gehen", "kommt", "kommen",
    "gibt", "geben", "macht", "machen", "sagt", "sagen", "zeigt", "zeigen",
    "nehmen", "nimmt", "brauchen", "braucht", "sehen", "sieht", "weiß",
    "wissen", "möchte", "möchten", "möchten",
    # Numbers and abbreviations
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht",
    "neun", "zehn", "prozent", "euro", "milliarden", "millionen",
    # Other common filler words
    "dem", "den", "der", "wohl", "dabei", "daran", "nun", "hin",
    "her", "immerhin", "nämlich", "eigentlich", "letztlich",
}

PROCEDURAL_PATTERN = r"\([^)]{1,60}\)"  # matches (Beifall), (Lachen), etc.
