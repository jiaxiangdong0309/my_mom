---
name: /openspec-archive
description: 归档已部署的 OpenSpec 变更并更新规范
---

请按照以下步骤归档 OpenSpec 变更：

**护栏**
- 优先采用直接、最小化的实现，仅在请求或明确需要时添加复杂性
- 将变更紧密限制在请求的结果范围内
- 如果需要额外的 OpenSpec 约定或澄清，请参考 `openspec/AGENTS.md`

**步骤**
1. 确定要归档的变更 ID：
   - 如果对话中提到了特定变更，运行 `openspec list` 确认
   - 如果不确定，运行 `openspec list` 并询问用户要归档哪个变更
2. 运行 `openspec list` 或 `openspec show <id>` 验证变更 ID
3. 运行 `openspec archive <id> --yes` 进行归档（仅对工具类变更使用 `--skip-specs`）
4. 审查命令输出，确认规范已更新，变更已移动到 `changes/archive/`
5. 运行 `openspec validate --strict` 验证归档结果

**参考**
- 使用 `openspec list` 确认变更 ID
- 使用 `openspec list --specs` 检查刷新后的规范
