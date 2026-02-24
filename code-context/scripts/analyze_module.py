#!/usr/bin/env python3
"""
Analyze module structure and generate/update Claude.md files.

Supports multiple programming languages and project types.
"""

import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    '.py',
    '.js', '.jsx', '.ts', '.tsx', '.mjs',
    '.java',
    '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx',
    '.go',
    '.rs',
    '.rb',
    '.php',
    '.swift',
    '.kt', '.kts',
    '.scala',
    '.sh', '.bash', '.zsh',
    '.sql',
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.yaml', '.yml', '.toml', '.json', '.xml',
    '.md',
}


def should_process_file(file_path: Path) -> bool:
    """Check if file should be processed."""
    if file_path.name.startswith('.') or file_path.name.startswith('_'):
        if file_path.name not in ['__init__.py', '.gitignore', '.dockerignore']:
            return False

    ext = file_path.suffix.lower()
    if ext in SUPPORTED_EXTENSIONS:
        return True

    if file_path.name in ['Dockerfile', 'dockerfile', 'Makefile', 'CMakeLists.txt']:
        return True

    return False


def is_xcode_project(directory: Path) -> bool:
    """Detect if this is an Xcode/iOS project."""
    # Check for Xcode project indicators
    xcode_indicators = [
        '*.xcodeproj',
        'Package.swift',
        'Podfile',
    ]

    # Search in current directory and parent directories
    current = directory
    while current != current.root:
        for indicator in xcode_indicators:
            if list(current.glob(indicator)):
                return True
        current = current.parent

    return False


def get_claude_md_filename(directory: Path) -> str:
    """Generate CLAUDE.md filename, with special handling for Xcode projects."""
    # Default filename
    if not is_xcode_project(directory):
        return 'CLAUDE.md'

    # For Xcode projects, use path-based naming
    # Get relative path from project root
    project_root = find_xcode_project_root(directory)
    if project_root and directory != project_root:
        relative_path = directory.relative_to(project_root)
        # Convert path segments to filename: CLAUDE_folder1_folder2.md
        path_parts = '_'.join(relative_path.parts)
        return f'CLAUDE_{path_parts}.md'

    return 'CLAUDE.md'


def find_xcode_project_root(directory: Path) -> Path | None:
    """Find the Xcode project root directory."""
    current = directory

    while current != current.root:
        # Check for Xcode project indicators
        if list(current.glob('*.xcodeproj')):
            return current
        if (current / 'Package.swift').exists():
            return current
        if (current / 'Podfile').exists():
            return current

        current = current.parent

    return None


def detect_project_type(directory: Path) -> str:
    """Detect project type."""
    files = list(directory.iterdir())
    file_names = {f.name for f in files}

    if is_xcode_project(directory):
        return 'Swift/Xcode'
    elif 'package.json' in file_names or 'tsconfig.json' in file_names:
        return 'JavaScript/TypeScript'
    elif 'requirements.txt' in file_names or 'setup.py' in file_names or 'pyproject.toml' in file_names:
        return 'Python'
    elif 'pom.xml' in file_names or 'build.gradle' in file_names:
        return 'Java'
    elif 'go.mod' in file_names:
        return 'Go'
    elif 'Cargo.toml' in file_names:
        return 'Rust'
    elif 'Gemfile' in file_names:
        return 'Ruby'
    elif 'composer.json' in file_names:
        return 'PHP'

    return 'Mixed/Unknown'


def analyze_module(directory: Path) -> dict[str, any]:
    """Analyze module structure."""
    files = []
    subdirs = []

    for item in directory.iterdir():
        if item.is_file() and should_process_file(item):
            files.append(item)
        elif item.is_dir() and not item.name.startswith('.'):
            if item.name not in ['__pycache__', 'node_modules', '.git', 'dist', 'build', 'target', 'vendor']:
                subdirs.append(item)

    file_info_list = []
    for file_path in files:
        info = analyze_file(file_path)
        file_info_list.append(info)

    all_imports = set()
    all_exports = set()

    for info in file_info_list:
        all_imports.update(info.get('imports', []))
        all_exports.update(info.get('exports', []))

    return {
        'files': file_info_list,
        'subdirectories': [d.name for d in subdirs],
        'imports': list(all_imports),
        'exports': list(all_exports),
        'project_type': detect_project_type(directory)
    }


def analyze_file(file_path: Path) -> dict[str, any]:
    """Analyze a single file."""
    ext = file_path.suffix.lower()
    content = read_file_safe(file_path)

    if not content:
        return {
            'name': file_path.name,
            'type': ext,
            'language': detect_language(ext),
            'imports': [],
            'exports': [],
            'functions': 0,
            'classes': 0,
            'description': 'Unable to read file'
        }

    language = detect_language(ext)

    if language == 'Python':
        return analyze_python_file(file_path, content)
    elif language in ['JavaScript', 'TypeScript']:
        return analyze_js_file(file_path, content)
    elif language == 'Java':
        return analyze_java_file(file_path, content)
    elif language in ['C', 'C++']:
        return analyze_cpp_file(file_path, content)
    elif language == 'Go':
        return analyze_go_file(file_path, content)
    elif language == 'Swift':
        return analyze_swift_file(file_path, content)
    else:
        return analyze_generic_file(file_path, content, language)


def detect_language(ext: str) -> str:
    """Detect language from extension."""
    lang_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.mjs': 'JavaScript',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.h': 'C/C++',
        '.hpp': 'C++',
        '.hxx': 'C++',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.kts': 'Kotlin',
        '.scala': 'Scala',
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.zsh': 'Shell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.scss': 'CSS',
        '.sass': 'CSS',
        '.less': 'CSS',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
        '.json': 'JSON',
        '.xml': 'XML',
        '.md': 'Markdown',
    }
    return lang_map.get(ext, 'Unknown')


def analyze_python_file(file_path: Path, content: str) -> dict:
    """Analyze Python file."""
    import re

    imports = []
    classes = []
    functions = []
    exports = []

    import_patterns = [
        r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
    ]

    for line in content.split('\n'):
        for pattern in import_patterns:
            match = re.match(pattern, line.strip())
            if match:
                imports.append(match.group(1))

    for line in content.split('\n'):
        class_match = re.match(r'^class\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if class_match:
            classes.append(class_match.group(1))

        func_match = re.match(r'^def\s+([a-z_][a-zA-Z0-9_]*)\s*\(', line.strip())
        if func_match:
            functions.append(func_match.group(1))

    all_match = re.search(r"__all__\s*=\s*\[(.*?)\]", content, re.DOTALL)
    if all_match:
        exports = [e.strip().strip('"\'') for e in all_match.group(1).split(',') if e.strip()]

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': 'Python',
        'imports': imports[:10],
        'exports': exports,
        'functions': functions,
        'classes': classes,
        'description': infer_file_description(file_path, classes, functions)
    }


def analyze_js_file(file_path: Path, content: str) -> dict:
    """Analyze JavaScript/TypeScript file."""
    import re

    imports = []
    classes = []
    functions = []
    exports = []

    import_patterns = [
        r"^import\s+.*?from\s+['\"]([^'\"]+)['\"]",
        r"^import\s+\(['\"]([^'\"]+)['\"]\)",
        r"^require\(['\"]([^'\"]+)['\"]\)",
        r"^import\s+\{([^}]+)\}"
    ]

    for line in content.split('\n'):
        for pattern in import_patterns:
            match = re.match(pattern, line.strip())
            if match:
                imports.append(match.group(1))

    for line in content.split('\n'):
        class_match = re.match(r'^class\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if class_match:
            classes.append(class_match.group(1))

        func_match = re.match(r'^(?:function\s+|const\s+|let\s+)?([a-z_][a-zA-Z0-9_]*)\s*=\s*(?:\([^)]*\)\s*=>|function)', line.strip())
        if func_match and not func_match.group(1).startswith('if'):
            functions.append(func_match.group(1))

    export_patterns = [
        r"^export\s+(?:const|let|function|class)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        r"^export\s+\{([^}]+)\}"
    ]
    for line in content.split('\n'):
        for pattern in export_patterns:
            match = re.match(pattern, line.strip())
            if match:
                exports.append(match.group(1))

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': detect_language(file_path.suffix),
        'imports': imports[:10],
        'exports': exports,
        'functions': functions,
        'classes': classes,
        'description': infer_file_description(file_path, classes, functions)
    }


def analyze_java_file(file_path: Path, content: str) -> dict:
    """Analyze Java file."""
    import re

    imports = []
    classes = []
    methods = []

    for line in content.split('\n'):
        match = re.match(r'^import\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*;', line.strip())
        if match:
            imports.append(match.group(1))

    class_match = re.search(r'^(?:public\s+)?class\s+([A-Z][a-zA-Z0-9_]*)', content)
    if class_match:
        classes.append(class_match.group(1))

    for line in content.split('\n'):
        match = re.match(r'^(?:public|private|protected)?\s*(?:static\s+)?(?:\w+)\s+([a-z_][a-zA-Z0-9_]*)\s*\(', line.strip())
        if match:
            methods.append(match.group(1))

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': 'Java',
        'imports': imports[:10],
        'exports': classes,
        'functions': methods,
        'classes': classes,
        'description': infer_file_description(file_path, classes, methods)
    }


def analyze_cpp_file(file_path: Path, content: str) -> dict:
    """Analyze C/C++ file."""
    import re

    includes = []
    classes = []
    functions = []

    for line in content.split('\n'):
        match = re.match(r'^#include\s+[<\"]([^>\"]+)[>\"]', line.strip())
        if match:
            includes.append(match.group(1))

    for line in content.split('\n'):
        class_match = re.match(r'^class\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if class_match:
            classes.append(class_match.group(1))

        func_match = re.match(r'^(?:\w+\s+)+([a-z_][a-zA-Z0-9_]*)\s*\(', line.strip())
        if func_match:
            functions.append(func_match.group(1))

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': detect_language(file_path.suffix),
        'imports': includes[:10],
        'exports': [],
        'functions': functions,
        'classes': classes,
        'description': infer_file_description(file_path, classes, functions)
    }


def analyze_go_file(file_path: Path, content: str) -> dict:
    """Analyze Go file."""
    import re

    imports = []
    structs = []
    functions = []

    for line in content.split('\n'):
        match = re.match(r'^import\s+"([^"]+)"', line.strip())
        if not match:
            match = re.match(r"^import\s+'([^']+)'", line.strip())
        if match:
            imports.append(match.group(1))

    for line in content.split('\n'):
        struct_match = re.match(r'^type\s+([A-Z][a-zA-Z0-9_]*)\s+struct', line.strip())
        if struct_match:
            structs.append(struct_match.group(1))

        func_match = re.match(r'^func\s+(?:\([a-z]*\)\s+)?([A-Z][a-zA-Z0-9_]*)\s*\(', line.strip())
        if func_match:
            functions.append(func_match.group(1))

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': 'Go',
        'imports': imports[:10],
        'exports': functions,
        'functions': functions,
        'classes': structs,
        'description': infer_file_description(file_path, structs, functions)
    }


def analyze_swift_file(file_path: Path, content: str) -> dict:
    """Analyze Swift file."""
    import re

    imports = []
    classes = []
    structs = []
    enums = []
    functions = []
    protocols = []

    # Extract imports
    for line in content.split('\n'):
        match = re.match(r'^import\s+([A-Za-z][A-Za-z0-9_]*)', line.strip())
        if match:
            imports.append(match.group(1))

    # Extract classes
    for line in content.split('\n'):
        class_match = re.match(r'^class\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if class_match:
            classes.append(class_match.group(1))

    # Extract structs
    for line in content.split('\n'):
        struct_match = re.match(r'^struct\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if struct_match:
            structs.append(struct_match.group(1))

    # Extract enums
    for line in content.split('\n'):
        enum_match = re.match(r'^enum\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if enum_match:
            enums.append(enum_match.group(1))

    # Extract protocols
    for line in content.split('\n'):
        protocol_match = re.match(r'^protocol\s+([A-Z][a-zA-Z0-9_]*)', line.strip())
        if protocol_match:
            protocols.append(protocol_match.group(1))

    # Extract functions
    for line in content.split('\n'):
        func_match = re.match(r'^func\s+([a-z_][a-zA-Z0-9_]*)\s*\(', line.strip())
        if func_match:
            functions.append(func_match.group(1))

    # Combine types for exports
    all_types = classes + structs + enums + protocols

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': 'Swift',
        'imports': imports[:10],
        'exports': all_types,
        'functions': functions,
        'classes': all_types,  # Includes classes, structs, enums, protocols
        'description': infer_swift_file_description(file_path, classes, structs, enums, functions)
    }


def infer_swift_file_description(file_path: Path, classes: list, structs: list, enums: list, functions: list) -> str:
    """Infer Swift file description."""
    name = file_path.name.lower()

    if 'view' in name:
        return 'SwiftUI or UIKit view component'
    elif 'viewmodel' in name or 'store' in name:
        return 'View model or state management'
    elif 'model' in name:
        return 'Data model definition'
    elif classes or structs or enums:
        type_count = len(classes) + len(structs) + len(enums)
        return f"Defines {type_count} types"
    elif functions:
        return f"Defines {len(functions)} functions"
    else:
        return 'Swift implementation'


def analyze_generic_file(file_path: Path, content: str, language: str) -> dict:
    """Analyze generic file."""
    file_type = infer_file_type(file_path)

    return {
        'name': file_path.name,
        'type': file_path.suffix,
        'language': language,
        'imports': [],
        'exports': [],
        'functions': [],
        'classes': [],
        'description': file_type
    }


def infer_file_type(file_path: Path) -> str:
    """Infer file type."""
    name = file_path.name.lower()

    if 'test' in name or 'spec' in name:
        return 'Test file'
    elif 'config' in name:
        return 'Configuration file'
    elif name.endswith('.md'):
        return 'Documentation'
    elif name in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 'go.mod', 'cargo.toml']:
        return 'Project configuration'
    elif name in ['readme', 'license', 'changelog']:
        return 'Project documentation'
    elif name in ['makefile', 'dockerfile', 'cmakelists.txt']:
        return 'Build script'

    ext = file_path.suffix.lower()
    type_map = {
        '.html': 'HTML file',
        '.css': 'Style file',
        '.scss': 'SASS style',
        '.sass': 'SASS style',
        '.json': 'JSON configuration',
        '.yaml': 'YAML configuration',
        '.yml': 'YAML configuration',
        '.toml': 'TOML configuration',
        '.xml': 'XML file',
        '.sql': 'SQL script',
        '.sh': 'Shell script',
    }

    return type_map.get(ext, 'Code file')


def infer_file_description(file_path: Path, classes: list, functions: list) -> str:
    """Infer file description."""
    name = file_path.name.lower()

    if 'test' in name or 'spec' in name:
        return 'Test cases'
    elif 'config' in name:
        return 'Configuration'
    elif classes:
        return f"Defines {len(classes)} classes"
    elif functions:
        return f"Defines {len(functions)} functions"
    else:
        return 'Code implementation'


def read_file_safe(file_path: Path) -> str:
    """Safely read file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Failed to read {file_path}: {e}")
        return None


def generate_claude_md(directory: Path, module_info: dict, output_path: Path = None):
    """Generate CLAUDE.md file."""
    if output_path is None:
        output_path = directory / get_claude_md_filename(directory)

    position = infer_module_position(directory, module_info)
    logic = infer_module_logic(directory, module_info)
    constraints = infer_module_constraints(directory, module_info)

    domain_list = generate_domain_list(module_info)

    content = f"""# {directory.name} Module

## Position

This module is responsible for: {position}

## Logic

This module executes: {logic}

## Constraints

When using this module, follow these constraints:

{constraints}

## Domain List

This module contains the following submodules and features:

| Name | Type | Language/Format | Description |
|------|------|-----------------|-------------|
"""

    for item in domain_list:
        content += f"| {item['name']} | {item['type']} | {item.get('language', '-')} | {item['description']} |\n"

    if module_info['imports']:
        content += f"""

## Dependencies

This module depends on:
{', '.join(module_info['imports'][:10])}
"""

    if module_info['exports']:
        content += f"""

This module exports:
{', '.join(module_info['exports'][:10])}
"""

    content += f"""

## Tech Stack

Project type: {module_info['project_type']}
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Generated {output_path}")


def infer_module_position(directory: Path, module_info: dict) -> str:
    """Infer module position."""
    dir_name = directory.name.lower()

    positions = {
        'api': 'API layer, handles requests and responses',
        'apis': 'API layer, handles requests and responses',
        'routes': 'API layer, defines routes',
        'controllers': 'Controller layer, handles request logic',
        'models': 'Data layer, defines data models',
        'schemas': 'Data layer, defines data structures',
        'types': 'Type definition layer',
        'services': 'Business logic layer, implements core functionality',
        'utils': 'Utility layer, provides helper functions',
        'helpers': 'Utility layer, provides helper functions',
        'lib': 'Library',
        'config': 'Configuration layer, manages settings',
        'configs': 'Configuration layer, manages settings',
        'components': 'Component layer, UI components',
        'views': 'View layer',
        'tests': 'Test layer',
        'test': 'Test layer',
        'specs': 'Test layer',
        'src': 'Source code directory',
        'docs': 'Documentation directory',
    }

    for key, value in positions.items():
        if key in dir_name:
            return value

    return 'Functional module'


def infer_module_logic(directory: Path, module_info: dict) -> str:
    """Infer module logic."""
    dir_name = directory.name.lower()
    file_count = len(module_info['files'])

    logics = {
        'api': 'Defines API endpoints, handles HTTP requests and responses',
        'routes': 'Defines routing rules',
        'models': 'Defines data models and validation rules',
        'services': 'Implements business logic, coordinates data and external services',
        'utils': 'Provides reusable utility functions',
        'helpers': 'Provides helper functions',
        'config': 'Loads and manages application configuration',
        'components': 'Defines reusable UI components',
    }

    for key, value in logics.items():
        if key in dir_name:
            return value

    return f"Contains {file_count} files, provides related functionality"


def infer_module_constraints(directory: Path, module_info: dict) -> str:
    """Infer module constraints."""
    dir_name = directory.name.lower()

    constraints = {
        'api': '- API endpoints should follow RESTful design principles\n- All endpoints need proper authentication and authorization\n- Request parameters must be validated',
        'services': '- Services should be stateless\n- Complex operations should be split into smaller functions\n- Exceptions must be handled properly',
        'models': '- Models must define types and validation rules\n- Sensitive data must be encrypted',
    }

    for key, value in constraints.items():
        if key in dir_name:
            return value

    return '- Refer to specific file documentation'


def generate_domain_list(module_info: dict) -> list[dict]:
    """Generate domain list."""
    items = []

    for file_info in module_info['files']:
        items.append({
            'name': file_info['name'],
            'type': 'File',
            'language': file_info.get('language', '-'),
            'description': file_info.get('description', 'Code file')
        })

    for subdir in module_info['subdirectories']:
        items.append({
            'name': subdir,
            'type': 'Directory',
            'description': 'Submodule'
        })

    return items


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze module and generate Claude.md')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--output', help='Output path for Claude.md')

    args = parser.parse_args()

    directory = Path(args.directory)

    if not directory.exists():
        print(f"❌ Error: Directory {directory} does not exist")
        sys.exit(1)

    if not directory.is_dir():
        print(f"❌ Error: {directory} is not a directory")
        sys.exit(1)

    output_path = Path(args.output) if args.output else None

    module_info = analyze_module(directory)
    generate_claude_md(directory, module_info, output_path)


if __name__ == '__main__':
    main()
