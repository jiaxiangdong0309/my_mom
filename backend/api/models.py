"""
Pydantic 数据模型
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MemoryCreate(BaseModel):
    """创建记忆请求"""
    title: str
    content: str
    tags: List[str]

class MemoryResponse(BaseModel):
    """记忆响应"""
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

class SearchRequest(BaseModel):
    """搜索请求"""
    query: str
    limit: int = 3
    filters: Optional[dict] = None

class SearchResult(BaseModel):
    """搜索结果"""
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    relevance: float

