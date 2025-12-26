#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite 关键词搜索脚本 - 通过 API 调用后端接口
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

def api_request(path, method="GET", data=None, api_url=DEFAULT_API_URL):
    """统一的 API 请求处理"""
    url = f"{api_url}{path}"

    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"无法连接到后端服务 ({api_url})。\n"
            f"请确保 Mymom 服务已启动：\n"
            f"  mymom"
        )
    except Exception as e:
        raise RuntimeError(f"API 请求失败: {str(e)}")

def list_all(api_url, limit=10):
    """获取最近记忆列表"""
    return api_request("/api/v1/memories/", api_url=api_url)[:limit]

def search_keyword(api_url, keyword, limit=10):
    """关键字搜索"""
    data = {"query": keyword, "limit": limit}
    return api_request("/api/v1/search/sqlite", method="POST", data=data, api_url=api_url)

def search_tag(api_url, tag, limit=10):
    """按标签筛选"""
    all_memories = api_request("/api/v1/memories/", api_url=api_url)
    filtered = [m for m in all_memories if tag in m.get("tags", [])]
    return filtered[:limit]

def get_by_id(api_url, memory_id):
    """根据 ID 获取详情"""
    return api_request(f"/api/v1/memories/{memory_id}", api_url=api_url)

def main():
    parser = argparse.ArgumentParser(description="Query the memory knowledge base via API.")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API base URL")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_parser = subparsers.add_parser("list", help="List all memories")
    list_parser.add_argument("--limit", type=int, default=10, help="Limit results")

    search_parser = subparsers.add_parser("search", help="Search by keyword")
    search_parser.add_argument("keyword", help="The keyword to search for")
    search_parser.add_argument("--limit", type=int, default=10, help="Limit results")

    tag_parser = subparsers.add_parser("tag", help="Search by tag")
    tag_parser.add_argument("tag", help="The tag to search for")
    tag_parser.add_argument("--limit", type=int, default=10, help="Limit results")

    get_parser = subparsers.add_parser("get", help="Get a memory by ID")
    get_parser.add_argument("id", type=int, help="The ID of the memory")

    args = parser.parse_args()

    try:
        if args.command == "list":
            results = list_all(args.api_url, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "search":
            results = search_keyword(args.api_url, args.keyword, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "tag":
            results = search_tag(args.api_url, args.tag, args.limit)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.command == "get":
            result = get_by_id(args.api_url, args.id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            parser.print_help()
    except Exception as e:
        print(json.dumps({"error": True, "message": str(e)}, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
