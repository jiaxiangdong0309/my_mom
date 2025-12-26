"""
搜索接口路由
"""
from fastapi import APIRouter
from .models import SearchRequest, SearchResult
from ..core.chroma_db import ChromaDB
from ..core.sqlite_db import SQLiteDB
from ..core.embedding import Embedding

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
    # ... existing implementation ...
    # (keeping the implementation from the file, just showing context)
    # ...

@router.post("/sqlite", response_model=list[SearchResult])
async def search_sqlite(data: SearchRequest):
    """关键字搜索 (SQLite)"""
    memories = sqlite_db.search_memories(data.query)

    results = []
    for memory in memories:
        results.append(SearchResult(
            id=memory["id"],
            title=memory["title"],
            content=memory["content"],
            tags=memory["tags"],
            created_at=memory["created_at"],
            relevance=1.0  # 关键字匹配默认相关度为 1.0
        ))

    return results[:data.limit]

