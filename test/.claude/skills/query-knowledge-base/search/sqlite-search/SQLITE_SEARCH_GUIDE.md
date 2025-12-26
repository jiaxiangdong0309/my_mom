# SQLite 关键词搜索指南

本指南详细说明如何使用 `query_db.py` 脚本进行 SQLite 关键词搜索。

---

## 脚本位置

脚本路径：`.claude/skills/query-knowledge-base/search/sqlite-search/query_db.py`

## 执行方式

**从项目根目录执行**（推荐）：
```bash
# 从项目根目录执行
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list
```

**或者先切换到脚本目录**：
```bash
cd .claude/skills/query-knowledge-base/search/sqlite-search
python3 query_db.py list
```

---

## 核心功能概览

`query_db.py` 提供以下查询方式：

1. **list** - 列出最近的记忆
2. **search** - 按关键词搜索
3. **tag** - 按标签筛选
4. **get** - 获取单条记忆详情

---

## 1. 列出最近的记忆

### 基本用法
```bash
# 从项目根目录执行
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list
```

默认返回最近 10 条记忆的简要信息（ID、标题、标签）。

### 限制数量
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list --limit 20
```

返回最近 20 条记忆。

### 使用场景
- 浏览最近添加的内容
- 快速查看知识库概况
- 找到特定记忆的 ID 以便查看详情

---

## 2. 按关键词搜索

### 基本用法
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "关键词"
```

在**标题**和**内容**中搜索包含指定关键词的记忆。

### 搜索技巧

#### 使用精确词汇
```bash
# 搜索 "Skills" 相关内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Skills"

# 搜索 "Python" 相关内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Python"
```

#### 使用中文搜索
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "技能"
```

#### 组合关键词
```bash
# 搜索包含 "Claude" 和 "Skills" 的内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Claude Skills"
```

### 返回结果
- 包含关键词的所有记忆
- 显示完整的内容字段
- 按创建时间倒序排列（最新的在前）

---

## 3. 按标签筛选

### 基本用法
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "标签名"
```

筛选带有特定标签的所有记忆。

### 常用标签示例
```bash
# 查看所有技术相关内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "技术"

# 查看所有开发相关内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "开发"

# 查看所有文档相关内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "文档"
```

### 多标签组合
当前版本每次只能筛选一个标签。如需多标签筛选，可以：
```bash
# 先获取一个标签的结果，再用 grep 过滤
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "Claude" | grep "Skills"
```

---

## 4. 获取单条记忆详情

### 基本用法
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get <ID>
```

### 示例
```bash
# 获取 ID 为 6 的记忆
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get 6
```

### 返回完整信息
- id - 记忆 ID
- title - 标题
- content - 完整内容
- tags - 标签列表
- created_at - 创建时间

---

## 输出格式

所有命令返回 **JSON 格式**，便于：

### 在终端查看
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list | python3 -m json.tool
```

### 用 jq 美化
```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Skills" | jq '.'
```

### 提取特定字段
```bash
# 只看标题
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list | jq -r '.[].title'

# 只看 ID 和标题
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list | jq '.[] | {id, title}'
```

---

## 常见使用场景

### 场景 1: 查找之前保存的文档
```bash
# 1. 先搜索关键词
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Skills"

# 2. 找到 ID 后查看完整内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get 6
```

### 场景 2: 浏览特定主题
```bash
# 按标签筛选
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "Claude"
```

### 场景 3: 检查最新添加的内容
```bash
# 列出最近 5 条
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list --limit 5
```

---

## 注意事项

1. **必须使用 `python3` 命令**
   - ❌ `python scripts/query_db.py ...` (可能不兼容)
   - ✅ `python3 scripts/query_db.py ...` (正确)

2. **搜索是大小写敏感的**
   - 搜索 "skills" 和 "Skills" 结果可能不同

3. **服务依赖**
   - 本脚本现在通过 API 访问数据。
   - 必须确保后端服务已启动（默认：`http://localhost:7937`）。
   - 如果服务未运行，请先执行：`mymom`。

4. **无结果的处理**
   - 搜索无结果时返回空列表 `[]`
   - ID 不存在时返回 JSON 格式的错误信息：
     ```json
     {
       "error": true,
       "message": "No memory found with ID: <ID>"
     }
     ```
   - 所有错误信息都使用统一的 JSON 格式，便于程序处理

5. **内容提取指南**
   - 当从对话上下文提取搜索关键词时：
     - 提取用户明确提到的关键词或短语
     - 如果用户提到"查找"、"搜索"、"找"等动词，提取其后的名词或短语
     - 如果用户提到标签，使用 `tag` 命令而非 `search` 命令
     - 如果用户提到 ID 或"第X条"，使用 `get` 命令
     - 如果用户只是说"看看最近的内容"或"列出"，使用 `list` 命令

---

## SQLite 搜索的特点

### 适用场景
- ✅ **精确关键词匹配**：用户明确知道要搜索的关键词
- ✅ **标签查询**：需要按标签筛选记忆
- ✅ **快速查找**：需要快速定位包含特定词汇的内容
- ✅ **结构化查询**：需要按 ID 获取、按时间排序等

### 搜索方式
- 使用 SQL `LIKE` 操作符进行模糊匹配
- 在 `title` 和 `content` 字段中搜索
- 大小写敏感

### 与向量搜索的区别
- SQLite 搜索：基于关键词匹配，需要精确或部分匹配
- 向量搜索：基于语义相似度，可以理解同义词和相关概念

---

## 快速参考

**执行前提**：从项目根目录执行，或使用完整路径

| 操作 | 命令 |
|------|------|
| 列出最近 10 条 | `python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list` |
| 列出最近 N 条 | `python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py list --limit N` |
| 搜索关键词 | `python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "关键词"` |
| 按标签筛选 | `python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py tag "标签名"` |
| 获取单条详情 | `python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get <ID>` |

---

## API 参数参考

### 全局参数
- `--db`: 指定数据库文件路径（默认：`backend/data/memories.db`）

### 子命令参数

#### `list` - 列出记忆
列出所有记忆，按创建时间倒序排列。
- `--limit`: (可选) 限制返回的结果数量，默认 10

#### `search` - 搜索关键词
在 `title` 和 `content` 字段中进行模糊搜索。
- `keyword`: (必填) 搜索词，支持中文和英文
- `--limit`: (可选) 限制返回的结果数量

#### `tag` - 按标签筛选
筛选包含指定标签的记忆。
- `tag`: (必填) 标签名称
- `--limit`: (可选) 限制返回的结果数量

#### `get` - 获取单条详情
获取指定 ID 的记忆完整信息。
- `id`: (必填) 记忆的 ID（数字）

---

## 下一步

- **使用示例**: 查看 [EXAMPLES.md](EXAMPLES.md) 了解复杂查询示例
- **向量搜索**: 如需语义搜索，查看 [../vector-search/VECTOR_SEARCH_GUIDE.md](../vector-search/VECTOR_SEARCH_GUIDE.md)
- **添加记忆**: 查看 [../../add/ADD_GUIDE.md](../../add/ADD_GUIDE.md) 了解如何添加新记忆

