# Code Context

Automatically maintain codebase context documentation and comments, supporting all major programming languages.

## Features

- **Multi-language Support**: Python, JavaScript/TypeScript, Java, Go, Rust, C/C++, Ruby, PHP, Swift/Xcode, Kotlin, etc.
- **Auto Comments**: Add INPUT/OUTPUT/POS header comments to source files
- **Module Documentation**: Generate CLAUDE.md files for each business module
  - Xcode/iOS projects use path-based naming: `CLAUDE_folder1_folder2.md`
- **Git Hook**: Support automatic updates to keep documentation in sync with code

## Quick Start

```bash
# Add comments to entire project
python3 scripts/add_file_headers.py .

# Generate module documentation
python3 scripts/analyze_module.py .

# Full update (comments + documentation)
python3 scripts/update_context.py

# Install Git hook
python3 scripts/install_git_hook.py
```

## Supported Languages

| Language | Extensions | Comment Format |
|----------|------------|----------------|
| Python | .py | `#` |
| JavaScript/TypeScript | .js, .ts, .jsx, .tsx | `//` |
| Java | .java | `//` |
| Go | .go | `//` |
| Rust | .rs | `//` |
| C/C++ | .c, .cpp, .h | `//` |
| Ruby | .rb | `#` |
| PHP | .php | `//` |
| Swift | .swift | `//` |
| Kotlin | .kt | `//` |
| Shell | .sh, .bash | `#` |
| SQL | .sql | `--` |
| HTML | .html | `<!-- -->` |
| CSS | .css, .scss | `/* */` |

## File Formats

### Header Comments (Multi-line Format)

```python
# INPUT:
#   Internal: app.models, app.services
#   External: pydantic, sqlalchemy
# OUTPUT:
#   Classes: UserService, AuthService
#   Functions: create_user, get_user, update_user
# POS: Business logic layer - implements core functionality
```

### CLAUDE.md

```markdown
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
```

## Scripts

- `add_file_headers.py` - Add/update file header comments
- `analyze_module.py` - Analyze module and generate CLAUDE.md
- `update_context.py` - Main update script
- `install_git_hook.py` - Install Git hook

## References

- [Header Comment Format](references/header_format.md)
- [CLAUDE.md Format](references/claude_md_format.md)
- [Template File](assets/templates/claude.md.template)

## License

MIT
