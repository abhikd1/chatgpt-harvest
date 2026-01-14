import os
import time
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from render_capture import save_render

app = FastAPI(title="Lightning Capture Server")

# Enable CORS for the extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaptureData(BaseModel):
    html: str
    source: str

@app.post("/")
async def capture(data: CaptureData):
    # Save asynchronously to avoid blocking the response
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # We run the save_render in a threadpool since it's sync file I/O
    loop = asyncio.get_event_loop()
    try:
        # save_render returns the Path object
        filepath = await loop.run_in_executor(None, save_render, data.html, data.source)
        # Convert Path to a web URL
        filename = filepath.name
        web_url = f"http://localhost:8770/renders/{filename}"
        return {"status": "success", "url": web_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/renders/{filename}")
async def get_render(filename: str):
    path = Path("renders") / filename
    if path.exists():
        return FileResponse(path)
    return JSONResponse(status_code=404, content={"message": "File not found"})

def run():
    print("\n" + "="*60)
    print("🚀 FASTAPI LIGHTNING SERVER (FROZEN MODE) ON 8770")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8770, log_level="warning")

if __name__ == "__main__":
    run()
