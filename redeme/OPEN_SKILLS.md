# OpenSkills：让 Claude Code 的 Skills 体系"跨代理通用"的 CLI

**项目**：numman-ali/openskills
**GitHub**：https://github.com/numman-ali/openskills
**npm**：openskills（`npm i -g openskills`）

**定位一句话**：把 Anthropic 的 SKILL.md 技能（含 marketplace）用 CLI + AGENTS.md 以注册表方式暴露给所有 AI 编码代理（Claude Code / Cursor / Windsurf / Aider 等）。

## 1. OpenSkills 解决了什么问题

### 1.1 你原本会遇到的痛点

- **技能生态被工具锁死**：Claude Code 的 skills 系统很强，但其他代理（Cursor/Windsurf/Aider）默认用不了同一套技能。
- **跨工具重复劳动**：同一个工作流（如 PDF/Excel/Docx 处理、代码审计、写作模板）要在不同工具里反复"再实现一次"。
- **缺一个"统一的技能注册表"**：代理需要一个可读、可解析的技能清单来做语义匹配与按需加载。

### 1.2 OpenSkills 的核心解法

OpenSkills 用两个关键约定把问题做成"可移植的工程能力"：

- **SKILL.md 仍然保持 Anthropic 规范**：技能就是带 YAML frontmatter 的 Markdown 指令 + 可选资源目录（`references/`, `scripts/`, `assets/`）。
- **把技能"登记"到 AGENTS.md**：生成与 Claude Code 同构的 `<available_skills>` XML 列表，让任何代理都能读到"有哪些技能、分别做什么"。

代理真正需要用某个技能时，再通过 `Bash("openskills read <skill-name>")` 按需加载该技能内容（渐进式披露，避免上下文污染）。

## 2. 如何使用（最短落地路径）

### 2.1 前置条件

- **Node.js**：20.6+（项目说明中提到的要求）
- **Git**：用于从 GitHub 拉取技能仓库
- **AGENTS.md**：sync 会更新该文件（通常建议项目里预先存在）

### 2.2 安装 CLI

```bash
npm i -g openskills
```

### 2.3 安装技能（从 Anthropic marketplace 或任意 GitHub 仓库）

```bash
# 从 Anthropic skills 仓库安装（默认交互式选择）
openskills install anthropics/skills

# 也可以从任意 GitHub 仓库安装
openskills install your-org/custom-skills
```

**常用参数**：

- `--global`：安装到全局目录（跨项目共享）
- `--universal`：安装到 `.agent/skills/`（多代理共享一个 AGENTS.md 时更友好，避免与 Claude Code 原生 `.claude/` 产生重复/冲突）
- `-y, --yes`：跳过交互（脚本/CI 用）

### 2.4 同步到 AGENTS.md（这是"让代理发现技能"的关键一步）

```bash
openskills sync
```

**可选**：

```bash
# 输出到自定义文件路径（不存在会自动创建）
openskills sync -o .ruler/AGENTS.md

# 非交互式
openskills sync -y
```

### 2.5 在代理里使用（按需加载技能）

当代理读取到 AGENTS.md 的 `<available_skills>` 后，遇到任务会做语义匹配；匹配到某个技能时执行：

```bash
openskills read <skill-name>
```

**例如**：

```bash
openskills read pdf
openskills read xlsx
```

### 2.6 其他常用命令

```bash
openskills list          # 列出已安装技能
openskills manage        # 交互式管理（安全默认不勾选）
openskills remove <name> # 移除指定技能
```

## 3. 如何实现的（核心机制与数据流）

### 3.1 三个"角色"与三份"关键资产"

- **Agent（使用方）**：读 AGENTS.md，决定要不要加载某个技能；真正加载时调用 `openskills read`。
- **OpenSkills CLI（承载方）**：负责安装 / 同步 / 读取技能内容。
- **Skills Repo / File System（技能存储）**：技能以文件夹形式存在，核心文件是 SKILL.md，可附带资源目录。

### 3.2 文件/目录约定

技能目录（单个技能）通常长这样：

```
<skill-name>/
  SKILL.md
  references/   # 可选：文档
  scripts/      # 可选：脚本
  assets/       # 可选：模板/配置
```

OpenSkills 支持多位置安装，并按优先级查找（同名只取最高优先级）：

1. `./.agent/skills/`（项目 universal）
2. `~/.agent/skills/`（全局 universal）
3. `./.claude/skills/`（项目）
4. `~/.claude/skills/`（全局）

### 3.3 install 做了什么

`openskills install <source>` 的本质是：

- 从 GitHub（或本地路径/私有仓库）拿到技能目录
- 交互式选择要安装的技能（或用 `-y` 自动）
- 把技能写入目标 skills 目录（`.claude/skills/` 或 `.agent/skills/` 等）

### 3.4 sync 做了什么

`openskills sync` 的本质是：

- 扫描已安装技能目录
- 读取每个技能的 SKILL.md frontmatter（主要是 `name` / `description`）
- 生成（或更新）AGENTS.md 中的 `<skills_system>` / `<available_skills>` XML 段落

让"技能清单"变成一个可被不同代理统一解析的注册表。

AGENTS.md 里关键结构类似：

```xml
<available_skills>
  <skill>
    <name>pdf</name>
    <description>...</description>
    <location>project</location>
  </skill>
</available_skills>
```

### 3.5 read 做了什么（渐进式披露的落点）

`openskills read <name>` 的本质是：

- 按上述优先级定位技能目录
- 输出技能 SKILL.md 内容（并提供 base directory，便于技能指令引用同目录下的 `references/`、`scripts/`、`assets/`）

### 3.6 端到端数据流（最核心的一张图）

（待补充流程图）

## 4. 资源与参考

- **OpenSkills GitHub**：https://github.com/numman-ali/openskills
- **npm 包**：https://www.npmjs.com/package/openskills
- **Anthropic skills（市场技能仓库）**：https://github.com/anthropics/skills
- **Anthropic 官方**：Agent Skills 规范与背景：https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
