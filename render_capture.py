"""
RENDER CAPTURE - Capture HTML/DOM snapshot of AI responses

This captures the ACTUAL RENDERED OUTPUT, not just text.
Preserves: bold, colors, tables, spacing, visual hierarchy.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class RenderCaptureManager:
    """Manages HTML snapshot captures of AI responses"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            script_dir = Path(__file__).parent
            base_dir = script_dir / "renders"
        
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Create index file if it doesn't exist
        self.index_file = self.base_dir / "index.json"
        if not self.index_file.exists():
            self._save_index([])
    
    def _load_index(self):
        """Load capture index"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_index(self, index):
        """Save capture index"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def save_render(self, html_content, metadata=None):
        """
        Save HTML render capture
        
        Args:
            html_content: HTML string of the rendered content
            metadata: Optional dict with source, timestamp, etc.
        
        Returns:
            Path to saved file
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RENDER_{timestamp}.html"
        filepath = self.base_dir / filename
        
        # Create full HTML document
        full_html = self._create_full_html(html_content, metadata)
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Update index
        index = self._load_index()
        index.append({
            'filename': filename,
            'timestamp': timestamp,
            'size_bytes': len(full_html),
            'metadata': metadata or {}
        })
        self._save_index(index)
        
        return filepath
    
    def _create_full_html(self, content, metadata):
        """Create complete HTML document using the external template"""
        
        source = metadata.get('source', 'Unknown') if metadata else 'Unknown'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load the template
        template_path = self.base_dir.parent / "viewer_template.html"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            # Fallback (formatted nicely)
            return f"<html><body style='max-width:800px; margin:2rem auto; font-family:sans-serif;'>{content}</body></html>"
            
        # Refined Metadata Block
        metadata_html = f"""
        <div class="metadata">
            <strong>Source:</strong> {source} • 
            <strong>Captured:</strong> {timestamp}
        </div>
        """
        
        full_content = metadata_html + content
        
        return template.replace("{{CONTENT_PLACEHOLDER}}", full_content)
    
    def list_renders(self):
        """List all render captures"""
        index = self._load_index()
        return index
    
    def get_stats(self):
        """Get render capture stats"""
        index = self._load_index()
        
        total_size = sum(item['size_bytes'] for item in index)
        
        return {
            'total_captures': len(index),
            'total_size_bytes': total_size,
            'total_size_kb': round(total_size / 1024, 2),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'latest': index[-1] if index else None
        }


# Global instance
_manager = RenderCaptureManager()


def save_render(html_content, source=None):
    """Save HTML render capture"""
    metadata = {'source': source} if source else None
    return _manager.save_render(html_content, metadata)


def list_renders():
    """List all render captures"""
    return _manager.list_renders()


def get_render_stats():
    """Get render capture stats"""
    return _manager.get_stats()


if __name__ == '__main__':
    # Test with sample HTML
    sample_html = """
<h1>🚀 Test Render Capture</h1>

<p>This is a <strong>test</strong> of the render capture system with <em>emphasis</em> and <code>inline code</code>.</p>

<h2>Features</h2>

<ul>
    <li>Preserves <strong>bold text</strong></li>
    <li>Preserves <em>italic text</em></li>
    <li>Preserves emojis: 🔥💡✨</li>
    <li>Preserves tables and code blocks</li>
</ul>

<h2>Code Example</h2>

<pre><code>def hello():
    print("Hello, World!")
    return True</code></pre>

<h2>Table Example</h2>

<table>
    <tr>
        <th>Feature</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Bold</td>
        <td>✅</td>
    </tr>
    <tr>
        <td>Italic</td>
        <td>✅</td>
    </tr>
    <tr>
        <td>Emojis</td>
        <td>✅</td>
    </tr>
</table>

<p>Unicode test: 世界 مرحبا мир 🌍</p>
"""
    
    filepath = save_render(sample_html, source='Test')
    print(f"✅ Saved render to: {filepath}")
    
    stats = get_render_stats()
    print(f"\n📊 Stats:")
    print(f"   Total captures: {stats['total_captures']}")
    print(f"   Total size: {stats['total_size_kb']} KB")
