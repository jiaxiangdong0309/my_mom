#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite 关键词搜索脚本 - 仅保留单一 API 搜索接口
"""
import json
import argparse
import sys

# 尝试导入 requests 库
try:
    import requests
except ImportError:
    sys.stderr.write("错误: 需要安装 mymem 环境或单独安装 requests 库\n")
    sys.stderr.write("请运行: pip install requests 或安装主程序\n")
    sys.exit(1)

# 默认 API 地址
DEFAULT_API_URL = "http://localhost:7937"

def search_sqlite(api_url, query):
    """通过单一接口进行 SQLite 搜索"""
    url = f"{api_url}/api/v1/search/sqlite"
    payload = {"query": query}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"无法连接到后端服务 ({api_url})。\n"
            f"请确保 Mymem 服务已启动：\n"
            f"  mymem start"
        )
    except Exception as e:
        raise RuntimeError(f"搜索失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="SQLite keyword search via single API endpoint.")
    parser.add_argument("query", help="The keyword to search for")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API base URL")

    args = parser.parse_args()

    try:
        results = search_sqlite(args.api_url, args.query)
        # 直接输出 JSON 结果，无任何解释文字
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        # 错误也以 JSON 格式输出到 stderr
        error_msg = {"error": True, "message": str(e)}
        print(json.dumps(error_msg, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
