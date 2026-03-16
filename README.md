# Agent Playground

一个为有前端经验的开发者设计的 **AI Agent 工程师学习路线**，从 Python 基础到多 Agent 系统，循序渐进。

## 背景

作者有 5 年前端开发经验（JS/TS），目标是转型 AI Agent 工程师。
本仓库记录了完整的学习课程内容和练习代码。

## 学习路线

```
Phase 0 · Python 基础（2周）
  ↓ 语法对比 / Pydantic / asyncio / uv 工具链
Phase 1 · Tool Agent（2周）
  ↓ LLM + Tool Calling + Agent Loop
  → 项目：GitHub Repo 分析 Agent
Phase 2 · ReAct Agent（2周）
  ↓ Thought → Action → Observation
  → 项目：Research Agent
Phase 3 · Plan-Execute Agent（2周）
  ↓ Planner + Executor 两阶段架构
  → 项目：Research Report 生成器
Phase 4 · RAG Agent（2周）
  ↓ Embedding + 向量数据库 + 检索管道
  → 项目：Codebase QA Assistant
Phase 5 · Multi-Agent System（3周）
  ↓ 角色设计 + Agent 通信 + Orchestrator
  → 项目：AI Developer Team
```

## 目录结构

```
agent-playground/
├── curriculum/          # 各阶段教程文档
│   ├── README.md        # 课程总览
│   ├── learner_profile.md
│   ├── phase-0-python-basics/
│   ├── phase-1-tool-agent/
│   ├── phase-2-react-agent/
│   ├── phase-3-plan-execute/
│   ├── phase-4-rag-agent/
│   └── phase-5-multi-agent/
├── practice/            # 练习题和代码实现
└── .claude/
    ├── agents/          # curriculum-mentor 导师 Agent 配置
    └── agent-memory/    # 跨会话学习进度记录
```

## 使用方式

教程文件在 `curriculum/` 下，每篇包含：

- **Why This Matters**：为什么要学这个
- **核心心智模型**：概念的本质，而不只是操作步骤
- **JS → Python 对照**：针对前端背景设计的对比说明
- **Practice**：动手练习，完成后再进入下一篇

建议按编号顺序学习，从 [`curriculum/phase-0-python-basics/01-python-for-js-devs.md`](curriculum/phase-0-python-basics/01-python-for-js-devs.md) 开始。

## 技术栈

- **语言**：Python 3.11+
- **包管理**：[uv](https://docs.astral.sh/uv/)
- **LLM**：Claude（Anthropic SDK）
- **数据验证**：Pydantic
- **HTTP 客户端**：httpx
- **向量数据库**：ChromaDB（Phase 4）
