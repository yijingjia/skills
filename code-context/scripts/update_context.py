#!/usr/bin/env python3
"""
Main update script: coordinates all context update operations.

This script will:
1. Add/update INPUT/OUTPUT/POS header comments for all source files
2. Generate/update Claude.md files for all module directories
3. Update parent directory Claude.md files progressively
"""

import sys
from pathlib import Path
from typing import Set


def add_file_headers(directory: Path):
    """Add header comments to all source files."""
    print("📝 Adding file headers...")

    sys.path.insert(0, str(Path(__file__).parent))
    from add_file_headers import process_directory

    process_directory(directory, dry_run=False)


def generate_module_docs(directory: Path, processed: Set[Path] = None):
    """Generate Claude.md for all module directories."""
    if processed is None:
        processed = set()

    if directory in processed:
        return

    processed.add(directory)

    print(f"📄 Generating module doc for {directory}...")

    sys.path.insert(0, str(Path(__file__).parent))
    from analyze_module import analyze_module, generate_claude_md

    module_info = analyze_module(directory)

    if should_have_claude_md(directory):
        generate_claude_md(directory, module_info)

    for item in directory.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['__pycache__', '.venv', 'venv', 'node_modules']:
            generate_module_docs(item, processed)


def should_have_claude_md(directory: Path) -> bool:
    """Check if directory should have Claude.md."""
    excluded = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', '.ruff_cache', 'dist', 'build'}

    if directory.name in excluded:
        return False

    code_files = list(directory.glob('*.py')) + list(directory.glob('*.js')) + list(directory.glob('*.ts'))
    if not code_files:
        return False

    return True


def update_parent_context(directory: Path):
    """Update parent directory Claude.md files."""
    parent = directory.parent

    while parent != directory.root:
        if should_have_claude_md(parent):
            print(f"📄 Updating parent doc for {parent}...")

            sys.path.insert(0, str(Path(__file__).parent))
            from analyze_module import analyze_module, generate_claude_md

            module_info = analyze_module(parent)
            generate_claude_md(parent, module_info)

        parent = parent.parent


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description='Update codebase context (file headers and module docs)')
    parser.add_argument('path', nargs='?', default='.', help='Path to process (default: current directory)')
    parser.add_argument('--headers-only', action='store_true', help='Only update file headers')
    parser.add_argument('--docs-only', action='store_true', help='Only update module docs')
    parser.add_argument('--no-parent', action='store_true', help='Do not update parent directories')

    args = parser.parse_args()

    path = Path(args.path).resolve()

    if not path.exists():
        print(f"❌ Error: {path} does not exist")
        sys.exit(1)

    if not path.is_dir():
        print(f"❌ Error: {path} is not a directory")
        sys.exit(1)

    print(f"🚀 Updating codebase context for {path}")
    print("=" * 50)

    if not args.docs_only:
        add_file_headers(path)

    if not args.headers_only:
        generate_module_docs(path)

        if not args.no_parent:
            update_parent_context(path)

    print("=" * 50)
    print("✅ Codebase context updated successfully!")


if __name__ == '__main__':
    main()
