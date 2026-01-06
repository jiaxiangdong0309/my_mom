#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量搜索脚本 - 通过 API 调用后端向量搜索接口
"""
import json
import argparse
import sys

# 尝试导入 requests 库
try:
    import requests
except ImportError:
    sys.stderr.write("错误: 需要安装 mymom 环境或单独安装 requests 库\n")
    sys.stderr.write("请运行: pip install requests 或安装主程序\n")
    sys.exit(1)

# 默认 API 地址
DEFAULT_API_URL = "http://localhost:7937"

def search_vector(query, limit=5, api_url=DEFAULT_API_URL):
    """调用后端向量搜索 API"""
    if not query or not query.strip():
        raise ValueError("query cannot be empty")

    if limit < 0:
        raise ValueError("limit must be non-negative")

    url = f"{api_url}/api/v1/search/"
    data = {"query": query, "limit": limit}

    try:
        response = requests.post(url, json=data, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"无法连接到后端服务 ({api_url})。\n"
            f"请确保 Mymom 服务已启动：\n"
            f"  mymom start"
        )
    except requests.exceptions.HTTPError as e:
        error_body = ""
        try:
            error_body = e.response.json()
        except:
            error_body = e.response.text
        raise RuntimeError(f"API 请求失败 (HTTP {e.response.status_code}): {error_body}")
    except Exception as e:
        raise RuntimeError(f"发生意外错误: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="向量语义搜索 - 通过 API 调用后端搜索接口")
    parser.add_argument("query", help="搜索查询文本")
    parser.add_argument("--limit", type=int, default=5, help="限制结果数量")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API 基础地址")

    args = parser.parse_args()

    try:
        results = search_vector(args.query, args.limit, args.api_url)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": True, "message": str(e)}, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
