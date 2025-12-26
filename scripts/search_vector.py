import sys
import os
import argparse
import numpy as np
from datetime import datetime

'''
 * 这个脚本用于搜索 ChromaDB 中的记忆
 *
 * 使用方法：
 * python3 search_vector.py "搜索关键字"
 '''
# 将 backend 目录添加到路径中，以便导入
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

try:
    from core.chroma_db import ChromaDB
    from core.sqlite_db import SQLiteDB
    from core.embedding import Embedding
except ImportError:
    print("错误: 无法导入 backend 模块。请确保在项目根目录下运行此脚本。")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ChromaDB 向量语义搜索脚本")
    parser.add_argument("query", type=str, help="搜索关键字")
    parser.add_argument("--limit", type=int, default=5, help="返回结果数量 (默认: 5)")
    args = parser.parse_args()

    # 初始化
    print(f"🔄 正在初始化搜索组件...")
    try:
        chroma_db = ChromaDB()
        sqlite_db = SQLiteDB()
        embedder = Embedding()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    # 1. 向量化查询
    print(f"🧪 正在分析查询意图: '{args.query}'...")
    query_embedding = embedder.encode(args.query)

    # 2. 向量搜索
    print("📡 正在进行语义检索...")
    try:
        vector_results = chroma_db.search(query_embedding, top_k=args.limit)
    except Exception as e:
        if "dimension" in str(e):
            print(f"❌ 搜索失败: 向量维度不匹配。")
            print(f"当前模型维度: {len(query_embedding)}")
            print(f"数据库期望维度: {str(e).split('dimension of ')[1].split(',')[0] if 'dimension of ' in str(e) else '未知'}")
            print("\n原因分析: 你可能更换了 Embedding 模型但尚未重新索引数据。")
            print("解决方案:")
            print("1. 在 backend/config.py 中检查 embedding_model 设置。")
            print("2. 如果更换了模型，请清空 data/chroma 目录并重新运行数据导入。")
        else:
            print(f"❌ 搜索失败: {e}")
        return

    # 3. 解析 ID 并去重
    memory_id_to_best_result = {}
    for vec_result in vector_results:
        chunk_id = vec_result["id"]
        metadata = vec_result.get("metadata", {})

        if "memory_id" in metadata:
            memory_id = metadata["memory_id"]
        else:
            try:
                memory_id = int(chunk_id)
            except ValueError:
                memory_id = int(chunk_id.split(":")[0])

        distance = vec_result.get("distance", 1.0)

        if memory_id not in memory_id_to_best_result:
            memory_id_to_best_result[memory_id] = {
                "memory_id": memory_id,
                "distance": distance
            }
        else:
            if distance < memory_id_to_best_result[memory_id]["distance"]:
                memory_id_to_best_result[memory_id]["distance"] = distance

    # 4. 从 SQLite 获取详情
    memory_ids = list(memory_id_to_best_result.keys())
    memories = sqlite_db.get_memories_by_ids(memory_ids)
    memory_dict = {mem["id"]: mem for mem in memories}

    # 5. 合并并计算相关性
    results = []
    for memory_id, best_result in memory_id_to_best_result.items():
        if memory_id in memory_dict:
            memory = memory_dict[memory_id]
            distance = best_result["distance"]
            # ChromaDB cosine 距离：0 表示完全相同，2 表示完全相反
            relevance = max(0.0, 1.0 - (distance / 2.0))
            results.append({
                **memory,
                "relevance": relevance
            })

    # 6. 排序
    results.sort(key=lambda x: x["relevance"], reverse=True)
    results = results[:args.limit]

    print(f"\n✅ 找到 {len(results)} 条匹配的记录 (向量语义搜索: '{args.query}'):")
    print("=" * 80)
    for res in results:
        print(f"ID: {res['id']} (相关度: {res['relevance']:.2%})")
        print(f"标题: {res['title']}")
        print(f"标签: {', '.join(res['tags']) if res['tags'] else '无'}")
        print(f"时间: {res['created_at']}")
        print("-" * 40)
        content_preview = res['content'][:200] + "..." if len(res['content']) > 200 else res['content']
        print(f"内容: {content_preview}")
        print("=" * 80)

if __name__ == "__main__":
    main()

