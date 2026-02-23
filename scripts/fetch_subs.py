#!/usr/bin/env python3
"""
fetch_subs.py — Scarica i sottotitoli auto-generati italiani da YouTube
per tutte le puntate di Tintoria. Usa yt-dlp.
Salva in data/subs/{youtube_id}.srt
Output: data/subs_status.json con lo stato di ogni download.
"""

import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA_DIR = "data"
SUBS_DIR = f"{DATA_DIR}/subs"
STATUS_FILE = f"{DATA_DIR}/subs_status.json"
TAGGED_FILE = f"{DATA_DIR}/episodes_tagged.json"

os.makedirs(SUBS_DIR, exist_ok=True)

def fetch_sub(video_id, ep_num, guest):
    """Download Italian auto-subs for a single video."""
    out_path = os.path.join(SUBS_DIR, video_id)
    srt_path = f"{out_path}.it.srt"

    # Skip if already downloaded
    if os.path.exists(srt_path) and os.path.getsize(srt_path) > 100:
        return video_id, ep_num, guest, "cached", os.path.getsize(srt_path)

    try:
        result = subprocess.run(
            ["yt-dlp",
             "--write-auto-sub",
             "--sub-lang", "it",
             "--sub-format", "srt",
             "--skip-download",
             "--no-warnings",
             "-o", out_path,
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=60
        )

        if os.path.exists(srt_path) and os.path.getsize(srt_path) > 100:
            return video_id, ep_num, guest, "ok", os.path.getsize(srt_path)
        else:
            return video_id, ep_num, guest, "no_subs", 0
    except subprocess.TimeoutExpired:
        return video_id, ep_num, guest, "timeout", 0
    except Exception as e:
        return video_id, ep_num, guest, f"error: {e}", 0


def main():
    with open(TAGGED_FILE) as f:
        data = json.load(f)

    episodes = data["episodes"]
    print(f"Episodi totali: {len(episodes)}")

    # Load existing status
    status = {}
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE) as f:
            status = json.load(f)

    done = 0
    total = len(episodes)
    ok_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(fetch_sub, ep["youtube_id"], ep["episode_number"], ep["guest"]): ep
            for ep in episodes
        }

        for future in as_completed(futures):
            vid, ep_num, guest, result, size = future.result()
            done += 1

            status[vid] = {"status": result, "size": size, "episode": ep_num}

            if result in ("ok", "cached"):
                ok_count += 1
                size_kb = size / 1024
                print(f"  [{done}/{total}] ✓ #{ep_num} {guest} ({size_kb:.0f}KB)")
            else:
                fail_count += 1
                print(f"  [{done}/{total}] ✗ #{ep_num} {guest} — {result}")

            # Save incrementally
            if done % 25 == 0:
                with open(STATUS_FILE, "w") as f:
                    json.dump(status, f, indent=2)

    # Final save
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

    print(f"\nCompletato: {ok_count} ok, {fail_count} falliti su {total}")

if __name__ == "__main__":
    main()
