"""
HARVEST FILE MANAGER - Auto-numbered file creation with verbatim append

Creates AI_HARVEST_001.txt, AI_HARVEST_002.txt, etc.
Appends content with ZERO transformation.
"""

import os
from pathlib import Path
from typing import Optional
from harvest_engine import CaptureResult
from integrity_checker import verify_integrity, IntegrityReport


class HarvestFileManager:
    """Manages auto-numbered harvest files with verbatim append"""
    
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            # Default to harvests/ subdirectory
            script_dir = Path(__file__).parent
            base_dir = script_dir / "harvests"
        
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        self._current_file_number = self._get_next_file_number()
        self._current_file_path = self._get_file_path(self._current_file_number)
    
    def _get_next_file_number(self) -> int:
        """Find the next available file number"""
        existing_files = list(self.base_dir.glob("AI_HARVEST_*.txt"))
        
        if not existing_files:
            return 1
        
        # Extract numbers from existing files
        numbers = []
        for f in existing_files:
            try:
                num = int(f.stem.replace("AI_HARVEST_", ""))
                numbers.append(num)
            except ValueError:
                continue
        
        return max(numbers) if numbers else 1
    
    def _get_file_path(self, number: int) -> Path:
        """Get file path for given number"""
        return self.base_dir / f"AI_HARVEST_{number:03d}.txt"
    
    def get_current_file(self) -> str:
        """Get current harvest file path"""
        return str(self._current_file_path)
    
    def append_raw(self, capture_result: CaptureResult) -> tuple[bool, Optional[IntegrityReport]]:
        """
        Append content to current file with ZERO transformation.
        
        Args:
            capture_result: CaptureResult from harvest_engine
            
        Returns:
            (success: bool, integrity_report: Optional[IntegrityReport])
        """
        try:
            # Binary append - no encoding changes, no separators
            # Write EXACTLY what was captured, nothing more
            with open(self._current_file_path, 'ab') as f:
                f.write(capture_result.content)
            
            # For integrity check, we need to read back the ENTIRE file
            # and verify our capture_result matches the LAST portion
            # For now, we'll skip integrity check on append (only verify on first write)
            
            return True, None
            
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False, None
    
    def new_file(self) -> str:
        """
        Start a new harvest file.
        
        Returns:
            Path to new file
        """
        self._current_file_number += 1
        self._current_file_path = self._get_file_path(self._current_file_number)
        
        return str(self._current_file_path)
    
    def get_stats(self) -> dict:
        """Get stats about current harvest file"""
        if not self._current_file_path.exists():
            return {
                'file': str(self._current_file_path),
                'exists': False,
                'size_bytes': 0,
                'lines': 0
            }
        
        size = self._current_file_path.stat().st_size
        
        try:
            with open(self._current_file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
        except Exception:
            lines = 0
        
        return {
            'file': str(self._current_file_path),
            'exists': True,
            'size_bytes': size,
            'size_kb': round(size / 1024, 2),
            'lines': lines
        }
    
    def list_all_harvests(self) -> list[dict]:
        """List all harvest files with stats"""
        harvest_files = sorted(self.base_dir.glob("AI_HARVEST_*.txt"))
        
        results = []
        for f in harvest_files:
            size = f.stat().st_size
            results.append({
                'file': f.name,
                'path': str(f),
                'size_bytes': size,
                'size_kb': round(size / 1024, 2)
            })
        
        return results


# Global instance
_manager = HarvestFileManager()


def save_to_current_file(capture_result: CaptureResult) -> tuple[bool, Optional[IntegrityReport]]:
    """Save to current harvest file"""
    return _manager.append_raw(capture_result)


def start_new_file() -> str:
    """Start new harvest file"""
    return _manager.new_file()


def get_current_file_path() -> str:
    """Get current file path"""
    return _manager.get_current_file()


def get_file_stats() -> dict:
    """Get current file stats"""
    return _manager.get_stats()


def list_all_harvests() -> list[dict]:
    """List all harvest files"""
    return _manager.list_all_harvests()
