"""
Embedding 简单封装
"""
import os

# 设置国内镜像源
# 方案：使用 ModelScope (阿里) 的镜像，通常比 hf-mirror 更稳定
os.environ["HF_ENDPOINT"] = "https://modelscope.cn/api/v1/models/server/huggingface"

from sentence_transformers import SentenceTransformer
import numpy as np
from ..config import settings

class Embedding:
    """Embedding 简单封装"""

    def __init__(self, model_name: str = None):
        """
        初始化 Embedding 模型
        """
        if model_name is None:
            model_name = settings.embedding_model

        print(f"🔄 正在从镜像站加载/下载模型: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("✅ 模型加载成功")

    def encode(self, text: str) -> np.ndarray:
        """
        生成向量

        Args:
            text: 输入文本

        Returns:
            向量数组
        """
        return self.model.encode(text)

