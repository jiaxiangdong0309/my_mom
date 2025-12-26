# 向量语义搜索指南

本指南详细说明如何使用 `query_vector.py` 脚本进行向量语义搜索。

---

## 功能说明

向量搜索基于语义相似度，可以：
- 理解查询的**语义含义**，而非仅匹配关键词
- 找到**同义词**和相关概念（如搜索"编程"能找到"开发"相关内容）
- 处理**自然语言查询**（如"关于学习方法的内容"）
- 返回按**相似度排序**的结果（包含 `relevance` 字段）

---

## 脚本位置

脚本路径：`.claude/skills/query-knowledge-base/search/vector-search/query_vector.py`

## 执行方式

**从项目根目录执行**（推荐）：
```bash
# 从项目根目录执行
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "查询内容"
```

**或者先切换到脚本目录**：
```bash
cd .claude/skills/query-knowledge-base/search/vector-search
python3 query_vector.py "查询内容"
```

---

## 前置条件

**重要**：向量搜索需要后端服务运行。

### 启动后端服务

在项目根目录执行：
```bash
cd backend
python3 main.py
```

后端服务默认运行在 `http://localhost:8000`

---

## 基本用法

### 1. 简单搜索

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法"
```

### 2. 限制结果数量

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "AI" --limit 3
```

### 3. 指定 API 地址

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "Python" --api-url http://localhost:8000
```

---

## 使用场景

### 场景 1: 语义查询

当查询意图不明确或使用自然语言描述时：

```bash
# 搜索"学习方法"相关的内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法"
```

**优势**：即使内容中没有"学习方法"这个词，也能找到相关的学习技巧、学习笔记等内容。

### 场景 2: 同义词搜索

查找同义词和相关概念：

```bash
# 搜索"编程"，能找到"开发"、"代码"等相关内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "编程"
```

### 场景 3: 概念查询

查找相关概念和主题：

```bash
# 搜索"机器学习"，能找到"AI"、"算法"、"数据科学"等相关内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "机器学习"
```

### 场景 4: 模糊查询

当用户描述不够精确时：

```bash
# 搜索"有用的内容"
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "有用的内容"
```

---

## 输出格式

所有命令返回 **JSON 格式**，包含以下字段：

```json
[
  {
    "id": 1,
    "title": "记忆标题",
    "content": "记忆内容",
    "tags": ["标签1", "标签2"],
    "created_at": "2024-01-01T00:00:00",
    "relevance": 0.95
  }
]
```

### 关键字段说明

- `relevance`: 相似度分数（0-1），数值越高表示与查询越相关
- 结果按 `relevance` 降序排列（最相关的结果在前）

### 美化输出

```bash
# 使用 json.tool 美化
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法" | python3 -m json.tool

# 使用 jq 提取特定字段
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法" | jq '.[] | {title, relevance}'
```

---

## 与 SQLite 搜索的区别

| 特性 | SQLite 搜索 | 向量搜索 |
|------|------------|---------|
| **搜索原理** | 关键词匹配（LIKE） | 语义相似度（Embedding） |
| **查询方式** | 精确关键词 | 自然语言描述 |
| **同义词支持** | ❌ | ✅ |
| **相关概念** | ❌ | ✅ |
| **大小写敏感** | ✅ | ❌ |
| **结果排序** | 按创建时间 | 按相似度 |
| **依赖要求** | 仅需数据库 | 需要后端服务 |
| **查询速度** | 快速 | 需要网络请求 |

### 何时使用向量搜索

✅ **使用向量搜索**：
- 查询意图不明确或模糊
- 需要理解同义词和相关概念
- 查询是自然语言描述
- 需要按相关性排序

❌ **不使用向量搜索**：
- 需要精确关键词匹配
- 需要按标签筛选
- 需要获取特定 ID
- 需要列出最近的内容

---

## 错误处理

### 后端服务未启动

如果后端服务未启动，会返回友好的错误提示：

```json
{
  "error": true,
  "message": "无法连接到后端服务 (http://localhost:8000)。\n请确保后端服务已启动：\n  cd backend && python3 main.py"
}
```

**解决方法**：启动后端服务
```bash
cd backend
python3 main.py
```

### 连接超时

如果请求超过 10 秒未响应：

```json
{
  "error": true,
  "message": "请求超时（超过 10 秒）。请检查后端服务是否正常运行。"
}
```

**解决方法**：检查后端服务状态，确保正常运行

### API 错误

如果 API 返回错误：

```json
{
  "error": true,
  "message": "API 请求失败 (HTTP 500): ..."
}
```

**解决方法**：检查后端日志，查看具体错误信息

---

## 最佳实践

### 1. 使用自然语言描述

✅ **推荐**：
```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "关于学习方法的内容"
```

❌ **不推荐**（应使用 SQLite 搜索）：
```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法"
```

### 2. 合理设置结果数量

根据需求设置 `--limit`：
- 快速预览：`--limit 3`
- 详细搜索：`--limit 10`
- 默认：`--limit 5`

### 3. 结合 SQLite 搜索

对于结构化查询（标签、ID、最近），使用 SQLite 搜索：
```bash
# 使用 SQLite 搜索按标签筛选
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "技术"
```

对于语义查询，使用向量搜索：
```bash
# 使用向量搜索查找相关概念
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "技术相关的内容"
```

---

## API 参数参考

### 位置参数

- `query`: (必填) 搜索查询文本（自然语言描述）

### 可选参数

- `--limit`: 限制返回的结果数量（默认: 5）
- `--api-url`: API 基础地址（默认: `http://localhost:8000`）

---

## 快速参考

| 操作 | 命令 |
|------|------|
| 基本搜索 | `python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "查询内容"` |
| 限制结果数量 | `python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "查询内容" --limit 3` |
| 指定 API 地址 | `python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "查询内容" --api-url http://localhost:8000` |

---

## 下一步

- **使用示例**: 查看 [EXAMPLES.md](EXAMPLES.md) 了解复杂查询示例
- **SQLite 搜索**: 如需精确关键词搜索，查看 [../sqlite-search/SQLITE_SEARCH_GUIDE.md](../sqlite-search/SQLITE_SEARCH_GUIDE.md)
- **决策指南**: 查看 [../SEARCH_GUIDE.md](../SEARCH_GUIDE.md) 了解如何选择合适的搜索方式
- **添加记忆**: 查看 [../../add/ADD_GUIDE.md](../../add/ADD_GUIDE.md) 了解如何添加新记忆

