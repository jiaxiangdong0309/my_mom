# 向量搜索使用示例

**执行前提**：从项目根目录执行以下命令，确保后端服务已启动

---

## 场景 1：语义查询

查找关于学习方法的内容，即使内容中没有"学习方法"这个词：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法" --limit 5
```

**优势**：能找到学习技巧、学习笔记、学习心得等相关内容。

---

## 场景 2：同义词搜索

搜索"编程"，能找到"开发"、"代码"、"编程语言"等相关内容：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "编程" --limit 5
```

---

## 场景 3：相关概念搜索

搜索"机器学习"，能找到"AI"、"算法"、"数据科学"、"深度学习"等相关内容：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "机器学习" --limit 5
```

---

## 场景 4：自然语言查询

使用自然语言描述查询意图：

```bash
# 查找有用的内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "有用的内容" --limit 3

# 查找关于 AI 的内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "关于 AI 的内容" --limit 5
```

---

## 场景 5：查看相似度分数

提取结果中的相似度分数，了解相关性：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "Python" | jq '.[] | {title, relevance}'
```

输出示例：
```json
{
  "title": "Python 学习笔记",
  "relevance": 0.95
}
{
  "title": "编程语言对比",
  "relevance": 0.82
}
```

---

## 场景 6：处理错误情况

### 后端服务未启动

如果后端服务未启动，会返回友好的错误提示：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "测试"
```

输出示例：
```json
{
  "error": true,
  "message": "无法连接到后端服务 (http://localhost:7937)。\n请确保 Mymom 服务已启动：\n  mymom"
}
```

**解决方法**：启动后端服务
```bash
cd backend
python3 main.py
```

---

## 场景 7：组合使用

先使用向量搜索找到相关内容，再使用 SQLite 搜索获取详细信息：

```bash
# 1. 使用向量搜索找到相关记忆
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "学习方法" --limit 3

# 2. 从结果中获取 ID，使用 SQLite 搜索查看详情
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py get <ID>
```

---

## 场景 8：对比两种搜索方式

### SQLite 搜索（精确匹配）

```bash
# 只能找到包含"Python"关键词的内容
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py search "Python"
```

### 向量搜索（语义理解）

```bash
# 能找到"Python"、"编程语言"、"开发工具"等相关内容
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "Python" --limit 5
```

---

## 场景 9：提取特定字段

使用 `jq` 提取和格式化结果：

```bash
# 只看标题和相似度
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "AI" | jq '.[] | {title, relevance}'

# 只看标题（纯文本）
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "AI" | jq -r '.[].title'

# 只看高相似度的结果（relevance > 0.8）
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "AI" | jq '.[] | select(.relevance > 0.8)'
```

---

## 场景 10：指定不同的 API 地址

如果后端服务运行在其他地址：

```bash
python3 .claude/skills/query-knowledge-base/search/vector-search/query_vector.py "测试" --api-url http://localhost:8080
```

