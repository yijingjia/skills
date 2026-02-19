#!/usr/bin/env python3
"""
Add or update INPUT/OUTPUT/POS header comments for source code files.

Supports multiple programming languages and comment formats.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# Language configuration: comment formats and file extensions
LANGUAGE_CONFIG = {
    'python': {
        'extensions': ['.py'],
        'comment_style': '#',
        'name': 'Python',
        'line_comment': True
    },
    'javascript': {
        'extensions': ['.js', '.jsx', '.mjs'],
        'comment_style': '//',
        'name': 'JavaScript',
        'line_comment': True
    },
    'typescript': {
        'extensions': ['.ts', '.tsx'],
        'comment_style': '//',
        'name': 'TypeScript',
        'line_comment': True
    },
    'java': {
        'extensions': ['.java'],
        'comment_style': '//',
        'name': 'Java',
        'line_comment': True
    },
    'cpp': {
        'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.h', '.hxx'],
        'comment_style': '//',
        'name': 'C++',
        'line_comment': True
    },
    'c': {
        'extensions': ['.c', '.h'],
        'comment_style': '//',
        'name': 'C',
        'line_comment': True
    },
    'go': {
        'extensions': ['.go'],
        'comment_style': '//',
        'name': 'Go',
        'line_comment': True
    },
    'rust': {
        'extensions': ['.rs'],
        'comment_style': '//',
        'name': 'Rust',
        'line_comment': True
    },
    'ruby': {
        'extensions': ['.rb'],
        'comment_style': '#',
        'name': 'Ruby',
        'line_comment': True
    },
    'php': {
        'extensions': ['.php'],
        'comment_style': '//',
        'name': 'PHP',
        'line_comment': True
    },
    'swift': {
        'extensions': ['.swift'],
        'comment_style': '//',
        'name': 'Swift',
        'line_comment': True
    },
    'kotlin': {
        'extensions': ['.kt', '.kts'],
        'comment_style': '//',
        'name': 'Kotlin',
        'line_comment': True
    },
    'scala': {
        'extensions': ['.scala'],
        'comment_style': '//',
        'name': 'Scala',
        'line_comment': True
    },
    'shell': {
        'extensions': ['.sh', '.bash', '.zsh'],
        'comment_style': '#',
        'name': 'Shell',
        'line_comment': True
    },
    'sql': {
        'extensions': ['.sql'],
        'comment_style': '--',
        'name': 'SQL',
        'line_comment': True
    },
    'html': {
        'extensions': ['.html', '.htm'],
        'comment_style': '<!--',
        'comment_end': '-->',
        'name': 'HTML',
        'line_comment': False
    },
    'css': {
        'extensions': ['.css', '.scss', '.sass', '.less'],
        'comment_style': '/*',
        'comment_end': '*/',
        'name': 'CSS',
        'line_comment': False
    },
    'yaml': {
        'extensions': ['.yaml', '.yml'],
        'comment_style': '#',
        'name': 'YAML',
        'line_comment': True
    },
    'toml': {
        'extensions': ['.toml'],
        'comment_style': '#',
        'name': 'TOML',
        'line_comment': True
    },
    'dockerfile': {
        'extensions': ['.dockerfile', 'Dockerfile'],
        'comment_style': '#',
        'name': 'Dockerfile',
        'line_comment': True
    },
}


def detect_language(file_path: Path) -> Optional[Dict]:
    """Detect the language type of a file."""
    ext = file_path.suffix.lower()

    if file_path.name == 'Dockerfile':
        return LANGUAGE_CONFIG['dockerfile']

    for lang, config in LANGUAGE_CONFIG.items():
        if ext in config['extensions']:
            return config

    return {
        'comment_style': '#',
        'name': 'Unknown',
        'line_comment': True
    }


def analyze_file_header(file_path: Path) -> Dict[str, any]:
    """Analyze file and extract INPUT/OUTPUT/POS information."""
    lang_config = detect_language(file_path)
    file_name = file_path.name.lower()
    parent_dir = file_path.parent.name.lower()

    input_info = infer_input(file_path, lang_config)
    output_info = infer_output(file_path, lang_config)
    pos_desc = infer_position(file_path, parent_dir, file_name)

    return {
        'INPUT': input_info,
        'OUTPUT': output_info,
        'POS': pos_desc,
        'lang_config': lang_config
    }


def infer_input(file_path: Path, lang_config: Dict) -> Dict[str, List[str]]:
    """Infer INPUT description, returns dict with internal and external lists."""
    content = read_file_safe(file_path)
    if not content:
        return {'internal': [], 'external': []}

    imports = []

    if lang_config['name'] == 'Python':
        imports = extract_python_imports(content)
    elif lang_config['name'] in ['JavaScript', 'TypeScript']:
        imports = extract_js_imports(content)
    elif lang_config['name'] == 'Java':
        imports = extract_java_imports(content)
    elif lang_config['name'] == 'Go':
        imports = extract_go_imports(content)
    elif lang_config['name'] in ['C', 'C++']:
        imports = extract_cpp_includes(content)

    if imports:
        internal = [imp for imp in imports if is_internal_import(imp, file_path)]
        external = [imp for imp in imports if imp not in internal]
        return {'internal': internal[:5], 'external': external[:5]}

    return {'internal': [], 'external': []}


def extract_python_imports(content: str) -> List[str]:
    """Extract Python imports."""
    imports = []
    patterns = [
        r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
    ]

    for line in content.split('\n'):
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                imports.append(match.group(1))

    return imports[:10]


def extract_js_imports(content: str) -> List[str]:
    """Extract JavaScript/TypeScript imports."""
    imports = []
    patterns = [
        r"^import\s+.*?from\s+['\"]([^'\"]+)['\"]",
        r"^import\s+\(['\"]([^'\"]+)['\"]\)",
        r"^require\(['\"]([^'\"]+)['\"]\)"
    ]

    for line in content.split('\n'):
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                imports.append(match.group(1))

    return imports[:10]


def extract_java_imports(content: str) -> List[str]:
    """Extract Java imports."""
    imports = []
    pattern = r'^import\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*;'

    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            imports.append(match.group(1))

    return imports[:10]


def extract_go_imports(content: str) -> List[str]:
    """Extract Go imports."""
    imports = []
    pattern1 = r'^import\s+"([^"]+)"'
    pattern2 = r"^import\s+'([^']+)'"

    for line in content.split('\n'):
        match = re.match(pattern1, line.strip())
        if not match:
            match = re.match(pattern2, line.strip())
        if match:
            imports.append(match.group(1))

    return imports[:10]


def extract_cpp_includes(content: str) -> List[str]:
    """Extract C/C++ includes."""
    includes = []
    pattern1 = r'^#include\s+<([^>]+)>'
    pattern2 = r'^#include\s+"([^"]+)"'

    for line in content.split('\n'):
        match = re.match(pattern1, line.strip())
        if not match:
            match = re.match(pattern2, line.strip())
        if match:
            includes.append(match.group(1))

    return includes[:10]


def is_internal_import(import_name: str, file_path: Path) -> bool:
    """Check if import is internal."""
    if import_name.startswith('.') or import_name.startswith('@/'):
        return True

    project_prefixes = ['app', 'src', 'lib', 'components', 'utils', 'services']
    for prefix in project_prefixes:
        if import_name.startswith(prefix + '/') or import_name.startswith(prefix + '.'):
            return True

    return False


def infer_output(file_path: Path, lang_config: Dict) -> Dict[str, any]:
    """Infer OUTPUT description, returns dict with classes and functions."""
    content = read_file_safe(file_path)
    if not content:
        return {'classes': [], 'functions': [], 'type': 'Code file'}

    file_name = file_path.name.lower()

    if 'test' in file_name or 'spec' in file_name:
        return {'classes': [], 'functions': [], 'type': 'Test cases'}
    elif 'config' in file_name:
        return {'classes': [], 'functions': [], 'type': 'Configuration'}
    elif file_name.endswith('.md'):
        return {'classes': [], 'functions': [], 'type': 'Documentation'}
    elif lang_config['name'] in ['HTML', 'CSS']:
        return {'classes': [], 'functions': [], 'type': f'{lang_config["name"]} code'}
    else:
        classes = extract_classes(content, lang_config['name'])
        functions = extract_functions(content, lang_config['name'])
        return {'classes': classes[:10], 'functions': functions[:10], 'type': 'Code implementation'}


def extract_classes(content: str, lang_name: str) -> List[str]:
    """Extract class definitions."""
    classes = []

    if lang_name == 'Python':
        pattern = r'^class\s+([A-Z][a-zA-Z0-9_]*)'
    elif lang_name in ['JavaScript', 'TypeScript']:
        pattern = r'^class\s+([A-Z][a-zA-Z0-9_]*)'
    elif lang_name == 'Java':
        pattern = r'^(?:public\s+)?class\s+([A-Z][a-zA-Z0-9_]*)'
    elif lang_name == 'Go':
        pattern = r'^type\s+([A-Z][a-zA-Z0-9_]*)\s+struct'
    else:
        return []

    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            classes.append(match.group(1))

    return classes[:10]


def extract_functions(content: str, lang_name: str) -> List[str]:
    """Extract function definitions."""
    functions = []

    if lang_name == 'Python':
        pattern = r'^def\s+([a-z_][a-zA-Z0-9_]*)\s*\('
    elif lang_name in ['JavaScript', 'TypeScript']:
        pattern = r'^(?:function\s+|const\s+|let\s+)?([a-z_][a-zA-Z0-9_]*)\s*=\s*(?:\([^)]*\)\s*=>|function)'
    elif lang_name == 'Java':
        pattern = r'^(?:public|private|protected)?\s*(?:static\s+)?(?:\w+)\s+([a-z_][a-zA-Z0-9_]*)\s*\('
    elif lang_name == 'Go':
        pattern = r'^func\s+(?:\([a-z]*\)\s+)?([A-Z][a-zA-Z0-9_]*)\s*\('
    else:
        return []

    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            functions.append(match.group(1))

    return functions[:20]


def infer_position(file_path: Path, parent_dir: str, file_name: str) -> str:
    """Infer POS description."""
    special_files = {
        'index.js': 'Module entry',
        'index.ts': 'Module entry',
        'main.py': 'Application entry',
        'main.js': 'Application entry',
        'main.ts': 'Application entry',
        'app.py': 'Application entry',
        'app.js': 'Application entry',
        'app.ts': 'Application entry',
        '__init__.py': 'Module initialization',
        'package.json': 'Package configuration',
        'dockerfile': 'Container configuration',
        'readme.md': 'Project documentation',
    }

    if file_name in special_files:
        return special_files[file_name]

    if 'api' in parent_dir or 'route' in parent_dir or 'controller' in parent_dir:
        return 'API layer - handles requests and responses'
    elif 'model' in parent_dir or 'schema' in parent_dir or 'type' in parent_dir:
        return 'Data layer - defines data structures'
    elif 'service' in parent_dir:
        return 'Business logic layer - implements core functionality'
    elif 'util' in parent_dir or 'helper' in parent_dir or 'lib' in parent_dir:
        return 'Utility layer - provides helper functions'
    elif 'component' in parent_dir or 'view' in parent_dir:
        return 'View layer - UI components'
    elif 'config' in parent_dir:
        return 'Configuration layer - manages settings'
    elif 'test' in parent_dir or 'spec' in parent_dir:
        return 'Test layer - test cases'
    elif 'middleware' in parent_dir:
        return 'Middleware layer - handles interception logic'

    if 'test' in file_name or 'spec' in file_name:
        return 'Test file'
    elif 'config' in file_name:
        return 'Configuration file'
    elif file_name.endswith('.md'):
        return 'Documentation'

    return 'Functional module'


def read_file_safe(file_path: Path) -> Optional[str]:
    """Safely read file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Failed to read {file_path}: {e}")
        return None


def has_existing_header(content: str, comment_style: str) -> bool:
    """Check if header comments already exist."""
    lines = content.split('\n')
    if len(lines) < 3:
        return False

    first_lines_clean = []
    for line in lines[:15]:
        cleaned = line.strip()
        for prefix in ['#', '//', '<!--', '/*', '--']:
            if cleaned.startswith(prefix):
                if prefix in ['<!--', '/*']:
                    cleaned = cleaned[len(prefix):].strip()
                else:
                    cleaned = cleaned[len(prefix):].strip()
                break
        first_lines_clean.append(cleaned)

    combined = ' '.join(first_lines_clean).upper()
    return 'INPUT:' in combined and 'OUTPUT:' in combined and 'POS:' in combined


def build_multiline_header(header_info: Dict[str, any], comment_style: str, is_line_comment: bool, comment_end: str = '') -> List[str]:
    """Build multiline header comments."""
    header_lines = []
    input_info = header_info['INPUT']
    output_info = header_info['OUTPUT']
    pos_desc = header_info['POS']

    if is_line_comment:
        # INPUT section
        header_lines.append(f"{comment_style} INPUT:")
        if input_info['internal']:
            header_lines.append(f"{comment_style}   Internal: {', '.join(input_info['internal'])}")
        if input_info['external']:
            header_lines.append(f"{comment_style}   External: {', '.join(input_info['external'])}")
        if not input_info['internal'] and not input_info['external']:
            header_lines.append(f"{comment_style}   No special dependencies")

        # OUTPUT section
        header_lines.append(f"{comment_style} OUTPUT:")
        if output_info['classes']:
            header_lines.append(f"{comment_style}   Classes: {', '.join(output_info['classes'])}")
        if output_info['functions']:
            header_lines.append(f"{comment_style}   Functions: {', '.join(output_info['functions'])}")
        if not output_info['classes'] and not output_info['functions']:
            header_lines.append(f"{comment_style}   {output_info['type']}")

        # POS section
        header_lines.append(f"{comment_style} POS: {pos_desc}")
    else:
        # Block comment style (HTML, CSS)
        header_lines.append(f"{comment_style} INPUT:")
        if input_info['internal']:
            header_lines.append(f"     Internal: {', '.join(input_info['internal'])}")
        if input_info['external']:
            header_lines.append(f"     External: {', '.join(input_info['external'])}")
        if not input_info['internal'] and not input_info['external']:
            header_lines.append("     No special dependencies")

        header_lines.append("   OUTPUT:")
        if output_info['classes']:
            header_lines.append(f"     Classes: {', '.join(output_info['classes'])}")
        if output_info['functions']:
            header_lines.append(f"     Functions: {', '.join(output_info['functions'])}")
        if not output_info['classes'] and not output_info['functions']:
            header_lines.append(f"     {output_info['type']}")

        header_lines.append(f"   POS: {pos_desc} {comment_end}")

    return header_lines


def add_or_update_header(file_path: Path, header_info: Dict[str, any], dry_run: bool = False):
    """Add or update file header comments."""
    lang_config = header_info['lang_config']
    comment_style = lang_config['comment_style']
    is_line_comment = lang_config.get('line_comment', True)
    comment_end = lang_config.get('comment_end', '')

    content = read_file_safe(file_path)
    if not content:
        return

    lines = content.split('\n')

    shebang = ''
    if lines and lines[0].startswith('#!'):
        shebang = lines[0]
        lines = lines[1:]

    encoding = ''
    if lines and ('coding' in lines[0] or 'encoding' in lines[0]):
        encoding = lines[0]
        lines = lines[1:]

    if has_existing_header(content, comment_style):
        header_end = 0
        in_header = True
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            if in_header and any(stripped.startswith(prefix) for prefix in ['#', '//', '<!--', '/*', '--', '*']):
                header_end = i + 1
            else:
                in_header = False
                break
        start_idx = header_end
    else:
        start_idx = 0

    header_lines = []

    if shebang:
        header_lines.append(shebang)
    if encoding:
        header_lines.append(encoding)

    header_lines.extend(build_multiline_header(header_info, comment_style, is_line_comment, comment_end))

    new_content = '\n'.join(header_lines) + '\n\n' + '\n'.join(lines[start_idx:]).lstrip()

    input_info = header_info['INPUT']
    output_info = header_info['OUTPUT']

    if dry_run:
        print(f"[DRY RUN] Would update {file_path}:")
        print("  INPUT:")
        if input_info['internal']:
            print(f"    Internal: {', '.join(input_info['internal'])}")
        if input_info['external']:
            print(f"    External: {', '.join(input_info['external'])}")
        print("  OUTPUT:")
        if output_info['classes']:
            print(f"    Classes: {', '.join(output_info['classes'])}")
        if output_info['functions']:
            print(f"    Functions: {', '.join(output_info['functions'])}")
        print(f"  POS: {header_info['POS']}")
        print(f"  Language: {lang_config['name']}")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {file_path} ({lang_config['name']})")


def process_directory(directory: Path, dry_run: bool = False, file_pattern: str = None):
    """Process all files in directory."""
    supported_extensions = set()
    for config in LANGUAGE_CONFIG.values():
        supported_extensions.update(config['extensions'])

    all_files = []
    for ext in supported_extensions:
        all_files.extend(directory.rglob(f'*{ext}'))

    all_files.extend(directory.rglob('Dockerfile'))

    excluded_dirs = {
        '.git', '.venv', 'venv', '__pycache__', 'node_modules',
        '.pytest_cache', '.ruff_cache', 'dist', 'build', 'target',
        '.next', '.nuxt', 'vendor', 'bower_components'
    }

    filtered_files = [
        f for f in all_files
        if not any(excluded in f.parts for excluded in excluded_dirs)
    ]

    if file_pattern:
        import fnmatch
        filtered_files = [
            f for f in filtered_files
            if fnmatch.fnmatch(f.name, file_pattern)
        ]

    for file_path in filtered_files:
        header_info = analyze_file_header(file_path)
        add_or_update_header(file_path, header_info, dry_run)


def main():
    """Main function."""
    import argparse

    supported_types = []
    for config in LANGUAGE_CONFIG.values():
        supported_types.extend(config['extensions'])

    parser = argparse.ArgumentParser(
        description='Add INPUT/OUTPUT/POS headers to source code files',
        epilog=f'Supported file types: {", ".join(sorted(set(supported_types)))}'
    )
    parser.add_argument('path', help='File or directory to process')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying them')
    parser.add_argument('--pattern', help='Only process files matching this pattern (e.g., "*.py")')

    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        print(f"❌ Error: {path} does not exist")
        sys.exit(1)

    if path.is_file():
        header_info = analyze_file_header(path)
        add_or_update_header(path, header_info, args.dry_run)
    else:
        process_directory(path, args.dry_run, args.pattern)


if __name__ == '__main__':
    main()
