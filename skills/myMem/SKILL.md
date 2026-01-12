---
name: query-knowledge-base
description: 查询和管理本地知识库中的记忆内容。当需要搜索知识库、查找记忆、添加新记忆、查看已保存的信息或检索历史记录时使用。
allowed-tools: Bash, Read
---

# 知识库查询和管理

## 路径说明

**CRITICAL - 所有文件路径均为相对于 Base directory 的相对路径。**

- Base directory 由技能系统在加载时动态提供（格式：`Base directory: /path/to/.claude/skills/query-knowledge-base`）
- 解析规则：`search/SEARCH_GUIDE.md` → `{Base directory}/search/SEARCH_GUIDE.md`
- **NEVER 使用绝对路径，始终使用相对路径配合 Base directory 解析**
- 即使技能目录被移动到其他位置，只要 Base directory 正确提供，相对路径即可正常工作

---

## 场景判断（CRITICAL - 必须先执行）

**MANDATORY - 在读取任何指南文件之前，必须先判断用户意图：**

- **搜索场景**：用户需要**查找、检索、查询**已存在的记忆
  - 关键词：搜索、查找、检索、查询、找、查看、列出、获取
  - 示例："帮我找一下关于Python的记忆"、"搜索包含'AI'的内容"、"查看所有标签为'技术'的记忆"

- **添加场景**：用户需要**保存、添加、存储**新信息到知识库
  - 关键词：添加、保存、存储、记录、记住、存储到知识库
  - 示例："把这个内容保存到知识库"、"添加一条新记忆"、"记住这个信息"

**NEVER 在未明确判断场景之前读取任何指南文件。**

---

## 📋 搜索/查询记忆

当判断为**搜索场景**时：

### Workflow

1. **MANDATORY - READ ENTIRE FILE**: 完整阅读 [`search/SEARCH_GUIDE.md`](search/SEARCH_GUIDE.md) (~195 lines)
   **NEVER 在阅读此文件时设置任何范围限制。**

2. **NEVER 在需要添加记忆时读取此文档。**

---

## ➕ 添加/保存记忆

当判断为**添加场景**时：

### Workflow

1. **依赖库验证**: 确保 `requests` 已安装 (`pip install requests`)。

2. **MANDATORY - READ ENTIRE FILE**: 完整阅读 [`add/ADD_GUIDE.md`](add/ADD_GUIDE.md) (~70 lines)
   **NEVER 在阅读此文件时设置任何范围限制。**

3. **NEVER 在需要搜索记忆时读取此文档。**
