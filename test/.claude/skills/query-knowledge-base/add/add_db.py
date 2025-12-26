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
    sys.stderr.write("错误: 需要安装 mymom 环境或单独安装 requests 库\n")
    sys.stderr.write("请运行: pip install requests 或安装主程序\n")
    sys.exit(1)

# 默认 API 地址
DEFAULT_API_URL = "http://localhost:7937/api/v1/memories/"

def validate_input(title, content):
    """验证输入参数"""
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

def add_memory(api_url, title, content, tags=None):
    """通过 API 接口添加一条新的记忆"""
    validate_input(title, content)

    if tags is None:
        tags = []

    data = {
        "title": title,
        "content": content,
        "tags": tags
    }

    try:
        response = requests.post(api_url, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        memory_id = result.get("id")

        if memory_id is None:
            raise ValueError("API 响应中缺少 id 字段")

        return memory_id
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"无法连接到 API 服务器: {api_url}\n请确保 Mymom 服务已启动（运行命令: mymom）")
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        try:
            error_response = e.response.json()
            error_detail = error_response.get("detail", str(e))
        except:
            error_detail = str(e)
        raise RuntimeError(f"API 请求失败: {error_detail}")
    except Exception as e:
        raise RuntimeError(f"发生意外错误: {str(e)}")

def print_result(success, message, memory_id=None, error=None):
    """统一输出 JSON 格式结果"""
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
    parser = argparse.ArgumentParser(description="Add new memory to the knowledge base via API.")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API endpoint URL (default: {DEFAULT_API_URL})")
    parser.add_argument("--title", required=True, help="Title of the memory")
    parser.add_argument("--content", required=True, help="Content of the memory")
    parser.add_argument("--tags", nargs="*", default=[], help="Tags for the memory")

    args = parser.parse_args()

    try:
        memory_id = add_memory(args.api_url, args.title, args.content, args.tags)
        print_result(
            success=True,
            message=f"Memory added successfully with ID: {memory_id}",
            memory_id=memory_id
        )
    except (ValueError, RuntimeError) as e:
        print_result(success=False, message="API request failed", error=str(e))
        sys.exit(1)
    except ConnectionError as e:
        print_result(success=False, message="Connection failed", error=str(e))
        sys.exit(1)
    except Exception as e:
        print_result(success=False, message="Unexpected error occurred", error=str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
