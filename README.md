# AI 知识记忆库

一个为 AI 编辑器用户提供的**本地知识记忆与检索工具**，支持结构化存储、语义搜索和全文检索，解决跨会话、跨编辑器的经验积累和复用问题。

## 项目概述

AI 知识记忆库是一个本地部署的知识管理系统，采用 **SQLite + ChromaDB 双库架构**，支持：

- 📝 **结构化知识存储**：标题、内容、标签、时间戳
- 🔍 **语义搜索**：基于向量相似度的智能检索
- 📄 **全文检索**：SQLite 全文搜索（FTS）
- 🏷️ **标签管理**：多标签分类与过滤
- 🌐 **Web UI**：可视化记忆管理与搜索界面
- 💡 **快速创建**：随机建议辅助快速录入

## 项目架构

本项目采用**三层架构设计**，清晰分离接入层、服务层和存储层，实现模块化和可扩展性。

### 架构层次

```mermaid
graph TB
    subgraph 接入层["接入层（上层）"]
        Skills["Skills<br/>AI编辑器集成"]
        WebUI["Web UI<br/>可视化前端"]
        Skills --> |自然语言交互| API
        WebUI --> |HTTP请求| API
    end

    subgraph 服务层["服务层（中层）"]
        API["FastAPI 接口层<br/>RESTful API"]
        Core["核心业务逻辑层"]
        API --> Core
        Core --> |文本处理| Embedding["Embedding<br/>向量化"]
        Core --> |文本分段| Splitter["Text Splitter<br/>文本分块"]
    end

    subgraph 存储层["存储层（下层）"]
        SQLite["SQLite<br/>结构化数据存储"]
        ChromaDB["ChromaDB<br/>向量数据库"]
    end

    Core --> |结构化数据| SQLite
    Embedding --> |向量数据| ChromaDB

    style 接入层 fill:#e1f5ff
    style 服务层 fill:#fff4e1
    style 存储层 fill:#e8f5e9
```

**架构图说明**：
- 🔵 **接入层**：提供多种接入方式，Skills 和 Web UI 并行
- 🟡 **服务层**：统一 API 接口，核心逻辑处理
- 🟢 **存储层**：双库存储，各司其职

### 架构说明

#### 1. 接入层（上层）

**Skills（AI 编辑器集成）**
- 通过 Cursor Skills 或 Claude MCP 协议集成到 AI 编辑器
- 支持自然语言交互，AI 可自动调用知识库功能
- 实现跨会话、跨编辑器的知识复用

**Web UI（可视化前端）**
- React + TypeScript 构建的现代化 Web 界面
- 提供记忆创建、编辑、删除、搜索等完整功能
- 支持语义搜索和全文检索两种模式切换

#### 2. 服务层（中层）

**FastAPI 接口层**
- 提供 RESTful API，统一对外接口
- 处理请求验证、错误处理、CORS 配置
- 支持 Swagger 自动文档生成

**核心业务逻辑层**
- **Embedding 模块**：文本向量化，使用 BAAI/bge-small-zh-v1.5 模型
- **Text Splitter 模块**：文本分块处理（chunk_size=1000, overlap=100）
- **业务逻辑封装**：协调双库操作，保证数据一致性

#### 3. 存储层（下层）

**SQLite 数据库**
- 存储结构化数据：id、title、content、tags、created_at
- 支持全文检索（FTS），快速关键词匹配
- 轻量级、零配置、本地存储

**ChromaDB 向量数据库**
- 存储文本向量数据，支持语义搜索
- 使用余弦相似度计算，返回相关性排序结果
- 持久化存储，支持增量更新

### 数据流向

**存储流程**：

```mermaid
sequenceDiagram
    participant User as 用户
    participant API as API接口
    participant SQLite as SQLite
    participant Splitter as 文本分块
    participant Embedding as 向量化
    participant ChromaDB as ChromaDB

    User->>API: 创建记忆（title, content, tags）
    API->>SQLite: 存储结构化数据
    SQLite-->>API: 返回 memory_id
    API->>Splitter: 文本分块处理
    Splitter-->>API: 返回文本块列表
    API->>Embedding: 向量化每个文本块
    Embedding-->>API: 返回向量数组
    API->>ChromaDB: 存储向量（关联 memory_id）
    ChromaDB-->>API: 存储成功
    API-->>User: 返回完整记忆数据
```

**搜索流程**：

```mermaid
sequenceDiagram
    participant User as 用户
    participant API as API接口
    participant Embedding as 向量化
    participant ChromaDB as ChromaDB
    participant SQLite as SQLite

    User->>API: 搜索查询（query）
    API->>Embedding: 查询文本向量化
    Embedding-->>API: 返回查询向量
    API->>ChromaDB: 向量相似度检索
    ChromaDB-->>API: 返回 memory_id 列表（按相关性排序）
    API->>SQLite: 批量查询完整数据
    SQLite-->>API: 返回记忆详情列表
    API->>API: 合并结果并计算相似度
    API-->>User: 返回搜索结果（按相关性排序）
```

### 架构优势

- ✅ **职责清晰**：三层架构，各司其职
- ✅ **双库互补**：SQLite 提供结构化查询，ChromaDB 提供语义搜索
- ✅ **易于扩展**：接口层统一，便于添加新的接入方式
- ✅ **本地优先**：所有数据存储在本地，保护隐私

## 技术栈

### 后端
- **语言**: Python 3.11+
- **框架**: FastAPI 0.109+
- **数据库**:
  - SQLite（结构化数据存储）
  - ChromaDB（向量数据库）
- **向量化**: sentence-transformers (BAAI/bge-small-zh-v1.5)
- **文本处理**: tiktoken（分词）

### 前端
- **框架**: React 18 + TypeScript 5
- **构建工具**: Vite 5
- **样式**: 原生 CSS（无 UI 框架）

## 项目结构

```
Mymom/
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
│   ├── store_data.py           # 数据存储测试
│   ├── search_sqlite.py        # SQLite 搜索测试
│   └── search_vector.py        # 向量搜索测试
├── docu/                       # 项目文档
├── requirements.txt            # Python 依赖
└── README.md                   # 项目说明
```

## 核心功能

### 1. 记忆管理
- ✅ 创建记忆（标题、内容、标签）
- ✅ 查看记忆列表（按时间倒序）
- ✅ 查看记忆详情
- ✅ 删除记忆（同步删除 SQLite 和 ChromaDB 数据）

### 2. 搜索功能
- ✅ **语义搜索**：基于向量相似度，支持自然语言查询
- ✅ **全文检索**：SQLite FTS，支持关键词匹配
- ✅ 搜索结果按相关性排序
- ✅ 显示相似度分数

### 3. 数据存储
- ✅ **SQLite**：存储结构化数据（id, title, content, tags, created_at）
- ✅ **ChromaDB**：存储向量数据，支持语义检索
- ✅ 文本自动分块（chunk_size=1000, overlap=100）
- ✅ 双库同步删除

### 4. Web 界面
- ✅ 记忆列表展示
- ✅ 创建/编辑表单
- ✅ 搜索界面（支持切换搜索模式）
- ✅ 快速创建建议
- ✅ 统计信息显示

## 快速开始

### 1. 环境要求

- Python 3.11+
- Node.js 18+ 和 npm

### 2. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
```

### 3. 启动服务

**方式一：使用一键启动脚本（推荐）**

```bash
python3 scripts/run_dev.py
```

脚本会自动启动后端和前端服务，并显示访问地址。

**方式二：手动启动**

```bash
# 终端 1：启动后端服务
cd backend
python3 main.py

# 终端 2：启动前端开发服务器
cd frontend
npm run dev
```

### 4. 访问应用

- **前端界面**: http://localhost:5173（Vite 默认端口）
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs（Swagger UI）

## API 接口

### 记忆管理

- `POST /api/v1/memories/` - 创建记忆
- `GET /api/v1/memories/` - 获取所有记忆列表
- `GET /api/v1/memories/{memory_id}` - 获取记忆详情
- `DELETE /api/v1/memories/{memory_id}` - 删除记忆
- `GET /api/v1/memories/stats` - 获取统计信息

### 搜索

- `POST /api/v1/search/` - 语义搜索（向量检索）

### 健康检查

- `GET /health` - 服务健康检查

## 开发说明

### 数据存储位置

- SQLite 数据库：`backend/data/memories.db`
- ChromaDB 数据：`backend/data/chroma/`

### 配置说明

配置文件：`backend/config.py`

主要配置项：
- `embedding_model`: 向量化模型（默认：BAAI/bge-small-zh-v1.5）
- `port`: 后端服务端口（默认：8000）
- `data_dir`: 数据存储目录（默认：`backend/data/`）

### 文本分块策略

- **块大小**: 1000 字符
- **重叠大小**: 100 字符
- **分块方式**: 按字符数切分（保留语义完整性）

## 开发状态

当前版本：**v0.1 - 核心功能已完成**

- ✅ 后端 API 开发完成
- ✅ 前端界面开发完成
- ✅ 双库存储架构实现
- ✅ 语义搜索功能实现
- ✅ 全文检索功能实现
- ✅ Web UI 交互完成
- ⏳ AI 编辑器集成（规划中）

## 相关文档

- [产品需求文档 (PRD)](docu/AI知识记忆库%20产品需求文档%20(PRD).md)
- [架构设计文档](docu/架构设计文档.md)
- [技术选型文档](docu/技术选型文档.md)
- [版本迭代规划](docu/版本迭代规划.md)

## 注意事项

1. **首次运行**：首次启动时会自动创建数据目录和数据库文件
2. **模型下载**：首次使用向量搜索时会自动下载 embedding 模型（约 100MB）
3. **端口占用**：确保 8000 和 5173 端口未被占用
4. **数据安全**：所有数据存储在本地，不会上传到云端

## 许可证

待定
