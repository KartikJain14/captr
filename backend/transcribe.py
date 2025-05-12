import os
import asyncio
import logging
import sys
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Timestamp format for logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY not found in .env file")
    sys.exit(1)

# GEMINI API FOR NOW
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_video_id(url: str) -> str:
    youtube_regex = (
        r"(?:https?://)?(?:www\.)?(?:youtube\.com(?:/[^/]+)?/[^/]+(?:\?v=|/)([a-zA-Z0-9_-]{11}))|(?:youtu\.be/([a-zA-Z0-9_-]{11}))"
    )
    match = re.match(youtube_regex, url)
    
    if match:
        return match.group(1) if match.group(1) else match.group(2)
    else:
        raise ValueError(f"Invalid YouTube URL format: {url}")


async def fetch_transcript(video_id: str) -> str:
    logging.info(f"Fetching transcript for video ID: {video_id}")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        lines = [
            f"{int(entry['start'])//60:02d}:{int(entry['start'])%60:02d} - {entry['text']}"
            for entry in transcript
        ]
        logging.info(f"Transcript fetched successfully with {len(lines)} lines.")
        return "\n".join(lines)
    except Exception as e:
        logging.exception(f"Transcript fetch failed for video ID: {video_id}")
        raise RuntimeError(f"Transcript fetch failed: {e}")


async def analyze_visual_segments(transcript_text: str) -> list[dict]:
    logging.info("Sending to Gemini for analysis")
    prompt = (
    "You are analyzing a YouTube video transcript from a technical or educational video (like a Data Structures & Algorithms tutorial). "
    "Identify two types of important teaching moments:\n"
    "1. Moments where a visual would significantly help (like a diagram, code snippet, recursion tree, etc).\n"
    "2. Moments where the explanation is deep or nuanced and should be elaborated into detailed notes or examples later by an AI.\n\n"
    "For each, return a line in the format:\n"
    "<MM:SS> - <type: visual/text> - <short description of what's being explained or what visual would help>\n\n"
    "Don't add any commentary, headers, or extra formatting. Just the lines.\n\n"
    f"Transcript:\n{transcript_text[:15000]}"
    )

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))

        highlights = []
        for line in response.text.strip().split("\n"):
            if "-" in line:
                parts = line.split("-", 1)
                highlights.append({
                    "timestamp": parts[0].strip(),
                    "description": parts[1].strip()
                })

        logging.info(f"Found {len(highlights)} visual highlight(s).")
        return highlights

    except Exception as e:
        logging.exception("Failed to analyze visual segments.")
        raise RuntimeError(f"Gemini visual analysis failed: {e}")


async def run(url: str):
    try:
        video_id = extract_video_id(url)
        logging.info(f"Video ID extracted: {video_id}")
        transcript = await fetch_transcript(video_id)
        highlights = await analyze_visual_segments(transcript)

        print("\n=== Visual Highlights ===")
        for item in highlights:
            print(f"{item['timestamp']} - {item['description']}")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <YouTube_URL>")
        sys.exit(1)

    video_url = sys.argv[1]
    logging.info(f"Running for video URL: {video_url}")
    asyncio.run(run(video_url))
