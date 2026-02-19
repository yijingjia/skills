# Lint Manager

A comprehensive lint configuration and error management skill for multi-language projects.

## Features

- **Language Detection**: Automatically detects programming languages in your project
- **Tool Installation**: Installs appropriate lint tools (ESLint, Ruff, SwiftLint, golangci-lint)
- **Configuration Generation**: Provides ready-to-use config templates
- **Lint Execution**: Runs lint checks with auto-fix support
- **Pre-commit Integration**: Supports staged-only linting for git hooks

## Supported Languages

| Language | Lint Tool | Config File |
|----------|-----------|-------------|
| JavaScript | ESLint | `.eslintrc.json` |
| TypeScript | ESLint | `.eslintrc.json` |
| Python | Ruff | `pyproject.toml` |
| Swift | SwiftLint | `.swiftlint.yml` |
| Go | golangci-lint | `.golangci.yml` |

## Directory Structure

```
lint-manager/
├── SKILL.md              # Skill definition for AI agents
├── README.md             # This file
├── scripts/
│   ├── detect_language.py    # Language detection script
│   ├── install_linter.py     # Linter installation script
│   └── run_lint.py           # Lint execution script
├── references/
│   ├── javascript.md     # ESLint documentation
│   ├── python.md         # Ruff documentation
│   ├── swift.md          # SwiftLint documentation
│   └── go.md             # golangci-lint documentation
└── assets/
    ├── eslintrc.json             # JavaScript ESLint config
    ├── eslintrc.typescript.json  # TypeScript ESLint config
    ├── ruff.toml                 # Python Ruff config
    ├── swiftlint.yml             # Swift SwiftLint config
    └── golangci.yml              # Go golangci-lint config
```

## Quick Start

### 1. Detect Languages

```bash
python3 scripts/detect_language.py /path/to/project
```

### 2. Install Lint Tools

```bash
# Install for specific language
python3 scripts/install_linter.py --language python --preset minimal

# Auto-detect and install all
python3 scripts/install_linter.py --preset minimal
```

### 3. Run Lint

```bash
# Lint all files
python3 scripts/run_lint.py

# Lint staged files only
python3 scripts/run_lint.py --staged

# Auto-fix issues
python3 scripts/run_lint.py --fix
```

## Configuration Presets

- **minimal**: Essential rules only, fast execution, recommended for new projects
- **full**: All recommended rules, strict checking, for production codebases

## License

MIT
