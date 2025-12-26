---
name: /openspec-proposal
description: 创建新的 OpenSpec 变更提案并进行严格验证
---

请按照以下步骤创建 OpenSpec 变更提案：

**护栏**
- 优先采用直接、最小化的实现，仅在请求或明确需要时添加复杂性
- 将变更紧密限制在请求的结果范围内
- 如果需要额外的 OpenSpec 约定或澄清，请参考 `openspec/AGENTS.md`
- 识别任何模糊或不明确的细节，在编辑文件之前询问必要的后续问题
- 在提案阶段不要编写任何代码。仅创建设计文档（proposal.md、tasks.md、design.md 和规范增量）

**步骤**
1. 审查 `openspec/project.md`，运行 `openspec list` 和 `openspec list --specs`，检查相关代码或文档以将提案基于当前行为
2. 选择一个唯一的动词开头的 `change-id`（使用 kebab-case，如 add-xxx、update-xxx）
3. 在 `openspec/changes/<id>/` 下创建以下文件：
   - `proposal.md` - 说明变更的原因、内容和影响
   - `tasks.md` - 实施任务清单
   - `design.md` - 技术决策（仅在需要时创建）
   - `specs/<capability>/spec.md` - 规范增量
4. 编写规范增量时使用 `## ADDED|MODIFIED|REMOVED Requirements` 格式
5. 每个需求至少包含一个 `#### Scenario:` 场景描述
6. 将 `tasks.md` 编写为有序的可验证工作项列表
7. 运行 `openspec validate <id> --strict` 进行验证并解决所有问题

**参考**
- 使用 `openspec show <id> --json --deltas-only` 检查详细信息
- 使用 `rg -n "Requirement:|Scenario:" openspec/specs` 搜索现有需求
- 使用 `rg <keyword>`、`ls` 或直接文件读取探索代码库
