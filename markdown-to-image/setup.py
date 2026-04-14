#!/usr/bin/env python3
"""
markdown-to-image 环境检测 + 安装
运行: python markdown-to-image/setup.py
"""

import sys
import subprocess
from pathlib import Path

print("\n🔍 检测环境...\n")

# Python 版本
major, minor = sys.version_info[:2]
if major < 3 or (major == 3 and minor < 8):
    print(f"❌ Python 版本过低 ({major}.{minor})，需要 3.8+")
    print("   请升级 Python: https://python.org")
    sys.exit(1)
print(f"✅ Python {major}.{minor}")

# 检测 playwright
playwright_ok = False
try:
    import playwright
    playwright_ok = True
    print("✅ playwright 已安装")
except ImportError:
    print("⚠️  playwright 未安装")

if not playwright_ok:
    print("\n📦 安装 playwright...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "playwright"],
        capture_output=False
    )
    if result.returncode != 0:
        print("❌ playwright 安装失败")
        sys.exit(1)
    print("✅ playwright 安装完成")

# 检测 Chromium
chromium_ok = False
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        path = pw.chromium.executable_path
        if Path(path).exists():
            chromium_ok = True
            print("✅ Chromium 已就绪")
except Exception:
    pass

if not chromium_ok:
    print("\n🌐 下载 Chromium（约 150MB，仅需一次）...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=False
    )
    if result.returncode != 0:
        print("❌ Chromium 下载失败")
        print("   请手动运行: python -m playwright install chromium")
        sys.exit(1)
    print("✅ Chromium 下载完成")

print("\n🎉 环境准备完成！\n")
print("使用方法:")
print("  python markdown-to-image/scripts/render.py <your-article.md>")
print("  python markdown-to-image/scripts/render.py <your-article.md> --theme dark\n")
print("支持主题: light（默认）| dark | warm | forest\n")
