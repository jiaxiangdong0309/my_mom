---
name: /openspec-apply
description: 实施已批准的 OpenSpec 变更
---

请按照以下步骤实施 OpenSpec 变更：

**护栏**
- 优先采用直接、最小化的实现，仅在请求或明确需要时添加复杂性
- 将变更紧密限制在请求的结果范围内
- 如果需要额外的 OpenSpec 约定或澄清，请参考 `openspec/AGENTS.md`

**步骤**
将这些步骤作为待办事项跟踪，逐一完成：
1. 阅读 `changes/<id>/proposal.md`、`design.md`（如果存在）和 `tasks.md` 以确认范围和验收标准
2. 按顺序处理任务，保持编辑最小化并专注于请求的变更
3. 在更新状态之前确认完成 - 确保 `tasks.md` 中的每个项目都已完成
4. 在所有工作完成后更新清单，将每个任务标记为 `- [x]`
5. 当需要额外上下文时，参考 `openspec list` 或 `openspec show <item>`

**参考**
- 使用 `openspec show <id> --json --deltas-only` 查看提案的额外上下文
