# -*- coding: utf-8 -*-
"""
FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import memories, search

app = FastAPI(title="AI Memory Hub")

# 配置 CORS（必须在路由之前添加）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 注册路由
app.include_router(memories.router)
app.include_router(search.router)

# 挂载前端静态文件（待前端构建后启用）
# app.mount("/", StaticFiles(directory="../frontend/dist"), name="frontend")

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

