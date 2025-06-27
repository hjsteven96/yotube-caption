import traceback
from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, InvalidVideoId

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to YouTube Transcript API"}

@app.get("/transcript")
async def get_transcript(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_list
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="Transcript not found for this video. It might be unavailable, private, or transcription is disabled.")
    except InvalidVideoId:
        raise HTTPException(status_code=400, detail="Invalid YouTube video ID. Please check the video ID.")
    except Exception as e:
        # Log the full traceback for unexpected errors
        print(f"An unexpected error occurred for video ID {video_id}:\n{traceback.format_exc()}")
        # For generic XML parsing errors, treat as transcript not found or unavailable
        if "no element found" in str(e).lower() or "failed to parse" in str(e).lower() or "transcription is disabled" in str(e).lower():
            raise HTTPException(status_code=404, detail="Failed to retrieve or parse transcript. The video might not have transcripts, it might be restricted, or transcription is disabled.")
        else:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") 