---
name: lint-manager
description: Comprehensive lint configuration and error management for multi-language projects. Automatically detects programming languages, generates appropriate lint configurations (ESLint, Ruff, SwiftLint, golangci-lint), installs required tools, runs lint checks, and auto-fixes errors with AI. Use for setting up linting for a new project, configuring pre-commit hooks, running lint on staged or specific files, auto-fixing lint errors, detecting project programming languages, and generating lint configuration files. Supports JavaScript/TypeScript, Python, Swift, and Go.
---

# Lint Manager

## Overview

Automated lint management for multi-language projects. Detects languages, generates configurations, installs tools, runs checks, and auto-fixes errors.

## Workflow

### 1. Detect Languages

Use `scripts/detect_language.py` to identify programming languages in the project:

```bash
python3 scripts/detect_language.py /path/to/project
```

Returns language list with confidence scores. Primary language is the first result.

**Example output:**
```json
{
  "detected": [
    {"language": "python", "confidence": 0.85, "score": 42},
    {"language": "javascript", "confidence": 0.15, "score": 8}
  ],
  "primary": "python"
}
```

### 2. Install Lint Tools

Use `scripts/install_linter.py` to install required lint tools:

```bash
# Install for specific language
python3 scripts/install_linter.py --language python --preset minimal

# Auto-detect and install all
python3 scripts/install_linter.py --preset minimal
```

**Presets:**
- `minimal`: Essential rules only (fast, for new projects)
- `full`: All recommended rules (strict, for production)

**Supported tools:**
- JavaScript/TypeScript: ESLint
- Python: Ruff
- Swift: SwiftLint
- Go: golangci-lint

### 3. Generate Configuration

Copy appropriate template from `assets/` to project root:

| Language | Config File | Template |
|----------|-------------|----------|
| JavaScript | `.eslintrc.json` | `assets/eslintrc.json` |
| TypeScript | `.eslintrc.json` | `assets/eslintrc.typescript.json` |
| Python | `pyproject.toml` | `assets/ruff.toml` |
| Swift | `.swiftlint.yml` | `assets/swiftlint.yml` |
| Go | `.golangci.yml` | `assets/golangci.yml` |

**Configuration strategy:** Ask user to choose between minimal (recommended for new projects) or strict (for production codebases).

### 4. Run Lint

Use `scripts/run_lint.py` to run lint checks:

```bash
# Lint all files
python3 scripts/run_lint.py

# Lint staged files only (for pre-commit)
python3 scripts/run_lint.py --staged

# Lint specific files
python3 scripts/run_lint.py --language python --files src/main.py

# Auto-fix issues
python3 scripts/run_lint.py --fix
python3 scripts/run_lint.py --fix --staged
```

### 5. Fix Errors

If lint errors are found:
1. Try auto-fix first with `--fix` flag
2. For remaining errors, use Edit tool to fix each issue
3. Re-run lint to verify fixes

## Common Workflows

### New Project Setup

1. Detect languages: `python3 scripts/detect_language.py`
2. Install tools: `python3 scripts/install_linter.py --preset minimal`
3. Ask user: "Use minimal or strict configuration?"
4. Copy config template to project root
5. Run initial lint: `python3 scripts/run_lint.py`

### Pre-commit Hook

1. Run: `python3 scripts/run_lint.py --staged --fix`
2. If errors remain, fix them with Edit tool
3. Re-run until clean

### Adding Lint to Existing Project

1. Detect languages
2. Install tools
3. Ask: "Keep existing config or generate new?"
4. If new, copy template (ask: minimal or strict?)
5. Run lint and fix any errors

## Resources

### scripts/

**`detect_language.py`**
- Scans project files and directories
- Returns detected languages with confidence scores
- Usage: Auto-detection step

**`install_linter.py`**
- Installs lint tools for detected languages
- Checks if already installed
- Supports minimal/full presets
- Usage: Tool installation

**`run_lint.py`**
- Runs lint tools on project files
- Supports staged-only mode for pre-commit
- Supports auto-fix mode
- Usage: Lint execution

### references/

Language-specific lint documentation:
- `javascript.md` - ESLint rules, TypeScript setup
- `python.md` - Ruff configuration, commands
- `swift.md` - SwiftLint rules, Xcode integration
- `go.md` - golangci-lint setup, CI integration

Load when:
- User asks about specific lint tool
- Need to troubleshoot linter issues
- User wants customization options

### assets/

Configuration file templates for each language. Copy to project root when generating configs.

## Error Handling

**Tool not installed:**
- Run `python3 scripts/install_linter.py --language <lang>`

**Config file missing:**
- Copy template from `assets/`
- Ask user: minimal or strict?

**Lint errors found:**
1. Run with `--fix` first
2. For remaining errors, parse and fix manually
3. Re-run to verify

**Permission denied:**
- Check file permissions
- Ensure tool is in PATH
