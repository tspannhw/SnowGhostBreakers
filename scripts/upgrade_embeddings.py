#!/usr/bin/env python3
"""
Upgrade Embedding Model Script
Upgrades from snowflake-arctic-embed-l to snowflake-arctic-embed-l-v2.0-8k
and from EMBED_TEXT_768 to AI_EMBED
"""

import os
import json
import re
from pathlib import Path

def upgrade_file(file_path):
    """Upgrade embedding references in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace function name
        content = content.replace('EMBED_TEXT_768', 'AI_EMBED')
        
        # Replace model name (with various quote styles)
        content = content.replace("'snowflake-arctic-embed-l'", "'snowflake-arctic-embed-l-v2.0-8k'")
        content = content.replace('"snowflake-arctic-embed-l"', '"snowflake-arctic-embed-l-v2.0-8k"')
        content = content.replace('snowflake-arctic-embed-l,', 'snowflake-arctic-embed-l-v2.0-8k,')
        
        # Handle cases where model name is referenced without quotes in markdown
        content = re.sub(
            r'\bsnowflake-arctic-embed-l\b(?!-v2\.0)',
            'snowflake-arctic-embed-l-v2.0-8k',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def upgrade_notebook(notebook_path):
    """Upgrade Jupyter notebook with special handling for JSON structure"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        updated = False
        
        # Process each cell
        for cell in notebook.get('cells', []):
            if 'source' in cell:
                for i, line in enumerate(cell['source']):
                    original_line = line
                    
                    # Replace function name
                    line = line.replace('EMBED_TEXT_768', 'AI_EMBED')
                    
                    # Replace model name
                    line = line.replace("'snowflake-arctic-embed-l'", "'snowflake-arctic-embed-l-v2.0-8k'")
                    line = line.replace('"snowflake-arctic-embed-l"', '"snowflake-arctic-embed-l-v2.0-8k"')
                    
                    if line != original_line:
                        cell['source'][i] = line
                        updated = True
        
        if updated:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2)
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing notebook {notebook_path}: {e}")
        return False

def main():
    """Main upgrade process"""
    print("🚀 Embedding Model Upgrade Script")
    print("=" * 60)
    print("Upgrading from:")
    print("  - Model: snowflake-arctic-embed-l")
    print("  - Function: EMBED_TEXT_768")
    print("\nUpgrading to:")
    print("  - Model: snowflake-arctic-embed-l-v2.0-8k")
    print("  - Function: AI_EMBED")
    print("=" * 60)
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Files to update
    files_to_check = [
        # Notebooks
        'notebooks/01_ghost_analytics.ipynb',
        'notebooks/generate_notebook.py',
        
        # Documentation (for completeness)
        'notebooks/IMAGE_ANALYTICS_ADDED.md',
        'notebooks/COMPLETE_ANALYTICS_GUIDE.md',
        'FEATURES_SUMMARY.md',
        'PROJECT_OVERVIEW.md',
        'STORED_PROCEDURE_FIXES.md',
        
        # Tests
        'tests/python/test_cortex_ai.py',
    ]
    
    updated_files = []
    skipped_files = []
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        
        if not full_path.exists():
            print(f"⚠️  Skipping (not found): {file_path}")
            skipped_files.append(file_path)
            continue
        
        print(f"📝 Processing: {file_path}")
        
        # Handle notebooks specially
        if file_path.endswith('.ipynb'):
            if upgrade_notebook(full_path):
                print(f"✅ Updated: {file_path}")
                updated_files.append(file_path)
            else:
                print(f"⏭️  No changes: {file_path}")
        else:
            if upgrade_file(full_path):
                print(f"✅ Updated: {file_path}")
                updated_files.append(file_path)
            else:
                print(f"⏭️  No changes: {file_path}")
    
    print()
    print("=" * 60)
    print("📊 Upgrade Summary")
    print("=" * 60)
    print(f"✅ Files Updated: {len(updated_files)}")
    for f in updated_files:
        print(f"   - {f}")
    
    if skipped_files:
        print(f"\n⚠️  Files Skipped: {len(skipped_files)}")
        for f in skipped_files:
            print(f"   - {f}")
    
    print()
    print("🎊 Upgrade complete!")
    print()
    print("Next steps:")
    print("1. Review changes: git diff")
    print("2. Re-run SQL files in Snowflake")
    print("3. Test notebooks")
    print("4. Run test suite: pytest tests/")

if __name__ == '__main__':
    main()

