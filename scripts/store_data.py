#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存储数据脚本 - 同时存储到 SQLite 和 ChromaDB
"""
import sys
import os
import argparse
import json
import numpy as np

'''
 * 这个脚本用于存储数据到 SQLite 和 ChromaDB
 *
 * 使用方法：
 * python3 store_data.py --title "Python学习" --content "Python是一种高级编程语言"
 *
 * 示例：
 * python3 store_data.py --title "FastAPI" --content "FastAPI是一个现代Web框架" --tags "Python" "Web" "API"
 *
 * 从文件读取内容
'''
# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.sqlite_db import SQLiteDB
from core.chroma_db import ChromaDB
from core.embedding import Embedding
from utils.text_splitter import split_text_by_chars


def store_memory(title: str, content: str, tags: list = None):
    """
    存储记忆到 SQLite 和 ChromaDB

    Args:
        title: 记忆标题
        content: 记忆内容
        tags: 标签列表（可选）

    Returns:
        存储的记忆 ID
    """
    if tags is None:
        tags = []

    # 初始化数据库和模型
    sqlite_db = SQLiteDB()
    chroma_db = ChromaDB()
    embedder = Embedding()

    # 1. 保存到 SQLite，获取 ID
    memory_id = sqlite_db.create_memory(
        title=title,
        content=content,
        tags=tags
    )

    # 2. 组合 title 和 content，然后切割文本
    full_text = f"{title}\n{content}"
    text_chunks = split_text_by_chars(full_text, chunk_size=1000, overlap=100)

    # 3. 为每个文本块生成向量并存储到 ChromaDB
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

            # 存储元数据
            metadatas_list.append({
                "memory_id": memory_id,
                "chunk_index": chunk_index,
                "title": title,
                "total_chunks": len(text_chunks)
            })

        # 批量添加到 ChromaDB
        embeddings_array = np.array(embeddings_list)
        chroma_db.add_vectors(
            ids=ids_list,
            embeddings=embeddings_array,
            metadatas=metadatas_list
        )

    return memory_id


def print_result(success: bool, message: str, memory_id: int = None, error: str = None):
    """
    统一输出 JSON 格式结果

    Args:
        success: 是否成功
        message: 消息
        memory_id: 记忆 ID（成功时）
        error: 错误信息（失败时）
    """
    result = {
        "success": success,
        "message": message
    }
    if success and memory_id is not None:
        result["id"] = memory_id
    if error:
        result["error"] = error

    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="存储数据到知识库（SQLite + ChromaDB）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python3 store_data.py --title "Python学习" --content "Python是一种高级编程语言"

  # 带标签
  python3 store_data.py --title "FastAPI" --content "FastAPI是一个现代Web框架" --tags "Python" "Web" "API"

  # 从文件读取内容
  python3 store_data.py --title "文档" --content-file "content.txt" --tags "文档"
        """
    )

    parser.add_argument("--title", required=True, help="记忆标题")

    # 内容可以通过参数或文件提供
    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument("--content", help="记忆内容")
    content_group.add_argument("--content-file", help="从文件读取记忆内容")

    parser.add_argument("--tags", nargs="*", default=[], help="标签列表（空格分隔）")

    args = parser.parse_args()

    # 获取内容
    if args.content_file:
        try:
            with open(args.content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print_result(
                success=False,
                message="文件未找到",
                error=f"无法读取文件: {args.content_file}"
            )
            sys.exit(1)
        except Exception as e:
            print_result(
                success=False,
                message="读取文件失败",
                error=str(e)
            )
            sys.exit(1)
    else:
        content = args.content

    # 验证输入
    if not args.title or not args.title.strip():
        print_result(
            success=False,
            message="验证失败",
            error="标题不能为空"
        )
        sys.exit(1)

    if not content or not content.strip():
        print_result(
            success=False,
            message="验证失败",
            error="内容不能为空"
        )
        sys.exit(1)

    try:
        # 存储数据
        memory_id = store_memory(
            title=args.title.strip(),
            content=content.strip(),
            tags=args.tags
        )

        # 返回成功结果
        print_result(
            success=True,
            message=f"数据存储成功，ID: {memory_id}",
            memory_id=memory_id
        )
    except Exception as e:
        print_result(
            success=False,
            message="存储失败",
            error=str(e)
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

