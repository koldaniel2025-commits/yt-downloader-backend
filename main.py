from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|\/|be\/)([\w-]{11})", url)
    return match.group(1) if match else ""

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/api/download")
def get_video_info(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing URL parameter")
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "videoQuality": "max"
    }
    
    try:
        response = requests.post("https://api.cobalt.tools/", json=payload, headers=headers, timeout=12)
        data = response.json()
        
        if response.status_code != 200 or data.get("status") in ["error", "rate-limit"]:
            error_msg = data.get("text", "לא ניתן לחלץ את הסרטון")
            raise HTTPException(status_code=500, detail=error_msg)
            
        video_id = extract_video_id(url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else None
        
        return {
            "title": "סרטון YouTube",
            "thumbnail": thumbnail_url,
            "download_url": data.get("url")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
