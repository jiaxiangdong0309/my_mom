import os
import shutil
import sys

# 设置路径
base_dir = os.path.dirname(os.path.abspath(__file__))
chroma_dir = os.path.join(base_dir, "backend", "data", "chroma")
sqlite_db = os.path.join(base_dir, "backend", "data", "memories.db")

def clear_data():
    print(f"🚀 正在准备清空数据以适配新模型 BAAI/bge-small-zh-v1.5 (512维)...")

    # 1. 清空 ChromaDB
    if os.path.exists(chroma_dir):
        print(f"🗑️ 正在删除 ChromaDB 目录: {chroma_dir}")
        try:
            shutil.rmtree(chroma_dir)
            print("✅ ChromaDB 目录已成功删除。")
        except Exception as e:
            print(f"❌ 删除 ChromaDB 目录失败: {e}")
            print("💡 提示: 请确保后端服务 (main.py) 已经停止运行，否则文件可能被占用。")
            return
    else:
        print("ℹ️ ChromaDB 目录不存在，无需删除。")

    # 2. 清空 SQLite (可选，用户说删过，但为了彻底同步建议也清空或保留)
    # 这里我们只提示用户，不强制删除 SQLite，除非他们想完全重来
    if os.path.exists(sqlite_db):
        print(f"ℹ️ 发现 SQLite 数据库: {sqlite_db}")
        print("💡 如果你希望完全重新开始，可以手动删除此文件。")

    print("\n✨ 清空完成！现在请执行以下步骤：")
    print("1. 确保已停止所有正在运行的 python3 main.py 进程。")
    print("2. 重新启动后端服务: cd backend && python3 main.py")
    print("3. 通过前端界面重新添加记忆。")
    print("4. 再次运行 search_vector.py 脚本进行搜索。")

if __name__ == "__main__":
    clear_data()

