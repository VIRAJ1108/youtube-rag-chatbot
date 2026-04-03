from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi


def load_youtube_transcript(video_id):
    
    # 🔹 Try best method first (structured)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        entries = []
        for entry in transcript:
            entries.append({
                "text": entry.text,
                "start": entry.start,
                "end": entry.start + entry.duration
            })

        return entries

    except Exception as e:
        print("Primary method failed:", e)

    # 🔹 Fallback (cloud-friendly)
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        loader = YoutubeLoader.from_youtube_url(url)
        docs = loader.load()

        entries = []
        for doc in docs:
            entries.append({
                "text": doc.page_content,
                "start": doc.metadata.get("start", 0),
                "end": doc.metadata.get("end", 0)
            })

        return entries

    except Exception as e:
        print("Fallback method failed:", e)
        return None