# Python Linting

## Ruff

**Tool**: Ruff (fast Python linter)
**Install**: `pip install ruff`
**Config**: `pyproject.toml` or `ruff.toml`

### Key Rules

| Category | Rules |
|----------|-------|
| Style | E (pycodestyle), W (warnings), I (isort) |
| Quality | F (Pyflakes), B (flake8-bugbear), UP (pyupgrade) |
| Complexity | C4 (flake8-comprehensions), SIM (simplify) |
| Refactoring | ARG (unused arguments), N (naming) |

### Configuration Levels

**Minimal**:
- E, F, I (style, errors, imports)
- Fast execution (< 100ms)

**Strict**:
- All minimal +
- B, C4, UP, SIM (bug detection, simplification)
- Type checking with mypy

### Common Commands

```bash
# Lint all files
ruff check .

# Lint specific file
ruff check src/main.py

# Auto-fix issues
ruff check . --fix

# Show diff without modifying
ruff check . --diff

# Format code
ruff format .
```

### Integration with Tools

**With Black**:
```bash
# Use Ruff for linting only
ruff check .

# Use Ruff for both linting and formatting
ruff check . --fix && ruff format .
```

**Pre-commit hook**:
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.0
  hooks:
    - id: ruff
      args: [--fix]
    - id: ruff-format
```

### Ruff vs Pylint/Flake8

| Feature | Ruff | Pylint | Flake8 |
|---------|------|--------|--------|
| Speed | 10-100x faster | Slow | Medium |
| Config | TOML/YAML | INI | INI |
| Auto-fix | Yes | No | No |
| Type checking | No (use mypy) | Partial | No |
