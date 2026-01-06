# 打包和安装指南

## 环境要求

- Python 3.11+
- Node.js 18+ 和 npm

---

## 一、本地运行（开发模式）

适用于开发和测试，代码修改后立即生效。

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
```

### 2. 可编辑安装（推荐）

```bash
# 安装包（可编辑模式）
pip install -e .
```

这样修改代码后无需重新安装。

### 3. 启动服务

**方式一：使用一键启动脚本（推荐）**

```bash
python3 scripts/run_dev.py
```

脚本会自动启动后端和前端开发服务器，并显示访问地址。

**方式二：手动启动（前后端分离）**

```bash
# 终端 1：启动后端服务
cd backend
python3 main.py

# 终端 2：启动前端开发服务器
cd frontend
npm run dev
```

### 4. 访问应用

- **Web 界面**: http://127.0.0.1:7937（默认端口，包含前端页面）
- **API 文档**: http://127.0.0.1:7937/docs（Swagger UI）
- **前端热更新**: http://localhost:3000（仅开发调试时使用）

---

## 二、打包执行（生产环境）

适用于生产部署，生成可分发的安装包。

### 1. 一键打包

```bash
python3 scripts/build_package.py
```

这个脚本会自动：
- 构建前端并集成到后端
- 生成 Python 分发包（wheel 和 tar.gz）

### 2. 安装包

```bash
# 从 wheel 文件安装（推荐）
pip install dist/mymom-0.1.0-py3-none-any.whl

# 或从源码安装
pip install dist/mymom-0.1.0.tar.gz
```

### 3. 启动服务

```bash
# 前台启动（自动检测为生产模式）
mymom start

# 后台启动
mymom start --bg

# 检查服务状态
mymom status

# 停止服务
mymom stop
```

> **说明**：`mymom start` 会自动检测环境。在生产环境（无 `.git` 目录）下，会以生产模式启动（无代码热重载）。

### 4. 访问应用

- **Web 界面**: http://127.0.0.1:7937（默认端口）
- **API 文档**: http://127.0.0.1:7937/docs（Swagger UI）

### 5. 卸载

```bash
pip uninstall mymom
```

---

## 三、发布到 PyPI（可选）

适用于开发者将包发布到官方 [PyPI](https://pypi.org/) 或 [TestPyPI](https://test.pypi.org/)。

### 1. 准备工作

发布前需要安装必要的工具，并获取 PyPI 的 API Token。

```bash
# 安装发布工具
pip install twine python-dotenv
```

在项目根目录创建 `.env` 文件，并添加你的 API Token：

```env
# 正式 PyPI Token (pypi-xxxx...)
PYPI_TOKEN=your_pypi_token

# TestPyPI Token (pypi-xxxx...)
TEST_PYPI_TOKEN=your_test_pypi_token
```

### 2. 发布到 TestPyPI（推荐先在测试环境验证）

```bash
python3 scripts/publish_test.py
```

该脚本会自动执行构建、检查、并上传到 TestPyPI。发布后可以通过以下命令测试安装：

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mymom
```

### 3. 发布到正式 PyPI

确认一切正常后，可以发布到正式环境：

```bash
python3 scripts/publish.py
```

### 4. 发布参数说明

`scripts/publish.py` 支持以下参数：
- `--test`: 发布到 TestPyPI。
- `--skip-build`: 跳过构建步骤，直接使用现有的 `dist/` 文件。

---

## 配置说明

### 环境变量

可通过环境变量配置（前缀 `MYMOM_`）：

- `MYMOM_PORT`: 服务端口（默认：7937）
- `MYMOM_HOST`: 服务主机（默认：127.0.0.1）
- `MYMOM_DATA_PATH`: 数据存储路径（覆盖自动选择）
- `MYMOM_EMBEDDING_MODEL`: Embedding 模型（默认：BAAI/bge-small-zh-v1.5）
- `MYMOM_ENV`: 环境模式（dev/prod/auto，默认：auto）

### 数据存储位置

数据存储位置根据运行环境自动选择：

- **开发环境**（项目目录存在 `.git`）：`./data/`
  - SQLite 数据库：`./data/memories.db`
  - ChromaDB 数据：`./data/chroma/`
- **用户环境**：`~/.mymom/data/`
  - SQLite 数据库：`~/.mymom/data/memories.db`
  - ChromaDB 数据：`~/.mymom/data/chroma/`
- **自定义位置**：通过环境变量 `MYMOM_DATA_PATH` 指定

---

## 注意事项

1. **首次运行**：首次启动时会自动创建数据目录和数据库文件
2. **模型下载**：首次使用向量搜索时会自动下载 embedding 模型（约 100MB），请确保网络连接正常
3. **端口占用**：默认端口是 7937，如果被占用可以通过环境变量 `MYMOM_PORT` 修改
4. **数据安全**：所有数据存储在本地，不会上传到云端
5. **前端构建**：前端构建产物会自动集成到 `backend/static/`，支持单端口访问

---

## 故障排查

### 问题：找不到 mymom 命令

**解决方案**：
- 确保 pip 安装目录在 PATH 中
- 尝试使用 `python3 -m backend.main` 直接运行

### 问题：静态文件无法加载

**解决方案**：
- 确保在打包前运行了 `scripts/build_dist.py`
- 检查 `backend/static/` 目录是否存在

### 问题：端口被占用

**解决方案**：
- 使用 `MYMOM_PORT` 环境变量指定其他端口
- 或通过 `mymom status` 检查是否有旧进程在运行
