# 🎨 RENDER MODE - SIMPLE GUIDE

## WHAT IS RENDER MODE?

**Text Mode**: Saves plain text (what you already know)
**Render Mode**: Saves the ACTUAL LOOK - bold, colors, tables, spacing

---

## 🚀 HOW TO USE RENDER MODE (3 SIMPLE STEPS)

### STEP 1: Start the Server

Open terminal and run:

```powershell
python capture_server.py
```

You'll see:
```
============================================================
🔒 RENDER CAPTURE SERVER
============================================================

✅ Server running on http://localhost:8765

📋 Waiting for browser captures...
```

**IMPORTANT**: Leave this window open! Don't close it.

---

### STEP 2: Create the Bookmarklet

This is a special bookmark that captures the visual look.

#### A. Open your browser (Chrome/Edge/Firefox)

#### B. Show bookmarks bar
- Press `Ctrl+Shift+B` to show bookmarks bar

#### C. Create new bookmark
1. Right-click on bookmarks bar
2. Click "Add page" or "Add bookmark"
3. In the "Name" field, type: **Capture Render**
4. In the "URL" field, paste this ENTIRE code (copy everything):

```
javascript:(function(){let s=window.getSelection();let h='';let src=window.location.hostname;if(s.rangeCount>0){let r=s.getRangeAt(0);let c=document.createElement('div');c.appendChild(r.cloneContents());h=c.innerHTML;}else{let gpt=document.querySelector('.markdown.prose');if(gpt){h=gpt.innerHTML;src='ChatGPT';}if(!h){let gem=document.querySelector('.model-response-text');if(gem){h=gem.innerHTML;src='Gemini';}}if(!h){let cl=document.querySelector('[data-test-render-count]');if(cl){h=cl.innerHTML;src='Claude';}}if(!h){h=document.body.innerHTML;}}if(!h){alert('❌ No content');return;}fetch('http://localhost:8765',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({html:h,source:src})}).then(r=>r.json()).then(d=>{if(d.status==='success'){alert('✅ Captured!\n\n'+d.message);}else{alert('❌ Failed:\n\n'+d.message);}}).catch(()=>{alert('❌ Server not running!\n\nRun: python capture_server.py');});})();
```

5. Click Save

---

### STEP 3: Capture AI Responses

#### A. Go to ChatGPT (or Gemini/Claude)

#### B. Ask any question
Example: "Explain Python decorators"

#### C. Wait for response

#### D. Click the "Capture Render" bookmark you just created

You'll see a popup: "✅ Captured!"

#### E. Check the terminal where server is running
You'll see:
```
✅ Captured render from ChatGPT
   Saved to: renders\RENDER_20260114_130500.html
```

#### F. Open the HTML file
```powershell
start renders\RENDER_20260114_130500.html
```

**You'll see the EXACT ChatGPT look - bold, colors, tables, everything!**

---

## 📊 VISUAL COMPARISON

### Text Mode Output:
```
# Python Decorators

A decorator is a function that modifies another function.

Example:
def my_decorator(func):
    return func
```

### Render Mode Output:
Opens in browser with:
- ✅ Actual bold headings
- ✅ Syntax-highlighted code
- ✅ Proper spacing
- ✅ Colors
- ✅ Tables with borders
- ✅ Exact ChatGPT look

---

## 🎯 COMPLETE EXAMPLE - DO THIS NOW

### 1. Start Server
```powershell
python capture_server.py
```
Leave it running.

### 2. Open New Terminal
Press `Ctrl+Shift+P` in VS Code → "New Terminal"

### 3. In Browser
- Go to ChatGPT
- Ask: "Show me a Python function with comments"
- Wait for response

### 4. Click "Capture Render" Bookmark

### 5. Check Terminal
You'll see the save message

### 6. Open the File
```powershell
start renders\RENDER_*.html
```

**You'll see the beautiful rendered output!**

---

## ❓ TROUBLESHOOTING

### Q: Bookmarklet says "Server not running"
**A**: Make sure `python capture_server.py` is running in a terminal

### Q: How do I create the bookmarklet?
**A**: 
1. Show bookmarks bar (Ctrl+Shift+B)
2. Right-click → Add bookmark
3. Paste the javascript code in URL field

### Q: Can I capture without bookmarklet?
**A**: No, you need the bookmarklet to capture the visual rendering from browser

### Q: Where are files saved?
**A**: In `renders/` folder as HTML files

---

## 🔥 QUICK REFERENCE

| Action | Command |
|--------|---------|
| Start server | `python capture_server.py` |
| Capture | Click bookmarklet in browser |
| View latest | `start renders\RENDER_*.html` |
| Stop server | Press Ctrl+C in server terminal |

---

## ✅ SUMMARY

**Render Mode = Visual Preservation**

1. Run `python capture_server.py` (leave it open)
2. Create bookmarklet (one-time setup)
3. Click bookmarklet on AI responses
4. Get beautiful HTML files with exact visual look

**That's it!**
