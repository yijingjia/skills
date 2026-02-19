#!/usr/bin/env python3
"""
Detects the programming language(s) used in a project.
Returns a list of detected languages with confidence scores.
"""

import sys
import json
from pathlib import Path
from collections import Counter


LANGUAGE_MARKERS = {
    "javascript": {
        "extensions": [".js", ".jsx", ".mjs", ".cjs"],
        "files": ["package.json", "yarn.lock", "package-lock.json", "tsconfig.json"],
        "dirs": ["node_modules"]
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "files": ["tsconfig.json", "tsconfig.build.json"],
        "dirs": []
    },
    "python": {
        "extensions": [".py", ".pyi"],
        "files": ["requirements.txt", "setup.py", "pyproject.toml", "poetry.lock", "Pipfile", "tox.ini"],
        "dirs": ["__pycache__", ".venv", "venv"]
    },
    "swift": {
        "extensions": [".swift"],
        "files": ["Package.swift", "Podfile", ".swiftlint.yml"],
        "dirs": ["Pods"]
    },
    "go": {
        "extensions": [".go"],
        "files": ["go.mod", "go.sum", "Gopkg.toml", "Gopkg.lock"],
        "dirs": []
    },
    "rust": {
        "extensions": [".rs"],
        "files": ["Cargo.toml", "Cargo.lock"],
        "dirs": ["target"]
    },
    "java": {
        "extensions": [".java", ".kt", ".kts"],
        "files": ["pom.xml", "build.gradle", "build.gradle.kts", "gradle.properties"],
        "dirs": []
    },
    "ruby": {
        "extensions": [".rb"],
        "files": ["Gemfile", "Rakefile", "Gemfile.lock"],
        "dirs": []
    },
    "php": {
        "extensions": [".php"],
        "files": ["composer.json", "composer.lock"],
        "dirs": ["vendor"]
    },
    "c/cpp": {
        "extensions": [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"],
        "files": ["CMakeLists.txt", "Makefile", "configure.ac"],
        "dirs": []
    },
    "csharp": {
        "extensions": [".cs"],
        "files": [".csproj", "sln", "packages.config"],
        "dirs": []
    }
}


def detect_languages(project_path: str = ".") -> dict:
    """
    Detect languages used in the project.

    Args:
        project_path: Path to the project directory (default: current directory)

    Returns:
        Dict with languages and their confidence scores
    """
    project_path = Path(project_path).resolve()

    if not project_path.exists():
        return {"error": f"Path does not exist: {project_path}"}

    scores = Counter()

    # Collect all files recursively
    try:
        all_files = list(project_path.rglob("*"))
    except PermissionError:
        all_files = []

    for file_path in all_files:
        if not file_path.is_file():
            continue

        # Skip common directories to ignore
        if any(part in file_path.parts for part in ['.git', 'node_modules', '__pycache__', 'venv', '.venv', 'target', 'dist', 'build', '.next', '.nuxt']):
            continue

        ext = file_path.suffix.lower()
        filename = file_path.name

        for lang, markers in LANGUAGE_MARKERS.items():
            # Check file extensions
            if ext in markers["extensions"]:
                scores[lang] += 1

            # Check for marker files (e.g., package.json, go.mod)
            if filename in markers["files"]:
                scores[lang] += 10  # Higher weight for marker files

    # Check for marker directories
    for item in project_path.iterdir():
        if item.is_dir():
            for lang, markers in LANGUAGE_MARKERS.items():
                if item.name in markers["dirs"]:
                    scores[lang] += 5

    # Normalize TypeScript and JavaScript
    if scores.get("typescript", 0) > 0:
        scores["javascript"] = scores.get("javascript", 0) + scores["typescript"]

    # Filter out very low scores
    total = sum(scores.values())
    if total == 0:
        return {"detected": [], "primary": None}

    detected = []
    for lang, score in scores.most_common():
        confidence = score / total
        if confidence > 0.05:  # At least 5% confidence
            detected.append({
                "language": lang,
                "confidence": round(confidence, 3),
                "score": score
            })

    primary = detected[0]["language"] if detected else None

    return {
        "detected": detected,
        "primary": primary
    }


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    result = detect_languages(project_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
