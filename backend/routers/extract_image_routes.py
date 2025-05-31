from fastapi import APIRouter, Body, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl
import sys
import os
import asyncio
from utils.extract_images import extract_video_id, parse_transcript, get_stream_url, extract_frames_python

extract_router = APIRouter(prefix="/api/frames", tags=["frames"])

class HighlightItem(BaseModel):
    timestamp: str
    description: str
    type: Optional[str] = "visual"

class FrameExtractionRequest(BaseModel):
    video_url: HttpUrl
    transcript_highlights: List[HighlightItem]

class FrameExtractionResponse(BaseModel):
    video_id: str
    frames_directory: str
    extracted_frames: List[str]

@extract_router.post("/", response_model=FrameExtractionResponse)
async def extract_video_frames(background_tasks: BackgroundTasks, request: FrameExtractionRequest = Body(...)):
    """Extract frames from a YouTube video based on transcript highlights.
    Processes in the background after initial response."""
    
    try:
        video_id = extract_video_id(str(request.video_url))
        output_image_dir = f"frames_{video_id}"
        
        formatted_transcript = "\n".join([
            f"{item.timestamp} - {item.type if item.type else 'visual'} - {item.description}" 
            for item in request.transcript_highlights
        ])
        
        timestamps = parse_transcript(formatted_transcript)
        
        if not timestamps:
            raise HTTPException(
                status_code=400,
                detail="No valid visual timestamps found in the highlights"
            )
        
        def process_video_frames():
            try:
                stream_url = get_stream_url(str(request.video_url))
                extract_frames_python(stream_url, timestamps, output_image_dir)

            except Exception as e:
                print(f"Background task error: {str(e)}")
        
        background_tasks.add_task(process_video_frames)
        

        frame_filenames = [filename for _, filename in timestamps]
        
        return {
            "video_id": video_id, 
            "frames_directory": output_image_dir, 
            "extracted_frames": frame_filenames
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract frames: {str(e)}")

@extract_router.get("/status/{video_id}")
async def check_extraction_status(video_id: str):
    """Check the status of frame extraction for a specific video."""
    
    try:
        output_image_dir = f"frames_{video_id}"
        
        if not os.path.exists(output_image_dir):
            return {"status": "not_started", "frames": []}
        
        frames = os.listdir(output_image_dir)
        
        if not frames:
            return {"status": "in_progress", "frames": []}
        
        return {"status": "completed", "frames": frames, "frames_directory": output_image_dir}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check extraction status: {str(e)}")