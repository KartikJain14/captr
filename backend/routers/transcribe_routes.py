from fastapi import APIRouter, Query, HTTPException, Body
from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl
import sys
import os
import asyncio
from utils.transcribe import process_video, analyze_visual_segments

transcribe_router = APIRouter(prefix="/api/transcript", tags=["transcript"])

class TranscriptRequest(BaseModel):
    transcript: str

class VideoRequest(BaseModel):
    url: HttpUrl

@transcribe_router.get("/")
async def get_transcript(url: str = Query(..., description="YouTube video URL")):
    """Get transcript and highlighted segments from a YouTube video."""

    try:
        result = await process_video(url)
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process video transcript: {str(e)}"
        )

@transcribe_router.post("/analyze")
async def analyze_transcript(request: TranscriptRequest):
    """Analyze an existing transcript for visual segments."""
    
    try:
        highlights = await analyze_visual_segments(request.transcript)
        return {"highlights": highlights}
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to analyze transcript: {str(e)}"
        )