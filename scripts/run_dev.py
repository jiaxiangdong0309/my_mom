#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同时启动前端和后端开发服务器

使用方法：
python3 scripts/run_dev.py

或者直接运行：
python3 scripts/run_dev.py
"""
import sys
import os
import subprocess
import signal
import time
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# 存储子进程
processes = []


def signal_handler(sig, frame):
    """处理 Ctrl+C 信号，优雅地关闭所有子进程"""
    print("\n\n🛑 正在关闭服务...")
    for process in processes:
        try:
            process.terminate()
        except:
            pass

    # 等待进程结束
    time.sleep(1)

    # 如果还有进程在运行，强制杀死
    for process in processes:
        try:
            if process.poll() is None:
                process.kill()
        except:
            pass

    print("✅ 所有服务已关闭")
    sys.exit(0)


def run_backend():
    """启动后端服务"""
    print("🚀 正在启动后端服务 (FastAPI)...")
    os.chdir(BACKEND_DIR)
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return process


def run_frontend():
    """启动前端服务"""
    print("🚀 正在启动前端服务 (Vite)...")
    os.chdir(FRONTEND_DIR)

    # 检查 node_modules 是否存在
    if not (FRONTEND_DIR / "node_modules").exists():
        print("⚠️  检测到 node_modules 不存在，正在安装依赖...")
        print("   这可能需要几分钟时间，请耐心等待...")
        install_process = subprocess.run(
            ["npm", "install"],
            cwd=FRONTEND_DIR,
            capture_output=True,
            text=True
        )
        if install_process.returncode != 0:
            print(f"❌ npm install 失败: {install_process.stderr}")
            return None

    process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return process


def print_output(process, prefix):
    """打印进程输出"""
    if process is None:
        return

    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{prefix}] {line.rstrip()}")
    except:
        pass


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 60)
    print("🎯 AI 知识记忆库 - 开发服务器")
    print("=" * 60)
    print()

    # 检查后端目录
    if not BACKEND_DIR.exists():
        print(f"❌ 错误: 后端目录不存在: {BACKEND_DIR}")
        sys.exit(1)

    # 检查前端目录
    if not FRONTEND_DIR.exists():
        print(f"❌ 错误: 前端目录不存在: {FRONTEND_DIR}")
        sys.exit(1)

    # 检查 main.py
    if not (BACKEND_DIR / "main.py").exists():
        print(f"❌ 错误: 后端入口文件不存在: {BACKEND_DIR / 'main.py'}")
        sys.exit(1)

    # 启动后端
    backend_process = run_backend()
    if backend_process:
        processes.append(backend_process)
        time.sleep(2)  # 等待后端启动

    # 启动前端
    frontend_process = run_frontend()
    if frontend_process:
        processes.append(frontend_process)

    if not processes:
        print("❌ 无法启动任何服务")
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ 服务启动成功！")
    print("=" * 60)
    print("📡 后端 API: http://localhost:8000")
    print("🌐 前端界面: http://localhost:5173")
    print("📚 API 文档: http://localhost:8000/docs")
    print()
    print("💡 提示: 按 Ctrl+C 停止所有服务")
    print("=" * 60)
    print()

    # 实时输出日志
    try:
        import threading

        def output_backend():
            print_output(backend_process, "后端")

        def output_frontend():
            print_output(frontend_process, "前端")

        if backend_process:
            backend_thread = threading.Thread(target=output_backend, daemon=True)
            backend_thread.start()

        if frontend_process:
            frontend_thread = threading.Thread(target=output_frontend, daemon=True)
            frontend_thread.start()

        # 等待进程结束
        while True:
            time.sleep(1)
            # 检查进程是否还在运行
            if backend_process and backend_process.poll() is not None:
                print("\n⚠️  后端服务已停止")
                break
            if frontend_process and frontend_process.poll() is not None:
                print("\n⚠️  前端服务已停止")
                break
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()

