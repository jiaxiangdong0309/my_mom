import sys
import os
import argparse
import json
from datetime import datetime

'''
 * 这个脚本用于搜索 SQLite 数据库中的记忆
 *
 * 使用方法：
 * python3 search_sqlite.py "搜索关键字"
 *
 * 示例：
 * python3 search_sqlite.py "Python"
 *
 '''
# 将 backend 目录添加到路径中，以便导入
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

try:
    from core.sqlite_db import SQLiteDB
except ImportError:
    print("错误: 无法导入 backend.core.sqlite_db。请确保在项目根目录下运行此脚本。")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="SQLite 关键字搜索脚本")
    parser.add_argument("query", type=str, help="搜索关键字")
    args = parser.parse_args()

    db = SQLiteDB()
    results = db.search_memories(args.query)

    print(f"\n🔍 找到 {len(results)} 条匹配的记录 (SQLite 关键字搜索: '{args.query}'):")
    print("=" * 80)

    if not results:
        print("未找到匹配的记录。")
    else:
        for res in results:
            print(f"ID: {res['id']}")
            print(f"标题: {res['title']}")
            print(f"标签: {', '.join(res['tags']) if res['tags'] else '无'}")
            print(f"时间: {res['created_at']}")
            print("-" * 40)
            content_preview = res['content'][:200] + "..." if len(res['content']) > 200 else res['content']
            print(f"内容: {content_preview}")
            print("=" * 80)

if __name__ == "__main__":
    main()

