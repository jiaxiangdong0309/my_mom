# 知识库添加指南 (CRITICAL: 存储核心)

**MANDATORY**: 当且仅当判断用户意图为“添加、保存、存储、记录”新信息到知识库时，必须遵循此指南。

## 1. 脚本路径说明

**脚本路径**: 脚本位于相对于 Base directory 的 `.claude/skills/query-knowledge-base/add/add_db.py`。

## 2. 标准原子化工作流 (MANDATORY Workflow)

**严禁跳过任何步骤：**

1.  **信息提取**:
    *   **TITLE**: 提取 10-30 字的描述性标题。
    *   **CONTENT**: 必须提取完整上下文。**NEVER** 存储残缺信息。
    *   **TAGS (CRITICAL)**:
        *   **MANDATORY**: 必须使用 `Read` 工具读取并参考 `add/frontend_tags.json`（路径相对于 Base directory）。
        *   **CRITICAL**: 优先匹配现有标签以保持一致性；若内容涉及新领域，允许自行提取高频关键词作为补充。
        *   **Requirement**: 必须包含至少 2 个标签。
2.  **变量封装**: 使用 `cat <<'EOF'` 语法封装 `$CONTENT`，防止 Shell 注入与转义错误。
3.  **脚本调用**: 使用完整 Python 命令执行，传递变量与参数。
4.  **结果验证**: 检查返回的 JSON 是否包含 `"success": true`。

## 3. 核心执行指令 (MANDATORY Syntax)

**必须使用以下语法模板，严禁使用普通的字符串参数传递。**

```bash
# STEP 1: 封装内容 (MANDATORY: 使用 'EOF' 严防转义错误)
CONTENT=$(cat <<'EOF'
# [标题]
[完整的多行内容，支持 Markdown、代码块、特殊字符]
EOF
)

# STEP 2: 执行添加 (CRITICAL: 确保路径与 Base directory 一致)
python3 .claude/skills/query-knowledge-base/add/add_db.py \
  --title "精准的标题" \
  --content "$CONTENT" \
  --tags 标签1 标签2
```

## 4. 结果反馈约束 (STRICT TERMINATION)

**严禁返回脚本输出的原始 JSON。AI 必须进入“静默反馈模式”，根据执行结果仅返回以下固定文本，严禁任何额外思考、解释或方案建议：**

*   **成功场景**: 必须且仅返回：`已经存储成功`
*   **失败场景**:
    *   **连接失败**: 若提示 `无法连接到 API 服务器`，必须立即停止任务，仅回复：`请运行 mymom start 开启服务，开启后向我发送 done 指令，我将继续完成操作`。
    *   **其他原因**: 必须且仅返回：`存储失败 原因：[具体错误描述]`

**NEVER**: 严禁在成功后输出 ID、路径、存储内容摘要或任何“已为您保存好”之类的客套话。严禁在失败后尝试分析失败原因或建议手动保存方案。

## 5. 严禁事项 (NEVER LIST)

*   **NEVER**: 严禁在脚本执行完毕后继续进行“下一步思考”或“备选方案生成”。
*   **NEVER**: 严禁在封装内容时遗漏 `cat <<'EOF'` 的单引号，否则 `$`, `` ` `` 等符号会被 Shell 解析。
*   **NEVER**: 严禁将大段代码直接作为命令行参数传递，必须通过变量 `$CONTENT` 引用。
*   **NEVER**: 严禁省略 `--tags` 参数，即使没有合适标签，也应根据内容生成技术栈标签。

## 6. 常见问题处理

| 错误表现 | 根本原因 | 强制对策 |
| :--- | :--- | :--- |
| `Connection failed` | 后端 `mymom` 未启动 | **MANDATORY**: 停止任务，要求用户运行 `mymom start` 并等待 `done` 指令。 |
| 变量 `$host` 丢失 | Heredoc 未使用 `'EOF'` | **CRITICAL**: 检查 `cat <<'EOF'` 是否包含单引号。 |
| `Permission denied` | 脚本权限问题 | 尝试 `python3 path/to/script.py` 而非直接运行。 |

---
**AUTHORITY**: 此文档为 `query-knowledge-base` 技能的存储操作终极指南，效力高于任何通用建议。
