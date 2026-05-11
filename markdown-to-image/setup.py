#!/usr/bin/env python3
"""
markdown-to-image 环境检测 + 安装
用法: 在 skill 根目录下运行 python3 setup.py

行为:
- 自动在 skill 根目录创建 .venv 虚拟环境（已存在则跳过）
- 在 .venv 中安装 playwright
- 通过 .venv 下载 Chromium（系统级缓存，所有 venv 共享）
"""

import sys
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
VENV_DIR = SKILL_DIR / ".venv"
VENV_PY = VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

print("\n🔍 检测环境...\n")

# 1. Python 版本
major, minor = sys.version_info[:2]
if major < 3 or (major == 3 and minor < 8):
    print(f"❌ Python 版本过低 ({major}.{minor})，需要 3.8+")
    print("   请升级 Python: https://python.org")
    sys.exit(1)
print(f"✅ Python {major}.{minor}")

# 2. 虚拟环境
if VENV_PY.exists():
    print(f"✅ 虚拟环境已就绪: {VENV_DIR}")
else:
    print(f"\n📦 创建虚拟环境 {VENV_DIR} ...")
    result = subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], capture_output=False)
    if result.returncode != 0 or not VENV_PY.exists():
        print("❌ 虚拟环境创建失败")
        sys.exit(1)
    print("✅ 虚拟环境创建完成")

# 3. playwright
print("\n🔍 检测 playwright...")
check = subprocess.run([str(VENV_PY), "-c", "import playwright"], capture_output=True)
if check.returncode == 0:
    print("✅ playwright 已安装")
else:
    print("📦 在虚拟环境中安装 playwright ...")
    result = subprocess.run([str(VENV_PY), "-m", "pip", "install", "playwright"], capture_output=False)
    if result.returncode != 0:
        print("❌ playwright 安装失败")
        sys.exit(1)
    print("✅ playwright 安装完成")

# 4. Chromium
print("\n🔍 检测 Chromium...")
check = subprocess.run(
    [str(VENV_PY), "-c", "from playwright.sync_api import sync_playwright\n"
                          "from pathlib import Path\n"
                          "with sync_playwright() as pw:\n"
                          "    p = pw.chromium.executable_path\n"
                          "    assert Path(p).exists(), p"],
    capture_output=True,
)
if check.returncode == 0:
    print("✅ Chromium 已就绪")
else:
    print("🌐 下载 Chromium（约 150MB，仅需一次，全局共享）...")
    result = subprocess.run([str(VENV_PY), "-m", "playwright", "install", "chromium"], capture_output=False)
    if result.returncode != 0:
        print("❌ Chromium 下载失败")
        print("   请手动运行: .venv/bin/python -m playwright install chromium")
        sys.exit(1)
    print("✅ Chromium 下载完成")

print("\n🎉 环境准备完成！\n")
print("使用方法（在 skill 根目录下）:")
print("  .venv/bin/python scripts/render.py <your-article.md>")
print("  .venv/bin/python scripts/render.py <your-article.md> --theme dark\n")
print("支持主题: light（默认）| dark | warm | forest")
print("支持字体: sans（默认）| serif\n")
