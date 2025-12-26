# 使用示例

**执行前提**：从项目根目录执行以下命令

## 场景 1：查找最近的学习笔记
如果你想看看最近保存了哪些关于 "Python" 的笔记：

```bash
python3 .claude/skills/query-knowledge-base/search/query_db.py search "Python" --limit 5
```

## 场景 2：按标签聚合信息
如果你想查找所有标记为 "待办" 的任务：

```bash
python3 .claude/skills/query-knowledge-base/search/query_db.py tag "待办"
```

## 场景 3：验证特定 ID 的数据
当你从搜索结果中拿到 ID，想看完整原文时：

```bash
python3 .claude/skills/query-knowledge-base/search/query_db.py get 123
```

## 场景 4：组合使用（逻辑处理）
你可以先搜索，然后根据返回的 JSON 进行进一步分析。例如，统计某个关键词在不同记忆中的出现频率等。

## 场景 5：处理错误情况
当 ID 不存在时，脚本会返回 JSON 格式的错误信息：

```bash
python3 .claude/skills/query-knowledge-base/search/query_db.py get 99999
```

输出示例：
```json
{
  "error": true,
  "message": "No memory found with ID: 99999"
}
```

