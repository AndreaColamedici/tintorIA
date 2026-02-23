#!/usr/bin/env python3
"""
build_search_index.py — Costruisce un indice di ricerca compatto per le trascrizioni.

Produce due file:
1. data/search_index.json — indice invertito: parola → [episode_numbers]
   (solo parole significative, no stopwords, min 4 chars)
2. data/search_snippets.json — per ogni episodio, il testo completo normalizzato
   (caricato on-demand dall'app)

Strategia: l'app carica solo l'indice (piccolo) per sapere QUALI puntate matchano,
poi carica i singoli transcript on-demand per mostrare gli snippet.
"""

import json, os, re, glob
from collections import defaultdict

DATA_DIR = "data"
TRANS_DIR = f"{DATA_DIR}/transcripts"

# Italian stopwords (most common function words)
STOPWORDS = set("""
a al alla alle allo ai agli ancora anche anzi avere
che chi ci con cosa come contro così da dal dalla dalle dallo dai dagli
degli dei del della delle dello di dopo dove e è ed era essere
fa fino fra già gli ha ho il in io la le lei lo loro lui
ma me mi mia mie miei mio molto molta ne né no noi non nostra nostro
o ogni oltre per perché più poi prima qualche quale quando quasi quello questa
questo qui se senza si sia siamo siete so solo sono sta stato stata
su sua sue suoi suo tra tu tua tue tuo tuoi tutti tutto un una uno
vai vi voi vostro
dei nel nella nelle nell nello negli dalla dall dallo dagli alle allo all
una che non sono per con del della come più anche questo questa
quello quella queste questi quelli quelle loro dove quando quanto stata stati stato
molto aveva erano dopo ancora lui lei prima sempre fatto dice fanno aveva avevo avevi
allora proprio così quindi perché bene bello bella tipo cioè insomma vabbè
un po' detto
""".split())

def tokenize(text):
    """Split text into lowercase tokens, only letters."""
    return re.findall(r'[a-zàèéìòùA-Z]{4,}', text.lower())


def main():
    # Load episodes metadata
    with open(f"{DATA_DIR}/episodes_tagged.json") as f:
        data = json.load(f)

    # Build inverted index
    index = defaultdict(set)  # word → set of episode numbers
    ep_texts = {}  # ep_number → clean text (for snippets)

    transcript_files = glob.glob(f"{TRANS_DIR}/*.txt")
    print(f"Trascrizioni: {len(transcript_files)}")

    for path in transcript_files:
        basename = os.path.basename(path).replace('.txt', '')
        ep_num = int(basename)

        with open(path) as f:
            text = f.read()

        # Skip header
        lines = text.split('\n', 2)
        if len(lines) > 2:
            text = lines[2]

        ep_texts[ep_num] = text
        tokens = tokenize(text)

        # Count word frequency in this episode
        word_freq = defaultdict(int)
        for t in tokens:
            word_freq[t] += 1

        # Add to index (skip stopwords and very common words)
        for word, freq in word_freq.items():
            if word not in STOPWORDS and len(word) >= 4:
                index[word].add(ep_num)

    # Convert sets to sorted lists
    index_json = {}
    for word, eps in index.items():
        # Only keep words that appear in at most 80% of episodes (too common = useless)
        if len(eps) < len(ep_texts) * 0.8:
            index_json[word] = sorted(eps)

    # Save index
    with open(f"{DATA_DIR}/search_index.json", "w") as f:
        json.dump(index_json, f, ensure_ascii=False, separators=(',', ':'))

    index_size = os.path.getsize(f"{DATA_DIR}/search_index.json")

    print(f"Parole nell'indice: {len(index_json):,}")
    print(f"Dimensione indice: {index_size / 1024 / 1024:.1f} MB")

    # Save per-episode snippets as separate small files (for on-demand loading)
    snippets_dir = f"{DATA_DIR}/search_snippets"
    os.makedirs(snippets_dir, exist_ok=True)

    for ep_num, text in ep_texts.items():
        with open(f"{snippets_dir}/{ep_num}.txt", "w") as f:
            f.write(text)

    # Also generate a compact "snippets" version: first 500 chars per episode
    # for the main JSON (so the app can show preview without loading full transcript)
    for ep in data["episodes"]:
        ep_num = ep["episode_number"]
        if ep_num in ep_texts:
            text = ep_texts[ep_num]
            # First 500 chars, cut at word boundary
            snippet = text[:500].rsplit(' ', 1)[0] + "..." if len(text) > 500 else text
            ep["transcript_snippet"] = snippet

    with open(f"{DATA_DIR}/episodes_tagged.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nIndice pronto. L'app può cercare in {len(ep_texts)} trascrizioni.")


if __name__ == "__main__":
    main()
