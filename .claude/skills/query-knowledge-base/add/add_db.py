#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import argparse
import sys

# 检查 Python 版本，确保使用 Python 3
if sys.version_info[0] < 3:
    sys.stderr.write("错误: 此脚本需要 Python 3.x\n")
    sys.stderr.write("请使用 'python3' 命令运行此脚本，例如:\n")
    sys.stderr.write("  python3 {} <参数>\n".format(sys.argv[0]))
    sys.exit(1)

# 尝试导入 requests 库
try:
    import requests
except ImportError:
    sys.stderr.write("错误: 需要安装 requests 库\n")
    sys.stderr.write("请运行: pip install requests\n")
    sys.exit(1)

# 默认 API 地址
DEFAULT_API_URL = "http://localhost:8000/api/v1/memories/"

def validate_input(title, content):
    """
    验证输入参数

    Args:
        title: 记忆标题
        content: 记忆内容

    Raises:
        ValueError: 如果验证失败
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

def add_memory(api_url, title, content, tags=None):
    """
    通过 API 接口添加一条新的记忆（同时存储到 SQLite 和向量数据库）

    Args:
        api_url: API 接口地址
        title: 记忆标题
        content: 记忆内容
        tags: 标签列表（可选）

    Returns:
        新添加记录的 ID

    Raises:
        ValueError: 如果输入验证失败
        requests.RequestException: 如果 API 请求失败
    """
    # 验证输入
    validate_input(title, content)

    # 处理标签
    if tags is None:
        tags = []

    # 准备请求数据
    data = {
        "title": title,
        "content": content,
        "tags": tags
    }

    # 发送 POST 请求到 API
    try:
        response = requests.post(api_url, json=data, timeout=30)
        response.raise_for_status()  # 如果状态码不是 2xx，抛出异常

        # 解析响应
        result = response.json()
        memory_id = result.get("id")

        if memory_id is None:
            raise ValueError("API 响应中缺少 id 字段")

        return memory_id
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"无法连接到 API 服务器: {api_url}\n请确保后端服务已启动（运行 python3 backend/main.py）")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"API 请求超时: {api_url}")
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        try:
            error_response = e.response.json()
            error_detail = error_response.get("detail", str(e))
        except:
            error_detail = str(e)
        raise ValueError(f"API 请求失败: {error_detail}")

def print_result(success, message, memory_id=None, error=None):
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
    parser = argparse.ArgumentParser(description="Add new memory to the knowledge base via API (stores to both SQLite and vector database).")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API endpoint URL (default: {DEFAULT_API_URL})")

    # 添加记忆的参数
    parser.add_argument("--title", required=True, help="Title of the memory")
    parser.add_argument("--content", required=True, help="Content of the memory")
    parser.add_argument("--tags", nargs="*", default=[], help="Tags for the memory (space-separated)")

    args = parser.parse_args()

    try:
        # 添加记忆（通过 API，会自动存储到 SQLite 和向量数据库）
        memory_id = add_memory(args.api_url, args.title, args.content, args.tags)

        # 返回成功结果
        print_result(
            success=True,
            message=f"Memory added successfully with ID: {memory_id} (stored in both SQLite and vector database)",
            memory_id=memory_id
        )
    except ValueError as e:
        # 输入验证错误或 API 错误
        print_result(
            success=False,
            message="Validation or API request failed",
            error=str(e)
        )
        sys.exit(1)
    except ConnectionError as e:
        # 连接错误
        print_result(
            success=False,
            message="Connection failed",
            error=str(e)
        )
        sys.exit(1)
    except TimeoutError as e:
        # 超时错误
        print_result(
            success=False,
            message="Request timeout",
            error=str(e)
        )
        sys.exit(1)
    except Exception as e:
        # 其他未知错误
        print_result(
            success=False,
            message="Unexpected error occurred",
            error=str(e)
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
