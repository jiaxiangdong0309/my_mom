"""
配置管理（支持环境变量）
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """配置（支持环境变量）"""

    # 基础路径（backend 目录）
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    # 数据路径（确保使用绝对路径）
    data_dir: str = os.path.join(base_dir, "data")
    chroma_dir: str = os.path.join(base_dir, "data", "chroma")
    db_path: str = os.path.join(base_dir, "data", "memories.db")

    # Embedding
    embedding_model: str = "BAAI/bge-small-zh-v1.5"

    # API
    port: int = 8000
    host: str = "0.0.0.0"

    class Config:
        env_file = ".env"

settings = Settings()

