# Swift Linting

## SwiftLint

**Tool**: SwiftLint
**Install**: `brew install swiftlint`
**Config**: `.swiftlint.yml`

### Key Rules

| Category | Rules |
|----------|-------|
| Style | line_length, identifier_name, indentation_width |
| Quality | force_unwrapping, force_cast, syntactic_sugar |
| Complexity | cyclomatic_complexity, function_body_length |
| Patterns | large_tuple, nesting, type_body_length |

### Configuration Levels

**Minimal**:
- Style rules (indentation, line length)
- Basic quality (force_unwrapping)
- Auto-fixable rules

**Strict**:
- All minimal +
- Complexity limits
- Custom rules for project standards

### Common Commands

```bash
# Lint all files
swiftlint lint

# Lint specific path
swiftlint lint --path Sources/

# Auto-fix issues
swiftlint --fix

# Generate config
swiftlint generate-config > .swiftlint.yml

# Print version
swiftlint version
```

### Xcode Build Phase Integration

Add to Build Phases in Xcode:

```
if which swiftlint >/dev/null; then
  swiftlint
else
  echo "warning: swiftlint not installed"
fi
```

### Opt-in Rules

Enable advanced rules:
```yaml
opt_in_rules:
  - empty_count
  - empty_string
  - explicit_init
  - closure_spacing
  - sorted_imports
```

### Custom Rules

Define project-specific patterns:
```yaml
custom_rules:
  marks:
    name: "Mark Comments"
    regex: '\\b(marks?|x?todo|fixme)\\b'
    message: "TODO or FIXME found"
    match_kinds:
      - comment
```

### Excluding Code

Inline exclusion:
```swift
// swiftlint:disable:next line_length
let veryLongString = "..."
```

Disable for entire file:
```swift
// swiftlint:disable all
// swiftlint:enable all
```
