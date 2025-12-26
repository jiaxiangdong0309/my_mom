# 搜索功能决策指南

本指南帮助 AI 根据查询意图选择合适的搜索方式。

---

## 两种搜索方式对比

| 特性 | SQLite 关键词搜索 | 向量语义搜索 |
|------|-----------------|-------------|
| **搜索原理** | 关键词匹配（LIKE） | 语义相似度（Embedding） |
| **适用场景** | 精确关键词、标签查询 | 语义理解、同义词、相关概念 |
| **查询速度** | 快速 | 需要调用后端 API |
| **依赖要求** | 需要后端服务运行 | 需要后端服务运行 |
| **结果排序** | 按创建时间 | 按相似度（relevance） |
| **大小写敏感** | 是 | 否 |

---

## 决策规则

### 1. 检查用户明确指定

如果用户明确提到：
- "关键词搜索"、"精确搜索" → 使用 **SQLite 搜索**
- "语义搜索"、"相似内容"、"相关概念" → 使用 **向量搜索**

### 2. 分析查询特征

#### 使用 SQLite 搜索的情况：
- ✅ 用户提供了**精确的关键词**（如："Python"、"Claude Skills"）
- ✅ 需要**按标签筛选**（如：`tag "技术"`）
- ✅ 需要**获取特定 ID** 的记忆（如：`get 123`）
- ✅ 需要**列出最近**的记忆（如：`list --limit 10`）
- ✅ 查询意图明确，关键词清晰

#### 使用向量搜索的情况：
- ✅ 查询意图**不明确**或**模糊**（如："关于学习的内容"）
- ✅ 需要理解**同义词**（如：搜索"编程"能找到"开发"相关内容）
- ✅ 需要查找**相关概念**（如：搜索"机器学习"能找到"AI"相关内容）
- ✅ 查询是**自然语言描述**而非关键词
- ✅ 用户描述的是**概念或想法**而非具体词汇

### 3. 决策流程

```
用户查询
  ↓
是否明确指定搜索方式？
  ├─ 是 → 使用指定方式
  └─ 否 → 继续判断
      ↓
是否包含标签、ID、或"最近"等结构化查询？
  ├─ 是 → 使用 SQLite 搜索
  └─ 否 → 继续判断
      ↓
查询是精确关键词还是自然语言描述？
  ├─ 精确关键词 → SQLite 搜索
  └─ 自然语言/概念 → 向量搜索
```

---

## 使用指南

### SQLite 关键词搜索

**指南位置**: [sqlite-search/SQLITE_SEARCH_GUIDE.md](sqlite-search/SQLITE_SEARCH_GUIDE.md)

**脚本路径**: `.claude/skills/query-knowledge-base/search/sqlite-search/query_db.py`

**基本用法**:
```bash
# 搜索关键词
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "关键词"

# 按标签筛选
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "标签名"

# 列出最近
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list --limit 10

# 获取单条
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get <ID>
```

### 向量语义搜索

**指南位置**: [vector-search/VECTOR_SEARCH_GUIDE.md](vector-search/VECTOR_SEARCH_GUIDE.md)

**脚本路径**: `.claude/skills/query-knowledge-base/search/vector-search/query_vector.py`

**基本用法**:
```bash
# 语义搜索
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "查询内容" --limit 5
```

**注意**: 所有的搜索现在都需要后端服务运行在 `http://localhost:7937`。如果服务未运行，请先执行 `mymom`。

---

## 示例场景

### 场景 1: 精确关键词查询
**用户**: "查找包含 'Python' 的记忆"

**决策**: SQLite 搜索（精确关键词）

**执行**:
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Python"
```

### 场景 2: 标签筛选
**用户**: "查看所有标记为 '技术' 的内容"

**决策**: SQLite 搜索（标签查询）

**执行**:
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "技术"
```

### 场景 3: 语义查询
**用户**: "查找关于学习方法的内容"

**决策**: 向量搜索（自然语言描述，概念查询）

**执行**:
```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法" --limit 5
```

### 场景 4: 同义词搜索
**用户**: "查找编程相关的内容"

**决策**: 向量搜索（"编程"可能匹配"开发"、"代码"等相关概念）

**执行**:
```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "编程" --limit 5
```

### 场景 5: 模糊查询
**用户**: "找一些关于 AI 的东西"

**决策**: 向量搜索（查询意图不明确，自然语言描述）

**执行**:
```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "AI" --limit 5
```

---

## 快速决策表

| 查询类型 | 搜索方式 | 示例 |
|---------|---------|------|
| 精确关键词 | SQLite | "Python"、"Claude Skills" |
| 标签筛选 | SQLite | `tag "技术"` |
| 获取 ID | SQLite | `get 123` |
| 列出最近 | SQLite | `list --limit 10` |
| 自然语言描述 | 向量 | "学习方法"、"关于 AI 的内容" |
| 同义词搜索 | 向量 | "编程"（匹配"开发"、"代码"） |
| 概念查询 | 向量 | "机器学习"（匹配"AI"、"算法"） |
| 模糊查询 | 向量 | "一些有用的内容" |

---

## 注意事项

1. **后端服务检查**：在进行任何搜索前，建议确保后端服务已启动（`http://localhost:7937`）。如果无法连接，请运行 `mymom`。

2. **性能考虑**：
   - SQLite 搜索：快速，无需网络请求
   - 向量搜索：需要调用 API，速度取决于网络和后端性能

3. **结果格式**：
   - SQLite 搜索：按创建时间排序
   - 向量搜索：按相似度（relevance）排序，包含 `relevance` 字段

4. **错误处理**：
   - SQLite 搜索：数据库文件不存在时返回错误
   - 向量搜索：后端服务未启动时返回友好提示

---

## 下一步

- **SQLite 搜索详细指南**: [sqlite-search/SQLITE_SEARCH_GUIDE.md](sqlite-search/SQLITE_SEARCH_GUIDE.md)
- **向量搜索详细指南**: [vector-search/VECTOR_SEARCH_GUIDE.md](vector-search/VECTOR_SEARCH_GUIDE.md)
- **SQLite 搜索示例**: [sqlite-search/EXAMPLES.md](sqlite-search/EXAMPLES.md)
- **向量搜索示例**: [vector-search/EXAMPLES.md](vector-search/EXAMPLES.md)
