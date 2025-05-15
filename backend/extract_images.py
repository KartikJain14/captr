import os
import re
import string
import ffmpeg
from yt_dlp import YoutubeDL

def sanitize_filename(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return "_".join(words[:6])

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else "video"

def parse_transcript(transcript):
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

def get_stream_url(video_url):
    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [info])
        best = max(formats, key=lambda f: f.get('height', 0) or 0)
        return best['url']

def extract_frames_python(stream_url, timestamps, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for ts, filename in timestamps:
        output_path = os.path.join(output_dir, filename)
        print(f"🖼️ Extracting frame at {ts} -> {output_path}")
        try:
            (
                ffmpeg
                .input(stream_url, ss=ts)
                .output(output_path, vframes=1)
                .run(quiet=True)
            )
        except ffmpeg.Error as e:
            print(f"❌ Failed to extract {filename}: {e}")

    print("🎉 All visual frames extracted successfully.")

def run(video_url, transcript_text):
    video_id = extract_video_id(video_url)
    output_image_dir = f"frames_{video_id}"

    print("🔍 Getting direct video stream URL...")
    stream_url = get_stream_url(video_url)

    timestamps = parse_transcript(transcript_text)
    extract_frames_python(stream_url, timestamps, output_image_dir)

if __name__ == "__main__":
    transcript = """
    00:20 - visual - Diagram showing the seven objects, their weights, and profits, and the knapsack with its capacity of 15kg.
    06:30 - visual - Table showing the calculation of profit/weight for each object.
    07:16 - text - Detailed explanation of the greedy approach for solving the fractional knapsack problem.
    14:38 - text - Differences between fractional knapsack and 0/1 knapsack problems.
    """
    video_url = "https://www.youtube.com/watch?v=oTTzNMHM05I"
    run(video_url, transcript)
