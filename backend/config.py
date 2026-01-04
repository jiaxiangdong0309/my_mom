"""
配置管理（支持环境变量）
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """配置（支持环境变量）"""

    # 基础路径（backend 目录）
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    project_root: Path = Path(base_dir).parent

    # 环境设置 (dev, prod, auto)
    # 支持通过环境变量 MYMOM_ENV 覆盖
    env: str = "auto"

    @property
    def is_dev(self) -> bool:
        """统一判断是否为开发环境"""
        env_val = self.env.lower()
        if env_val in ["dev", "development"]:
            return True
        if env_val in ["prod", "production"]:
            return False

        # 默认逻辑 (auto): 检查是否存在 .git 目录
        return (self.project_root / ".git").exists()

    # 智能路径管理
    # 1. 优先使用环境变量 MYMOM_DATA_PATH
    # 2. 如果是开发环境，使用项目根目录下的 ./data
    # 3. 否则认为是用户环境，使用 ~/.mymom/data
    def _get_default_data_dir(self) -> str:
        env_path = os.getenv("MYMOM_DATA_PATH")
        if env_path:
            return os.path.abspath(env_path)

        # 使用统一的环境判断属性
        if self.is_dev:
            return str(self.project_root / "data")

        # 用户环境，存放在家目录
        user_home_data = Path.home() / ".mymom" / "data"
        return str(user_home_data)

    @property
    def data_dir(self) -> str:
        path = self._get_default_data_dir()
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def chroma_dir(self) -> str:
        path = os.path.join(self.data_dir, "chroma")
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def db_path(self) -> str:
        return os.path.join(self.data_dir, "memories.db")

    # Embedding
    embedding_model: str = "BAAI/bge-small-zh-v1.5"

    # API
    port: int = 7937
    host: str = "127.0.0.1"

    class Config:
        env_prefix = "MYMOM_"
        env_file = ".env"

settings = Settings()

