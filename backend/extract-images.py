import subprocess
import os
from yt_dlp import YoutubeDL
import re
import string

# === Helper function to sanitize filenames ===
def sanitize_filename(text):
    """
    Convert text to a safe filename by removing punctuation and making it lowercase.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    words = text.split()
    return "_".join(words[:6])  # limit to first 6 words

# === Extract the video ID from the YouTube URL ===
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else "video"

# === Parse the transcript to get timestamps for visual frames ===
def parse_transcript(transcript):
    """
    Parses the transcript and returns a list of timestamps and filenames for visual frames.
    """
    timestamps = []
    lines = transcript.strip().split("\n")
    for line in lines:
        match = re.match(r"(\d{2}:\d{2})\s*-\s*(visual|text)\s*-\s*(.+)", line.strip())
        if match:
            time, type_, desc = match.groups()
            if type_.lower() == "visual":
                full_time = "00:" + time
                safe_desc = sanitize_filename(desc)
                filename = f"{time.replace(':', '_')}_{safe_desc}.png"
                timestamps.append((full_time, filename))
    return timestamps

# === Download the video from YouTube ===
def download_video(video_url, output_path):
    """
    Downloads the video from YouTube using yt-dlp.
    """
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': 'mp4',
        'noplaylist': True
    }

    print("📥 Downloading video...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("✅ Download complete!")

# === Extract frames from the video at given timestamps ===
def extract_frames(video_path, timestamps, output_dir):
    """
    Extracts frames from the video at the specified timestamps.
    """
    print(timestamps)
    print(video_path)
    print(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    for ts, filename in timestamps:
        output_path = os.path.join(output_dir, filename)
        print(filename)
        print(f"🖼️ Extracting frame at {ts} -> {output_path}")
        command = [
            "ffmpeg", "-ss", ts,
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        print(command)
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("🎉 All visual frames extracted successfully.")

# === Main function to run the download and extraction process ===
def run(video_url, transcript_text):
    """
    Main function to handle downloading the video, parsing the transcript, and extracting frames.
    """
    video_id = extract_video_id(video_url)
    output_video_path = f"{video_id}.mp4"
    output_image_dir = f"frames_{video_id}"

    download_video(video_url, output_video_path)
    timestamps = parse_transcript(transcript_text)
    extract_frames(output_video_path, timestamps, output_image_dir)

# === Example usage ===
if __name__ == "__main__":
    transcript = """
    00:20 - visual - Diagram showing the seven objects, their weights, and profits, and the knapsack with its capacity of 15kg.
    06:30 - visual - Table showing the calculation of profit/weight for each object.
    07:16 - text - Detailed explanation of the greedy approach for solving the fractional knapsack problem with multiple examples demonstrating different scenarios (e.g., handling remaining weight capacity after selecting an item).
    14:38 - text - Elaborate on the differences between the fractional knapsack problem and the 0/1 knapsack problem, providing examples for each.
    """
    video_url = "https://www.youtube.com/watch?v=oTTzNMHM05I&list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O&index=40"
    run(video_url, transcript)
