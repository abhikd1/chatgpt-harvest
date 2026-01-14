import re
from typing import List, Tuple

class MarkdownValidator:
    """Enforce archival-quality Markdown standards."""
    
    FORBIDDEN_PATTERNS = [
        r"(?i)(sure|here'?s what|as an ai|earlier you)",
        r"(?i)(let me know|feel free|hope this helps)",
        r"(?i)(in this conversation|we discussed|continuing from)",
    ]
    
    REQUIRED_ELEMENTS = {
        'headers': r'^#{1,3}\s+.+$',
        'code_blocks': r'^```\w+\n[\s\S]*?\n```$',
    }
    
    def validate_content(self, content: str) -> Tuple[bool, List[str]]:
        """Check if content meets archival standards."""
        errors = []
        
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, content, re.MULTILINE):
                errors.append(f"Conversational artifact detected")
        
        if not re.search(r'^#\s+', content, re.MULTILINE):
            errors.append("Missing top-level header")
        
        lines = content.split('\n')
        code_block_opens = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                lang_match = re.match(r'^```(\w*)', line.strip())
                if lang_match:
                    lang = lang_match.group(1)
                    if lang:
                        code_block_opens.append((i+1, lang))
                    else:
                        if len(code_block_opens) == len([l for l in lines[:i] if l.strip() == '```']):
                            errors.append(f"Code block at line {i+1} missing language specification")
        
        return len(errors) == 0, errors
    
    def check_self_containment(self, content: str) -> bool:
        """Verify content has no external dependencies."""
        dependency_markers = [
            'see above', 'mentioned earlier', 'as discussed',
            'previous section', 'next time', 'we will continue'
        ]
        
        content_lower = content.lower()
        return not any(marker in content_lower for marker in dependency_markers)
