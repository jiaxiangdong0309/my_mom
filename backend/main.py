# -*- coding: utf-8 -*-
"""
FastAPI 应用入口
"""
import os
import sys
import logging
from pathlib import Path

# 兼容直接运行和模块运行两种方式
# 确保项目根目录在 sys.path 中，统一使用绝对导入
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 统一使用绝对导入，避免 reloader 子进程中的相对导入问题
from backend.api import memories, search
from backend.config import settings

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI(title="AI Memory Hub")

# 配置 CORS（必须在路由之前添加）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 分发模式下允许更多来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 注册 API 路由
app.include_router(memories.router)
app.include_router(search.router)

# 静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}

# 挂载前端静态文件
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # 如果是 API 请求，由路由器处理；如果是静态文件，直接返回 index.html (支持 SPA)
        if full_path.startswith("api/"):
            return None # 让 FastAPI 继续寻找匹配的路由

        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # 默认返回 index.html 支持 React Router
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    async def root_fallback():
        return {"message": "Mymem API is running. Frontend not built yet."}

def run_server():
    import uvicorn
    # 根据环境决定是否开启 reload
    reload = settings.is_dev
    mode = "开发模式" if reload else "生产模式"
    logging.info(f"正在以 {mode} 启动服务器 (reload={reload})...")

    # 使用模块方式运行，支持相对导入
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=reload)

def cli():
    """CLI 入口函数"""
    import argparse
    import sys
    import socket
    import subprocess
    import time

    parser = argparse.ArgumentParser(description="Mymem - AI 知识记忆库 CLI 工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # start 命令
    start_parser = subparsers.add_parser("start", help="启动服务")
    start_parser.add_argument("--bg", action="store_true", help="在后台启动服务")

    # status 命令
    subparsers.add_parser("status", help="检查服务状态")

    # stop 命令
    subparsers.add_parser("stop", help="停止服务")

    args = parser.parse_args()

    def is_port_open(host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((host, port)) == 0

    def stop_service():
        """停止服务"""
        try:
            # 查找占用端口的进程
            if os.name == 'nt':
                # Windows 系统
                result = subprocess.run(
                    ['netstat', '-ano'],
                    capture_output=True,
                    text=True
                )
                # 解析 netstat 输出找到端口对应的 PID
                for line in result.stdout.split('\n'):
                    if f':{settings.port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) > 4:
                            pid = parts[-1]
                            try:
                                subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                                print(f"✅ 已停止服务 (PID: {pid})")
                                return True
                            except subprocess.CalledProcessError:
                                pass
            else:
                # macOS/Linux 系统
                result = subprocess.run(
                    ['lsof', '-ti', f':{settings.port}'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            subprocess.run(['kill', pid], check=True)
                            print(f"✅ 已停止服务 (PID: {pid})")
                        except subprocess.CalledProcessError:
                            pass
                    return True
            return False
        except Exception as e:
            print(f"❌ 停止服务时出错: {e}")
            return False

    if args.command == "status":
        if is_port_open(settings.host, settings.port):
            print(f"✅ Mymem 服务正在运行: http://{settings.host}:{settings.port}")
        else:
            print(f"❌ Mymem 服务未运行")
        sys.exit(0)

    elif args.command == "stop":
        if not is_port_open(settings.host, settings.port):
            print(f"❌ Mymem 服务未运行")
            sys.exit(0)

        if stop_service():
            # 等待一下，确认服务已停止
            time.sleep(1)
            if not is_port_open(settings.host, settings.port):
                print(f"✅ 服务已成功停止")
            else:
                print(f"⚠️  服务可能仍在运行，请手动检查")
        else:
            print(f"❌ 未能找到占用端口 {settings.port} 的进程")
        sys.exit(0)

    elif args.command == "start" or args.command is None:
        if is_port_open(settings.host, settings.port):
            print(f"✨ Mymem 服务已在 http://{settings.host}:{settings.port} 运行。")
            sys.exit(0)

        if getattr(args, 'bg', False):
            # 后台启动模式
            print("🚀 正在后台启动 Mymem 服务...")
            log_file = os.path.join(os.path.expanduser("~"), "mymem_service.log")

            # 使用 uvicorn 直接启动，更可靠
            import uvicorn
            python_exe = sys.executable

            # 构建 uvicorn 命令
            cmd = [
                python_exe, "-m", "uvicorn",
                "backend.main:app",
                "--host", settings.host,
                "--port", str(settings.port)
            ]

            # 根据开发模式决定是否启用 reload
            if settings.is_dev:
                cmd.append("--reload")
                print(f"📝 开发模式已启用，代码修改将自动重载")

            if os.name == 'nt':
                subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=open(log_file, "a"),
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    cmd,
                    stdout=open(log_file, "a"),
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    preexec_fn=os.setpgrp
                )

            # 等待启动
            for i in range(5):
                time.sleep(1)
                if is_port_open(settings.host, settings.port):
                    print(f"✅ 服务启动成功: http://{settings.host}:{settings.port}")
                    print(f"📝 日志文件: {log_file}")
                    sys.exit(0)
            print(f"⏳ 服务正在启动中，请稍后通过 `mymem status` 检查。")
            print(f"📝 日志文件: {log_file}")
        else:
            print(f"🚀 正在启动 Mymem 服务 (端口: {settings.port})...")
            run_server()
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()

