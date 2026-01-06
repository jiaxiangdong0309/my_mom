#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键发布脚本：构建并发布到 PyPI
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

PROJECT_ROOT = Path(__file__).parent.parent

# 常量定义
SEPARATOR = "=" * 60
PACKAGE_NAME = "mymom"
TESTPYPI_INSTALL_CMD = (
    "pip install --index-url https://test.pypi.org/simple/ "
    "--extra-index-url https://pypi.org/simple/ mymom"
)
PYPI_PROJECT_URL = "https://pypi.org/project/mymom/"


def load_env_file():
    """加载 .env 文件"""
    if not load_dotenv:
        return False

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        print(f"ℹ️  未找到 .env 文件: {env_file}")
        print("   提示：可以创建 .env 文件并添加 PYPI_TOKEN 或 TEST_PYPI_TOKEN")
        return False

    load_dotenv(env_file, override=True)
    print(f"✅ 已加载 .env 文件: {env_file}")
    return True


def get_token(is_test=False):
    """从环境变量获取 token"""
    token_name = "TEST_PYPI_TOKEN" if is_test else "PYPI_TOKEN"
    return os.environ.get(token_name)


def run_command(cmd, check=True, env=None):
    """运行命令"""
    print(f"🔧 执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, shell=False, env=env)
    return result.returncode == 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="发布 mymom 到 PyPI")
    parser.add_argument(
        "--test",
        action="store_true",
        help="发布到 TestPyPI（测试）",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="跳过构建步骤（使用已有的 dist/ 文件）",
    )
    args = parser.parse_args()

    # 步骤 1: 构建包
    if not args.skip_build:
        print(f"\n{SEPARATOR}")
        print("步骤 1/3: 构建分发包")
        print(SEPARATOR)
        build_script = PROJECT_ROOT / "scripts" / "build_package.py"
        if not run_command([sys.executable, str(build_script)]):
            print("❌ 构建失败")
            sys.exit(1)

    # 步骤 2: 检查包
    print(f"\n{SEPARATOR}")
    print("步骤 2/3: 检查打包文件")
    print(SEPARATOR)
    dist_dir = PROJECT_ROOT / "dist"
    if not dist_dir.exists():
        print("❌ dist/ 目录不存在，请先运行构建")
        sys.exit(1)

    dist_files = list(dist_dir.glob("*"))
    if not dist_files:
        print("❌ dist/ 目录为空")
        sys.exit(1)

    check_cmd = [sys.executable, "-m", "twine", "check"] + [
        str(f) for f in dist_files
    ]
    if not run_command(check_cmd):
        print("❌ 检查失败")
        sys.exit(1)

    # 步骤 3: 上传
    print(f"\n{SEPARATOR}")
    repository_name = "TestPyPI" if args.test else "PyPI"
    print(f"步骤 3/3: 上传到 {repository_name}")
    print(SEPARATOR)

    # 重新加载 .env 文件确保获取最新值
    load_env_file()

    # 获取 token
    token = get_token(is_test=args.test)
    token_name = "TEST_PYPI_TOKEN" if args.test else "PYPI_TOKEN"

    # 构建上传命令
    upload_cmd = [sys.executable, "-m", "twine", "upload"]
    if args.test:
        upload_cmd.extend(["--repository", "testpypi"])
    upload_cmd.extend([str(f) for f in dist_files])

    # 设置环境变量（如果提供了 token）
    env = os.environ.copy()
    if token:
        print(f"✅ 检测到 token（来自 .env 文件的 {token_name}），将自动使用")
        env["TWINE_USERNAME"] = "__token__"
        env["TWINE_PASSWORD"] = token
    else:
        print("\n⚠️  未检测到 token")
        print(f"\n可以通过以下方式设置：")
        print(f"1. 在 .env 文件中添加：{token_name}=你的完整token")
        print(f"2. 或设置环境变量：export {token_name}='你的完整token'")
        print("\n提示：使用 API token 时，token 格式为 pypi-xxxxxxxxxxxxx（包括 pypi- 前缀）")
        try:
            input("\n按 Enter 继续（如果无法输入，请在 .env 文件中配置 token）...")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️  非交互式环境")
            print(f"请在项目根目录创建 .env 文件，添加：{token_name}=你的token")
            sys.exit(1)

    if not run_command(upload_cmd, env=env):
        print("❌ 上传失败")
        if not token:
            print(f"\n💡 提示：尝试在 .env 文件中设置 {token_name} 后重新运行")
        sys.exit(1)

    print(f"\n{SEPARATOR}")
    print("✨ 发布成功！")
    print(SEPARATOR)
    if args.test:
        print("\n测试安装:")
        print(f"  {TESTPYPI_INSTALL_CMD}")
    else:
        print("\n安装方式:")
        print(f"  pip install {PACKAGE_NAME}")
        print("\n项目页面:")
        print(f"  {PYPI_PROJECT_URL}")


if __name__ == "__main__":
    main()

