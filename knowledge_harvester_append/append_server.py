import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import uvicorn

app = FastAPI(title="ChatGPT Harvest - Append Mode")

# Allow CORS for the extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaptureData(BaseModel):
    html: str
    source: str

MASTER_FILE = Path("master_harvest.html")
TEMPLATE_FILE = Path("master_template.html")

def init_master_file():
    """Initializes the master file if it doesn't exist."""
    if not MASTER_FILE.exists():
        if TEMPLATE_FILE.exists():
            with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            # Replace placeholder with an append marker
            marker = "\n        <!-- APPEND_HERE -->\n"
            initial_content = content.replace("{{CONTENT_PLACEHOLDER}}", marker)
            with open(MASTER_FILE, 'w', encoding='utf-8') as f:
                f.write(initial_content)
        else:
            # Fallback basic template if master_template.html is missing
            with open(MASTER_FILE, 'w', encoding='utf-8') as f:
                f.write("<html><body><!-- APPEND_HERE --></body></html>")

def append_to_master(new_html: str, source: str):
    """Appends new content to the master file before the marker."""
    init_master_file()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Wrap new content with a separator and metadata
    wrapped_content = f"""
    <div class="harvest-entry" style="margin-top: 60px; border-top: 2px solid #374151; padding-top: 30px; margin-bottom: 20px;">
        <div class="metadata" style="color: #9ca3af; font-family: sans-serif; font-size: 0.9em; margin-bottom: 15px; background: #1f2937; padding: 10px; border-radius: 6px; display: inline-block;">
            <b>Captured:</b> {timestamp} | <b>Platform:</b> {source}
        </div>
        <div class="content">
            {new_html}
        </div>
    </div>
    <!-- APPEND_HERE -->
    """
    
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    if "<!-- APPEND_HERE -->" in full_content:
        updated_content = full_content.replace("<!-- APPEND_HERE -->", wrapped_content)
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    else:
        # Emergency recovery if marker is lost
        with open(MASTER_FILE, 'a', encoding='utf-8') as f:
            f.write(wrapped_content)

@app.post("/")
async def capture(data: CaptureData):
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, append_to_master, data.html, data.source)
        web_url = f"http://localhost:8771/view"
        return {"status": "success", "url": web_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/view")
async def view_master():
    if MASTER_FILE.exists():
        return FileResponse(MASTER_FILE)
    return HTMLResponse("<h1>No captures yet.</h1>")

def run():
    print("\n" + "="*60)
    print("HARVEST APPEND SERVER RUNNING ON 8771")
    print("Single File Mode: master_harvest.html")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8771, log_level="warning")

if __name__ == "__main__":
    run()
