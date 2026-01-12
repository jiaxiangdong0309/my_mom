# 项目详细说明

本文档包含项目的技术栈、文件结构、核心功能清单、API 接口定义以及开发相关的配置信息。


可视化页面：
![可视化页面](image.png)

## 技术栈

### 后端
- **语言**: Python 3.11+
- **框架**: FastAPI 0.109+
- **数据库**:
  - SQLite（结构化数据存储）
  - ChromaDB（向量数据库）
- **向量化**: sentence-transformers (BAAI/bge-small-zh-v1.5)
- **文本处理**: 文本分块（chunk_size=1000, overlap=100）

### 前端
- **框架**: React 18 + JavaScript (JSX)
- **构建工具**: Vite 5
- **样式**: 原生 CSS（无 UI 框架）
- **可视化**: @visactor/vchart（标签统计图表）

## 项目结构

```
Mymem/
├── backend/                    # 后端服务
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置管理
│   ├── api/                    # API 路由层
│   │   ├── memories.py         # 记忆存储接口
│   │   ├── search.py           # 搜索接口
│   │   └── models.py           # Pydantic 数据模型
│   ├── core/                   # 核心功能层
│   │   ├── chroma_db.py        # ChromaDB 封装
│   │   ├── sqlite_db.py        # SQLite 封装
│   │   └── embedding.py        # Embedding 向量化
│   ├── utils/                  # 工具函数
│   │   └── text_splitter.py    # 文本分段处理
│   └── data/                   # 数据存储目录（自动创建）
│       ├── chroma/             # ChromaDB 数据
│       └── memories.db         # SQLite 数据库
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── api/                # API 调用封装
│   │   ├── components/         # React 组件
│   │   │   ├── Layout.jsx      # 布局组件
│   │   │   ├── MemoryList.jsx  # 记忆列表
│   │   │   ├── MemoryCard.jsx  # 记忆卡片
│   │   │   ├── MemoryForm.jsx  # 创建/编辑表单
│   │   │   ├── MemoryDetail.jsx # 记忆详情
│   │   │   ├── SearchBar.jsx   # 搜索栏
│   │   │   ├── SearchResults.jsx # 搜索结果
│   │   │   └── SuggestionCard.jsx # 建议卡片
│   │   ├── utils/              # 工具函数
│   │   ├── App.jsx             # 主应用组件
│   │   └── main.jsx            # 入口文件
│   ├── package.json
│   └── vite.config.js
├── scripts/                    # 工具脚本
│   ├── run_dev.py              # 一键启动开发服务器
│   ├── build_dist.py           # 构建前端并集成到后端
│   ├── build_package.py        # 一键打包脚本
│   ├── store_data.py           # 数据存储测试
│   ├── search_sqlite.py        # SQLite 搜索测试
│   └── search_vector.py        # 向量搜索测试
├── docu/                       # 项目文档
├── dist/                       # 打包产物（构建后生成）
├── pyproject.toml              # Python 项目配置
├── requirements.txt            # Python 依赖
├── INSTALL.md                  # 安装指南
├── PACKAGE.md                  # 打包指南
└── README.md                   # 项目说明
```

## 核心功能清单

### 1. 记忆管理
- ✅ 创建记忆（标题、内容、标签）
- ✅ 查看记忆列表（按时间倒序）
- ✅ 查看记忆详情（Dialog 弹窗）
- ✅ 编辑记忆
- ✅ 删除记忆（同步删除 SQLite 和 ChromaDB 数据）
- ✅ 统计信息（SQLite/ChromaDB 数据量）

### 2. 搜索功能
- ✅ **语义搜索**：基于向量相似度，支持自然语言查询
- ✅ **全文检索**：SQLite FTS，支持关键词匹配
- ✅ 搜索结果按相关性排序
- ✅ 显示相似度分数
- ✅ 支持切换搜索模式（前端 UI）

### 3. 数据存储
- ✅ **SQLite**：存储结构化数据
- ✅ **ChromaDB**：存储向量数据
- ✅ 文本自动分块
- ✅ 双库同步删除
- ✅ 智能路径选择（开发/用户环境自动识别）

### 4. CLI 工具
- ✅ `mymem start` - 前台启动服务
- ✅ `mymem start --bg` - 后台启动服务
- ✅ `mymem status` - 检查服务状态
- ✅ `mymem stop` - 停止服务

## API 接口

### 记忆管理
- `POST /api/v1/memories/` - 创建记忆
- `GET /api/v1/memories/` - 获取所有记忆列表
- `GET /api/v1/memories/{memory_id}` - 获取记忆详情
- `DELETE /api/v1/memories/{memory_id}` - 删除记忆
- `GET /api/v1/memories/stats` - 获取统计信息

### 搜索
- `POST /api/v1/search/` - 语义搜索（向量检索）
- `POST /api/v1/search/sqlite` - 全文检索（SQLite FTS）

### 健康检查
- `GET /health` - 服务健康检查

## 开发与配置

### 数据存储位置
数据存储位置根据运行环境自动选择：
- **开发环境**（项目目录存在 `.git`）：`./data/`
- **用户环境**：`~/.mymem/data/`
- **自定义位置**：通过环境变量 `MYMEM_DATA_PATH` 指定

### 配置说明
可通过环境变量配置（前缀 `MYMEM_`）：
- `MYMEM_PORT`: 服务端口（默认：7937）
- `MYMEM_HOST`: 服务主机（默认：127.0.0.1）
- `MYMEM_DATA_PATH`: 数据存储路径
- `MYMEM_EMBEDDING_MODEL`: Embedding 模型
- `MYMEM_ENV`: 环境模式 (dev/prod/auto)

## 开发状态
当前版本：**v0.1.1**
- ✅ 核心功能已完成
- ✅ 双库架构、语义搜索、CLI 工具、Web UI 全部上线
- ⏳ AI 编辑器集成 (Skills) - 规划中

## 相关文档链接
- [产品需求文档 (PRD)](docu/AI知识记忆库%20产品需求文档%20(PRD).md)
- [架构设计文档](docu/架构设计文档.md)
- [技术选型文档](docu/技术选型文档.md)
- [版本迭代规划](docu/版本迭代规划.md)
