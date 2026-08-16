from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# הגדרת CORS מלאה כדי ש-Base44 לא יחסום את הבקשה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok", "message": "Server is running"}

@app.get("/api/download")
def get_video_info(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing URL parameter")
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "title": info.get("title", "Video"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "download_url": info.get("url")
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
