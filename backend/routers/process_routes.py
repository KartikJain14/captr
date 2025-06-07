import os
import shutil
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import asyncio
import google.generativeai as genai
from utils.transcribe import process_video
from utils.extract_images import extract_video_id, extract_frames_python, get_stream_url, parse_transcript

process_router = APIRouter(prefix="/api/process", tags=["process"])

class FullProcessingRequest(BaseModel):
    video_url: str

class FullProcessingResponse(BaseModel):
    video_id: str
    url: str
    transcript_highlights: List[Dict[str, str]]
    frames_directory: str
    extracted_frames: List[str]
    markdown_document: str
    status: str = "completed"

@process_router.post("/full", response_model=FullProcessingResponse)
async def process_video_fully(request: FullProcessingRequest):
    try:
        video_url = request.video_url
        video_id = extract_video_id(video_url)
        video_info = {"video_id": video_id, "url": video_url}
        
        # Get transcript and highlights
        transcript_data = await process_video(video_url)
        transcript_highlights = transcript_data["highlights"]
        
        # Extract frames based on highlights
        frames_directory = f"frames_{video_id}"
        os.makedirs(frames_directory, exist_ok=True)
        
        formatted_transcript = "\n".join([
            f"{item['timestamp']} - visual - {item['description']}" 
            for item in transcript_highlights
        ])
        
        timestamps = parse_transcript(formatted_transcript)
        
        # Extract frames
        try:
            stream_url = get_stream_url(video_url)
            extracted_frames = extract_frames_python(stream_url, timestamps, frames_directory)
        except Exception as e:
            logging.error(f"Frame extraction error: {str(e)}")
            extracted_frames = []
        
        # Create a dedicated folder for this research document
        docs_dir = "research_documents"
        os.makedirs(docs_dir, exist_ok=True)
        
        document_folder = os.path.join(docs_dir, f"{video_id}_research")
        os.makedirs(document_folder, exist_ok=True)
        
        # Create images subfolder
        images_folder = os.path.join(document_folder, "images")
        os.makedirs(images_folder, exist_ok=True)
        
        # Generate markdown with local image references
        markdown = f"# Research Document: {video_id}\n\n"
        markdown += f"Video URL: {video_url}\n\n"
        
        copied_images = []
        
        # Process highlights and generate concise notes with Gemini
        for i, highlight in enumerate(transcript_highlights):
            markdown += f"## {i+1}. {highlight['description']}\n\n"
            markdown += f"Timestamp: {highlight['timestamp']}\n\n"
            
            # Find matching frame
            matching_frames = [f for f in extracted_frames 
                              if highlight['timestamp'].replace(':', '_') in f]
            
            if matching_frames:
                original_frame_path = os.path.join(frames_directory, matching_frames[0])
                if os.path.exists(original_frame_path):
                    # Copy image to the document's images folder
                    dest_filename = matching_frames[0]
                    dest_path = os.path.join(images_folder, dest_filename)
                    
                    shutil.copy2(original_frame_path, dest_path)
                    copied_images.append(dest_filename)
                    
                    # Add image reference to markdown (using relative path)
                    markdown += f"![{highlight['description']}](images/{dest_filename})\n\n"
            
            # Generate concise notes with Gemini
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            Create concise educational notes (maximum 150 words) for this concept from a video:

            Topic: {highlight['description']}
            Timestamp: {highlight['timestamp']}

            Your notes should:
            1. Explain the key concept clearly
            2. Include only essential points
            3. Use bullet points where appropriate
            4. Be under 150 words total

            Format as Markdown.
            """
            
            try:
                response = model.generate_content(prompt)
                markdown += f"{response.text}\n\n"
            except Exception as e:
                logging.error(f"Error generating notes: {str(e)}")
                markdown += "Notes unavailable for this segment.\n\n"
            
            markdown += "---\n\n"
        
        # Generate concise summary
        try:
            summary_prompt = f"""
            Create a brief summary (maximum 100 words) of this video content:

            Video topic areas: {', '.join([h['description'] for h in transcript_highlights])}
            
            Include:
            - Main theme or purpose
            - 2-3 key takeaways
            - Keep under 200 words total
            """
            
            summary_response = model.generate_content(summary_prompt)
            markdown += f"## Summary\n\n{summary_response.text}\n\n"
        except Exception as e:
            logging.error(f"Error generating summary: {str(e)}")
        
        # Save markdown to file with video ID as filename
        markdown_filename = f"{video_id}.md"
        markdown_path = os.path.join(document_folder, markdown_filename)
        
        with open(markdown_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown)
        
        # Clean up original image directory after copying relevant images
        if os.path.exists(frames_directory):
            shutil.rmtree(frames_directory)
            logging.info(f"Deleted original image directory: {frames_directory}")
        
        return FullProcessingResponse(
            video_id=video_id,
            url=video_url,
            transcript_highlights=transcript_highlights,
            frames_directory=document_folder,
            extracted_frames=copied_images,
            markdown_document=markdown,
            status="completed"
        )

    except Exception as e:
        logging.exception("Error in /full processing route")
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
