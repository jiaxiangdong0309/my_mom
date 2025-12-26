#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务自检与启动脚本：
用于 AI Skills 调用时确保后端服务已启动。
"""
import socket
import subprocess
import time
import sys
import os
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

def is_port_open(host, port):
    """检查端口是否开放"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def start_service_daemon():
    """以后台守护进程方式启动服务"""
    print("🚀 正在启动 Mymom 服务...")

    # 切换到后端目录以确保路径正确
    os.chdir(BACKEND_DIR)

    # 使用 nohup 或类似方式在后台运行，并将输出重定向
    log_file = PROJECT_ROOT / "mymom_service.log"

    # 判定操作系统
    if os.name == 'nt':  # Windows
        # Windows 下使用 start /B 启动后台进程
        subprocess.Popen(
            ["python", "main.py"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
            stdout=open(log_file, "a"),
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL
        )
    else:  # Unix/Linux/macOS
        # 使用 subprocess.Popen 启动，不等待其结束
        subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=open(log_file, "a"),
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            preexec_fn=os.setpgrp  # 创建新的进程组，脱离当前控制终端
        )

    print(f"✅ 服务已在后台启动，日志请查看: {log_file}")

def main():
    # 默认配置，后续可从环境变量读取
    host = os.getenv("MYMOM_HOST", "127.0.0.1")
    port = int(os.getenv("MYMOM_PORT", 7937))

    if is_port_open(host, port):
        print(f"✨ Mymom 服务已在 {host}:{port} 运行。")
        sys.exit(0)

    start_service_daemon()

    # 等待服务启动
    max_retries = 10
    for i in range(max_retries):
        time.sleep(1)
        if is_port_open(host, port):
            print(f"✅ 服务启动成功，响应于 {host}:{port}")
            sys.exit(0)
        print(f"⏳ 正在等待服务就绪... ({i+1}/{max_retries})")

    print("❌ 服务启动超时，请检查日志。")
    sys.exit(1)

if __name__ == "__main__":
    main()

