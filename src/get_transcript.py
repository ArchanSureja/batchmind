import re
import sys
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL"""
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def get_transcript(video_id):
    """Fetch the transcript of the video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"

def save_transcript_to_file(transcript, filename="data/transcript.txt"):
    """Save the transcript to a text file"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcript)
    print(f"Transcript saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <YouTube-Video-URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    video_id = extract_video_id(youtube_url)

    if not video_id:
        print("Invalid YouTube URL.")
        sys.exit(1)

    transcript = get_transcript(video_id)
    save_transcript_to_file(transcript)
