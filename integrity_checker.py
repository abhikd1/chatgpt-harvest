"""
INTEGRITY CHECKER - Validates byte-identical preservation

If even ONE character differs, the system has FAILED.
"""

import hashlib
from dataclasses import dataclass
from typing import Optional
from harvest_engine import CaptureResult


@dataclass
class IntegrityReport:
    """Report of integrity verification"""
    passed: bool
    char_count_match: bool
    emoji_count_match: bool
    fence_count_match: bool
    line_break_match: bool
    checksum_match: bool
    original_checksum: str
    saved_checksum: str
    error_message: Optional[str] = None


class IntegrityChecker:
    """Validates that saved content is byte-identical to source"""
    
    def verify_file(self, original: CaptureResult, saved_path: str) -> IntegrityReport:
        """
        Comprehensive integrity verification.
        
        Args:
            original: Original CaptureResult from capture
            saved_path: Path to saved file
            
        Returns:
            IntegrityReport with detailed verification results
        """
        try:
            # Read saved file as bytes
            with open(saved_path, 'rb') as f:
                saved_bytes = f.read()
            
            # Decode for metric calculation
            saved_content = saved_bytes.decode('utf-8')
            
            # Calculate all metrics
            saved_char_count = len(saved_content)
            saved_emoji_count = self._count_emojis(saved_content)
            saved_fence_count = saved_content.count('```')
            saved_line_breaks = saved_content.count('\n')
            saved_checksum = hashlib.sha256(saved_bytes).hexdigest()
            
            # Verify each metric
            char_match = saved_char_count == original.char_count
            emoji_match = saved_emoji_count == original.emoji_count
            fence_match = saved_fence_count == original.markdown_fence_count
            line_match = saved_line_breaks == original.line_break_count
            checksum_match = saved_checksum == original.checksum
            
            # Overall pass/fail
            passed = all([char_match, emoji_match, fence_match, line_match, checksum_match])
            
            error_msg = None
            if not passed:
                errors = []
                if not char_match:
                    errors.append(f"Character count mismatch: {original.char_count} → {saved_char_count}")
                if not emoji_match:
                    errors.append(f"Emoji count mismatch: {original.emoji_count} → {saved_emoji_count}")
                if not fence_match:
                    errors.append(f"Markdown fence mismatch: {original.markdown_fence_count} → {saved_fence_count}")
                if not line_match:
                    errors.append(f"Line break mismatch: {original.line_break_count} → {saved_line_breaks}")
                if not checksum_match:
                    errors.append(f"Checksum mismatch: {original.checksum[:8]}... → {saved_checksum[:8]}...")
                error_msg = "; ".join(errors)
            
            return IntegrityReport(
                passed=passed,
                char_count_match=char_match,
                emoji_count_match=emoji_match,
                fence_count_match=fence_match,
                line_break_match=line_match,
                checksum_match=checksum_match,
                original_checksum=original.checksum,
                saved_checksum=saved_checksum,
                error_message=error_msg
            )
            
        except Exception as e:
            return IntegrityReport(
                passed=False,
                char_count_match=False,
                emoji_count_match=False,
                fence_count_match=False,
                line_break_match=False,
                checksum_match=False,
                original_checksum=original.checksum,
                saved_checksum="ERROR",
                error_message=f"Verification failed: {str(e)}"
            )
    
    def _count_emojis(self, content: str) -> int:
        """Count emojis in content"""
        import re
        emoji_pattern = re.compile(
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
        return len(emoji_pattern.findall(content))
    
    def quick_verify(self, original: CaptureResult, saved_path: str) -> bool:
        """
        Quick checksum-only verification.
        
        Args:
            original: Original CaptureResult
            saved_path: Path to saved file
            
        Returns:
            True if checksums match, False otherwise
        """
        try:
            with open(saved_path, 'rb') as f:
                saved_bytes = f.read()
            
            saved_checksum = hashlib.sha256(saved_bytes).hexdigest()
            return saved_checksum == original.checksum
        except Exception:
            return False


# Global instance
_checker = IntegrityChecker()


def verify_integrity(original: CaptureResult, saved_path: str) -> IntegrityReport:
    """Verify file integrity"""
    return _checker.verify_file(original, saved_path)


def quick_check(original: CaptureResult, saved_path: str) -> bool:
    """Quick checksum verification"""
    return _checker.quick_verify(original, saved_path)
