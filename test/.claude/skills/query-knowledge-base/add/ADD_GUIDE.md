# 知识库添加指南

本指南说明如何使用 `add_db.py` 脚本向知识库添加新记忆。

## 脚本位置

脚本路径：`.claude/skills/query-knowledge-base/add/add_db.py`

**执行方式**：使用完整路径执行脚本。

**前置条件**：
- 后端服务必须已启动（运行 `mymom`）
- 需要安装 `requests` 库（`pip install requests`）

## 内容提取指南

当需要存储记忆时，AI 需要自行提取以下信息：

- **`title`**: 从对话或内容中提取简洁、描述性的标题（建议 10-30 字）
- **`content`**: 建议提取完整的相关内容（包括上下文、代码、说明等）
- **`tags`**: 从内容中提取关键词作为标签（建议 2-5 个，涵盖技术栈、主题、类型等）
  - **参考规范**: 为了保持数据的一致性和可搜索性，请优先参考 `frontend_tags.json` 中的推荐标签。

## 核心原则

1. **统一使用命令替换方式**：无论内容长短，都使用 `CONTENT=$(cat <<'EOF')` 方式传递内容，避免 Shell 解析错误。
2. **通过 API 存储**：脚本通过 HTTP API 调用后端服务，会自动同时存储到 SQLite 数据库和向量数据库（ChromaDB），确保数据一致性。

## 基本模板

```bash
CONTENT=$(cat <<'EOF')
# 这里是完整的多行内容
可以包含:
- 多行文本
- 代码块
- 特殊字符
- 中文标点
- 任何格式
EOF
)

python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "标题" \
  --content "$CONTENT" \
  --tags 标签1 标签2
```

## 关键点说明

1. **`$(cat <<'EOF')`** - 将 heredoc 内容捕获到变量
2. **`'EOF'`** (单引号) - 防止变量展开和特殊字符转义
3. **`"$CONTENT"`** (双引号) - 保留换行符和所有格式
4. **反斜杠 `\`** - 用于长命令换行，提高可读性

## 示例

### 示例 1: Markdown 文档

```bash
CONTENT=$(cat <<'EOF'
# Python 装饰器学习笔记

## 基本概念

装饰器是修改其他函数功能的函数。

## 示例代码

```python
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

## 使用场景
- 日志记录
- 性能测试
- 权限验证
EOF
)

python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "Python 装饰器学习笔记" \
  --content "$CONTENT" \
  --tags Python 学习 编程
```

### 示例 2: 包含特殊字符的配置文档

```bash
CONTENT=$(cat <<'EOF'
# Nginx 配置说明

## 基本配置

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
```

注意：配置中的 `$host` 变量会被正确保留。
EOF
)

python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "Nginx 配置说明" \
  --content "$CONTENT" \
  --tags Nginx 配置 服务器
```

## 命令参数说明

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--title` | 记忆标题 | `--title "Python 学习笔记"` |
| `--content` | 记忆内容 | `--content "$CONTENT"` |

### 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--tags` | 标签列表（空格分隔） | `--tags Python 学习 编程` |
| `--api-url` | API 接口地址（可选，默认：`http://localhost:7937/api/v1/memories/`） | `--api-url http://localhost:7937/api/v1/memories/` |

## 数据结构说明

### 存储字段

| 字段 | 类型 | 说明 | 是否必需 |
|------|------|------|---------|
| `id` | INTEGER | 主键，自动生成 | 自动 |
| `title` | TEXT | 记忆标题 | 必需 |
| `content` | TEXT | 记忆内容（支持多行、Markdown） | 必需 |
| `tags` | TEXT | 标签数组（JSON格式），如 `["Python", "学习"]` | 可选（默认空数组） |
| `created_at` | TIMESTAMP | 创建时间，自动生成 | 自动 |

### 返回格式

成功添加后返回 JSON：

```json
{
  "success": true,
  "message": "Memory added successfully with ID: 6 (stored in both SQLite and vector database)",
  "id": 6
}
```

**注意**:
- `tags` 在数据库中存储为 JSON 数组字符串，命令行参数使用空格分隔，脚本会自动转换为 JSON 格式
- 脚本通过 API 接口存储数据，会自动同时存储到 SQLite 数据库和向量数据库（ChromaDB）
- 使用前请确保后端服务已启动（运行 `mymom`），否则会提示连接错误

## 常见问题

### Q: 如何处理包含单引号、双引号、$ 变量等特殊字符的内容？

**方法**: 使用 `'EOF'` 单引号包裹，heredoc 内的所有特殊字符都会被正确处理：

```bash
CONTENT=$(cat <<'EOF')
这里可以使用 "双引号" 和 '单引号'
甚至可以使用 $变量 和 `命令`
EOF
)
```

### Q: 标签是必需的吗？

**不是**。`--tags` 参数是可选的：

```bash
# 不添加标签
python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "标题" \
  --content "$CONTENT"

# 添加多个标签
python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "标题" \
  --content "$CONTENT" \
  --tags 标签1 标签2 标签3
```

### Q: 提示"无法连接到 API 服务器"怎么办？

**原因**: 后端服务未启动。

**解决方法**:
1. 确保后端服务已启动（运行 `mymom`）
2. 检查 API 地址是否正确（默认：`http://localhost:7937/api/v1/memories/`）
3. 如果后端运行在其他端口，使用 `--api-url` 参数指定正确的地址

### Q: 提示"需要安装 requests 库"怎么办？

**解决方法**: 运行 `pip install requests` 安装依赖库。

### Q: 数据存储到哪里了？

**说明**: 脚本通过 API 接口存储，数据会同时保存到：
- **SQLite 数据库**：`backend/data/memories.db`（存储完整记录）
- **向量数据库（ChromaDB）**：`backend/data/chroma/`（存储向量索引，用于语义搜索）

这样可以同时支持精确查询和语义搜索。

## 输出格式

成功添加后会返回 JSON 格式结果：

```json
{
  "success": true,
  "message": "Memory added successfully with ID: 6 (stored in both SQLite and vector database)",
  "id": 6
}
```

失败时返回格式：

```json
{
  "success": false,
  "message": "Connection failed",
  "error": "无法连接到 API 服务器: http://localhost:7937/api/v1/memories/\n请确保 Mymom 服务已启动（运行命令: mymom）"
}
```

## 快速参考

| 场景 | 方法 |
|------|------|
| 所有内容 | 统一使用命令替换 `CONTENT=$(cat <<'EOF')` |
| 代码块/特殊字符 | 使用 `'EOF'` 单引号包裹 |
| 无标签 | 省略 `--tags` 参数 |
| 后端服务 | 使用前确保后端已启动（`mymom`） |
| 自定义 API 地址 | 使用 `--api-url` 参数指定 |
