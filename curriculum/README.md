# AI Agent 工程师学习路线
> 为有 5 年前端经验的开发者设计，JS/TS → Python → Agent 开发

---

## 学习路径总览

```
Phase 0 (2周)
Python 核心 for JS Devs
↓
Phase 1 (2周)
Tool Agent
↓
Phase 2 (2周)
ReAct Agent
↓
Phase 3 (2周)
Plan-Execute Agent
↓
Phase 4 (2周)
RAG Agent
↓
Phase 5 (3周)
Multi-Agent System
```

---

## 文件夹结构

```
curriculum/
├── README.md                    ← 你在这里
├── learner_profile.md           ← 你的学习档案
│
├── phase-0-python-basics/
│   ├── 01-python-for-js-devs.md       ← Python 语法 vs JS 对比
│   ├── 02-pydantic-and-types.md       ← 类型系统 & Pydantic
│   ├── 03-async-python.md             ← asyncio & async/await
│   └── 04-tooling-uv-venv.md          ← 包管理 & 项目工具链
│
├── phase-1-tool-agent/
│   ├── 01-agent-basics.md             ← LLM + Tool = Agent
│   ├── 02-first-agent.md              ← 实现第一个 Agent
│   └── 03-github-repo-analyzer.md     ← 项目：GitHub Repo 分析器
│
├── phase-2-react-agent/
│   ├── 01-react-pattern.md            ← Thought-Action-Observation
│   ├── 02-agent-loop.md               ← 实现 ReAct loop
│   ├── 03-tool-registry.md            ← Tool 注册系统
│   └── 04-research-agent.md           ← 项目：Research Agent
│
├── phase-3-plan-execute/
│   ├── 01-task-decomposition.md       ← 任务拆解思维
│   ├── 02-planner-agent.md            ← Planner 实现
│   ├── 03-executor-agent.md           ← Executor 实现
│   └── 04-research-workflow.md        ← 项目：Research Report Agent
│
├── phase-4-rag-agent/
│   ├── 01-embeddings.md               ← 向量嵌入原理
│   ├── 02-vector-db.md                ← 向量数据库
│   ├── 03-retrieval-pipeline.md       ← 检索管道
│   └── 04-codebase-qa-agent.md        ← 项目：Codebase QA Agent
│
└── phase-5-multi-agent/
    ├── 01-multi-agent-architecture.md ← 多 Agent 架构
    ├── 02-agent-communication.md      ← Agent 间通信
    ├── 03-orchestration.md            ← 编排器设计
    └── 04-ai-dev-team.md              ← 项目：AI Developer Team
```

---

## 每个 Phase 的交付物

| Phase | 核心概念 | 最终项目 |
|-------|---------|---------|
| 0 | Python 基础 | 能读写 Python，配置好开发环境 |
| 1 | Tool Calling | GitHub Repo 分析 Agent |
| 2 | ReAct Loop | Research Agent |
| 3 | Plan & Execute | Research Report 生成器 |
| 4 | RAG | Codebase QA Assistant |
| 5 | Multi-Agent | AI Developer Team |

---

## 使用这套教程的方式

1. **顺序学习**：不要跳过 Phase 0，Python 基础会直接影响后面的理解
2. **动手实践**：每个 tutorial 末尾有 Practice，必须亲手写代码
3. **记录问题**：在每个文件的 Q&A 章节追加你的问题
4. **遇到卡点**：把你的代码和报错直接发给 Claude Code，说"我在学 [阶段]，遇到这个问题"

---

## 开始之前

先看 [learner_profile.md](./learner_profile.md)，确认你的背景信息正确。

然后从 [phase-0-python-basics/01-python-for-js-devs.md](./phase-0-python-basics/01-python-for-js-devs.md) 开始。
