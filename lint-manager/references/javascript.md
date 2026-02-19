# JavaScript/TypeScript Linting

## ESLint

**Tool**: ESLint
**Install**: `npm install --save-dev eslint`
**Config**: `.eslintrc.json` or `eslint.config.js`

### Key Rules

| Category | Rules |
|----------|-------|
| Style | indent, quotes, semi, comma-spacing |
| Quality | no-unused-vars, no-console, no-debugger |
| Errors | no-undef, no-extra-semi, no-const-assign |
| TypeScript | @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars |

### Configuration Levels

**Minimal** (fresh projects):
- Basic style rules (indent, quotes, semi)
- Quality warnings (no-console, no-unused-vars)
- Essential error detection

**Strict** (production):
- All minimal rules +
- Complex type checking
- Code complexity limits
- Import/export validation

### Common Commands

```bash
# Lint all files
npx eslint src/

# Lint specific file
npx eslint src/app.ts

# Auto-fix issues
npx eslint src/ --fix

# Check rules only
npx eslint --print-config src/
```

### With TypeScript

```bash
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

Required in `.eslintrc.json`:
```json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": ["plugin:@typescript-eslint/recommended"]
}
```
