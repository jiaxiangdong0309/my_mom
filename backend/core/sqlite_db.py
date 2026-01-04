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

        # 创建 FTS5 虚拟表（不使用外部内容模式，以便独立存储分词后的内容）
        # 这种方式对于中文检索最稳健
        cursor.execute("DROP TABLE IF EXISTS memories_fts")
        cursor.execute("""
            CREATE VIRTUAL TABLE memories_fts USING fts5(
                title,
                content,
                tags
            )
        """)

        # 移除可能存在的旧触发器
        cursor.execute("DROP TRIGGER IF EXISTS memories_ai")
        cursor.execute("DROP TRIGGER IF EXISTS memories_ad")
        cursor.execute("DROP TRIGGER IF EXISTS memories_au")

        # 初始存量数据搬迁（带分词处理）
        cursor.execute("SELECT id, title, content, tags FROM memories")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute(
                "INSERT INTO memories_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)",
                (
                    row["id"],
                    self._tokenize_for_fts(row["title"]),
                    self._tokenize_for_fts(row["content"]),
                    self._tokenize_for_fts(row["tags"])
                )
            )

        # 如果表已存在但没有 updated_at 字段，则添加
        try:
            cursor.execute("ALTER TABLE memories ADD COLUMN updated_at TIMESTAMP")
            self.conn.commit()
        except sqlite3.OperationalError:
            # 字段已存在，忽略错误
            pass
        self.conn.commit()

    def _tokenize_for_fts(self, text: str) -> str:
        """
        为 FTS5 准备的分词逻辑：在每个字符间添加空格
        这样可以将每个中文字符当作一个独立的词处理，实现完美的全文检索效果
        """
        if not text:
            return ""
        # 去掉原有的多余空格，并重新按字符拆分
        chars = [c for c in text if not c.isspace()]
        return " ".join(chars)

    def create_memory(self, title: str, content: str, tags: List[str]) -> int:
        """
        创建记录
        """
        cursor = self.conn.cursor()
        tags_json = json.dumps(tags, ensure_ascii=False)

        # 使用本地时间（而不是 SQLite 的 CURRENT_TIMESTAMP，它可能返回 UTC）
        created_at = datetime.now().isoformat()

        # 1. 存入主表
        cursor.execute(
            "INSERT INTO memories (title, content, tags, created_at) VALUES (?, ?, ?, ?)",
            (title, content, tags_json, created_at)
        )
        memory_id = cursor.lastrowid

        # 2. 同步存入 FTS 表（手动分词）
        cursor.execute(
            "INSERT INTO memories_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)",
            (
                memory_id,
                self._tokenize_for_fts(title),
                self._tokenize_for_fts(content),
                self._tokenize_for_fts(tags_json)
            )
        )

        self.conn.commit()
        return memory_id

    def update_memory(self, memory_id: int, title: str, content: str, tags: List[str]) -> bool:
        """
        更新记录
        """
        cursor = self.conn.cursor()
        tags_json = json.dumps(tags, ensure_ascii=False)

        # 使用本地时间（而不是 SQLite 的 CURRENT_TIMESTAMP，它可能返回 UTC）
        updated_at = datetime.now().isoformat()

        # 1. 更新主表
        cursor.execute(
            "UPDATE memories SET title = ?, content = ?, tags = ?, updated_at = ? WHERE id = ?",
            (title, content, tags_json, updated_at, memory_id)
        )

        # 2. 同步更新 FTS 表
        cursor.execute(
            "INSERT OR REPLACE INTO memories_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)",
            (
                memory_id,
                self._tokenize_for_fts(title),
                self._tokenize_for_fts(content),
                self._tokenize_for_fts(tags_json)
            )
        )

        self.conn.commit()
        return cursor.rowcount > 0

    def delete_memory(self, memory_id: int) -> bool:
        """
        删除记录
        """
        cursor = self.conn.cursor()

        # 1. 删除主表
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))

        # 2. 同步删除 FTS 表
        cursor.execute("DELETE FROM memories_fts WHERE rowid = ?", (memory_id,))

        self.conn.commit()
        return cursor.rowcount > 0

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

    def search_memories(self, query: str) -> List[Dict]:
        """
        基于 FTS5 的全文检索（标题、内容或标签）

        Args:
            query: 搜索关键字

        Returns:
            匹配的记录列表（按相关度排序）
        """
        if not query:
            return []

        cursor = self.conn.cursor()

        # 1. 关键：将搜索词也进行空格分词
        # 比如用户搜 "模式" -> 变成 "模 式"
        # 这样 MATCH 语法才能匹配到 FTS 表中被拆分开的字符
        tokenized_query = self._tokenize_for_fts(query)

        # 打印搜索信息
        print(f"[SQLiteDB] 执行 FTS5 全文检索 (空格分词模式)", flush=True)
        print(f"[SQLiteDB] 查询词: '{query}' -> 分词: '{tokenized_query}'", flush=True)

        # 使用 FTS5 的 MATCH 语法
        # 提取 f.rank 以便后续计算相关度分数
        sql = """
            SELECT m.*, f.rank
            FROM memories m
            JOIN memories_fts f ON m.id = f.rowid
            WHERE memories_fts MATCH ?
            ORDER BY rank
        """

        try:
            # FTS5 的查询词如果包含特殊字符可能报错，这里做一个简单的转义处理
            # 在空格分词模式下，我们将 tokenized_query 整体放入引号中作为短语搜索
            # 这样搜索 "模 式" 必须是这两个字紧挨着的才算匹配
            phrase_query = f'"{tokenized_query}"'
            cursor.execute(sql, (phrase_query,))
        except sqlite3.OperationalError as e:
            print(f"[SQLiteDB] FTS5 搜索遇到语法错误: {e}，尝试不带引号查询...", flush=True)
            try:
                cursor.execute(sql, (tokenized_query,))
            except sqlite3.OperationalError:
                # 最后的兜底方案：退回到原始的 LIKE 搜索
                print(f"[SQLiteDB] 尝试失败，退回到 LIKE 搜索", flush=True)
                return self._search_like(cursor, query)

        rows = cursor.fetchall()
        print(f"[SQLiteDB] SQL查询返回 {len(rows)} 行", flush=True)

        result = []
        for row in rows:
            memory_dict = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "tags": json.loads(row["tags"]),
                "rank": row["rank"] if "rank" in row.keys() else 0,
                "created_at": datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"]
            }
            # 处理 updated_at 字段（可能为 None）
            if "updated_at" in row.keys() and row["updated_at"] is not None:
                memory_dict["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
            else:
                memory_dict["updated_at"] = None
            result.append(memory_dict)

        print(f"[SQLiteDB] 搜索完成，返回 {len(result)} 条记录", flush=True)
        return result

    def _search_like(self, cursor, query):
        """内部辅助：退回到 LIKE 搜索"""
        search_pattern = f"%{query}%"
        cursor.execute(
            "SELECT * FROM memories WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
            (search_pattern, search_pattern, search_pattern)
        )
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
            if "updated_at" in row.keys() and row["updated_at"] is not None:
                memory_dict["updated_at"] = datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"]
            else:
                memory_dict["updated_at"] = None
            result.append(memory_dict)
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

