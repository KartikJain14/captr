from fastapi import APIRouter, Body, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
from utils.transcribe import process_video
from utils.extract_images import extract_video_id, extract_frames_python, get_stream_url, parse_transcript
from pydantic import BaseModel, HttpUrl
import os

process_router = APIRouter(prefix="/api/process", tags=["process"])

class VideoProcessingRequest(BaseModel):
    video_url: str

class VideoProcessingResponse(BaseModel):
    video_id: str
    url: str
    transcript_highlights: List[Dict[str, str]]
    frames_directory: Optional[str] = None
    extracted_frames: Optional[List[str]] = None
    status: str = "processing"

def get_video_info(url: str) -> Dict:
    video_id = extract_video_id(url)
    return {
        "video_id": video_id,
        "url": url
    }

def compile_research_document(video_info: Dict, transcript_data: Dict, key_frames: Dict) -> Dict:
    return {
        "video_id": video_info["video_id"],
        "url": video_info["url"],
        "transcript_highlights": transcript_data["highlights"],
        "frames_directory": key_frames.get("frames_directory"),
        "extracted_frames": key_frames.get("extracted_frames", []),
        "status": "completed"
    }

@process_router.post("/video", response_model=VideoProcessingResponse)
async def process_youtube_video(
    request: VideoProcessingRequest,
    background_tasks: BackgroundTasks
):
    try:
        video_url = request.video_url
        
        # 1. Get video info
        video_info = get_video_info(video_url)
        
        # 2. Process video to get transcript and highlights
        transcript_data = await process_video(video_url)
        
        # 3. Extract frames based on highlights
        video_id = video_info["video_id"]
        output_image_dir = f"frames_{video_id}"
        os.makedirs(output_image_dir, exist_ok=True)
        
        # Format transcript highlights for frame extraction
        formatted_transcript = "\n".join([
            f"{item['timestamp']} - visual - {item['description']}" 
            for item in transcript_data["highlights"]
        ])
        
        timestamps = parse_transcript(formatted_transcript)
        frame_filenames = [filename for _, filename in timestamps]
        
        # Add frame extraction as background task
        async def extract_frames_background():
            try:
                stream_url = get_stream_url(video_url)
                extract_frames_python(stream_url, timestamps, output_image_dir)
            except Exception as e:
                print(f"Error extracting frames: {str(e)}")
        
        background_tasks.add_task(extract_frames_background)
        
        key_frames = {
            "frames_directory": output_image_dir,
            "extracted_frames": frame_filenames
        }
        
        # 4. Compile final document
        document = compile_research_document(video_info, transcript_data, key_frames)
        
        return VideoProcessingResponse(**document)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")