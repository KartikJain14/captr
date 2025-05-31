import os
import re
import string
import cv2
import subprocess
from yt_dlp import YoutubeDL

def sanitize_filename(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return "_".join(words[:6])

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return None

def parse_transcript(transcript):
    """Extract timestamps and descriptions from transcript text."""
    timestamps = []
    lines = transcript.strip().split('\n')
    
    pattern = r'(\d{2}:\d{2}:\d{2}|\d{2}:\d{2})\s*-\s*visual\s*-\s*(.+)'
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            timestamp = match.group(1)
            description = match.group(2).strip()
            
            # Ensure timestamp is in HH:MM:SS format
            if len(timestamp) == 5:  # MM:SS format
                timestamp = "00:" + timestamp
                
            # Create sanitized filename
            filename = f"{timestamp.replace(':', '_')}_visual_{sanitize_filename(description)}.png"
            
            timestamps.append((timestamp, filename))
    
    return timestamps

def get_stream_url(video_url):
    """Get direct video stream URL using yt-dlp."""
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info['url']

def extract_frames_python(stream_url, timestamps, output_dir):
    """Extract frames using OpenCV."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video capture
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print(f"Error: Could not open video stream")
            return False
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if fps <= 0:
            print("Warning: Could not determine FPS, using default of 30")
            fps = 30
            
        frame_filenames = []
        
        for timestamp_str, output_filename in timestamps:
            # Parse timestamp (HH:MM:SS)
            parts = timestamp_str.split(':')
            if len(parts) == 3:
                h, m, s = map(int, parts)
                seconds = h * 3600 + m * 60 + s
            else:
                m, s = map(int, parts)
                seconds = m * 60 + s
                
            # Calculate frame number
            frame_number = int(seconds * fps)
            
            if frame_number >= total_frames:
                print(f"⚠️ Timestamp {timestamp_str} exceeds video length, skipping")
                continue
                
            # Set position and read frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if ret:
                output_path = os.path.join(output_dir, output_filename)
                print(f"🖼️ Extracting frame at {timestamp_str} -> {output_path}")
                cv2.imwrite(output_path, frame)
                frame_filenames.append(output_filename)
            else:
                print(f"❌ Failed to extract frame at {timestamp_str}")
        
        # Release resources
        cap.release()
        return frame_filenames
        
    except Exception as e:
        print(f"Error extracting frames: {str(e)}")
        return []

def run(video_url, transcript_text):
    """Main function to extract frames from a video."""
    try:
        video_id = extract_video_id(video_url)
        output_dir = f"frames_{video_id}"
        timestamps = parse_transcript(transcript_text)
        
        if not timestamps:
            print("No visual highlights found in transcript")
            return False
            
        stream_url = get_stream_url(video_url)
        extract_frames_python(stream_url, timestamps, output_dir)
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False