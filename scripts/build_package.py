#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打包脚本：
1. 构建前端并集成到后端
2. 构建 Python 分发包
"""
import os
import subprocess
import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

def run_command(cmd, cwd=None, check=True):
    """运行命令"""
    print(f"🔧 执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=check)
    return result.returncode == 0

def build_frontend():
    """构建前端"""
    print("\n" + "="*60)
    print("步骤 1/2: 构建前端")
    print("="*60)

    build_script = PROJECT_ROOT / "scripts" / "build_dist.py"
    if not run_command([sys.executable, str(build_script)]):
        print("❌ 前端构建失败")
        sys.exit(1)

    print("✅ 前端构建完成\n")

def build_package():
    """构建 Python 包"""
    print("="*60)
    print("步骤 2/2: 构建 Python 包")
    print("="*60)

    # 检查是否安装了 build 工具
    try:
        import build
    except ImportError:
        print("📦 正在安装构建工具...")
        if not run_command([sys.executable, "-m", "pip", "install", "build", "wheel"]):
            print("❌ 安装构建工具失败")
            sys.exit(1)

    # 清理旧的构建产物
    dist_dir = PROJECT_ROOT / "dist"
    build_dir = PROJECT_ROOT / "build"

    if dist_dir.exists():
        import shutil
        print("🧹 清理旧的构建产物...")
        shutil.rmtree(dist_dir)

    if build_dir.exists():
        import shutil
        shutil.rmtree(build_dir)

    # 构建包
    if not run_command([sys.executable, "-m", "build"]):
        print("❌ Python 包构建失败")
        sys.exit(1)

    print("\n✅ Python 包构建完成")

    # 显示构建产物
    if dist_dir.exists():
        print("\n📦 构建产物:")
        for item in sorted(dist_dir.iterdir()):
            size = item.stat().st_size / (1024 * 1024)  # MB
            print(f"   - {item.name} ({size:.2f} MB)")

def main():
    try:
        build_frontend()
        build_package()

        print("\n" + "="*60)
        print("✨ 打包完成！")
        print("="*60)
        print("\n安装方式:")
        print("  pip install dist/mymom-0.1.0-py3-none-any.whl")
        print("\n或查看 INSTALL.md 了解更多信息。")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

