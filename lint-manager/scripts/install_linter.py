#!/usr/bin/env python3
"""
Installs lint tools for the detected project languages.
Supports: ESLint, Ruff, SwiftLint, golangci-lint
"""

import os
import sys
import json
import subprocess
from pathlib import Path


LINTERS = {
    "javascript": {
        "tool": "eslint",
        "install_cmd": "npm install --save-dev eslint",
        "check_cmd": "npx eslint --version",
        "config_file": ".eslintrc.json",
        "packages": {
            "full": ["eslint", "@typescript-eslint/parser", "@typescript-eslint/eslint-plugin", "eslint-config-prettier"],
            "minimal": ["eslint"]
        }
    },
    "typescript": {
        "tool": "eslint",
        "install_cmd": "npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin",
        "check_cmd": "npx eslint --version",
        "config_file": ".eslintrc.json",
        "packages": {
            "full": ["eslint", "@typescript-eslint/parser", "@typescript-eslint/eslint-plugin", "eslint-config-prettier"],
            "minimal": ["eslint", "@typescript-eslint/parser", "@typescript-eslint/eslint-plugin"]
        }
    },
    "python": {
        "tool": "ruff",
        "install_cmd": "pip install ruff",
        "check_cmd": "ruff --version",
        "config_file": "pyproject.toml",
        "packages": {
            "full": ["ruff"],
            "minimal": ["ruff"]
        }
    },
    "swift": {
        "tool": "swiftlint",
        "install_cmd": "brew install swiftlint",
        "check_cmd": "swiftlint version",
        "config_file": ".swiftlint.yml",
        "packages": {
            "full": [],
            "minimal": []
        }
    },
    "go": {
        "tool": "golangci-lint",
        "install_cmd": "curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin",
        "check_cmd": "golangci-lint --version",
        "config_file": ".golangci.yml",
        "packages": {
            "full": [],
            "minimal": []
        }
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


def check_tool_installed(tool: str, check_cmd: str) -> bool:
    """Check if a lint tool is already installed."""
    result = run_command(check_cmd)
    return result["success"]


def install_tool(language: str, preset: str = "minimal", project_path: str = ".") -> dict:
    """
    Install lint tool for a specific language.

    Args:
        language: Programming language (javascript, python, swift, go)
        preset: Installation preset (minimal, full)
        project_path: Project directory path

    Returns:
        Dict with installation result
    """
    if language not in LINTERS:
        return {
            "success": False,
            "error": f"Unsupported language: {language}"
        }

    linter = LINTERS[language]
    tool = linter["tool"]

    # Check if already installed
    if check_tool_installed(tool, linter["check_cmd"]):
        return {
            "success": True,
            "message": f"{tool} is already installed",
            "tool": tool,
            "config_file": linter["config_file"]
        }

    # Install the tool
    install_cmd = linter["install_cmd"]

    # For JavaScript/TypeScript, we can customize the install command based on preset
    if language in ["javascript", "typescript"]:
        packages = linter["packages"].get(preset, linter["packages"]["minimal"])
        install_cmd = f"npm install --save-dev {' '.join(packages)}"

    result = run_command(install_cmd, cwd=project_path)

    return {
        "success": result["success"],
        "message": f"Installing {tool}" + (" completed" if result["success"] else " failed"),
        "tool": tool,
        "config_file": linter["config_file"],
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "returncode": result.get("returncode")
    }


def install_all(languages: list, preset: str = "minimal", project_path: str = ".") -> dict:
    """
    Install lint tools for multiple languages.

    Args:
        languages: List of programming languages
        preset: Installation preset (minimal, full)
        project_path: Project directory path

    Returns:
        Dict with installation results for all languages
    """
    results = {}
    for lang in languages:
        results[lang] = install_tool(lang, preset, project_path)

    return results


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Install lint tools")
    parser.add_argument("--language", "-l", help="Programming language")
    parser.add_argument("--preset", "-p", default="minimal", choices=["minimal", "full"], help="Installation preset")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.language:
        result = install_tool(args.language, args.preset, args.path)
    else:
        # Auto-detect languages
        sys.path.insert(0, Path(__file__).parent)
        from detect_language import detect_languages
        detection = detect_languages(args.path)
        languages = [lang["language"] for lang in detection.get("detected", [])]
        result = install_all(languages, args.preset, args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
