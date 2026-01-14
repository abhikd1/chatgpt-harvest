import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from validator import MarkdownValidator

@dataclass
class QualityReport:
    """Quality assessment results."""
    is_valid: bool
    readability_score: float
    self_contained: bool
    formatting_errors: List[str]
    timestamp: str

class QualityAnalyzer:
    """Assess content against keeper standards."""
    
    def __init__(self):
        self.validator = MarkdownValidator()
    
    def analyze(self, content: str) -> QualityReport:
        """Run comprehensive quality checks."""
        is_valid, errors = self.validator.validate_content(content)
        self_contained = self.validator.check_self_containment(content)
        readability = self._calculate_readability(content)
        
        return QualityReport(
            is_valid=is_valid and self_contained,
            readability_score=readability,
            self_contained=self_contained,
            formatting_errors=errors,
            timestamp=datetime.now().isoformat()
        )
    
    def _calculate_readability(self, content: str) -> float:
        """Simple readability heuristic."""
        lines = content.split('\n')
        
        has_headers = sum(1 for line in lines if line.startswith('#'))
        has_spacing = sum(1 for line in lines if line.strip() == '')
        total_lines = len(lines)
        
        if total_lines == 0:
            return 0.0
        
        header_ratio = has_headers / total_lines
        spacing_ratio = has_spacing / total_lines
        
        return min(100.0, (header_ratio * 50 + spacing_ratio * 50) * 100)
