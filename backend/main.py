# -*- coding: utf-8 -*-
"""
FastAPI 应用入口
"""
import os
import sys
from pathlib import Path

# 兼容直接运行和模块运行两种方式
# 如果是直接运行（python3 backend/main.py），需要处理导入路径
if __name__ == "__main__" and __package__ is None:
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    # 直接运行时使用绝对导入
    from backend.api import memories, search
    from backend.config import settings
else:
    # 模块运行时使用相对导入
    from .api import memories, search
    from .config import settings

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

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
        return {"message": "Mymom API is running. Frontend not built yet."}

def run_server():
    import uvicorn
    # 使用模块方式运行，支持相对导入
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=False)

def cli():
    """CLI 入口函数"""
    import argparse
    import sys
    import socket
    import subprocess
    import time

    parser = argparse.ArgumentParser(description="Mymom - AI 知识记忆库 CLI 工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # start 命令
    start_parser = subparsers.add_parser("start", help="启动服务")
    start_parser.add_argument("--daemon", action="store_true", help="在后台启动服务")

    # status 命令
    subparsers.add_parser("status", help="检查服务状态")

    args = parser.parse_args()

    def is_port_open(host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((host, port)) == 0

    if args.command == "status":
        if is_port_open(settings.host, settings.port):
            print(f"✅ Mymom 服务正在运行: http://{settings.host}:{settings.port}")
        else:
            print(f"❌ Mymom 服务未运行")
        sys.exit(0)

    elif args.command == "start" or args.command is None:
        if is_port_open(settings.host, settings.port):
            print(f"✨ Mymom 服务已在 http://{settings.host}:{settings.port} 运行。")
            sys.exit(0)

        if getattr(args, 'daemon', False):
            # 后台启动模式
            print("🚀 正在后台启动 Mymom 服务...")
            log_file = os.path.join(os.path.expanduser("~"), "mymom_service.log")

            # 使用 uvicorn 直接启动，更可靠
            import uvicorn
            python_exe = sys.executable

            # 构建 uvicorn 命令
            cmd = [
                python_exe, "-m", "uvicorn",
                "backend.main:app",
                "--host", settings.host,
                "--port", str(settings.port),
                "--no-reload"
            ]

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
            print(f"⏳ 服务正在启动中，请稍后通过 `mymom status` 检查。")
            print(f"📝 日志文件: {log_file}")
        else:
            print(f"🚀 正在启动 Mymom 服务 (端口: {settings.port})...")
            run_server()
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()

