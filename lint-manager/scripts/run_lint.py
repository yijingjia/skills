#!/usr/bin/env python3
"""
Runs lint tools on specified files or the entire project.
Supports auto-fix mode and staged-only mode.
"""

import os
import sys
import json
import subprocess
from pathlib import Path


LINT_COMMANDS = {
    "javascript": {
        "lint": "npx eslint {files} --format json",
        "lint_readable": "npx eslint {files}",
        "fix": "npx eslint {files} --fix",
        "config": ".eslintrc.json"
    },
    "typescript": {
        "lint": "npx eslint {files} --format json",
        "lint_readable": "npx eslint {files}",
        "fix": "npx eslint {files} --fix",
        "config": ".eslintrc.json"
    },
    "python": {
        "lint": "ruff check {files} --output-format json",
        "lint_readable": "ruff check {files}",
        "fix": "ruff check {files} --fix",
        "config": "pyproject.toml"
    },
    "swift": {
        "lint": "swiftlint lint --reporter json",
        "lint_readable": "swiftlint lint",
        "fix": "swiftlint --fix",
        "config": ".swiftlint.yml"
    },
    "go": {
        "lint": "golangci-lint run {files} --out-format json",
        "lint_readable": "golangci-lint run {files}",
        "fix": "golangci-lint run {files} --fix",
        "config": ".golangci.yml"
    }
}


def run_command(cmd: str, cwd: str = None) -> dict:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or os.getcwd()
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_staged_files(project_path: str = ".") -> list:
    """Get list of staged files from git."""
    result = run_command("git diff --cached --name-only --diff-filter=ACM", cwd=project_path)
    if result["success"]:
        files = [f for f in result["stdout"].split("\n") if f.strip()]
        return files
    return []


def filter_files_by_language(files: list, language: str) -> list:
    """Filter files by language extension."""
    extensions = {
        "javascript": [".js", ".jsx", ".mjs", ".cjs"],
        "typescript": [".ts", ".tsx"],
        "python": [".py", ".pyi"],
        "swift": [".swift"],
        "go": [".go"]
    }

    lang_exts = extensions.get(language, [])
    return [f for f in files if any(f.endswith(ext) for ext in lang_exts)]


def run_lint(language: str, files: list = None, fix: bool = False, staged_only: bool = False, project_path: str = ".") -> dict:
    """
    Run lint tool for a specific language.

    Args:
        language: Programming language
        files: Specific files to lint (None for all)
        fix: Whether to auto-fix issues
        staged_only: Only lint staged files
        project_path: Project directory path

    Returns:
        Dict with lint results
    """
    if language not in LINT_COMMANDS:
        return {
            "success": False,
            "error": f"Unsupported language: {language}"
        }

    commands = LINT_COMMANDS[language]

    # Determine files to lint
    if staged_only:
        files_to_check = get_staged_files(project_path)
        files_to_check = filter_files_by_language(files_to_check, language)
    elif files:
        files_to_check = files
    else:
        # Default to common source directories
        source_dirs = {
            "javascript": "src",
            "typescript": "src",
            "python": ".",
            "swift": ".",
            "go": "./..."
        }
        files_to_check = [source_dirs.get(language, ".")]

    if not files_to_check:
        return {
            "success": True,
            "message": f"No {language} files to lint",
            "results": []
        }

    # Build command
    cmd_template = commands["fix"] if fix else commands["lint"]
    files_str = " ".join(files_to_check)
    cmd = cmd_template.format(files=files_str)

    result = run_command(cmd, cwd=project_path)

    # Parse output
    try:
        if result["success"]:
            output = result.get("stdout", "")
            # Try to parse JSON output
            if output:
                try:
                    parsed = json.loads(output)
                    return {
                        "success": True,
                        "language": language,
                        "fixed": fix,
                        "results": parsed,
                        "files_checked": len(files_to_check)
                    }
                except json.JSONDecodeError:
                    pass
        return {
            "success": result["success"],
            "language": language,
            "fixed": fix,
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "files_checked": len(files_to_check)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "language": language
        }


def run_all_linters(languages: list, fix: bool = False, staged_only: bool = False, project_path: str = ".") -> dict:
    """
    Run lint tools for all detected languages.

    Args:
        languages: List of programming languages
        fix: Whether to auto-fix issues
        staged_only: Only lint staged files
        project_path: Project directory path

    Returns:
        Dict with results for all languages
    """
    results = {}
    for lang in languages:
        results[lang] = run_lint(lang, fix=fix, staged_only=staged_only, project_path=project_path)

    # Overall success
    all_success = all(r.get("success", False) for r in results.values())

    return {
        "success": all_success,
        "results": results,
        "fixed": fix,
        "staged_only": staged_only
    }


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Run lint tools")
    parser.add_argument("--language", "-l", help="Programming language")
    parser.add_argument("--files", "-f", nargs="+", help="Specific files to lint")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--staged", action="store_true", help="Only lint staged files")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.language:
        result = run_lint(args.language, args.files, args.fix, args.staged, args.path)
    else:
        # Auto-detect languages
        sys.path.insert(0, Path(__file__).parent)
        from detect_language import detect_languages
        detection = detect_languages(args.path)
        languages = [lang["language"] for lang in detection.get("detected", [])]
        result = run_all_linters(languages, args.fix, args.staged, args.path)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
