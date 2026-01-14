import re
from pathlib import Path
from typing import Dict
from analyzer import QualityAnalyzer

class KnowledgeLogAppender:
    """Safe append operations to knowledge log."""
    
    def __init__(self, log_path: str = "knowledge_log.md"):
        self.log_path = Path(log_path)
        self.analyzer = QualityAnalyzer()
    
    def append_entry(self, content: str, force: bool = False) -> bool:
        """Append content after quality validation."""
        report = self.analyzer.analyze(content)
        
        if not report.is_valid and not force:
            print("[ERROR] Quality check failed:")
            for error in report.formatting_errors:
                print(f"  - {error}")
            return False
        
        separator = "\n\n---\n\n"
        
        if self.log_path.exists():
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(separator)
                f.write(content)
        else:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"[OK] Entry appended (readability: {report.readability_score:.1f}%)")
        return True
    
    def get_stats(self) -> Dict[str, int]:
        """Analyze knowledge log statistics."""
        if not self.log_path.exists():
            return {'entries': 0, 'headers': 0, 'code_blocks': 0, 'total_lines': 0}
        
        content = self.log_path.read_text(encoding='utf-8')
        
        return {
            'entries': content.count('\n---\n') + 1,
            'headers': len(re.findall(r'^#', content, re.MULTILINE)),
            'code_blocks': len(re.findall(r'^```', content, re.MULTILINE)) // 2,
            'total_lines': len(content.split('\n'))
        }
