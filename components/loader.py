from youtube_transcript_api import YouTubeTranscriptApi

def load_youtube_transcript(video_id: str):
    api = YouTubeTranscriptApi()

    transcript = api.fetch("7ARBJQn6QkM")

    documents = []

    for entry in transcript:
        documents.append({
            "text": entry.text,
            "start": entry.start,
            "end": entry.start + entry.duration
        })

    return documents