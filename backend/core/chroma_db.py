"""
ChromaDB 简单封装
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import numpy as np
import os
from config import settings

class ChromaDB:
    """ChromaDB 简单封装"""

    def __init__(self, persist_dir: str = None):
        """
        初始化 ChromaDB 客户端

        Args:
            persist_dir: 持久化目录路径，默认使用 settings.chroma_dir
        """
        if persist_dir is None:
            persist_dir = settings.chroma_dir

        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="memories",
            metadata={"hnsw:space": "cosine"}
        )

    def add_vectors(self, ids: List[str], embeddings: np.ndarray, metadatas: List[Dict]):
        """
        添加向量

        Args:
            ids: 向量 ID 列表
            embeddings: 向量数组
            metadatas: 元数据列表
        """
        # 将 numpy 数组转换为列表
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas
        )

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        """
        向量搜索

        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量（实际返回的块数量，可能包含同一记忆的多个块）

        Returns:
            搜索结果列表，每个结果包含 id、distance 和 metadata
        """
        # 将 numpy 数组转换为列表
        query_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
        # 增加返回数量，因为可能需要去重
        results = self.collection.query(
            query_embeddings=[query_list],
            n_results=top_k * 3  # 多返回一些，以便去重后有足够的结果
        )

        # 格式化返回结果
        formatted_results = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i, chunk_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {}
                formatted_results.append({
                    "id": chunk_id,  # 保持原始ID格式 "memory_id:chunk_index"
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "metadata": metadata
                })

        return formatted_results

    def delete(self, ids: List[str]):
        """
        删除向量

        Args:
            ids: 要删除的向量 ID 列表
        """
        if ids:
            self.collection.delete(ids=ids)

    def count(self) -> int:
        """
        获取向量总数

        Returns:
            向量总数
        """
        return self.collection.count()

