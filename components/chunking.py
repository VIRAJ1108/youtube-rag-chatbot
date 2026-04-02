def create_chunks(transcript_entries, chunk_duration=20):
    chunks = []

    current_chunk = []
    chunk_start = transcript_entries[0]["start"]

    for entry in transcript_entries:
        current_chunk.append(entry)

        current_duration = entry["end"] - chunk_start

        if current_duration >= chunk_duration:
            chunk_text = " ".join([e["text"] for e in current_chunk])

            chunks.append({
                "text": chunk_text,
                "start": chunk_start,
                "end": entry["end"]
            })

            # Reset properly
            current_chunk = []
            chunk_start = entry["end"]   # ✅ important fix

    # last chunk
    if current_chunk:
        chunk_text = " ".join([e["text"] for e in current_chunk])
        chunks.append({
            "text": chunk_text,
            "start": chunk_start,
            "end": current_chunk[-1]["end"]
        })

    return chunks