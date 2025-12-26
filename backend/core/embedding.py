"""
Embedding 简单封装
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from config import settings

class Embedding:
    """Embedding 简单封装"""

    def __init__(self, model_name: str = None):
        """
        初始化 Embedding 模型

        Args:
            model_name: 模型名称，默认从 settings.embedding_model 读取
        """
        if model_name is None:
            model_name = settings.embedding_model
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        """
        生成向量

        Args:
            text: 输入文本

        Returns:
            向量数组
        """
        return self.model.encode(text)

