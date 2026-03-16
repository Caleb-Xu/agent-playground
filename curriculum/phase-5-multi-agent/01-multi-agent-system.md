---
topic: Multi-Agent System
concepts: [多Agent架构, Agent通信, Orchestrator, 角色设计, AI Dev Team]
prerequisites: [phase-4-rag-agent/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Multi-Agent System：AI Developer Team

## Why This Matters

单个 Agent 擅长单一任务，但复杂的软件开发需要：
- 产品理解（PM）
- 架构设计（Architect）
- 代码实现（Developer）
- 质量审查（Reviewer）

Multi-Agent 让不同角色的专业 Agent 协作完成复杂任务。

---

## 核心心智模型

```
单 Agent：一个全能但容易混乱的"万金油"

Multi-Agent：专业分工

用户需求
    ↓
Orchestrator（总指挥）
  ├── PM Agent        → 分析需求，拆解任务
  ├── Architect Agent → 设计技术方案
  ├── Developer Agent → 写代码
  └── Reviewer Agent  → 审查代码质量
    ↓
最终交付物
```

---

## Lesson 1：Agent 角色设计

每个 Agent 的核心是**专属 System Prompt**，定义它的角色和职责：

```python
# agent/roles.py

PM_SYSTEM = """
你是一名资深产品经理（PM Agent）。

你的职责：
1. 分析用户需求，识别核心功能
2. 拆解成具体的技术任务
3. 输出结构化的需求文档

输出格式：
{
  "feature": "功能名称",
  "user_story": "作为...，我想要...，以便...",
  "acceptance_criteria": ["标准1", "标准2"],
  "technical_tasks": ["任务1", "任务2"]
}
"""

ARCHITECT_SYSTEM = """
你是一名资深软件架构师（Architect Agent）。

你的职责：
1. 接收技术任务列表
2. 设计系统架构和数据结构
3. 选择合适的技术方案
4. 输出详细的技术设计文档

考虑因素：可扩展性、可维护性、简洁性
"""

DEVELOPER_SYSTEM = """
你是一名资深 Python 开发者（Developer Agent）。

你的职责：
1. 根据技术设计实现代码
2. 写清晰、有类型注解的代码
3. 每个函数都有文档字符串
4. 代码要可以直接运行

约束：
- 使用 Python 3.11+
- 使用 Pydantic 处理数据结构
- 使用 asyncio 处理异步操作
"""

REVIEWER_SYSTEM = """
你是一名代码审查专家（Reviewer Agent）。

你的职责：
1. 审查代码质量
2. 找出潜在的 bug
3. 提出改进建议
4. 给出总体评分（1-10）

审查维度：
- 正确性：代码逻辑是否正确
- 可读性：代码是否易于理解
- 安全性：是否有安全漏洞
- 性能：是否有明显的性能问题
"""
```

---

## Lesson 2：Agent 间通信

```python
# agent/messages.py
from pydantic import BaseModel
from typing import Any, Literal
from datetime import datetime

class AgentMessage(BaseModel):
    """Agent 之间传递的消息"""
    from_agent: str
    to_agent: str
    message_type: Literal["task", "result", "feedback", "question"]
    content: Any
    timestamp: str = ""

    def model_post_init(self, __context):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class TaskMessage(AgentMessage):
    message_type: Literal["task"] = "task"
    priority: int = 1

class ResultMessage(AgentMessage):
    message_type: Literal["result"] = "result"
    success: bool = True
    artifacts: dict = {}  # 交付物，比如代码、文档等
```

---

## Lesson 3：Orchestrator

```python
# agent/orchestrator.py
from anthropic import AsyncAnthropic
from .roles import PM_SYSTEM, ARCHITECT_SYSTEM, DEVELOPER_SYSTEM, REVIEWER_SYSTEM
import asyncio
import json

client = AsyncAnthropic()

async def run_agent_with_role(
    system_prompt: str,
    task: str,
    context: str = ""
) -> str:
    """运行一个特定角色的 Agent"""
    user_content = task
    if context:
        user_content = f"上下文信息：\n{context}\n\n任务：{task}"

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    return response.content[0].text

async def run_dev_team(user_requirement: str) -> dict:
    """
    运行完整的 AI 开发团队工作流
    """
    print(f"\n需求：{user_requirement}")
    artifacts = {}

    # Step 1: PM 分析需求
    print("\n[PM Agent] 分析需求...")
    pm_output = await run_agent_with_role(
        PM_SYSTEM,
        f"请分析以下需求并输出结构化需求文档：\n{user_requirement}"
    )
    artifacts["requirements"] = pm_output
    print(f"需求文档完成（{len(pm_output)} 字符）")

    # Step 2: Architect 设计方案
    print("\n[Architect Agent] 设计架构...")
    architect_output = await run_agent_with_role(
        ARCHITECT_SYSTEM,
        "请根据需求设计技术架构",
        context=pm_output
    )
    artifacts["architecture"] = architect_output
    print(f"架构设计完成（{len(architect_output)} 字符）")

    # Step 3: Developer 实现代码
    print("\n[Developer Agent] 实现代码...")
    code_output = await run_agent_with_role(
        DEVELOPER_SYSTEM,
        "请根据架构设计实现核心代码",
        context=f"需求文档：\n{pm_output}\n\n架构设计：\n{architect_output}"
    )
    artifacts["code"] = code_output
    print(f"代码实现完成（{len(code_output)} 字符）")

    # Step 4: Reviewer 审查代码
    print("\n[Reviewer Agent] 代码审查...")
    review_output = await run_agent_with_role(
        REVIEWER_SYSTEM,
        "请对以下代码进行审查",
        context=code_output
    )
    artifacts["review"] = review_output
    print(f"代码审查完成（{len(review_output)} 字符）")

    return artifacts
```

---

## Lesson 4：完整项目示例

```python
# main.py
import asyncio
from dotenv import load_dotenv
from agent.orchestrator import run_dev_team

load_dotenv()

async def main():
    # 给 AI Dev Team 一个真实任务
    requirement = """
    实现一个 URL 健康检查工具：
    - 输入一个 URL 列表
    - 并发检查每个 URL 的响应状态
    - 输出每个 URL 的状态码、响应时间
    - 超时时间 5 秒
    - 输出格式：JSON 报告
    """

    artifacts = await run_dev_team(requirement)

    print("\n" + "="*50)
    print("交付物汇总：")
    for name, content in artifacts.items():
        print(f"\n--- {name.upper()} ---")
        print(content[:300] + "..." if len(content) > 300 else content)

asyncio.run(main())
```

---

## 进阶：并行 Agent 执行

某些任务可以并行：

```python
# Architect 和 PM 同时工作（如果任务独立）
pm_task = run_agent_with_role(PM_SYSTEM, requirement)
architect_task = run_agent_with_role(ARCHITECT_SYSTEM, requirement)

# 并发执行
pm_output, architect_output = await asyncio.gather(pm_task, architect_task)
```

---

## 完成标准

- [ ] 4 个 Agent 角色有清晰的专属 System Prompt
- [ ] 每个 Agent 的输出作为下一个 Agent 的输入（上下文传递）
- [ ] Orchestrator 能协调完整流程
- [ ] 最终交付物包含需求文档 + 架构设计 + 代码 + 审查报告

---

## 下一步

完成了这 5 个阶段，你已经掌握了主流 Agent 模式。

进阶方向：
- **Claude Agent SDK**：用 Anthropic 官方 SDK 构建更复杂的 Multi-Agent
- **LangGraph**：用图结构管理复杂 Agent 工作流
- **AI Frontend Developer Agent**：结合你的前端背景，构建能写前端代码的 Agent

---

## Q&A

（在这里追加你学习过程中遇到的问题）
