import os
import asyncio
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import uvicorn
import re

app = FastAPI(title="ChatGPT Harvest - Editable Log")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaptureData(BaseModel):
    html: str
    source: str

class UpdateData(BaseModel):
    id: str
    html: str

class DeleteData(BaseModel):
    id: str

MASTER_FILE = Path("master_harvest.html")
TEMPLATE_FILE = Path("master_template.html")

def init_master_file():
    """Ensures the master file exists and is structurally sound."""
    if not MASTER_FILE.exists():
        if TEMPLATE_FILE.exists():
            with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            # Ensure the marker is INSIDE the container
            marker = "\n            <!-- APPEND_HERE -->\n        "
            initial_content = content.replace("{{CONTENT_PLACEHOLDER}}", marker)
            with open(MASTER_FILE, 'w', encoding='utf-8') as f:
                f.write(initial_content)
        else:
            with open(MASTER_FILE, 'w', encoding='utf-8') as f:
                f.write('<html><body><div class="container"><!-- APPEND_HERE --></div></body></html>')

def append_to_master(new_html: str, source: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_id = str(uuid.uuid4())
    
    # 🧬 SURGICAL WRAPPING LOGIC (Using unique comments for 100% safe deletion)
    wrapped_content = f"""
        <!-- ENTRY_START_{entry_id} -->
        <div class="harvest-entry" id="{entry_id}" style="margin-top: 50px; border-top: 2px dashed #374151; padding-top: 20px; position: relative;">
            <div class="entry-controls" style="position: absolute; top: 10px; right: 0; display: flex; gap: 10px; opacity: 0.2; transition: opacity 0.3s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.2">
                <button onclick="editEntry('{entry_id}')" class="control-btn edit-btn" title="Edit">✏️</button>
                <button onclick="saveEntry('{entry_id}')" class="control-btn save-btn" style="display:none;" title="Save">💾</button>
                <button onclick="deleteEntry('{entry_id}')" class="control-btn delete-btn" title="Delete">🗑️</button>
            </div>
            <div class="metadata" style="color: #9ca3af; font-size: 0.8em; margin-bottom: 10px;">
                Captured on: {timestamp} | Source: {source}
            </div>
            <div class="content">
                {new_html}
            </div>
        </div>
        <!-- ENTRY_END_{entry_id} -->
        <!-- APPEND_HERE -->
    """
    
    init_master_file()
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    if "<!-- APPEND_HERE -->" not in full_content:
        # Emergency recovery: if marker is gone, re-add it at the end of the container
        if '</div>' in full_content:
            parts = full_content.split('</div>')
            # Assuming last div is container end
            full_content = '</div>'.join(parts[:-1]) + "\n<!-- APPEND_HERE -->\n</div>" + parts[-1]

    updated_content = full_content.replace("<!-- APPEND_HERE -->", wrapped_content)
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)

@app.post("/")
async def capture(data: CaptureData):
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, append_to_master, data.html, data.source)
        return {"status": "success", "url": "http://localhost:8771/view"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/update")
async def update_entry(data: UpdateData):
    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 🧬 Split-Based Surgical Replacement
        start_marker = f"<!-- ENTRY_START_{data.id} -->"
        end_marker = f"<!-- ENTRY_END_{data.id} -->"
        
        if start_marker not in content or end_marker not in content:
            return JSONResponse(status_code=404, content={"status": "error", "message": "Entry markers lost"})

        prefix, remainder = content.split(start_marker)
        entry_to_modify, suffix = remainder.split(end_marker)
        
        content_prefix = '<div class="content">'
        parts = entry_to_modify.split(content_prefix)
        
        # Preserve the tail (closing divs) of the content region
        # Structure: <div class="content"> [HTML] </div> </div>
        # We find the tail starting from the last </div> </div>
        tail_search = entry_to_modify.rfind('</div>')
        second_last_div = entry_to_modify[:tail_search].rfind('</div>')
        tail = entry_to_modify[second_last_div:]
        
        new_entry_block = parts[0] + content_prefix + f"\n                {data.html}\n            " + tail
        new_content = prefix + start_marker + new_entry_block + end_marker + suffix
        
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/delete")
async def delete_entry(data: DeleteData):
    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        start_marker = f"<!-- ENTRY_START_{data.id} -->"
        end_marker = f"<!-- ENTRY_END_{data.id} -->"
        
        if start_marker not in content:
            return {"status": "success"}

        prefix, remainder = content.split(start_marker)
        _, suffix = remainder.split(end_marker)
        
        new_content = prefix + suffix
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/clear")
async def clear_log():
    try:
        if MASTER_FILE.exists():
            os.remove(MASTER_FILE)
        init_master_file()
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/view")
async def view_master():
    if MASTER_FILE.exists():
        return FileResponse(MASTER_FILE)
    return HTMLResponse("<h1>No captures yet.</h1>")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("HARVEST EDITABLE SERVER RUNNING ON 8771")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8771, log_level="warning")
