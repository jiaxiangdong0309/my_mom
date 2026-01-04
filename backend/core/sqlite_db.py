"""
SQLite 简单封装
"""
import sqlite3
import json
import os
from typing import List, Optional, Dict
from datetime import datetime
from ..config import settings

class SQLiteDB:
    """SQLite 简单封装"""

    def __init__(self, db_path: str = None):
        """
        初始化 SQLite 连接

        Args:
            db_path: 数据库文件路径，默认使用 settings.db_path
        """
        if db_path is None:
            db_path = settings.db_path

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        """创建表"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        # 如果表已存在但没有 updated_at 字段，则添加
        try:
            cursor.execute("ALTER TABLE memories ADD COLUMN updated_at TIMESTAMP")
            self.conn.commit()
        except sqlite3.OperationalError:
            # 字段已存在，忽略错误
            pass
        self.conn.commit()

    def create_memory(self, title: str, content: str, tags: List[str]) -> int:
        """
        创建记录

        Args:
            title: 标题
            content: 内容
            tags: 标签列表

        Returns:
            创建的记录 ID
        """
        cursor = self.conn.cursor()
        tags_json = json.dumps(tags, ensure_ascii=False)
        cursor.execute(
            "INSERT INTO memories (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tags_json)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_memory(self, memory_id: int) -> Optional[Dict]:
        """
        获取单条记录

        Args:
            memory_id: 记录 ID

        Returns:
            记录字典或 None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        result = {
            "id": row["id"],
            "title": row["title"],
            "content": row["content"],
            "tags": json.loads(row["tags"]),
            "created_at": datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
        }
        # 处理 updated_at 字段（可能为 None）
        if "updated_at" in row.keys() and row["updated_at"] is not None:
            result["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
        else:
            result["updated_at"] = None
        return result

    def get_all_memories(self) -> List[Dict]:
        """
        获取所有记录（按创建时间倒序）

        Returns:
            记录列表
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories ORDER BY created_at DESC")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            memory_dict = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "tags": json.loads(row["tags"]),
                "created_at": datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
            }
            # 处理 updated_at 字段（可能为 None）
            if "updated_at" in row.keys() and row["updated_at"] is not None:
                memory_dict["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
            else:
                memory_dict["updated_at"] = None
            result.append(memory_dict)
        return result

    def get_memories_by_ids(self, ids: List[int]) -> List[Dict]:
        """
        批量获取记录

        Args:
            ids: 记录 ID 列表

        Returns:
            记录列表
        """
        if not ids:
            return []
        cursor = self.conn.cursor()
        placeholders = ",".join("?" * len(ids))
        cursor.execute(f"SELECT * FROM memories WHERE id IN ({placeholders})", ids)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            memory_dict = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "tags": json.loads(row["tags"]),
                "created_at": datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
            }
            # 处理 updated_at 字段（可能为 None）
            if "updated_at" in row.keys() and row["updated_at"] is not None:
                memory_dict["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
            else:
                memory_dict["updated_at"] = None
            result.append(memory_dict)
        return result

    def update_memory(self, memory_id: int, title: str, content: str, tags: List[str]) -> bool:
        """
        更新记录

        Args:
            memory_id: 记录 ID
            title: 标题
            content: 内容
            tags: 标签列表

        Returns:
            是否成功
        """
        cursor = self.conn.cursor()
        tags_json = json.dumps(tags, ensure_ascii=False)
        cursor.execute(
            "UPDATE memories SET title = ?, content = ?, tags = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (title, content, tags_json, memory_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_memory(self, memory_id: int) -> bool:
        """
        删除记录

        Args:
            memory_id: 记录 ID

        Returns:
            是否成功
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def search_memories(self, query: str) -> List[Dict]:
        """
        关键字搜索（标题、内容或标签）

        Args:
            query: 搜索关键字

        Returns:
            匹配的记录列表
        """
        cursor = self.conn.cursor()
        search_pattern = f"%{query}%"

        # 打印搜索信息
        print(f"[SQLiteDB] 执行关键字搜索", flush=True)
        print(f"[SQLiteDB] 搜索模式: '{search_pattern}'", flush=True)
        print(f"[SQLiteDB] SQL查询: SELECT * FROM memories WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY created_at DESC", flush=True)

        cursor.execute(
            "SELECT * FROM memories WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
            (search_pattern, search_pattern, search_pattern)
        )
        rows = cursor.fetchall()

        print(f"[SQLiteDB] SQL查询返回 {len(rows)} 行", flush=True)

        result = []
        for idx, row in enumerate(rows, 1):
            memory_dict = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "tags": json.loads(row["tags"]),
                "created_at": datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
            }
            # 处理 updated_at 字段（可能为 None）
            if "updated_at" in row.keys() and row["updated_at"] is not None:
                memory_dict["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
            else:
                memory_dict["updated_at"] = None
            result.append(memory_dict)

            # 打印每条记录的简要信息
            title_short = memory_dict["title"][:40] + "..." if len(memory_dict["title"]) > 40 else memory_dict["title"]
            print(f"[SQLiteDB]   结果 {idx}: [ID:{memory_dict['id']}] {title_short}", flush=True)

        print(f"[SQLiteDB] 搜索完成，返回 {len(result)} 条记录", flush=True)
        return result

    def count(self) -> int:
        """
        获取记录总数

        Returns:
            记录总数
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        row = cursor.fetchone()
        # 使用索引访问，因为 COUNT(*) 返回的是元组
        return row[0] if row else 0

