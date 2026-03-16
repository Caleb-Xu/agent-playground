---
topic: Plan-Execute Agent
concepts: [任务分解, Planner, Executor, 两阶段架构, 复杂任务处理]
prerequisites: [phase-2-react-agent/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Plan-Execute Agent

## Why This Matters

ReAct Agent 每次只想一步，适合简单任务。
遇到复杂任务（比如"帮我写一份完整的技术调研报告"），ReAct 容易迷失。

**Plan-Execute 的核心思想：先想清楚全局，再逐步执行。**

---

## 核心心智模型

```
ReAct（边想边做）：
  问题 → 思考 → 行动 → 思考 → 行动 → ... → 答案
  特点：灵活但容易跑偏

Plan-Execute（先想后做）：
  问题
    ↓ Planner
  计划：[步骤1, 步骤2, 步骤3, ...]
    ↓ Executor
  执行步骤1 → 结果1
  执行步骤2 → 结果2
  执行步骤3 → 结果3
    ↓
  综合 → 最终答案
  特点：有条理，适合复杂任务
```

---

## 架构设计

```
用户问题
    ↓
Planner Agent
  - 输入：用户问题
  - 输出：有序步骤列表 [Step1, Step2, ...]
    ↓
Executor Agent（循环）
  - 输入：当前步骤 + 之前步骤的结果
  - 输出：当前步骤的结果
    ↓
Synthesizer
  - 输入：所有步骤的结果
  - 输出：最终报告
```

---

## Milestone 1：Planner 实现

```python
# agent/planner.py
from pydantic import BaseModel
from anthropic import AsyncAnthropic
import json

client = AsyncAnthropic()

class ExecutionStep(BaseModel):
    step_number: int
    description: str       # 这一步要做什么
    tool_hint: str         # 建议用哪个工具
    depends_on: list[int] = []  # 依赖哪些步骤的结果

class ExecutionPlan(BaseModel):
    goal: str
    steps: list[ExecutionStep]
    estimated_steps: int

PLANNER_PROMPT = """
你是一个任务规划专家。

给定一个复杂任务，你需要将其分解为具体的执行步骤。

要求：
- 每个步骤只做一件事
- 步骤之间要有逻辑顺序
- 指出每步需要用的工具
- 步骤数量控制在 3-8 步

输出格式（JSON）：
{
  "goal": "总体目标",
  "steps": [
    {
      "step_number": 1,
      "description": "具体要做的事",
      "tool_hint": "建议使用的工具名",
      "depends_on": []
    }
  ],
  "estimated_steps": 4
}
"""

async def create_plan(task: str) -> ExecutionPlan:
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=PLANNER_PROMPT,
        messages=[{"role": "user", "content": f"请为以下任务制定执行计划：\n\n{task}"}]
    )

    text = response.content[0].text
    # 提取 JSON
    import re
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        data = json.loads(json_match.group())
        return ExecutionPlan.model_validate(data)

    raise ValueError(f"无法解析计划：{text}")
```

---

## Milestone 2：Executor 实现

```python
# agent/executor.py
from .planner import ExecutionStep
from .react_agent import run_react_agent
from .tool_registry import registry

async def execute_step(
    step: ExecutionStep,
    previous_results: dict[int, str]
) -> str:
    """执行单个步骤"""
    # 构建上下文：这一步要做什么 + 之前步骤的结果
    context = f"当前任务：{step.description}\n"

    if step.depends_on:
        context += "\n之前步骤的结果：\n"
        for dep_step in step.depends_on:
            if dep_step in previous_results:
                context += f"步骤{dep_step}结果：{previous_results[dep_step]}\n"

    # 用 ReAct Agent 执行这一步
    trace = await run_react_agent(
        question=context,
        tools=registry.get_tool_definitions(),
        tool_functions=registry.get_functions(),
        max_steps=5
    )

    return trace.final_answer
```

---

## Milestone 3：Workflow Engine

```python
# agent/workflow.py
from .planner import create_plan, ExecutionPlan
from .executor import execute_step

async def run_plan_execute(task: str) -> dict:
    print(f"\n任务：{task}")
    print("=" * 50)

    # Phase 1: 规划
    print("\n[规划阶段]")
    plan = await create_plan(task)
    print(f"目标：{plan.goal}")
    print(f"步骤数：{plan.estimated_steps}")
    for step in plan.steps:
        print(f"  Step {step.step_number}: {step.description}")

    # Phase 2: 执行
    print("\n[执行阶段]")
    results = {}

    for step in plan.steps:
        print(f"\n执行 Step {step.step_number}: {step.description}")
        result = await execute_step(step, results)
        results[step.step_number] = result
        print(f"结果（摘要）：{result[:100]}...")

    # Phase 3: 综合
    print("\n[综合阶段]")
    final = await synthesize_results(plan, results)

    return {
        "task": task,
        "plan": plan.model_dump(),
        "step_results": results,
        "final_report": final
    }

async def synthesize_results(plan, results: dict) -> str:
    """把所有步骤结果综合成最终报告"""
    from anthropic import AsyncAnthropic
    client = AsyncAnthropic()

    steps_summary = "\n".join([
        f"步骤{k}（{plan.steps[k-1].description}）：\n{v}"
        for k, v in results.items()
    ])

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"任务目标：{plan.goal}\n\n各步骤执行结果：\n{steps_summary}\n\n请综合以上信息，生成一份完整的报告。"
        }]
    )
    return response.content[0].text
```

---

## Milestone 4：项目示例

```python
# main.py
import asyncio
from dotenv import load_dotenv
from agent.workflow import run_plan_execute

load_dotenv()

async def main():
    result = await run_plan_execute(
        "对比分析 LangChain、AutoGen 和 CrewAI 这三个 AI Agent 框架，"
        "从易用性、功能、社区活跃度等维度给出选型建议"
    )
    print("\n" + "=" * 50)
    print("最终报告：")
    print(result["final_report"])

asyncio.run(main())
```

---

## 完成标准

- [ ] Planner 能生成合理的 3-8 步计划
- [ ] Executor 能根据上下文（依赖步骤的结果）执行每步
- [ ] 最终报告综合了所有步骤的信息
- [ ] 整体架构分 Planner / Executor / Synthesizer 三层

---

## Q&A

（在这里追加你学习过程中遇到的问题）
