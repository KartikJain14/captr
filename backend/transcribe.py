import os
import asyncio
import logging
import sys
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import google.generativeai as genai

# Timestamp format for logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY not found in .env file")
    sys.exit(1)

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


async def fetch_transcript_with_language_fallback(video_id: str) -> tuple:
    """Fetch transcript with language fallback and translation if needed."""
    logging.info(f"Fetching transcript for video ID: {video_id}")
    try:

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            english_transcript = transcript_list.find_transcript(['en'])
            transcript_data = english_transcript.fetch()
            logging.info(f"Found English transcript for video ID: {video_id}")
            return transcript_data, "en", False  
        
        except NoTranscriptFound:
            available_transcript = next(transcript_list._manually_created_transcripts.values().__iter__(), None)
            
            if not available_transcript:
                available_transcript = next(transcript_list._generated_transcripts.values().__iter__(), None)
            
            if available_transcript:
                lang_code = available_transcript.language_code
                transcript_data = available_transcript.fetch()
                logging.info(f"Found transcript in {lang_code} for video ID: {video_id}")
                return transcript_data, lang_code, True  
            else:
                raise NoTranscriptFound(video_id)
                
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logging.error(f"No transcripts available for video ID: {video_id}. Error: {e}")
        raise RuntimeError(f"No transcripts available: {e}")
    except Exception as e:
        logging.exception(f"Transcript fetch failed for video ID: {video_id}")
        raise RuntimeError(f"Transcript fetch failed: {e}")


async def translate_transcript(transcript_data, source_lang):
    """Translate non-English transcript to English using Gemini."""
    logging.info(f"Translating transcript from {source_lang} to English")
    
    transcript_text = "\n".join([
        f"{int(entry['start'])//60:02d}:{int(entry['start'])%60:02d} - {entry['text']}"
        for entry in transcript_data
    ])[:15000]
    
    prompt = (
        f"Translate the following video transcript from {source_lang} to English. "
        "Maintain the timestamp format at the beginning of each line.\n\n"
        f"{transcript_text}"
    )
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        
        translated_text = response.text.strip()
        logging.info(f"Translation completed successfully")
        
        return translated_text
    except Exception as e:
        logging.exception("Failed to translate transcript")
        raise RuntimeError(f"Translation failed: {e}")


async def format_transcript(transcript_data, needs_translation=False, source_lang=None):
    """Format transcript data, translating if necessary."""
    if needs_translation and source_lang:
        translated_text = await translate_transcript(transcript_data, source_lang)
        return translated_text
    else:

        lines = [
            f"{int(entry['start'])//60:02d}:{int(entry['start'])%60:02d} - {entry['text']}"
            for entry in transcript_data
        ]
        return "\n".join(lines)


async def analyze_visual_segments(transcript_text: str) -> list[dict]:
    logging.info("Sending to Gemini for analysis")
    prompt = (
        "You are analyzing a YouTube video transcript from a technical or educational video. "
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


async def process_video(url: str) -> dict:
    """Process video URL - extract transcript and analyze."""
    try:
        video_id = extract_video_id(url)
        logging.info(f"Processing video ID: {video_id}")
        
        transcript_data, lang_code, needs_translation = await fetch_transcript_with_language_fallback(video_id)
        formatted_transcript = await format_transcript(transcript_data, needs_translation, lang_code)
        highlights = await analyze_visual_segments(formatted_transcript)
        
        result = {
            "video_id": video_id,
            "highlights": highlights
        } 
        return result
        
    except Exception as e:
        logging.exception(f"Error processing video: {e}")
        raise RuntimeError(f"Video processing failed: {e}")


async def run(url: str):
    try:
        result = await process_video(url)
            
        print("\n=== Visual Highlights ===")
        for item in result["highlights"]:
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