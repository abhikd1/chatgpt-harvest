import sys
from pathlib import Path
from analyzer import QualityAnalyzer
from appender import KnowledgeLogAppender

def main():
    """Command-line interface for knowledge capture."""
    if len(sys.argv) < 2:
        print("Usage: python knowledge_capture.py <command>")
        print("Commands: validate, append, stats")
        return
    
    command = sys.argv[1]
    appender = KnowledgeLogAppender()
    
    if command == "validate":
        content = sys.stdin.read()
        analyzer = QualityAnalyzer()
        report = analyzer.analyze(content)
        
        if report.is_valid:
            print("[OK] Content passes all quality checks")
            print(f"[STATS] Readability: {report.readability_score:.1f}%")
            print(f"[SECURE] Self-contained: {report.self_contained}")
        else:
            print("[ERROR] Quality issues detected:")
            for error in report.formatting_errors:
                print(f"  - {error}")
            if not report.self_contained:
                print("  - Content has external dependencies")
    
    elif command == "append":
        # Check if a file was provided as an argument
        file_arg = None
        for arg in sys.argv[2:]:
            if not arg.startswith('--'):
                file_arg = arg
                break
        
        if file_arg and Path(file_arg).exists():
            content = Path(file_arg).read_text(encoding='utf-8')
        else:
            # Read as binary to avoid Windows encoding issues with stdin
            if hasattr(sys.stdin, 'buffer'):
                content = sys.stdin.buffer.read().decode('utf-8', errors='ignore')
            else:
                content = sys.stdin.read()
            
        force = "--force" in sys.argv
        success = appender.append_entry(content, force=force)
        sys.exit(0 if success else 1)
    
    elif command == "stats":
        stats = appender.get_stats()
        print("[STATS] Knowledge Log Statistics")
        print(f"  Entries: {stats['entries']}")
        print(f"  Headers: {stats['headers']}")
        print(f"  Code Blocks: {stats['code_blocks']}")
        print(f"  Total Lines: {stats['total_lines']}")
    
    else:
        print(f"[ERROR] Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
