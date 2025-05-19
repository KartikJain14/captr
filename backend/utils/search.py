import os
import asyncio
import json
from dotenv import load_dotenv
import google.generativeai as genai
import yt_dlp


async def get_youtube_search_queries(user_prompt, model_name="gemini-1.5-flash"):
    """Generate YouTube search queries using Gemini."""

    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)

    gemini_prompt = (
        f"List only 3 concise YouTube search queries to explore the topic: '{user_prompt}'. "
        "Do not include any preamble or extra formatting — just return the 3 search phrases as plain lines."
    )

    # Run synchronous Gemini API call in executor to prevent blocking
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None, lambda: model.generate_content(gemini_prompt)
    )

    search_queries = [
        line.strip()
        for line in response.text.strip().split("\n")
        if line.strip() and not line.lower().startswith("here")
    ]

    return search_queries[:3]


async def search_youtube_video(query, max_results=3):
    """Asynchronously search YouTube videos for a single query."""
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "force_generic_extractor": True,
            "ignoreerrors": True,
            "playlistend": max_results,
        }

        search_query = f"ytsearch{max_results}:{query}"

        # Run yt-dlp in an executor to prevent blocking the event loop
        loop = asyncio.get_running_loop()
        results = await loop.run_in_executor(
            None, lambda: extract_info_with_ytdlp(search_query, ydl_opts)
        )

        videos = []
        for vid in results.get("entries", []):
            if vid:
                video_info = {
                    "title": vid.get("title", "N/A"),
                    "url": f"https://www.youtube.com/watch?v={vid.get('id')}",
                    "view_count": vid.get("view_count", "N/A"),
                    "upload_date": vid.get("upload_date", "N/A"),
                }
                videos.append(video_info)

        return videos

    except Exception as e:
        print(f"Exception in searching '{query}': {e}")
        return []


def extract_info_with_ytdlp(url, options):
    """Extract info using yt-dlp (synchronous function to be run in executor)"""
    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False)


async def search_youtube_videos(search_queries, max_results=3):
    """Asynchronously search YouTube videos for multiple queries."""

    search_tasks = [
        search_youtube_video(query, max_results) for query in search_queries
    ]
    results = await asyncio.gather(*search_tasks)

    # Track unique videos
    unique_videos = {}
    for query, videos in zip(search_queries, results):
        for video in videos:
            if video["url"] not in unique_videos:
                unique_videos[video["url"]] = {"query": query, "video": video}

    # Organize results without duplicates
    final_results = {}
    for query in search_queries:
        final_results[query] = []

    # Add videos back to their original query results
    for entry in unique_videos.values():
        final_results[entry["query"]].append(entry["video"])

    return final_results


async def main():
    """Main async method to orchestrate the search process."""
    try:
        user_prompt = input("Enter a topic or prompt: ")

        search_queries = await get_youtube_search_queries(user_prompt)
        print("\nGenerated Search Queries:")
        for i, q in enumerate(search_queries, 1):
            print(f"{i}. {q}")

        youtube_results = await search_youtube_videos(search_queries)

        print("\nYouTube Results:")
        for query, videos in youtube_results.items():
            print(f"\nQuery: {query}")
            for vid in videos:
                print(f" - {vid['title']}")
                print(f"   URL: {vid['url']}")
                print(f"   Views: {vid['view_count']}")
                print(f"   Upload Date: {vid['upload_date']}")

    except Exception as e:
        print(f"Error in main process: {e}")


if __name__ == "__main__":
    asyncio.run(main())
