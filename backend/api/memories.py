"""
存储接口路由
"""
from fastapi import APIRouter, HTTPException
from .models import MemoryCreate, MemoryResponse
from ..core.chroma_db import ChromaDB
from ..core.sqlite_db import SQLiteDB
from ..core.embedding import Embedding
from ..utils.text_splitter import split_text_by_chars
import numpy as np

router = APIRouter(prefix="/api/v1/memories", tags=["memories"])

# 禁用自动重定向，统一路径行为
router.redirect_slashes = False

# 直接实例化（后续可改为依赖注入）
chroma_db = ChromaDB()
sqlite_db = SQLiteDB()
embedder = Embedding()

@router.post("/", response_model=MemoryResponse)
async def create_memory(data: MemoryCreate):
    """存储记忆"""
    try:
        # 1. 保存到 SQLite，获取 ID
        memory_id = sqlite_db.create_memory(
            title=data.title,
            content=data.content,
            tags=data.tags
        )

        # 2. 组合 title 和 content，然后切割文本
        full_text = f"{data.title}\n{data.content}"
        text_chunks = split_text_by_chars(full_text, chunk_size=1000, overlap=100)

        # 3. 为每个文本块生成向量并存储
        if text_chunks:
            embeddings_list = []
            ids_list = []
            metadatas_list = []

            for chunk_index, chunk in enumerate(text_chunks):
                # 生成向量
                embedding = embedder.encode(chunk)
                embeddings_list.append(embedding)

                # 使用 memory_id:chunk_index 作为唯一ID
                chunk_id = f"{memory_id}:{chunk_index}"
                ids_list.append(chunk_id)

                # 存储元数据，包含原始记忆ID和块索引
                metadatas_list.append({
                    "memory_id": memory_id,
                    "chunk_index": chunk_index,
                    "title": data.title,
                    "total_chunks": len(text_chunks)
                })

            # 批量添加到 ChromaDB
            embeddings_array = np.array(embeddings_list)
            chroma_db.add_vectors(
                ids=ids_list,
                embeddings=embeddings_array,
                metadatas=metadatas_list
            )

        # 4. 获取完整记录返回
        memory = sqlite_db.get_memory(memory_id)
        if memory is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve created memory")

        return MemoryResponse(**memory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[MemoryResponse])
async def list_memories():
    """获取所有记忆列表"""
    memories = sqlite_db.get_all_memories()
    return [MemoryResponse(**mem) for mem in memories]

@router.get("/stats")
async def get_stats():
    """获取数据库统计信息"""
    try:
        sqlite_count = sqlite_db.count()
        chroma_count = chroma_db.count()
        return {
            "sqlite_count": sqlite_count,
            "chroma_count": chroma_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: int):
    """获取记忆详情"""
    memory = sqlite_db.get_memory(memory_id)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return MemoryResponse(**memory)

@router.delete("/{memory_id}")
async def delete_memory(memory_id: int):
    """删除记忆"""
    # 先检查是否存在
    memory = sqlite_db.get_memory(memory_id)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")

    # 删除 SQLite 数据
    sqlite_db.delete_memory(memory_id)

    # 删除 ChromaDB 向量（需要删除所有相关的块）
    # 查询所有以 memory_id: 开头的ID
    collection = chroma_db.collection
    # 获取所有文档，筛选出属于这个memory_id的块
    all_docs = collection.get()
    chunk_ids_to_delete = []

    for doc_id in all_docs["ids"]:
        # 检查是否是旧格式（纯数字ID）
        if doc_id == str(memory_id):
            chunk_ids_to_delete.append(doc_id)
        # 检查是否是新格式（memory_id:chunk_index）
        elif doc_id.startswith(f"{memory_id}:"):
            chunk_ids_to_delete.append(doc_id)

    # 批量删除所有相关的块
    if chunk_ids_to_delete:
        chroma_db.delete(ids=chunk_ids_to_delete)

    return {"message": "Memory deleted successfully"}

