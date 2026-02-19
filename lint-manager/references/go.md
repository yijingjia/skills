# Go Linting

## golangci-lint

**Tool**: golangci-lint (meta-linter)
**Install**: See below
**Config**: `.golangci.yml`

### Installation

```bash
# macOS/Linux
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin

# With Go
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# macOS (Homebrew)
brew install golangci-lint
```

### Key Linters

| Category | Linters |
|----------|---------|
| Style | gofmt, goimports, misspell |
| Bugs | errcheck, staticcheck, govet |
| Performance | prealloc, unconvert |
| Complexity | gocyclo, dupl, funlen |
| Security | gosec |

### Configuration Levels

**Minimal**:
- gofmt (formatting)
- errcheck (error handling)
- govet (common mistakes)

**Strict**:
- All minimal +
- staticcheck (static analysis)
- gosec (security)
- Complexity limits

### Common Commands

```bash
# Lint all packages
golangci-lint run

# Lint specific package
golangci-lint run ./pkg/...

# Auto-fix issues
golangci-lint run --fix

# Fast mode (caching)
golangci-lint run --fast

# Specific linters only
golangci-lint run --disable-all --enable gofmt,goimports

# Configuration test
golangci-lint config verify
```

### CI Integration

**GitHub Actions**:
```yaml
- name: golangci-lint
  uses: golangci/golangci-lint-action@v3
  with:
    version: latest
```

**Pre-commit hook**:
```bash
# .git/hooks/pre-commit
golangci-lint run --fix
```

### Performance Tips

```yaml
# .golangci.yml
run:
  timeout: 5m
  go: '1.21'
  modules-download-mode: readonly

linters:
  fast: true  # Only fast linters
```

### Common Issues

**Unused code**:
```yaml
linters:
  disable:
    - unused  # Can be noisy with generics
```

**False positives**:
```yaml
issues:
  exclude-rules:
    - linters: [staticcheck]
      text: "SA9003:"
```
