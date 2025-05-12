import os
import asyncio
import json
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai

async def get_youtube_search_queries(user_prompt, model_name='gemini-1.5-flash'):
    """Generate YouTube search queries using Gemini."""

    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)

    gemini_prompt = (
        f"List only 3 concise YouTube search queries to explore the topic: '{user_prompt}'. "
        "Do not include any preamble or extra formatting — just return the 3 search phrases as plain lines.")

    # Run synchronous Gemini API call in executor to prevent blocking
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: model.generate_content(gemini_prompt)
    )

    # Clean up results
    search_queries = [
        line.strip()
        for line in response.text.strip().split("\n")
        if line.strip() and not line.lower().startswith("here")
    ]

    return search_queries[:3]

async def search_youtube_video(query, max_results=10):
    """Asynchronously search YouTube videos for a single query."""
    try:
        # Use subprocess.Popen with asyncio to run non-blocking
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", 
            f"ytsearch{max_results}:{query}", 
            "--dump-json",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for the subprocess to complete
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            print(f"Error searching for '{query}': {stderr.decode()}")
            return []

        videos = []
        for line in stdout.decode().strip().split("\n"):
            if line.strip():
                try:
                    vid = json.loads(line)
                    video_info = {
                        "title": vid.get("title", "N/A"),
                        "url": f"https://www.youtube.com/watch?v={vid.get('id')}",
                        "view_count": vid.get("view_count", "N/A"),
                        "upload_date": vid.get("upload_date", "N/A")
                    }
                    videos.append(video_info)
                except json.JSONDecodeError:
                    print(f"Could not parse JSON for a video in query: {query}")

        return videos

    except Exception as e:
        print(f"Exception in searching '{query}': {e}")
        return []

async def search_youtube_videos(search_queries, max_results=3):
    """Asynchronously search YouTube videos for multiple queries."""
    # Run searches concurrently
    search_tasks = [search_youtube_video(query, max_results) for query in search_queries]
    results = await asyncio.gather(*search_tasks)

    # Track unique videos
    unique_videos = {}
    for query, videos in zip(search_queries, results):
        for video in videos:
            if video['url'] not in unique_videos:
                unique_videos[video['url']] = {
                    'query': query,
                    'video': video
                }

    # Organize results without duplicates
    final_results = {}
    for query in search_queries:
        final_results[query] = []

    # Add videos back to their original query results
    for entry in unique_videos.values():
        final_results[entry['query']].append(entry['video'])

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