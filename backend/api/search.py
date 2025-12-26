"""
搜索接口路由
"""
from fastapi import APIRouter
from api.models import SearchRequest, SearchResult
from core.chroma_db import ChromaDB
from core.sqlite_db import SQLiteDB
from core.embedding import Embedding

router = APIRouter(prefix="/api/v1/search", tags=["search"])

# 禁用自动重定向，统一路径行为
router.redirect_slashes = False

# 直接实例化（后续可改为依赖注入）
chroma_db = ChromaDB()
sqlite_db = SQLiteDB()
embedder = Embedding()

@router.post("/", response_model=list[SearchResult])
async def search(data: SearchRequest):
    """语义搜索"""
    # 1. 查询向量化
    query_embedding = embedder.encode(data.query)

    # 2. 向量检索（ChromaDB 返回 ID 和 distance）
    # 返回的ID格式是 "memory_id:chunk_index"
    vector_results = chroma_db.search(query_embedding, top_k=data.limit)

    if not vector_results:
        return []

    # 3. 解析ID，提取memory_id，并去重（同一记忆的多个块只保留相关性最高的）
    memory_id_to_best_result = {}
    for vec_result in vector_results:
        chunk_id = vec_result["id"]
        metadata = vec_result.get("metadata", {})

        # 从metadata中获取memory_id，如果没有则从ID中解析
        if "memory_id" in metadata:
            memory_id = metadata["memory_id"]
        else:
            # 兼容旧格式：如果ID是纯数字
            try:
                memory_id = int(chunk_id)
            except ValueError:
                # 新格式：memory_id:chunk_index
                memory_id = int(chunk_id.split(":")[0])

        distance = vec_result.get("distance", 1.0)

        # 如果这个memory_id还没有记录，或者这个块的相关性更高，则更新
        if memory_id not in memory_id_to_best_result:
            memory_id_to_best_result[memory_id] = {
                "memory_id": memory_id,
                "distance": distance
            }
        else:
            # 保留距离更小的（相关性更高）
            if distance < memory_id_to_best_result[memory_id]["distance"]:
                memory_id_to_best_result[memory_id]["distance"] = distance

    # 4. 从 SQLite 批量获取完整数据
    memory_ids = list(memory_id_to_best_result.keys())
    memories = sqlite_db.get_memories_by_ids(memory_ids)

    # 创建 ID 到记忆的映射
    memory_dict = {mem["id"]: mem for mem in memories}

    # 5. 合并结果（将 distance 转换为相似度）
    # ChromaDB cosine 距离：0 表示完全相同，2 表示完全相反
    # 相似度 = 1 - (distance / 2)，归一化到 [0, 1]
    results = []
    for memory_id, best_result in memory_id_to_best_result.items():
        if memory_id in memory_dict:
            memory = memory_dict[memory_id]
            distance = best_result["distance"]
            relevance = max(0.0, 1.0 - (distance / 2.0))  # 归一化到 [0, 1]

            results.append(SearchResult(
                id=memory["id"],
                title=memory["title"],
                content=memory["content"],
                tags=memory["tags"],
                created_at=memory["created_at"],
                relevance=relevance
            ))

    # 6. 按相关性排序（从高到低）
    results.sort(key=lambda x: x.relevance, reverse=True)

    # 7. 限制返回数量
    return results[:data.limit]

