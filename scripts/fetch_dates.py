#!/usr/bin/env python3
"""
fetch_dates.py — Estrae le date di upload per ogni video di Tintoria.
Usa yt-dlp con --skip-download per ottenere i metadati completi (inclusa upload_date).
Processa i video in parallelo con ThreadPoolExecutor per velocità.
Salva risultati incrementalmente in data/dates.json.
"""

import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

DATA_DIR = "data"
DATES_FILE = f"{DATA_DIR}/dates.json"
TAGGED_FILE = f"{DATA_DIR}/episodes_tagged.json"

def fetch_date(video_id):
    """Fetch upload_date for a single video using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "%(upload_date)s",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30
        )
        date_str = result.stdout.strip()
        if date_str and date_str != "NA" and len(date_str) == 8:
            # Format: YYYYMMDD → YYYY-MM-DD
            return video_id, f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return video_id, None
    except Exception as e:
        print(f"  Error {video_id}: {e}", file=sys.stderr)
        return video_id, None

def main():
    # Load episodes
    with open(TAGGED_FILE) as f:
        data = json.load(f)

    # Load existing dates (for incremental updates)
    existing = {}
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE) as f:
            existing = json.load(f)
        print(f"Date già salvate: {len(existing)}")

    # Find which IDs still need dates
    all_ids = [(ep["youtube_id"], ep.get("episode_number"), ep.get("guest"))
               for ep in data["episodes"]]
    to_fetch = [(vid, num, guest) for vid, num, guest in all_ids if vid not in existing]

    print(f"Video totali: {len(all_ids)}")
    print(f"Da scaricare: {len(to_fetch)}")

    if not to_fetch:
        print("Tutte le date sono già presenti!")
        return

    # Fetch in parallel (8 threads — gentle on YouTube)
    dates = dict(existing)
    done = 0
    total = len(to_fetch)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_date, vid): (vid, num, guest)
                   for vid, num, guest in to_fetch}

        for future in as_completed(futures):
            vid, num, guest = futures[future]
            video_id, date = future.result()
            done += 1

            if date:
                dates[video_id] = date
                status = f"✓ {date}"
            else:
                status = "✗ no date"

            print(f"  [{done}/{total}] #{num} {guest} — {status}")

            # Save incrementally every 20 videos
            if done % 20 == 0:
                with open(DATES_FILE, "w") as f:
                    json.dump(dates, f, indent=2)

    # Final save
    with open(DATES_FILE, "w") as f:
        json.dump(dates, f, indent=2)

    found = sum(1 for v in dates.values() if v)
    print(f"\nCompletato: {found}/{len(all_ids)} date trovate.")
    print(f"Salvato in {DATES_FILE}")

if __name__ == "__main__":
    main()
