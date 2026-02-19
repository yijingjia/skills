---
name: code-context
description: Automatically maintain codebase context documentation and comments for all major programming languages. Adds INPUT/OUTPUT/POS header comments to source files, generates Claude.md module documentation, and supports Git hooks for automatic updates. Use for keeping codebase documentation in sync with code, improving AI context understanding, adding structural comments to files, generating module-level documentation, and setting up automatic documentation workflows. Supports Python, JavaScript/TypeScript, Java, Go, Rust, C/C++, Ruby, PHP, Swift, Kotlin, Shell, SQL, HTML, and CSS.
---

# Code Context

Automatically maintain codebase context documentation and comments, supporting all major programming languages.

## Overview

This skill helps maintain codebase documentation by:
- Adding INPUT/OUTPUT/POS header comments to source files
- Generating Claude.md module documentation files
- Setting up Git hooks for automatic documentation updates
- Supporting 15+ programming languages

## Header Comment Format

### Three-Line Format

All source files include structured header comments:

\`\`\`python
# INPUT: Internal: app.models, app.services; External: pydantic, sqlalchemy
# OUTPUT: Classes: UserService, AuthService; Functions: create_user, get_user, update_user
# POS: Business logic layer — implements core functionality
\`\`\`

### Field Descriptions

**INPUT** - What the file depends on:
- Internal modules (app.models.user, app.services.auth)
- External libraries (pydantic, sqlalchemy)
- Configuration files, environment variables

**OUTPUT** - What the file provides:
- Exported classes, functions, APIs
- Data types and interfaces

**POS** - Position and role in the system:
- API layer — handles HTTP requests
- Business logic layer — implements core functionality
- Data layer — defines data structures

## Claude.md Module Documentation

Each business module directory gets a \`Claude.md\` file:

\`\`\`markdown
# Module Name

## Position
This module is responsible for: ...

## Logic
This module executes: ...

## Constraints
- ...

## Domain List
| Name | Type | Description |
|------|------|-------------|
| ... | ... | ... |
\`\`\`

## Quick Start

### Add Comments to Project

\`\`\`bash
# Add comments to entire project
python3 scripts/add_file_headers.py .

# Add comments to specific directory
python3 scripts/add_file_headers.py ./src

# Add comments for specific language
python3 scripts/add_file_headers.py . --language python
\`\`\`

### Generate Module Documentation

\`\`\`bash
# Generate Claude.md for current directory
python3 scripts/analyze_module.py .

# Generate for specific directory
python3 scripts/analyze_module.py ./src/services
\`\`\`

### Full Update

\`\`\`bash
# Run complete update (comments + documentation)
python3 scripts/update_context.py
\`\`\`

### Install Git Hook

\`\`\`bash
# Install pre-commit hook for automatic updates
python3 scripts/install_git_hook.py
\`\`\`

## Supported Languages

| Language | Extensions | Comment Format |
|----------|------------|----------------|
| Python | .py | \`#\` |
| JavaScript/TypeScript | .js, .ts, .jsx, .tsx | \`//\` |
| Java | .java | \`//\` |
| Go | .go | \`//\` |
| Rust | .rs | \`//\` |
| C/C++ | .c, .cpp, .h | \`//\` |
| Ruby | .rb | \`#\` |
| PHP | .php | \`//\` |
| Swift | .swift | \`//\` |
| Kotlin | .kt | \`//\` |
| Shell | .sh, .bash | \`#\` |
| SQL | .sql | \`--\` |
| HTML | .html | \`<!-- -->\` |
| CSS | .css, .scss | \`/* */\` |

## Common Workflows

### New Project Setup

1. **Add header comments**:
   \`\`\`bash
   python3 scripts/add_file_headers.py .
   \`\`\`

2. **Generate module documentation**:
   \`\`\`bash
   python3 scripts/analyze_module.py .
   \`\`\`

3. **Install Git hook** (optional):
   \`\`\`bash
   python3 scripts/install_git_hook.py
   \`\`\`

### Update Existing Project

1. **Add/update comments**:
   \`\`\`bash
   python3 scripts/add_file_headers.py . --update
   \`\`\`

2. **Regenerate documentation**:
   \`\`\`bash
   python3 scripts/analyze_module.py . --force
   \`\`\`

### Pre-commit Workflow

When Git hook is installed:
1. Make code changes
2. Git hook automatically runs on pre-commit
3. Header comments and Claude.md files are updated
4. Review and commit the updated documentation

## Scripts

### \`add_file_headers.py\`

Add or update file header comments.

**Usage:**
\`\`\`bash
python3 scripts/add_file_headers.py <path> [options]
\`\`\`

**Options:**
- \`--language <lang>\` - Process only specific language
- \`--update\` - Update existing headers instead of skipping
- \`--dry-run\` - Show what would be changed without making changes

### \`analyze_module.py\`

Analyze module and generate Claude.md documentation.

**Usage:**
\`\`\`bash
python3 scripts/analyze_module.py <path> [options]
\`\`\`

**Options:**
- \`--force\` - Overwrite existing Claude.md files
- \`--output <file>\` - Specify output file name (default: Claude.md)

### \`update_context.py\`

Run complete update (comments + documentation).

**Usage:**
\`\`\`bash
python3 scripts/update_context.py [path]
\`\`\`

Runs both \`add_file_headers.py\` and \`analyze_module.py\` in sequence.

### \`install_git_hook.py\`

Install Git pre-commit hook for automatic updates.

**Usage:**
\`\`\`bash
python3 scripts/install_git_hook.py
\`\`\`

**What it does:**
- Creates \`.git/hooks/pre-commit\` if not exists
- Adds hook script to run \`update_context.py\` on staged files
- Makes hook executable

## Resources

### references/

**\`header_format.md\`** - Header comment format specification
- Field descriptions (INPUT, OUTPUT, POS)
- Placement rules
- Best practices
- Load when: User asks about header comment format

**\`claude_md_format.md\`** - Claude.md format specification (Chinese)
- Module documentation structure
- Field descriptions (Position, Logic, Constraints, Domain List)
- Auto-generation details
- Load when: User asks about Claude.md files

### assets/

**\`templates/\`** - Template files for generated documentation
- \`claude.md.template\` - Claude.md template

**\`hooks/\`** - Git hook templates
- Pre-commit hook script template

## Best Practices

1. **Run on initial setup** - Add headers to all files when starting a project
2. **Update after changes** - Re-run scripts after significant code changes
3. **Manual refinement** - Auto-generated content may need manual adjustment
4. **Commit with code** - Include documentation updates in the same commit
5. **Use Git hooks** - Automate documentation maintenance with pre-commit hooks

## Error Handling

**No files found:**
- Verify the path is correct
- Check that files have supported extensions

**Permission denied:**
- Check file/directory permissions
- Ensure write access to target files

**Existing headers:**
- Use \`--update\` flag to overwrite existing headers
- Without \`--update\`, files with headers are skipped

**Git hook not working:**
- Verify \`.git/hooks/pre-commit\` is executable: \`chmod +x .git/hooks/pre-commit\`
- Check that Python scripts are executable
- Ensure script path in hook is correct

## Troubleshooting

**Comments not added:**
- Check file extension is in supported languages list
- Verify file is not in ignored directories (.git, node_modules, venv, etc.)

**Documentation inaccurate:**
- Auto-generated content is based on code analysis
- Manually edit Claude.md files to improve accuracy
- Re-run scripts after manual edits (use \`--force\` to overwrite)

**Git hook slow:**
- Hook runs on entire project by default
- Modify hook script to only process changed files
- Consider running manually instead of on every commit
