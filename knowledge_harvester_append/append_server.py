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
import httpx
from groq import Groq

# GROQ_API_KEY = "gsk_..." # REDACTED FOR SECURITY
def get_groq_key():
    # Try environment variable first
    key = os.getenv("GROQ_API_KEY")
    if key: return key
    
    # Try local file
    key_file = Path("groq_key.txt")
    if key_file.exists():
        k = key_file.read_text().strip()
        if k and not k.startswith("gsk_"):
             print("⚠️ Warning: groq_key.txt does not look like a valid Groq key.")
        return k
    return None

api_key = get_groq_key()
if not api_key or api_key == "PASTE_KEY_HERE":
    print("ERROR: No Groq API Key found. AI features will fail. Create groq_key.txt.")
else:
    print(f"Groq API Key loaded: {api_key[:10]}...")

groq_client = Groq(api_key=api_key or "FAILED_KEY")

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

class BatchDeleteData(BaseModel):
    ids: list[str]

class SummarizeData(BaseModel):
    id: str
    content: str
    system_prompt: str = "You are a research assistant. Provide a concise, 1-sentence TL;DR summary of the following content. Do not say 'Here is the summary' or use any fluff. Just the facts."
    user_prompt: str = ""

MASTER_FILE = Path("master_harvest.html")
TEMPLATE_FILE = Path("master_template.html")

async def generate_tldr(content: str, system_prompt: str = None, user_prompt: str = "", model="llama-3.3-70b-versatile"):
    def _call_groq():
        nonlocal system_prompt
        try:
            if not system_prompt:
                system_prompt = "Summarize this content in exactly one concise, punchy sentence. No fluff."
                
            clean_text = re.sub(r'<[^>]*>', '', content)
            prompt_content = f"{user_prompt}\n\nCONTENT:\n{clean_text[:4000]}" if user_prompt else clean_text[:4000]
            
            print(f"AI Request: Model={model}, PromptLen={len(prompt_content)}")
            
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_content}
                ],
                timeout=45 # Increased timeout for deep reasoning
            )
            res = response.choices[0].message.content.strip()
            print(f"AI Response Received ({len(res)} chars)")
            return res
        except Exception as e:
            err_msg = f"Groq API Error: {type(e).__name__}: {e}"
            print(f"Error: {err_msg}")
            return f"Error: {str(e)}"

    return await asyncio.to_thread(_call_groq)

async def call_ollama(model: str, system_prompt: str, user_prompt: str):
    """Hits the local Ollama API using the correct Chat endpoint."""
    url = "http://localhost:11434/api/chat"
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {"temperature": 0.3}
            })
            if response.status_code == 200:
                res = response.json().get("message", {}).get("content", "").strip()
                return res
            return None
    except Exception as e:
        print(f"Ollama Connection Error ({model}): {e}")
        return None

async def generate_deep_research_tldr(content: str, system_prompt: str = None, user_prompt: str = ""):
    """
    Implements the requested 2-step process optimized for a normal laptop:
    Step 1: LLaMA Deep Reasoning (~6-7 GB RAM)
    Step 2: Phi-3 Explanation (~3-4 GB RAM)
    """
    print("\n--- DEEP RESEARCH MISSION (LOCAL OLLAMA) ---")
    start_time = datetime.now()
    clean_text = re.sub(r'<[^>]*>', '', content)[:4000]
    
    # STEP 1: LLaMA Deep Reasoning
    reasoning_sys = "You are a Deep Reasoning Agent. Think step-by-step. Analyze the core logic and technical nuances. Output your thought process first."
    tldr_reasoning = None

    # Priority: GROQ (Cloud) -> OLLAMA (Local)
    if groq_client and api_key and api_key != "FAILED_KEY":
        print("STEP 1: LLaMA Deep Reasoning (Cloud Groq 70B)...")
        tldr_reasoning = await generate_tldr(content, reasoning_sys, "Extract core logic.", model="llama-3.3-70b-versatile")
    
    if not tldr_reasoning or "Error:" in tldr_reasoning:
        print("Fallback: Using Local Ollama for Step 1 (Llama 3.1)...")
        tldr_reasoning = await call_ollama("llama3.1", reasoning_sys, clean_text)

    # STEP 2: Concise Explanation
    explain_sys = system_prompt or "Provide a punchy 1-sentence TL;DR based on the reasoning provided."
    explain_user = f"REASONING:\n{tldr_reasoning}\n\nCONTENT:\n{clean_text}\n\nFinal 1-sentence summary:"
    tldr_final = None

    if groq_client and api_key and api_key != "FAILED_KEY":
        print("STEP 2: Concise Explanation (Cloud Groq Llama 8B)...")
        tldr_final = await generate_tldr(content, explain_sys, explain_user, model="llama-3.1-8b-instant")
    
    if not tldr_final or "Error:" in tldr_final:
        print("Fallback: Using Local Ollama for Step 2 (Phi-3)...")
        tldr_final = await call_ollama("phi3:mini", explain_sys, explain_user)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"RESEARCH MISSION COMPLETE: {duration:.1f}s [TOTAL LOAD: ~11GB RAM]")
    print("-------------------------------------------\n")
    
    return tldr_final

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
            <div class="entry-controls" style="position: absolute; top: 10px; right: 0; display: flex; gap: 10px; align-items: center; opacity: 0.8; transition: opacity 0.3s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.8">
                <input type="checkbox" class="entry-select" data-id="{entry_id}" onchange="refreshBatchUI()" style="width: 18px; height: 18px; cursor: pointer; margin-right: 10px;">
                <button onclick="copyEntry('{entry_id}')" class="control-btn copy-btn" title="Copy">📋</button>
                <button onclick="editEntry('{entry_id}')" class="control-btn edit-btn" title="Edit">✏️</button>
                <button onclick="saveEntry('{entry_id}')" class="control-btn save-btn" style="display:none;" title="Save">💾</button>
                <button onclick="openEntryAI('{entry_id}')" class="control-btn ai-btn" title="AI Process">🤖</button>
                <button onclick="deleteEntry('{entry_id}')" class="control-btn delete-btn" title="Delete">🗑️</button>
            </div>
            <div class="metadata" style="color: #9ca3af; font-size: 0.8em; margin-bottom: 5px;">
                Captured on: {timestamp} | Source: {source}
            </div>
            <div class="tldr-container" style="background: rgba(59, 130, 246, 0.05); border-left: 3px solid #3b82f6; padding: 10px 15px; margin-bottom: 15px; font-size: 13px; font-style: italic; color: var(--text-primary);">
                <strong>⚡ AI TL;DR:</strong> <span class="tldr-content" id="tldr-{entry_id}">Generating summary...</span>
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
    return entry_id

# Global lock for file operations to prevent race conditions
file_lock = asyncio.Lock()

@app.post("/")
async def capture(data: CaptureData):
    try:
        entry_id = append_to_master(data.html, data.source)
        # Background task for TL;DR with default prompt
        asyncio.create_task(process_tldr_and_update(entry_id, data.html))
        return {"status": "success", "url": "http://localhost:8771/view", "id": entry_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

async def update_file_tldr(entry_id: str, tldr: str):
    # This just updates the file, doesn't need to generate anything
    try:
        async with file_lock: 
            with open(MASTER_FILE, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            start_marker = f"<!-- ENTRY_START_{entry_id} -->"
            if start_marker not in file_content: return
            
            prefix, remainder = file_content.split(start_marker)
            entry_parts = remainder.split(f"<!-- ENTRY_END_{entry_id} -->")
            if len(entry_parts) < 2: return
            entry_block, suffix = entry_parts[0], entry_parts[1]
            
            pattern = rf'id="tldr-{entry_id}">.*?</span>'
            replacement = f'id="tldr-{entry_id}">{tldr}</span>'
            new_entry_block = re.sub(pattern, replacement, entry_block, flags=re.DOTALL)
            
            updated_file = prefix + start_marker + new_entry_block + f"<!-- ENTRY_END_{entry_id} -->" + suffix
            with open(MASTER_FILE, 'w', encoding='utf-8') as f:
                f.write(updated_file)
    except Exception as e:
        print(f"File update failed: {e}")

async def process_tldr_and_update(entry_id: str, content: str, system_prompt: str = None, user_prompt: str = ""):
    # Use the new Deep Research Pipeline for all captures
    tldr = await generate_deep_research_tldr(content, system_prompt, user_prompt)
    await update_file_tldr(entry_id, tldr)

@app.post("/summarize")
async def summarize(data: SummarizeData):
    try:
        tldr = await generate_deep_research_tldr(data.content, data.system_prompt, data.user_prompt)
        # Still update the file for persistence
        asyncio.create_task(update_file_tldr(data.id, tldr))
        return {"status": "success", "tldr": tldr}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/summarize_all")
async def summarize_all(data: SummarizeData):
    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = re.findall(r'<!-- ENTRY_START_(.*?) -->', content)
        
        async def run_all():
            for entry_id in entries:
                # Find entry content
                pattern = rf'<!-- ENTRY_START_{entry_id} -->[\s\S]*?<div class="content">\s*(.*?)\s*</div>[\s\S]*?<!-- ENTRY_END_{entry_id} -->'
                match = re.search(pattern, content)
                if match:
                    entry_content = match.group(1)
                    await process_tldr_and_update(entry_id, entry_content, data.system_prompt, data.user_prompt)
        
        asyncio.create_task(run_all())
        return {"status": "success", "count": len(entries)}
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

@app.post("/batch_delete")
async def batch_delete(data: BatchDeleteData):
    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for entry_id in data.ids:
            start_marker = f"<!-- ENTRY_START_{entry_id} -->"
            end_marker = f"<!-- ENTRY_END_{entry_id} -->"
            if start_marker in content and end_marker in content:
                prefix, remainder = content.split(start_marker)
                _, suffix = remainder.split(end_marker)
                content = prefix + suffix
        
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
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
    if not MASTER_FILE.exists():
        return HTMLResponse("<h1>No captures yet.</h1>")
    
    try:
        # Read the current log data
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # Extract the entries block
        # We look for the first entry start or just the container content
        if "<!-- ENTRY_START_" in log_content:
            parts = log_content.split("<!-- ENTRY_START_")
            # Keep everything from the first marker onwards until the end of the container
            # Actually, let's just find the container content carefully
            container_start = '<div class="container">'
            container_end = '</div>' # Assuming last div is container end
            
            if container_start in log_content:
                c_parts = log_content.split(container_start)
                inner = c_parts[1].rsplit(container_end, 1)[0]
                entries_html = inner.strip()
            else:
                entries_html = "<!-- APPEND_HERE -->"
        else:
            entries_html = "<!-- APPEND_HERE -->"

        # Read the latest template
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Inject entries into the latest template UI
        final_html = template_content.replace("{{CONTENT_PLACEHOLDER}}", entries_html)
        
        return HTMLResponse(final_html)
    except Exception as e:
        return HTMLResponse(f"<h1>Error rendering log: {str(e)}</h1>")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("HARVEST EDITABLE SERVER RUNNING ON 8771")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8771, log_level="warning")
