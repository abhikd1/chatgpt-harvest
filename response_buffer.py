"""
RESPONSE BUFFER - In-memory storage for exact AI responses

Holds raw response bytes until user decides what to do with it.
"""

from typing import Optional
from harvest_engine import CaptureResult, capture, remove_footer


class ResponseBuffer:
    """Thread-safe buffer for holding the current AI response"""
    
    def __init__(self):
        self._current: Optional[CaptureResult] = None
        self._raw_content: Optional[str] = None
    
    def store(self, content: str) -> CaptureResult:
        """
        Store AI response in buffer with ZERO mutation.
        
        Args:
            content: Raw AI response (may include footer)
            
        Returns:
            CaptureResult with integrity checksum
        """
        # Store raw content for potential re-capture
        self._raw_content = content
        
        # Remove footer before capture (footer is not part of AI response)
        clean_content = remove_footer(content)
        
        # Capture with zero transformation
        self._current = capture(clean_content)
        
        return self._current
    
    def get_current(self) -> Optional[CaptureResult]:
        """Get current buffered response"""
        return self._current
    
    def get_raw(self) -> Optional[str]:
        """Get raw content including footer"""
        return self._raw_content
    
    def get_content_bytes(self) -> Optional[bytes]:
        """Get content as bytes (for saving)"""
        if self._current:
            return self._current.content
        return None
    
    def get_content_str(self) -> Optional[str]:
        """Get content as string (for clipboard)"""
        if self._current:
            return self._current.content.decode('utf-8')
        return None
    
    def clear(self):
        """Clear buffer (after discard or successful save)"""
        self._current = None
        self._raw_content = None
    
    def has_content(self) -> bool:
        """Check if buffer has content"""
        return self._current is not None
    
    def get_stats(self) -> dict:
        """Get stats about buffered content"""
        if not self._current:
            return {}
        
        from harvest_engine import _engine
        return _engine.get_stats(self._current)


# Global buffer instance
_buffer = ResponseBuffer()


def store_response(content: str) -> CaptureResult:
    """Store response in global buffer"""
    return _buffer.store(content)


def get_current_response() -> Optional[CaptureResult]:
    """Get current buffered response"""
    return _buffer.get_current()


def get_content_for_clipboard() -> Optional[str]:
    """Get content as string for clipboard"""
    return _buffer.get_content_str()


def get_content_for_save() -> Optional[bytes]:
    """Get content as bytes for file save"""
    return _buffer.get_content_bytes()


def clear_buffer():
    """Clear the buffer"""
    _buffer.clear()


def has_buffered_content() -> bool:
    """Check if buffer has content"""
    return _buffer.has_content()


def get_buffer_stats() -> dict:
    """Get stats about buffered content"""
    return _buffer.get_stats()
