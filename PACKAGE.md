# 打包和安装指南

## 快速开始

### 1. 一键打包

```bash
python3 scripts/build_package.py
```

这个脚本会自动：
- 构建前端并集成到后端
- 生成 Python 分发包（wheel 和 tar.gz）

### 2. 安装包

```bash
pip install dist/mymom-0.1.0-py3-none-any.whl
```

### 3. 运行

```bash
# 启动服务
mymom start

# 检查状态
mymom status

# 后台启动
mymom start --daemon
```

### 4. 访问

- Web 界面: http://127.0.0.1:7937
- API 文档: http://127.0.0.1:7937/docs

## 详细步骤

### 步骤 1: 构建前端

```bash
python3 scripts/build_dist.py
```

### 步骤 2: 构建 Python 包

```bash
# 安装构建工具
pip install build wheel

# 构建包
python3 -m build
```

### 步骤 3: 安装

```bash
# 从 wheel 文件安装（推荐）
pip install dist/mymom-0.1.0-py3-none-any.whl

# 或从源码安装
pip install dist/mymom-0.1.0.tar.gz
```

### 步骤 4: 使用

安装后，`mymom` 命令会被添加到系统 PATH：

```bash
# 查看帮助
mymom --help

# 启动服务（前台）
mymom start

# 启动服务（后台）
mymom start --daemon

# 检查服务状态
mymom status
```

## 开发模式安装

如果你想在开发时直接使用，可以使用可编辑安装：

```bash
pip install -e .
```

这样修改代码后无需重新安装。

## 卸载

```bash
pip uninstall mymom
```

## 注意事项

1. **首次运行**：首次启动时会自动下载 embedding 模型（约 100MB）
2. **数据存储**：
   - 开发环境：`./data/`
   - 用户环境：`~/.mymom/data/`
   - 自定义：设置 `MYMOM_DATA_PATH` 环境变量
3. **端口配置**：默认 7937，可通过 `MYMOM_PORT` 环境变量修改

## 环境变量

- `MYMOM_DATA_PATH`: 数据存储路径
- `MYMOM_PORT`: 服务端口（默认：7937）
- `MYMOM_HOST`: 服务主机（默认：127.0.0.1）
- `MYMOM_EMBEDDING_MODEL`: Embedding 模型

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

