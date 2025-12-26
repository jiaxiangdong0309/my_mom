#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import json
import argparse
import sys
import os
from datetime import datetime
from contextlib import contextmanager

# 检查 Python 版本，确保使用 Python 3
if sys.version_info[0] < 3:
    sys.stderr.write("错误: 此脚本需要 Python 3.x\n")
    sys.stderr.write("请使用 'python3' 命令运行此脚本，例如:\n")
    sys.stderr.write("  python3 {} <参数>\n".format(sys.argv[0]))
    sys.exit(1)

# 数据库路径（相对于项目根目录）
DEFAULT_DB_PATH = "backend/data/memories.db"

def find_db_path(db_path):
    """
    查找数据库文件路径

    Args:
        db_path: 初始数据库路径

    Returns:
        找到的数据库路径

    Raises:
        FileNotFoundError: 如果找不到数据库文件
    """
    if os.path.exists(db_path):
        return db_path

    # 尝试相对于脚本位置寻找
    alt_path = os.path.join(os.path.dirname(__file__), "../../../backend/data/memories.db")
    if os.path.exists(alt_path):
        return alt_path

    raise FileNotFoundError(f"Database file not found at {db_path} or {alt_path}")

@contextmanager
def get_connection(db_path):
    """
    获取数据库连接的上下文管理器

    Args:
        db_path: 数据库文件路径

    Yields:
        sqlite3.Connection: 数据库连接对象
    """
    db_path = find_db_path(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def format_row(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "tags": json.loads(row["tags"]),
        "created_at": row["created_at"]
    }

def list_all(db_path, limit=None):
    """
    列出所有记忆，按创建时间倒序

    Args:
        db_path: 数据库文件路径
        limit: 限制返回的结果数量（可选）

    Returns:
        list: 记忆列表
    """
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM memories ORDER BY created_at DESC"
        if limit:
            query += " LIMIT ?"
            cursor.execute(query, (limit,))
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        results = [format_row(row) for row in rows]
    return results

def search_keyword(db_path, keyword, limit=None):
    """
    按关键词搜索记忆

    Args:
        db_path: 数据库文件路径
        keyword: 搜索关键词
        limit: 限制返回的结果数量（可选）

    Returns:
        list: 匹配的记忆列表
    """
    if not keyword or not keyword.strip():
        raise ValueError("keyword cannot be empty")

    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM memories
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{keyword}%"
        if limit:
            query += " LIMIT ?"
            cursor.execute(query, (search_pattern, search_pattern, limit))
        else:
            cursor.execute(query, (search_pattern, search_pattern))
        rows = cursor.fetchall()
        results = [format_row(row) for row in rows]
    return results

def search_tag(db_path, tag, limit=None):
    """
    按标签筛选记忆

    Args:
        db_path: 数据库文件路径
        tag: 标签名称
        limit: 限制返回的结果数量（可选）

    Returns:
        list: 匹配的记忆列表
    """
    if not tag or not tag.strip():
        raise ValueError("tag cannot be empty")

    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memories ORDER BY created_at DESC")
        rows = cursor.fetchall()

        results = []
        for row in rows:
            data = format_row(row)
            if tag in data["tags"]:
                results.append(data)
                if limit and len(results) >= limit:
                    break

    return results

def get_by_id(db_path, memory_id):
    """
    根据 ID 获取单条记忆

    Args:
        db_path: 数据库文件路径
        memory_id: 记忆 ID

    Returns:
        dict: 记忆对象，如果不存在则返回 None
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        result = format_row(row) if row else None
    return result

def main():
    parser = argparse.ArgumentParser(description="Query the memory knowledge base.")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="Path to the database file")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List all
    list_parser = subparsers.add_parser("list", help="List all memories")
    list_parser.add_argument("--limit", type=int, help="Limit the number of results")

    # Search
    search_parser = subparsers.add_parser("search", help="Search by keyword")
    search_parser.add_argument("keyword", help="The keyword to search for")
    search_parser.add_argument("--limit", type=int, help="Limit the number of results")

    # Tag
    tag_parser = subparsers.add_parser("tag", help="Search by tag")
    tag_parser.add_argument("tag", help="The tag to search for")
    tag_parser.add_argument("--limit", type=int, help="Limit the number of results")

    # Get
    get_parser = subparsers.add_parser("get", help="Get a memory by ID")
    get_parser.add_argument("id", type=int, help="The ID of the memory")

    args = parser.parse_args()

    try:
        if args.command == "list":
            results = list_all(args.db, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "search":
            results = search_keyword(args.db, args.keyword, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "tag":
            results = search_tag(args.db, args.tag, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "get":
            result = get_by_id(args.db, args.id)
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                # 统一返回 JSON 格式的错误信息
                error_result = {
                    "error": True,
                    "message": f"No memory found with ID: {args.id}"
                }
                print(json.dumps(error_result, indent=2, ensure_ascii=False))
                sys.exit(1)
        else:
            parser.print_help()
    except FileNotFoundError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_result = {
            "error": True,
            "message": f"Unexpected error: {str(e)}"
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

