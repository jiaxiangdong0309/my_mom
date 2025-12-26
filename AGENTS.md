# AI 编程助手指南


## 核心规则（必须永远执行）

1. **禁止启动服务** - 永远不要执行 `python3 main.py`、`npm run dev` 等启动命令。提示用户手动运行。

2. **准确理解意图** - 区分请求类型（简单问答/修复bug/实现方案/研究知识点/写需求），按需回答。简单问题直接回答，不要过度展开项目相关内容。

3. **充分调研再行动** - 写代码或回答前，先深度理解上下文（阅读相关文件、搜索代码库、理解影响范围），避免引入新bug或给出不合适的方案。

## 项目概述

本地知识记忆库：SQLite + ChromaDB 双库存储，FastAPI 后端 + React 前端。

## 开发准则

### 架构原则
- **无抽象层**：直接实现，不创建抽象基类
- **直接实例化**：不使用依赖注入
- **够用即可**：不预留过度扩展点

### 代码风格
- **Python**: 类型提示、PEP 8、snake_case、docstring
- **TypeScript**: ES6+、PascalCase 组件、camelCase 函数/变量

### 项目结构
```
backend/
  ├── api/        # 路由层
  ├── core/       # SQLite、ChromaDB、Embedding 封装
  └── utils/      # 工具函数
frontend/src/
  ├── api/        # API 调用
  └── components/ # React 组件
data/             # 本地存储（自动创建）
```

## 重要约束

1. **本地优先**：数据不上云
2. **极简架构**：避免过度设计
3. **单用户场景**：当前版本面向单用户
4. **不自动运行服务**：提示用户手动启动

## 技术栈

- **后端**: Python 3.11+、FastAPI、SQLite、ChromaDB、sentence-transformers
- **前端**: React 18、TypeScript 5、Vite 5

---

<!-- OPENSPEC:START -->
# OpenSpec 使用说明

当请求出现以下情况时，始终打开 `@/openspec/AGENTS.md`：
- 提及规划或提案（proposal、spec、change、plan 等）
- 引入新功能、破坏性变更、架构转变或大型性能/安全工作
- 听起来不明确，在编码之前需要权威规范

保留此托管块，以便 'openspec update' 可以刷新说明。

<!-- OPENSPEC:END -->
