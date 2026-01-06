#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试发布脚本：快速发布到 TestPyPI

使用方法：
python3 scripts/publish_test.py

或者直接运行：
python3 scripts/publish_test.py --skip-build  # 跳过构建步骤
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# TestPyPI 命令模板
TESTPYPI_INDEX_URL = "https://test.pypi.org/simple/"
PYPI_INDEX_URL = "https://pypi.org/simple/"
PACKAGE_NAME = "mymom"

TESTPYPI_INSTALL_CMD = (
    f"pip install --index-url {TESTPYPI_INDEX_URL} "
    f"--extra-index-url {PYPI_INDEX_URL} {PACKAGE_NAME}"
)
TESTPYPI_UPGRADE_CMD = (
    f"pip install --upgrade --index-url {TESTPYPI_INDEX_URL} "
    f"--extra-index-url {PYPI_INDEX_URL} {PACKAGE_NAME}"
)


def load_env_file():
    """从 .env 文件加载 TEST_PYPI_TOKEN"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("⚠️  未安装 python-dotenv，无法从 .env 文件读取配置")
        print("   提示：pip install python-dotenv")
        return False

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        print(f"ℹ️  未找到 .env 文件: {env_file}")
        print("   提示：可以创建 .env 文件并添加：TEST_PYPI_TOKEN=你的token")
        return False

    load_dotenv(env_file, override=True)
    print(f"✅ 已加载 .env 文件: {env_file}")

    token = os.environ.get("TEST_PYPI_TOKEN")
    if token:
        print("✅ 已从 .env 文件读取 TEST_PYPI_TOKEN")
        return True

    print("⚠️  .env 文件中未找到 TEST_PYPI_TOKEN")
    print("   提示：请在 .env 文件中添加：TEST_PYPI_TOKEN=你的token")
    return False


def print_usage_commands():
    """打印使用说明命令"""
    separator = "=" * 60
    print(f"\n{separator}")
    print("📦 TestPyPI 安装和使用说明")
    print(separator)
    print()
    print("1️⃣  安装（从 TestPyPI）：")
    print(f"   {TESTPYPI_INSTALL_CMD}")
    print()
    print("2️⃣  卸载：")
    print(f"   pip uninstall {PACKAGE_NAME}")
    print()
    print("3️⃣  升级：")
    print(f"   {TESTPYPI_UPGRADE_CMD}")
    print()
    print("4️⃣  启动服务：")
    print(f"   {PACKAGE_NAME} start          # 前台启动")
    print(f"   {PACKAGE_NAME} start --bg     # 后台启动")
    print()
    print("5️⃣  其他命令：")
    print(f"   {PACKAGE_NAME} status         # 查看服务状态")
    print(f"   {PACKAGE_NAME} stop           # 停止服务")
    print()
    print("💡 提示：")
    print("   - TestPyPI 是测试环境，包名和正式 PyPI 相同")
    print("   - 安装时需要同时指定 test.pypi.org 和 pypi.org（因为依赖包在正式 PyPI）")
    print("   - 服务默认运行在 http://127.0.0.1:7937")
    print(separator)


def main():
    """测试发布到 TestPyPI"""
    parser = argparse.ArgumentParser(
        description="测试发布 mymom 到 TestPyPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整流程（构建 + 发布）
  python3 scripts/publish_test.py

  # 跳过构建步骤（使用已有的 dist/ 文件）
  python3 scripts/publish_test.py --skip-build
        """,
    )

    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="跳过构建步骤（使用已有的 dist/ 文件）",
    )

    args = parser.parse_args()

    # 加载 .env 文件获取 TEST_PYPI_TOKEN
    separator = "=" * 60
    print(separator)
    print("🔍 检查环境配置")
    print(separator)
    load_env_file()
    print()

    # 构建命令
    publish_script = SCRIPT_DIR / "publish.py"
    cmd = [sys.executable, str(publish_script), "--test"]
    if args.skip_build:
        cmd.append("--skip-build")

    # 调用主发布脚本
    print(separator)
    print("🚀 开始测试发布到 TestPyPI")
    print(separator)
    print()

    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print_usage_commands()
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发布过程中出现错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

