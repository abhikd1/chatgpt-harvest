"""
LOSSLESS AI RESPONSE HARVEST ENGINE

Philosophy: Glass mirror - reflects without thinking, improving, or modifying.
If even one emoji, line break, or space changes, the system has FAILED.
"""

import hashlib
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class CaptureResult:
    """Result of a lossless capture operation"""
    content: bytes  # Raw bytes, not string
    char_count: int
    emoji_count: int
    markdown_fence_count: int
    line_break_count: int
    checksum: str
    integrity_verified: bool


class HarvestEngine:
    """Character-level preservation engine with ZERO transformation"""
    
    def __init__(self):
        # More comprehensive emoji pattern
        self.emoji_pattern = re.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+", 
            flags=re.UNICODE
        )
    
    def capture_exact(self, content: str) -> CaptureResult:
        """
        Captures content with ZERO transformation.
        
        FORBIDDEN operations:
        - strip()
        - normalize()
        - encode/decode cycles
        - replace()
        - format()
        - Any string mutation
        
        Args:
            content: Raw AI response as string
            
        Returns:
            CaptureResult with integrity checksum
        """
        # Convert to bytes ONCE - no round trips
        content_bytes = content.encode('utf-8')
        
        # Calculate metrics WITHOUT mutating content
        char_count = len(content)
        emoji_count = len(self.emoji_pattern.findall(content))
        markdown_fence_count = content.count('```')
        line_break_count = content.count('\n')
        
        # SHA-256 checksum for integrity verification
        checksum = hashlib.sha256(content_bytes).hexdigest()
        
        return CaptureResult(
            content=content_bytes,
            char_count=char_count,
            emoji_count=emoji_count,
            markdown_fence_count=markdown_fence_count,
            line_break_count=line_break_count,
            checksum=checksum,
            integrity_verified=True
        )
    
    def verify_integrity(self, original: CaptureResult, saved_path: str) -> bool:
        """
        Verify that saved file is byte-identical to original capture.
        
        Args:
            original: Original CaptureResult
            saved_path: Path to saved file
            
        Returns:
            True if byte-identical, False otherwise
        """
        try:
            with open(saved_path, 'rb') as f:
                saved_bytes = f.read()
            
            saved_checksum = hashlib.sha256(saved_bytes).hexdigest()
            
            return saved_checksum == original.checksum
        except Exception:
            return False
    
    def remove_footer(self, content: str) -> str:
        """
        Remove ONLY the control footer, preserve everything else.
        
        Footer pattern:
        ────────────────────────
        [PRESS: C]  → COPY EXACT RESPONSE
        [PRESS: S]  → SAVE TO CURRENT FILE
        [PRESS: N]  → START NEW FILE
        [PRESS: X]  → IGNORE
        ────────────────────────
        """
        footer_pattern = (
            r"────────────────────────\n"
            r"\[PRESS: C\]  → COPY EXACT RESPONSE\n"
            r"\[PRESS: S\]  → SAVE TO CURRENT FILE\n"
            r"\[PRESS: N\]  → START NEW FILE\n"
            r"\[PRESS: X\]  → IGNORE\n"
            r"────────────────────────"
        )
        
        # Remove footer if present at the end
        content_without_footer = re.sub(footer_pattern + r'$', '', content, flags=re.MULTILINE)
        
        return content_without_footer
    
    def get_stats(self, result: CaptureResult) -> dict:
        """Get human-readable stats about captured content"""
        return {
            'characters': result.char_count,
            'emojis': result.emoji_count,
            'code_blocks': result.markdown_fence_count // 2,  # Opening + closing
            'lines': result.line_break_count + 1,
            'bytes': len(result.content),
            'checksum': result.checksum[:8] + '...',  # First 8 chars
        }


# Global instance
_engine = HarvestEngine()


def capture(content: str) -> CaptureResult:
    """Convenience function for capturing content"""
    return _engine.capture_exact(content)


def verify(original: CaptureResult, saved_path: str) -> bool:
    """Convenience function for verifying integrity"""
    return _engine.verify_integrity(original, saved_path)


def remove_footer(content: str) -> str:
    """Convenience function for removing control footer"""
    return _engine.remove_footer(content)
