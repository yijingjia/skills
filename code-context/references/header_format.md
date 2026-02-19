# Header Comment Format Specification

All Python source files should include three header comment lines at the top describing the file's INPUT, OUTPUT, and POS.

## Format

```python
# INPUT: {input/dependency description}
# OUTPUT: {output/provides description}
# POS: {position/role description}
```

## Field Descriptions

### INPUT
- **Purpose**: Describe what the file depends on
- **Content**: List internal modules, external libraries, configuration, and other dependencies
- **Examples**:
  - `# INPUT: Internal: app.models.user, app.services.auth; External: pydantic, sqlalchemy`
  - `# INPUT: External: fastapi, pydantic`
  - `# INPUT: No special dependencies`

### OUTPUT
- **Purpose**: Describe what the file provides
- **Content**: List exported classes, functions, APIs, etc.
- **Examples**:
  - `# OUTPUT: Exports: User, CreateUserRequest; Classes: User; Functions: 5`
  - `# OUTPUT: Classes: UserService; Functions: 12`
  - `# OUTPUT: Utility/helper code`

### POS (Position)
- **Purpose**: Describe the file's position and role in the system
- **Content**: Describe the layer the file belongs to and its responsibilities
- **Examples**:
  - `# POS: API layer — handles HTTP requests`
  - `# POS: Business logic layer — implements core functionality`
  - `# POS: Data layer — defines data structures`

## Placement

Header comments must appear at the very top of the file, in this order:

1. **Shebang** (if applicable): `#!/usr/bin/env python3`
2. **Encoding declaration** (if needed): `# -*- coding: utf-8 -*-`
3. **INPUT/OUTPUT/POS comments** (required)
4. **Blank line**
5. **Module docstring** (optional but recommended)
6. **Import statements**
7. **Code**

Example:

```python
#!/usr/bin/env python3
# INPUT: Internal: app.models.user; External: fastapi, pydantic
# OUTPUT: Exports: router, UserCreateRequest; Classes: 0; Functions: 3
# POS: API layer — handles HTTP requests

"""
User-related API endpoints
"""

from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.post("/users")
async def create_user(request: UserCreateRequest):
    ...
```

## Auto-Generation

Header comments can be added or updated automatically by the `add_file_headers.py` script. The script will:

1. Parse the Python file's AST
2. Extract import information
3. Identify classes and functions
4. Infer file functionality
5. Generate or update the three comment lines

## Manual Maintenance

Auto-generated comments may need manual adjustment:

1. **INPUT**: Add important runtime dependencies (e.g. environment variables, config files)
2. **OUTPUT**: Add externally exposed API endpoints, events, etc.
3. **POS**: Adjust layer description to match the actual architecture

## Why Header Comments?

1. **Quick understanding**: Understand a file's purpose without reading the full code
2. **AI-friendly**: AI loads the header first and gets context quickly
3. **Dependency tracking**: Clearly show dependencies between modules
4. **Architecture view**: Use the POS field to understand system architecture at a glance

## Best Practices

1. **Keep it concise**: Each comment line should not exceed 100 characters
2. **Be accurate**: Avoid vague or ambiguous descriptions
3. **Update promptly**: Keep comments in sync when code changes
4. **Use consistent format**: Follow the project's agreed format and terminology
