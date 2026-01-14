"""
BROWSER EXTENSION BRIDGE - Captures rendered HTML from browser

This script runs a local server that:
1. Receives HTML via POST (from extension)
2. Saves it as a file using render_capture.py
3. SERVES the file via GET so you can view it in the browser
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from render_capture import save_render

class CaptureHandler(BaseHTTPRequestHandler):
    """HTTP handler for receiving AND viewing HTML captures"""
    
    SERVER_PORT = 8766  # Default port if not specified
    RENDER_DIR = Path(__file__).parent / "renders"

    def do_GET(self):
        """Serve render files so they can be clicked and viewed"""
        # 1. Root path check
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"<h1>Render Capture Server Active</h1><p>Ready to serve renders.</p>")
            return
        
        # 2. Serve saved renders
        if self.path.startswith('/renders/'):
            # Decode URL path (handle spaces etc)
            import urllib.parse
            filename = self.path.replace('/renders/', '')
            filename = urllib.parse.unquote(filename)
            
            file_path = self.RENDER_DIR / filename
            
            if file_path.exists() and file_path.is_file():
                self.send_response(200)
                # Simple MIME type guessing
                if filename.endswith('.json'):
                    self.send_header('Content-Type', 'application/json')
                else:
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # 3. 404 for anything else
        self.send_error(404, f"File not found: {self.path}")

    def do_POST(self):
        """Handle POST request with HTML content"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            data = json.loads(post_data.decode('utf-8'))
            html_content = data.get('html', '')
            source = data.get('source', 'Browser')
            
            if html_content:
                filepath = save_render(html_content, source=source)
                
                # Create localhost URL (using the requested header Host if possible, or default)
                host = self.headers.get('Host', f'localhost:{self.server.server_port}')
                file_url = f"http://{host}/renders/{filepath.name}"
                
                response = {
                    'status': 'success',
                    'message': f'Saved! Click to view.',
                    'filepath': str(filepath),
                    'url': file_url 
                }
                
                print(f"✅ Captured: {filepath.name}")
            else:
                response = {
                    'status': 'error',
                    'message': 'No HTML content provided'
                }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error handling request: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {'status': 'error', 'message': str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging to keep terminal clean"""
        pass


def start_server(port=8766):
    """Start the capture server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CaptureHandler)
    
    print("\n" + "="*60)
    print("🔒 RENDER CAPTURE SERVER (WEB VIEW ENABLED)")
    print("="*60)
    print(f"\n✅ Server running on http://localhost:{port}")
    print("\n📋 Waiting for browser captures...")
    print("\n💡 Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        httpd.shutdown()


if __name__ == '__main__':
    port = 8766
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number, using default 8766")
    
    start_server(port)
