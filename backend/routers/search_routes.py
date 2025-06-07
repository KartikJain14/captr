from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional
import sys
import os
import asyncio
from utils.search import get_youtube_search_queries, search_youtube_videos

search_router = APIRouter(prefix="/api/search", tags=["search"])

@search_router.get("/")
async def search(prompt: str = Query(..., description="User's search prompt")):
    try:
        search_queries = await get_youtube_search_queries(prompt)

        youtube_results = await search_youtube_videos(search_queries)
        
        return {"search_queries": search_queries, 
                "results": youtube_results}
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to search YouTube videos: {str(e)}"
        )

@search_router.get("/queries")
async def get_queries(prompt: str = Query(..., description="User's search prompt")):
    try:
        search_queries = await get_youtube_search_queries(prompt)
        return {"search_queries": search_queries}
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate search queries: {str(e)}"
        )