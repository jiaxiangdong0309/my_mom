#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量搜索脚本 - 通过 API 调用后端向量搜索接口
"""
import urllib.request
import urllib.error
import json
import argparse
import sys

# 默认 API 地址
DEFAULT_API_URL = "http://localhost:8000"

def search_vector(query, limit=5, api_url=DEFAULT_API_URL):
    """
    调用后端向量搜索 API

    Args:
        query: 查询文本
        limit: 返回结果数量限制
        api_url: API 基础地址

    Returns:
        list: 搜索结果列表

    Raises:
        urllib.error.URLError: 连接失败
        urllib.error.HTTPError: HTTP 错误
        TimeoutError: 请求超时
        json.JSONDecodeError: JSON 解析错误
    """
    if not query or not query.strip():
        raise ValueError("query cannot be empty")

    if limit < 0:
        raise ValueError("limit must be non-negative")

    # 构建请求数据
    data = json.dumps({"query": query, "limit": limit}).encode('utf-8')

    # 构建请求
    url = f"{api_url}/api/v1/search/"
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        # 发送请求（10 秒超时）
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError) or "Connection refused" in str(e):
            raise ConnectionError(
                f"无法连接到后端服务 ({api_url})。\n"
                f"请确保后端服务已启动：\n"
                f"  cd backend && python3 main.py"
            ) from e
        raise ConnectionError(f"连接失败: {e}") from e
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode('utf-8')
        except:
            pass
        raise RuntimeError(f"API 请求失败 (HTTP {e.code}): {error_body}") from e
    except TimeoutError:
        raise TimeoutError(f"请求超时（超过 10 秒）。请检查后端服务是否正常运行。") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"响应解析失败: {e}") from e

def main():
    parser = argparse.ArgumentParser(
        description="向量语义搜索 - 通过 API 调用后端搜索接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本搜索
  python3 query_vector.py "学习方法"

  # 限制结果数量
  python3 query_vector.py "AI" --limit 3

  # 指定 API 地址
  python3 query_vector.py "Python" --api-url http://localhost:8000
        """
    )

    parser.add_argument(
        "query",
        help="搜索查询文本（自然语言描述）"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="限制返回的结果数量（默认: 5）"
    )

    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"API 基础地址（默认: {DEFAULT_API_URL}）"
    )

    args = parser.parse_args()

    try:
        results = search_vector(args.query, args.limit, args.api_url)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except ValueError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except TimeoutError as e:
        error_result = {
            "error": True,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_result = {
            "error": True,
            "message": f"意外错误: {str(e)}"
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

