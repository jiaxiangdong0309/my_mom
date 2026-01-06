# SQLite 关键词搜索指南

## 核心指令

**MANDATORY: 从项目根目录执行**

```bash
python3 .claude/skills/query-knowledge-base/search/sqlite-search/query_db.py "搜索词"
```

---

## 执行准则

1. **干净利索**:
   - 搜出内容：直接输出 JSON 结果。
   - 未搜出内容：直接输出"未找到匹配记忆"。
   - **禁止任何开场白、过程说明或总结性废话。**

---

## AUTHORITY: 授权声明

本文档定义的单一搜索方式是 SQLite 搜索的唯一合法途径。AI 在执行此类搜索时，必须表现得像一个精准的自动化脚本，严禁输出任何非 JSON 的解释内容。
