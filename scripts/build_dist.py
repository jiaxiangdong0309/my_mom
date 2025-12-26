#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化构建脚本：
1. 构建前端 (npm run build)
2. 将构建产物拷贝到后端静态文件目录 (backend/static)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
STATIC_DIR = BACKEND_DIR / "static"

def build_frontend():
    """构建前端"""
    print("🚀 正在构建前端...")
    if not (FRONTEND_DIR / "node_modules").exists():
        print("📦 正在安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)
    print("✅ 前端构建完成")

def integrate_frontend():
    """集成前端到后端"""
    print("📂 正在集成前端产物到后端...")
    dist_dir = FRONTEND_DIR / "dist"

    if not dist_dir.exists():
        print("❌ 错误: 前端构建产物目录不存在 (frontend/dist)")
        sys.exit(1)

    # 清理并创建后端静态文件目录
    if STATIC_DIR.exists():
        shutil.rmtree(STATIC_DIR)
    os.makedirs(STATIC_DIR)

    # 拷贝构建产物
    for item in os.listdir(dist_dir):
        s = dist_dir / item
        d = STATIC_DIR / item
        if s.is_dir():
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    print(f"✅ 前端产物已拷贝至: {STATIC_DIR}")

def main():
    try:
        build_frontend()
        integrate_frontend()
        print("\n✨ 集成构建成功！现在可以运行 `python3 backend/main.py` 启动完整服务。")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程中出错: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生意外错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

