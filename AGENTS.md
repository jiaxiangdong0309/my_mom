# AI 编程助手指南


## 核心规则（必须永远执行）

1. **禁止启动服务** - 永远不要执行 `python3 main.py`、`npm run dev`、`mymom start` 等启动命令。提示用户手动运行。

2. **准确理解意图** - 区分请求类型（简单问答/修复bug/实现方案/研究知识点/写需求），按需回答。简单问题直接回答，不要过度展开项目相关内容。

3. **充分调研再行动** - 写代码或回答前，先深度理解上下文（阅读相关文件、搜索代码库、理解影响范围），避免引入新bug或给出不合适的方案。

## 项目概述

**AI 知识记忆库**：一个本地部署的知识管理系统，采用**三层架构设计**（接入层、服务层、存储层），支持结构化存储、语义搜索和全文检索。

### 核心特性
- 📝 **结构化知识存储**：标题、内容、标签、时间戳
- 🔍 **双模式搜索**：语义搜索（向量检索）和全文检索（SQLite FTS）
- 🏷️ **标签管理**：多标签分类与过滤
- 🌐 **Web UI**：React 构建的可视化界面
- 💡 **快速创建**：随机建议辅助快速录入
- 📊 **用户画像**：标签统计可视化（云图、饼图、柱状图）
- 🚀 **CLI 工具**：`mymom` 命令行工具，支持前台/后台启动
- 📦 **打包安装**：支持 pip 安装，一键部署

### 三层架构

```
接入层（上层）
  ├── Skills（AI编辑器集成）- 规划中
  └── Web UI（可视化前端）- 已完成

服务层（中层）
  ├── FastAPI 接口层（RESTful API）
  ├── Embedding 模块（文本向量化）
  └── Text Splitter 模块（文本分块）

存储层（下层）
  ├── SQLite（结构化数据存储）
  └── ChromaDB（向量数据库）
```

## 开发准则

### 架构原则
- **无抽象层**：直接实现，不创建抽象基类
- **直接实例化**：不使用依赖注入
- **够用即可**：不预留过度扩展点
- **三层分离**：接入层、服务层、存储层职责清晰

### 代码风格
- **Python**: 类型提示、PEP 8、snake_case、docstring
- **JavaScript/JSX**: ES6+、PascalCase 组件、camelCase 函数/变量

### 项目结构
```
backend/
  ├── main.py              # FastAPI 入口（含 CLI）
  ├── config.py            # 配置管理（智能路径选择）
  ├── api/                  # 路由层
  │   ├── memories.py      # 记忆管理接口
  │   ├── search.py        # 搜索接口（语义/全文）
  │   └── models.py        # Pydantic 数据模型
  ├── core/                 # 核心功能层
  │   ├── chroma_db.py     # ChromaDB 封装
  │   ├── sqlite_db.py     # SQLite 封装
  │   └── embedding.py     # Embedding 向量化
  ├── utils/                # 工具函数
  │   └── text_splitter.py # 文本分段处理
  └── static/               # 前端构建产物（自动集成）

frontend/src/
  ├── api/                  # API 调用封装
  ├── components/           # React 组件
  │   ├── Layout.jsx
  │   ├── MemoryList.jsx
  │   ├── MemoryCard.jsx
  │   ├── MemoryForm.jsx
  │   ├── MemoryDetail.jsx
  │   ├── SearchBar.jsx
  │   ├── SearchResults.jsx
  │   ├── SuggestionCard.jsx
  │   ├── UserProfile.jsx
  │   └── Tag*.jsx（可视化组件）
  ├── utils/                # 工具函数
  └── App.jsx               # 主应用组件

scripts/                    # 工具脚本
  ├── run_dev.py           # 一键启动开发服务器
  ├── build_dist.py        # 构建前端并集成到后端
  └── build_package.py     # 一键打包脚本

data/                       # 本地存储（自动创建，开发环境）
```

## 重要约束

1. **本地优先**：数据不上云，所有数据存储在本地
2. **极简架构**：避免过度设计，够用即可
3. **单用户场景**：当前版本面向单用户
4. **不自动运行服务**：提示用户手动启动（`mymom start` 或 `python3 scripts/run_dev.py`）
5. **智能路径选择**：
   - 开发环境（存在 `.git`）：`./data/`
   - 用户环境：`~/.mymom/data/`
   - 可通过 `MYMOM_DATA_PATH` 环境变量自定义

## 技术栈

### 后端
- **语言**: Python 3.11+
- **框架**: FastAPI 0.109+
- **数据库**:
  - SQLite（结构化数据存储，支持 FTS 全文检索）
  - ChromaDB（向量数据库，支持语义搜索）
- **向量化**: sentence-transformers (BAAI/bge-small-zh-v1.5)
- **文本处理**: 文本分块（chunk_size=1000, overlap=100）

### 前端
- **框架**: React 18 + JavaScript (JSX)
- **构建工具**: Vite 5
- **样式**: 原生 CSS（无 UI 框架）
- **可视化**: @visactor/vchart（标签统计图表）

### CLI 工具
- **命令**: `mymom`（通过 `pip install -e .` 安装后可用）
- **功能**: `start`（前台/后台）、`status`、`stop`

## 核心功能

### 1. 记忆管理
- ✅ 创建记忆（标题、内容、标签）
- ✅ 查看记忆列表（按时间倒序）
- ✅ 查看记忆详情（Dialog 弹窗）
- ✅ 编辑记忆
- ✅ 删除记忆（同步删除 SQLite 和 ChromaDB 数据）
- ✅ 统计信息（SQLite/ChromaDB 数据量）

### 2. 搜索功能
- ✅ **语义搜索**：基于向量相似度，支持自然语言查询
  - 使用 ChromaDB 向量检索
  - 阈值过滤（relevance >= 0.7）
  - 间隔分析（智能分割，保留相关性高的结果）
- ✅ **全文检索**：SQLite FTS，支持关键词匹配
- ✅ 搜索结果按相关性排序
- ✅ 显示相似度分数
- ✅ 支持切换搜索模式（前端 UI）

### 3. 数据存储
- ✅ **SQLite**：存储结构化数据（id, title, content, tags, created_at）
- ✅ **ChromaDB**：存储向量数据，支持语义检索
- ✅ 文本自动分块（chunk_size=1000, overlap=100）
- ✅ 双库同步删除
- ✅ 智能路径选择（开发/用户环境自动识别）

### 4. Web 界面
- ✅ 记忆列表展示
- ✅ 创建/编辑表单
- ✅ 搜索界面（支持切换搜索模式：语义搜索/全文检索）
- ✅ 快速创建建议（随机生成，可折叠）
- ✅ 用户画像页面（标签云图、饼图、柱状图）
- ✅ 统计信息显示
- ✅ 前端构建产物集成到后端（单端口访问）

### 5. CLI 工具
- ✅ `mymom start` - 前台启动服务
- ✅ `mymom start --bg` - 后台启动服务
- ✅ `mymom status` - 检查服务状态
- ✅ `mymom stop` - 停止服务

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

## 搜索策略

### 语义搜索流程
1. 查询文本向量化（使用 BAAI/bge-small-zh-v1.5）
2. ChromaDB 向量检索（top_k=10）
3. 去重处理（同一记忆的多个块只保留相关性最高的）
4. 从 SQLite 批量获取完整数据
5. 计算相似度（distance 转换为 relevance，归一化到 [0, 1]）
6. 阈值过滤（relevance >= 0.7）
7. 间隔分析（找到相关性明显下降的临界点，智能分割）
8. 按相关性排序返回

### 全文检索流程
1. SQLite FTS 关键词匹配
2. 返回匹配的记忆列表
3. 默认 relevance=1.0（关键字匹配）

## 配置说明

### 环境变量
- `MYMOM_PORT` - 服务端口（默认：7937）
- `MYMOM_HOST` - 服务主机（默认：127.0.0.1）
- `MYMOM_DATA_PATH` - 数据存储路径（覆盖自动选择）
- `MYMOM_EMBEDDING_MODEL` - Embedding 模型（默认：BAAI/bge-small-zh-v1.5）
- `MYMOM_ENV` - 环境模式（dev/prod/auto，默认：auto）

### 配置文件
- `backend/config.py` - 配置管理（支持环境变量）
- 智能环境识别：存在 `.git` 目录 → 开发环境 → `./data/`
- 用户环境：`~/.mymom/data/`

## 开发状态

当前版本：**v0.1.0 - 核心功能已完成**

- ✅ 后端 API 开发完成
- ✅ 前端界面开发完成
- ✅ 双库存储架构实现
- ✅ 语义搜索功能实现（含阈值过滤和间隔分析）
- ✅ 全文检索功能实现
- ✅ Web UI 交互完成
- ✅ CLI 命令行工具（`mymom` 命令）
- ✅ 打包和安装支持（pip install）
- ✅ 用户画像可视化（标签统计）
- ✅ 前端构建集成（静态文件自动部署）
- ⏳ AI 编辑器集成（Skills）- 规划中

## 注意事项

1. **首次运行**：首次启动时会自动创建数据目录和数据库文件
2. **模型下载**：首次使用向量搜索时会自动下载 embedding 模型（约 100MB），请确保网络连接正常
3. **端口占用**：默认端口是 7937，如果被占用可以通过环境变量 `MYMOM_PORT` 修改
4. **数据安全**：所有数据存储在本地，不会上传到云端
5. **数据位置**：开发环境使用 `./data/`，用户环境使用 `~/.mymom/data/`，可通过 `MYMOM_DATA_PATH` 自定义
6. **前端构建**：前端构建产物会自动集成到 `backend/static/`，支持单端口访问

---

<!-- OPENSPEC:START -->
# OpenSpec 使用说明

当请求出现以下情况时，始终打开 `@/openspec/AGENTS.md`：
- 提及规划或提案（proposal、spec、change、plan 等）
- 引入新功能、破坏性变更、架构转变或大型性能/安全工作
- 听起来不明确，在编码之前需要权威规范

保留此托管块，以便 'openspec update' 可以刷新说明。

<!-- OPENSPEC:END -->
