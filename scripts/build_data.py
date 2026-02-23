#!/usr/bin/env python3
"""
build_data.py — Elabora il dump grezzo di yt-dlp e produce:
  - data/episodes.json (strutturato, solo puntate numerate)
  - data/episodes_raw.json (dump completo pulito)
  - data/tintoria.db (SQLite)
"""

import json, re, sqlite3, os
from datetime import datetime

RAW = "raw_playlist.jsonl"
OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# --- 1. Leggi il dump grezzo ---
videos = []
with open(RAW) as f:
    for line in f:
        videos.append(json.loads(line))

print(f"Video totali letti: {len(videos)}")

# --- 2. Parsing: separa puntate numerate da extra ---
episode_pattern = re.compile(r'Tintoria\s*#(\d+)\s+(.*)', re.IGNORECASE)

episodes = []
extras = []

for v in videos:
    title = v.get("title", "")
    m = episode_pattern.match(title)

    duration_s = v.get("duration") or 0
    hours = int(duration_s // 3600)
    minutes = int((duration_s % 3600) // 60)
    seconds = int(duration_s % 60)
    if hours:
        duration_fmt = f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        duration_fmt = f"{minutes}:{seconds:02d}"

    # Thumbnail migliore
    thumbs = v.get("thumbnails", [])
    thumb_url = thumbs[-1]["url"] if thumbs else ""

    record = {
        "youtube_id": v["id"],
        "title": title,
        "description": v.get("description", ""),
        "duration_seconds": int(duration_s),
        "duration_formatted": duration_fmt,
        "view_count": v.get("view_count", 0),
        "thumbnail_url": thumb_url,
        "youtube_url": f"https://www.youtube.com/watch?v={v['id']}",
    }

    if m:
        ep_num = int(m.group(1))
        guest = m.group(2).strip()
        record["episode_number"] = ep_num
        record["guest"] = guest
        record["is_numbered"] = True
        episodes.append(record)
    else:
        record["episode_number"] = None
        record["guest"] = None
        record["is_numbered"] = False
        extras.append(record)

episodes.sort(key=lambda x: x["episode_number"])

# Statistiche
unique_guests = set(e["guest"] for e in episodes if e["guest"])
total_views = sum(v.get("view_count", 0) for v in videos)

# Numeri puntate presenti
present = set(e["episode_number"] for e in episodes)
expected = set(range(1, max(present) + 1)) if present else set()
missing = sorted(expected - present)

print(f"Puntate numerate: {len(episodes)} (dalla #{min(present)} alla #{max(present)})")
print(f"Video extra: {len(extras)}")
print(f"Ospiti unici: {len(unique_guests)}")
print(f"Views totali: {total_views:,.0f}")
if missing:
    # Raggruppa i numeri mancanti in range
    ranges = []
    start = missing[0]
    end = missing[0]
    for n in missing[1:]:
        if n == end + 1:
            end = n
        else:
            ranges.append(f"#{start}-#{end}" if start != end else f"#{start}")
            start = end = n
    ranges.append(f"#{start}-#{end}" if start != end else f"#{start}")
    print(f"Puntate mancanti: {', '.join(ranges)} ({len(missing)} totali)")

# --- 3. Salva JSON ---
with open(f"{OUT_DIR}/episodes.json", "w") as f:
    json.dump({
        "meta": {
            "total_episodes": len(episodes),
            "total_extras": len(extras),
            "unique_guests": len(unique_guests),
            "total_views": total_views,
            "missing_episodes": missing,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        },
        "episodes": episodes,
        "extras": extras
    }, f, ensure_ascii=False, indent=2)

# Raw completo (tutti i campi utili)
raw_clean = []
for v in videos:
    thumbs = v.get("thumbnails", [])
    raw_clean.append({
        "id": v["id"],
        "title": v.get("title", ""),
        "description": v.get("description", ""),
        "duration": v.get("duration"),
        "duration_string": v.get("duration_string"),
        "view_count": v.get("view_count"),
        "channel": v.get("channel"),
        "thumbnails": [t.get("url") for t in thumbs] if thumbs else [],
        "url": f"https://www.youtube.com/watch?v={v['id']}",
        "availability": v.get("availability"),
        "live_status": v.get("live_status"),
    })

with open(f"{OUT_DIR}/episodes_raw.json", "w") as f:
    json.dump(raw_clean, f, ensure_ascii=False, indent=2)

print(f"\nJSON salvati in {OUT_DIR}/")

# --- 4. Database SQLite ---
db_path = f"{OUT_DIR}/tintoria.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
CREATE TABLE episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    youtube_id TEXT UNIQUE NOT NULL,
    episode_number INTEGER,
    title TEXT NOT NULL,
    guest TEXT,
    upload_date TEXT,
    duration_seconds INTEGER,
    duration_formatted TEXT,
    description TEXT,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER,
    thumbnail_url TEXT,
    youtube_url TEXT,
    tags TEXT,
    has_transcription INTEGER DEFAULT 0,
    is_numbered INTEGER DEFAULT 1
)
""")

c.execute("""
CREATE TABLE guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    episode_count INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    first_appearance INTEGER,
    last_appearance INTEGER
)
""")

c.execute("""
CREATE TABLE transcriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER NOT NULL,
    text TEXT,
    segments TEXT,
    language TEXT DEFAULT 'it',
    model TEXT,
    created_at TEXT,
    FOREIGN KEY (episode_id) REFERENCES episodes(id)
)
""")

# Inserisci episodi
all_records = episodes + extras
for ep in all_records:
    c.execute("""
        INSERT INTO episodes (youtube_id, episode_number, title, guest,
            duration_seconds, duration_formatted, description, view_count,
            thumbnail_url, youtube_url, is_numbered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ep["youtube_id"], ep["episode_number"], ep["title"], ep["guest"],
        ep["duration_seconds"], ep["duration_formatted"], ep["description"],
        ep["view_count"], ep["thumbnail_url"], ep["youtube_url"],
        1 if ep["is_numbered"] else 0
    ))

# Inserisci ospiti
guest_stats = {}
for ep in episodes:
    g = ep["guest"]
    if g not in guest_stats:
        guest_stats[g] = {"count": 0, "views": 0, "first": ep["episode_number"], "last": ep["episode_number"]}
    guest_stats[g]["count"] += 1
    guest_stats[g]["views"] += ep["view_count"] or 0
    guest_stats[g]["last"] = max(guest_stats[g]["last"], ep["episode_number"])

for name, stats in guest_stats.items():
    c.execute("""
        INSERT INTO guests (name, episode_count, total_views, first_appearance, last_appearance)
        VALUES (?, ?, ?, ?, ?)
    """, (name, stats["count"], stats["views"], stats["first"], stats["last"]))

conn.commit()
conn.close()

print(f"Database SQLite creato: {db_path}")
print(f"\nDone!")
