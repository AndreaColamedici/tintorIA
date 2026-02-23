#!/usr/bin/env python3
"""
build_transcripts.py — Converte gli SRT auto-generati in testo pulito.
Rimuove timestamp, numeri di sequenza, e duplicati da sovrapposizione.
Produce:
  - data/transcripts/{episode_number}.txt (testo pulito per puntata)
  - Aggiorna episodes_tagged.json con campo 'transcript' (snippet) e 'has_transcription'
"""

import json, os, re, glob

DATA_DIR = "data"
SUBS_DIR = f"{DATA_DIR}/subs"
TRANS_DIR = f"{DATA_DIR}/transcripts"
TAGGED_FILE = f"{DATA_DIR}/episodes_tagged.json"

os.makedirs(TRANS_DIR, exist_ok=True)


def clean_srt(srt_text):
    """Parse SRT and produce clean, deduplicated text."""
    # Split into blocks (separated by blank lines)
    blocks = re.split(r'\n\s*\n', srt_text.strip())

    lines_seen = []
    for block in blocks:
        block_lines = block.strip().split('\n')
        # SRT blocks: index, timestamp, text (1+ lines)
        text_lines = []
        for line in block_lines:
            line = line.strip()
            # Skip sequence numbers and timestamps
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'\d{2}:\d{2}:\d{2}', line):
                continue
            if line:
                text_lines.append(line)

        text = ' '.join(text_lines).strip()
        if text:
            lines_seen.append(text)

    # Deduplicate overlapping lines (auto-subs repeat a lot)
    # Strategy: keep a line only if it adds new content vs previous
    cleaned = []
    prev = ""
    for line in lines_seen:
        # If line is fully contained in previous, skip
        if line in prev:
            continue
        # If previous is fully contained in line (extension), replace
        if prev in line and prev:
            if cleaned:
                cleaned[-1] = line
            else:
                cleaned.append(line)
        else:
            cleaned.append(line)
        prev = line

    # Join into paragraphs (new paragraph every ~500 chars for readability)
    full_text = ' '.join(cleaned)

    # Clean up multiple spaces
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    # Remove ">> " speaker markers from auto-subs
    full_text = full_text.replace('>> ', '')

    # Break into paragraphs every ~5 sentences (roughly)
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    paragraphs = []
    current = []
    for s in sentences:
        current.append(s)
        if len(current) >= 6:
            paragraphs.append(' '.join(current))
            current = []
    if current:
        paragraphs.append(' '.join(current))

    return '\n\n'.join(paragraphs)


def main():
    with open(TAGGED_FILE) as f:
        data = json.load(f)

    # Build a map of youtube_id → episode
    id_to_ep = {ep["youtube_id"]: ep for ep in data["episodes"]}

    # Process all SRT files
    srt_files = glob.glob(f"{SUBS_DIR}/*.it.srt")
    print(f"File SRT trovati: {len(srt_files)}")

    processed = 0
    total_words = 0

    for srt_path in srt_files:
        filename = os.path.basename(srt_path)
        video_id = filename.replace('.it.srt', '')

        ep = id_to_ep.get(video_id)
        if not ep:
            continue

        with open(srt_path, encoding='utf-8', errors='replace') as f:
            srt_text = f.read()

        clean_text = clean_srt(srt_text)

        if len(clean_text) < 50:
            continue

        # Save transcript
        ep_num = ep["episode_number"]
        out_path = f"{TRANS_DIR}/{ep_num:03d}.txt"
        with open(out_path, 'w') as f:
            f.write(f"# Tintoria #{ep_num} — {ep['guest']}\n\n")
            f.write(clean_text)

        # Update episode record
        ep["has_transcription"] = True
        words = len(clean_text.split())
        total_words += words
        ep["transcript_words"] = words
        # Store a snippet (first 300 chars) for search preview
        ep["transcript_snippet"] = clean_text[:300].rsplit(' ', 1)[0] + "..."

        processed += 1

    # Update JSON
    data["meta"]["transcriptions_count"] = processed
    data["meta"]["total_transcript_words"] = total_words

    with open(TAGGED_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nTrascrizioni processate: {processed}")
    print(f"Parole totali: {total_words:,}")
    avg = total_words // processed if processed else 0
    print(f"Media per puntata: ~{avg:,} parole")

    # Show a sample
    sample = [ep for ep in data["episodes"] if ep.get("has_transcription")]
    if sample:
        s = sample[len(sample)//2]
        print(f"\nCampione — #{s['episode_number']} {s['guest']}:")
        print(f"  Parole: {s['transcript_words']}")
        print(f"  Snippet: {s['transcript_snippet'][:150]}...")


if __name__ == "__main__":
    main()
