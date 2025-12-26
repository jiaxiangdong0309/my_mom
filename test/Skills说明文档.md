# Anthropic Skills 说明文档

## 概述

Skills 是模块化能力包，通过目录结构组织指令、脚本和资源来扩展 Claude 的功能。

**核心特点**：
- **模型自动调用**：Claude 根据 `description` 自动决定何时使用（无需手动触发）
- **渐进式加载**：按需读取文件，节省 token
- **Git 可共享**：项目技能可通过团队协作共享

---

## 目录结构

### 项目技能（推荐）

```
.claude/skills/
└── your-skill-name/
    ├── SKILL.md          # 必需：主指令文件
    ├── FORMS.md          # 可选：表单处理指南
    ├── REFERENCE.md      # 可选：API 参考文档
    ├── EXAMPLES.md       # 可选：使用示例
    └── scripts/          # 可选：可执行脚本
        ├── helper.py
        └── validate.py
```

**位置**：项目根目录下的 `.claude/skills/`
**用途**：团队协作、项目特定需求
**特点**：可通过 Git 共享

### 个人技能

```
~/.claude/skills/
└── your-skill-name/
    └── SKILL.md
```

**位置**：用户主目录下的 `~/.claude/skills/`
**用途**：个人工作流、实验性技能

---

## SKILL.md 核心格式

### 最小示例

```yaml
---
name: your-skill-name
description: 具体描述技能功能和使用场景，包含关键词
---

# 技能标题

## 指令内容
提供清晰的步骤指导...
```

### 完整示例

```yaml
---
name: pdf-processing
description: 从PDF提取文本和表格，填写表单，合并文档。处理PDF文件、表单或文档提取时使用。
allowed-tools: Read, Grep, Glob, Bash
---

# PDF 处理

## 快速开始

提取文本：
```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能
- 表单填写：见 [FORMS.md](FORMS.md)
- API 参考：见 [REFERENCE.md](REFERENCE.md)
- 使用示例：见 [EXAMPLES.md](EXAMPLES.md)
```

---

## YAML Frontmatter 字段说明

### 必需字段

| 字段 | 说明 | 限制 |
|------|------|------|
| `name` | 技能名称 | 最多64字符，只能用小写字母、数字、连字符 |
| `description` | 技能描述 | 最多1024字符，**最重要字段** |

### 可选字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `allowed-tools` | 限制可用工具 | `Read, Grep, Glob` |

---

## 关键要点

### 1. description 是核心

**好的描述**（具体、包含关键词）：
```yaml
description: 分析Excel表格，创建数据透视表，生成图表。用于处理Excel文件、电子表格或.xlsx格式的数据分析。
```

**差的描述**（模糊）：
```yaml
description: 帮助处理文档
```

**原则**：
- 包含技能做什么
- 包含何时使用
- 包含关键触发词

### 2. 渐进式披露

Claude 按需读取文件，不一次性加载所有内容：

```
SKILL.md (被触发时读取)
  ├── 引用 FORMS.md (需要时读取)
  ├── 引用 REFERENCE.md (需要时读取)
  └── 引用 EXAMPLES.md (需要时读取)
```

**原则**：
- SKILL.md 保持简洁（<500行）
- 详细内容放单独文件
- 避免深层嵌套

### 3. 命名规范

推荐使用**动名词形式**（verb + -ing）：
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`

避免：
- 模糊名称：`helper`, `utils`, `tools`
- 保留字：`anthropic-helper`, `claude-tools`

### 4. 避免深层嵌套

**正确**（一层引用）：
```
SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
└── FORMS.md
```

**错误**（多层嵌套）：
```
SKILL.md
└── advanced.md
    └── details.md
```

---

## 工作原理

1. **自动发现**：Claude 扫描 `.claude/skills/*/SKILL.md`
2. **元数据预加载**：启动时加载所有 Skills 的 `name` 和 `description`
3. **智能触发**：根据用户请求和 `description` 匹配，自动选择相关 Skill
4. **按需加载**：只读取 SKILL.md，其他文件按需读取
5. **脚本执行**：scripts/ 中的脚本可直接执行，不占用上下文

---

## 技能示例

### 简单技能（单文件）

```
commit-helper/
└── SKILL.md
```

```yaml
---
name: generating-commit-messages
description: 从git diff生成清晰的提交信息。写提交信息或审查暂存更改时使用。
---

# 生成提交信息

## 流程
1. 运行 `git diff --staged` 查看更改
2. 生成包含以下内容的提交信息：
   - 50字符以内的摘要
   - 详细描述
   - 受影响的组件

## 最佳实践
- 使用现在时态
- 说明做什么和为什么，而不是怎么做
```

### 复杂技能（多文件）

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
├── EXAMPLES.md
└── scripts/
    ├── analyze_form.py
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**：
```yaml
---
name: pdf-processing
description: 提取文本、填写表单、合并PDF。处理PDF文件、表单或文档提取时使用。需要pypdf和pdfplumber包。
---

# PDF 处理

## 快速开始

提取文本：
```python
import pdfplumber

with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 功能模块
- **表单填写**：见 [FORMS.md](FORMS.md)
- **API 参考**：见 [REFERENCE.md](REFERENCE.md)
- **使用示例**：见 [EXAMPLES.md](EXAMPLES.md)

## 依赖安装
```bash
pip install pypdf pdfplumber
```
```

---

## 最佳实践

### 1. 保持专注

每个技能专注一个能力：

**好的分离**：
- "PDF 表单填写"
- "Excel 数据分析"
- "Git 提交信息"

**太宽泛**：
- "文档处理" → 应拆分为多个技能

### 2. 使用工作流和检查清单

对于复杂任务，提供可复制的检查清单：

```markdown
## PDF 表单填写流程

复制此检查清单：
```
任务进度：
- [ ] 步骤1：分析表单
- [ ] 步骤2：创建字段映射
- [ ] 步骤3：验证映射
- [ ] 步骤4：填写表单
- [ ] 步骤5：验证输出
```

**步骤1：分析表单**
运行：`python scripts/analyze_form.py input.pdf`

**步骤2：创建字段映射**
编辑 `fields.json` 添加字段值

...（以此类推）
```

### 3. 实现反馈循环

```markdown
## 文档编辑流程

1. 编辑 word/document.xml
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果验证失败 → 修复 → 再次验证
4. **只有在验证通过后才继续**
5. 重新打包文档
```

### 4. 提供具体示例

```markdown
## 提交信息格式

参考以下示例：

**示例1**：
输入：添加JWT用户认证
输出：
```
feat(auth): 实现基于JWT的认证

添加登录端点和令牌验证中间件
```

**示例2**：
输入：修复报告中日期显示错误
输出：
```
fix(reports): 修正时区转换中的日期格式

在整个报告生成中统一使用UTC时间戳
```
```

---

## 常见问题

### Q: Claude 不使用我的 Skill？

**检查清单**：
1. ✅ `description` 是否具体？包含关键词？
2. ✅ YAML 语法是否正确？
3. ✅ 文件是否在正确位置？`.claude/skills/skill-name/SKILL.md`
4. ✅ 文件是否存在？`ls .claude/skills/*/SKILL.md`

### Q: YAML 语法错误？

**检查要点**：
- 开头和结尾都有 `---`
- 不使用制表符，只用空格
- 字段名正确缩进

### Q: 如何调试？

```bash
# 查看所有技能
ls .claude/skills/

# 查看特定技能
cat .claude/skills/my-skill/SKILL.md

# 检查 YAML 语法
cat .claude/skills/my-skill/SKILL.md | head -n 10
```

---

## 资料来源

- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Skill authoring best practices - Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Equipping agents for the real world with Agent Skills - Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [anthropics/skills GitHub Repository](https://github.com/anthropics/skills)

---

## 快速开始

创建你的第一个 Skill：

```bash
# 1. 创建技能目录
mkdir -p .claude/skills/my-first-skill

# 2. 创建 SKILL.md
code .claude/skills/my-first-skill/SKILL.md

# 3. 测试技能
# 问 Claude: "你能帮我处理 X 吗？"
```
