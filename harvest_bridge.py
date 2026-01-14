"""
HARVEST BRIDGE - Promote harvested content to quality-checked knowledge log

Workflow:
1. Capture AI responses losslessly → AI_HARVEST_XXX.txt
2. Review and decide what's valuable
3. Promote to knowledge_log.md with quality validation
"""

import sys
from pathlib import Path
from validator import validate
from appender import append


def promote_harvest_file(harvest_path: str, skip_validation: bool = False):
    """
    Promote harvest file content to knowledge_log.md
    
    Args:
        harvest_path: Path to harvest file
        skip_validation: If True, skip quality validation (keep lossless)
    """
    harvest_file = Path(harvest_path)
    
    if not harvest_file.exists():
        print(f"❌ File not found: {harvest_path}")
        return False
    
    # Read harvest content
    try:
        with open(harvest_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        return False
    
    if not content.strip():
        print("❌ File is empty")
        return False
    
    print(f"📄 Promoting: {harvest_file.name}")
    print(f"   Size: {len(content)} characters\n")
    
    if skip_validation:
        # Direct append without validation (lossless mode)
        print("⚠️  Skipping validation (lossless mode)")
        try:
            append(content)
            print(f"✅ Promoted to knowledge_log.md (lossless)")
            return True
        except Exception as e:
            print(f"❌ Append failed: {e}")
            return False
    else:
        # Quality validation mode
        print("🔍 Running quality validation...")
        result = validate(content)
        
        if not result['passed']:
            print("\n❌ Validation failed:")
            for issue in result['issues']:
                print(f"   • {issue}")
            print("\nOptions:")
            print("  1. Fix issues manually and try again")
            print("  2. Use --skip-validation to promote as-is")
            return False
        
        print("✅ Validation passed")
        
        # Append to knowledge log
        try:
            append(result['content'])
            print(f"✅ Promoted to knowledge_log.md")
            return True
        except Exception as e:
            print(f"❌ Append failed: {e}")
            return False


def list_harvest_files():
    """List all available harvest files"""
    script_dir = Path(__file__).parent
    harvests_dir = script_dir / "harvests"
    
    if not harvests_dir.exists():
        print("📁 No harvest files yet")
        return
    
    harvest_files = sorted(harvests_dir.glob("AI_HARVEST_*.txt"))
    
    if not harvest_files:
        print("📁 No harvest files yet")
        return
    
    print("\n📚 Available Harvest Files:\n")
    
    for f in harvest_files:
        size = f.stat().st_size
        size_kb = round(size / 1024, 2)
        
        # Preview first line
        try:
            with open(f, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()[:60]
        except Exception:
            first_line = "(unable to read)"
        
        print(f"  {f.name}")
        print(f"    Size: {size_kb} KB")
        print(f"    Preview: {first_line}...")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python harvest_bridge.py list")
        print("  python harvest_bridge.py promote <harvest_file>")
        print("  python harvest_bridge.py promote <harvest_file> --skip-validation")
        print("\nExamples:")
        print("  python harvest_bridge.py list")
        print("  python harvest_bridge.py promote harvests/AI_HARVEST_001.txt")
        print("  python harvest_bridge.py promote harvests/AI_HARVEST_001.txt --skip-validation")
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        list_harvest_files()
    elif command == 'promote':
        if len(sys.argv) < 3:
            print("❌ Please specify harvest file path")
            print("Example: python harvest_bridge.py promote harvests/AI_HARVEST_001.txt")
            return
        
        harvest_path = sys.argv[2]
        skip_validation = '--skip-validation' in sys.argv
        
        success = promote_harvest_file(harvest_path, skip_validation)
        sys.exit(0 if success else 1)
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: list, promote")


if __name__ == '__main__':
    main()
