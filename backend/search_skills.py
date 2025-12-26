#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时脚本：使用向量搜索查找 'skills' 相关的记忆
"""
import sys
import os

# 添加 backend 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.chroma_db import ChromaDB
from core.sqlite_db import SQLiteDB
from core.embedding import Embedding

def search_skills():
    """搜索与 'skills' 相关的记忆"""
    # 初始化组件
    chroma_db = ChromaDB()
    sqlite_db = SQLiteDB()
    embedder = Embedding()

    # 查询文本
    query = "skills"
    print(f"🔍 正在搜索与 '{query}' 相关的记忆...\n")

    # 1. 查询向量化
    query_embedding = embedder.encode(query)

    # 2. 向量检索（返回 top 10）
    top_k = 10
    vector_results = chroma_db.search(query_embedding, top_k=top_k)

    if not vector_results:
        print("❌ 没有找到相关记忆")
        return

    # 3. 解析ID，提取memory_id，并去重
    memory_id_to_best_result = {}
    for vec_result in vector_results:
        chunk_id = vec_result["id"]
        metadata = vec_result.get("metadata", {})

        # 从metadata中获取memory_id，如果没有则从ID中解析
        if "memory_id" in metadata:
            memory_id = metadata["memory_id"]
        else:
            try:
                memory_id = int(chunk_id)
            except ValueError:
                memory_id = int(chunk_id.split(":")[0])

        distance = vec_result.get("distance", 1.0)

        # 保留相关性最高的块
        if memory_id not in memory_id_to_best_result:
            memory_id_to_best_result[memory_id] = {
                "memory_id": memory_id,
                "distance": distance
            }
        else:
            if distance < memory_id_to_best_result[memory_id]["distance"]:
                memory_id_to_best_result[memory_id]["distance"] = distance

    # 4. 从 SQLite 批量获取完整数据
    memory_ids = list(memory_id_to_best_result.keys())
    memories = sqlite_db.get_memories_by_ids(memory_ids)

    # 创建 ID 到记忆的映射
    memory_dict = {mem["id"]: mem for mem in memories}

    # 5. 合并结果并计算相似度
    results = []
    for memory_id, best_result in memory_id_to_best_result.items():
        if memory_id in memory_dict:
            memory = memory_dict[memory_id]
            distance = best_result["distance"]
            relevance = max(0.0, 1.0 - (distance / 2.0))  # 归一化到 [0, 1]

            results.append({
                "id": memory["id"],
                "title": memory["title"],
                "content": memory["content"],
                "tags": memory["tags"],
                "created_at": memory["created_at"],
                "relevance": relevance
            })

    # 6. 按相关性排序
    results.sort(key=lambda x: x["relevance"], reverse=True)

    # 7. 显示结果
    print(f"✅ 找到 {len(results)} 条相关记忆：\n")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"\n【结果 {i}】相关性: {result['relevance']:.2%}")
        print(f"ID: {result['id']}")
        print(f"标题: {result['title']}")
        print(f"标签: {', '.join(result['tags']) if result['tags'] else '无'}")
        print(f"创建时间: {result['created_at']}")
        print(f"\n内容预览:")
        content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
        print(f"{content_preview}")
        print("-" * 80)

if __name__ == "__main__":
    search_skills()



