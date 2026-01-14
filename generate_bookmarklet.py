#!/usr/bin/env python3
"""
Generate optimized bookmarklet HTML with the latest capture code
"""

import re

# Read the optimized bookmarklet
with open('capture_bookmarklet_optimized.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Remove the javascript: prefix and comments
js_code = re.sub(r'^javascript:\s*', '', js_code)
js_code = re.sub(r'//.*?$', '', js_code, flags=re.MULTILINE)  # Remove single-line comments
js_code = re.sub(r'/\*.*?\*/', '', js_code, flags=re.DOTALL)  # Remove multi-line comments

# Minify: remove extra whitespace
js_code = re.sub(r'\s+', ' ', js_code)
js_code = js_code.strip()

# Add javascript: prefix
bookmarklet_code = 'javascript:' + js_code

# Escape for HTML attribute
bookmarklet_html = bookmarklet_code.replace('"', '&quot;').replace("'", "\\'")

# Create the HTML
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Optimized Render Capture - Instant Loading</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .container {{
            background: white;
            border-radius: 16px;
            padding: 40px;
            max-width: 900px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}

        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.2em;
        }}

        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .highlight {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}

        .highlight h3 {{
            color: #856404;
            margin-bottom: 10px;
        }}

        .highlight ul {{
            margin-left: 20px;
            color: #555;
        }}

        .highlight li {{
            margin: 8px 0;
        }}

        .step {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}

        .step h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .step p {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }}

        .drag-link {{
            display: inline-block;
            background: #ffc107;
            color: #000;
            padding: 20px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.2em;
            margin: 15px 0;
            cursor: move;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.4);
        }}

        .drag-link:hover {{
            background: #ffb300;
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(255, 193, 7, 0.6);
        }}

        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-block;
            margin: 10px 10px 10px 0;
        }}

        .btn:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .code-box {{
            background: #282c34;
            color: #61dafb;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            word-break: break-all;
            margin: 15px 0;
            max-height: 150px;
            overflow-y: auto;
        }}

        .alert {{
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: none;
        }}

        .alert-success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}

        .badge {{
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }}
    </style>
</head>

<body>
    <div class="container">
        <h1>⚡ Optimized Render Capture <span class="badge">FAST</span></h1>
        <p class="subtitle">Instant-loading AI response capture for ChatGPT/Gemini/Claude</p>

        <div class="highlight">
            <h3>🚀 What's New in This Version:</h3>
            <ul>
                <li>✅ <strong>Instant rendering</strong> - No more blank screens or delays</li>
                <li>✅ <strong>Strips Monaco editor bloat</strong> - 10x smaller files</li>
                <li>✅ <strong>Updated ChatGPT selectors</strong> - Works with 2026 UI</li>
                <li>✅ <strong>Clean HTML output</strong> - No style conflicts</li>
                <li>✅ <strong>Fixed port</strong> - Now uses 8766 correctly</li>
            </ul>
        </div>

        <div class="step">
            <h2>Step 1: Show Bookmarks Bar</h2>
            <p>Press <strong>Ctrl+Shift+B</strong> (Windows/Linux) or <strong>Cmd+Shift+B</strong> (Mac) to show your browser's bookmarks bar</p>
        </div>

        <div class="step">
            <h2>Step 2: Drag This Link to Bookmarks Bar</h2>
            <p>Click and drag this button to your bookmarks bar:</p>
            <a href="{bookmarklet_code}" class="drag-link">
                ⚡ Capture Render (Fast)
            </a>
            <p style="margin-top: 15px;"><em>Or copy the code below and create bookmark manually:</em></p>
            <button class="btn" onclick="copyCode()">📋 Copy Code</button>
            <div class="code-box" id="code">{bookmarklet_code}</div>
            <div class="alert alert-success" id="copyAlert">✅ Code copied! Now create a bookmark and paste this as the URL.</div>
        </div>

        <div class="step">
            <h2>Step 3: Start the Server</h2>
            <p>Before using the bookmarklet, start the capture server:</p>
            <div class="code-box" style="color: #98c379;">python capture_server.py</div>
            <p>Or double-click: <strong>START_RENDER_SERVER.bat</strong></p>
        </div>

        <div class="step">
            <h2>Step 4: Use It!</h2>
            <p>1. Go to ChatGPT/Gemini/Claude</p>
            <p>2. Get an AI response</p>
            <p>3. Click the "⚡ Capture Render (Fast)" bookmark</p>
            <p>4. See popup: "✅ Captured!"</p>
            <p>5. Open: <code>renders/RENDER_*.html</code> - loads instantly!</p>
        </div>

        <div class="highlight">
            <h3>💡 Pro Tips:</h3>
            <ul>
                <li>The bookmarklet auto-detects ChatGPT, Gemini, and Claude</li>
                <li>Select specific text before clicking to capture only that part</li>
                <li>Files now open <strong>instantly</strong> with no blank screen</li>
                <li>Monaco editor bloat is automatically stripped</li>
            </ul>
        </div>
    </div>

    <script>
        function copyCode() {{
            const code = document.getElementById('code').textContent;
            navigator.clipboard.writeText(code).then(() => {{
                const alert = document.getElementById('copyAlert');
                alert.style.display = 'block';
                setTimeout(() => {{
                    alert.style.display = 'none';
                }}, 3000);
            }});
        }}
    </script>
</body>

</html>'''

# Write the HTML file
with open('create_bookmarklet_optimized.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated: create_bookmarklet_optimized.html")
print(f"Bookmarklet size: {len(bookmarklet_code)} characters")
print("\nOpen this file in your browser to get the optimized bookmarklet!")
