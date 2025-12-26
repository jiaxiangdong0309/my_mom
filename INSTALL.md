# Mymom 安装和使用指南

## 打包项目

### 1. 构建前端

首先需要构建前端并集成到后端：

```bash
python3 scripts/build_dist.py
```

这会：
- 安装前端依赖（如果需要）
- 构建前端项目
- 将构建产物复制到 `backend/static/` 目录

### 2. 构建 Python 包

```bash
# 安装构建工具（如果还没有）
pip install build wheel

# 构建分发包
python3 -m build
```

构建完成后，会在 `dist/` 目录下生成：
- `mymom-0.1.0.tar.gz` - 源码分发包
- `mymom-0.1.0-py3-none-any.whl` - 预构建的 wheel 包（推荐使用）

## 安装包

### 方式一：从本地 wheel 文件安装（推荐）

```bash
pip install dist/mymom-0.1.0-py3-none-any.whl
```

### 方式二：从本地源码安装

```bash
pip install dist/mymom-0.1.0.tar.gz
```

### 方式三：直接从项目目录安装（开发模式）

```bash
pip install -e .
```

## 使用

安装完成后，可以使用 `mymom` 命令：

### 启动服务

```bash
# 前台启动（默认）
mymom start

# 后台启动
mymom start --daemon
```

### 检查服务状态

```bash
mymom status
```

### 访问应用

服务启动后，访问：
- **Web 界面**: http://127.0.0.1:7937
- **API 文档**: http://127.0.0.1:7937/docs

## 数据存储位置

安装后的数据存储位置：

- **开发环境**（项目目录有 `.git`）：`./data/`
- **用户环境**：`~/.mymom/data/`
- **自定义位置**：设置环境变量 `MYMOM_DATA_PATH`

## 卸载

```bash
pip uninstall mymom
```

## 注意事项

1. **首次运行**：首次启动时会自动下载 embedding 模型（约 100MB），请确保网络连接正常
2. **端口占用**：默认端口是 7937，如果被占用可以通过环境变量 `MYMOM_PORT` 修改
3. **数据安全**：所有数据存储在本地，不会上传到云端

## 环境变量配置

可以通过环境变量自定义配置：

- `MYMOM_DATA_PATH`: 数据存储路径
- `MYMOM_PORT`: 服务端口（默认：7937）
- `MYMOM_HOST`: 服务主机（默认：127.0.0.1）
- `MYMOM_EMBEDDING_MODEL`: Embedding 模型（默认：BAAI/bge-small-zh-v1.5）

