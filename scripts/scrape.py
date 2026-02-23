#!/usr/bin/env python3
"""
scrape.py — Scarica i metadati di tutti i video dal canale YouTube di Tintoria.
Usa yt-dlp in modalità flat-playlist (solo metadati, nessun download).

Requisiti: pip install yt-dlp

Output: raw_playlist.jsonl (un JSON per riga, un video per riga)
"""

import subprocess
import sys
import os

CHANNEL_URL = "https://www.youtube.com/@TintoriaPodcast/videos"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw_playlist.jsonl")

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        CHANNEL_URL,
    ]

    print(f"Scaricamento metadati da {CHANNEL_URL}...")
    print(f"Output: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w") as f:
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

    if proc.returncode != 0:
        print(f"Errore: {proc.stderr}", file=sys.stderr)
        sys.exit(1)

    # Conta le righe
    with open(OUTPUT_FILE) as f:
        count = sum(1 for _ in f)

    print(f"Completato: {count} video estratti.")
    print(f"Esegui build_data.py per generare i file strutturati.")

if __name__ == "__main__":
    main()
