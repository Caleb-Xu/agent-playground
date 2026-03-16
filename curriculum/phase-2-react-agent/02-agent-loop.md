---
topic: ReAct Agent Loop 实现
concepts: [ReAct loop, reasoning trace, tool registry, 步骤记录]
prerequisites: [phase-2-react-agent/01-react-pattern.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# ReAct Agent Loop 实现

## 核心升级：带推理追踪的 Agent

在 Phase 1 的 Agent Loop 基础上，增加：
1. 每步记录 Thought + Action + Observation
2. 完成后可以看到完整推理链

```python
# agent/react_agent.py
from dataclasses import dataclass, field
from typing import Any
import json
import asyncio
from anthropic import AsyncAnthropic

@dataclass
class ReActStep:
    """记录 ReAct 的一个推理步骤"""
    step_number: int
    thought: str = ""
    action: str = ""
    action_input: dict = field(default_factory=dict)
    observation: str = ""

@dataclass
class ReActTrace:
    """完整的推理链"""
    question: str
    steps: list[ReActStep] = field(default_factory=list)
    final_answer: str = ""

    def print_trace(self):
        print(f"\n问题：{self.question}")
        print("=" * 50)
        for step in self.steps:
            print(f"\nStep {step.step_number}:")
            if step.thought:
                print(f"  Thought: {step.thought}")
            if step.action:
                print(f"  Action: {step.action}({json.dumps(step.action_input, ensure_ascii=False)})")
            if step.observation:
                print(f"  Observation: {step.observation[:200]}")
        print(f"\nFinal Answer: {self.final_answer}")

client = AsyncAnthropic()

REACT_SYSTEM = """
你是一个使用 ReAct 模式的 AI 研究助手。

在决定使用工具之前，先在内心进行推理（thinking_text 参数中体现）。
使用工具获取信息，然后决定下一步。

当你已经收集足够信息时，直接给出最终答案，不要再调用工具。
"""

async def run_react_agent(
    question: str,
    tools: list[dict],
    tool_functions: dict,
    max_steps: int = 10
) -> ReActTrace:
    trace = ReActTrace(question=question)
    messages = [{"role": "user", "content": question}]

    for step_num in range(1, max_steps + 1):
        current_step = ReActStep(step_number=step_num)

        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages,
            system=REACT_SYSTEM,
            # 启用扩展思考（让推理可见）
            # 注意：需要 claude-3-7-sonnet 或更新版本支持
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # 提取最终答案
            for block in response.content:
                if hasattr(block, "text"):
                    current_step.thought = "已收集足够信息，准备给出最终答案"
                    trace.final_answer = block.text
                    trace.steps.append(current_step)
                    return trace

        elif response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    current_step.action = block.name
                    current_step.action_input = block.input

                    # 执行工具
                    tool_fn = tool_functions.get(block.name)
                    if tool_fn:
                        result = await tool_fn(**block.input)
                    else:
                        result = {"error": f"工具 {block.name} 不存在"}

                    observation = json.dumps(result, ensure_ascii=False)
                    current_step.observation = observation

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": observation
                    })

            trace.steps.append(current_step)
            messages.append({"role": "user", "content": tool_results})

    trace.final_answer = "达到最大步骤限制，未能完成任务"
    return trace
```

---

## Tool Registry 模式

随着工具增多，用一个注册机制管理：

```python
# agent/tool_registry.py
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict
    function: Callable

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, name: str, description: str, parameters: dict):
        """装饰器：注册工具"""
        def decorator(fn: Callable) -> Callable:
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
                function=fn
            )
            return fn
        return decorator

    def get_tool_definitions(self) -> list[dict]:
        """返回给 LLM 的工具定义列表"""
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters
            }
            for t in self._tools.values()
        ]

    def get_functions(self) -> dict[str, Callable]:
        """返回工具名 → 函数的映射"""
        return {name: t.function for name, t in self._tools.items()}

# 全局注册表
registry = ToolRegistry()

# 使用装饰器注册工具
@registry.register(
    name="web_search",
    description="搜索网络获取最新信息",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    }
)
async def web_search(query: str) -> dict:
    # 实际项目里接入真实搜索 API
    return {"results": [f"关于 '{query}' 的搜索结果..."]}
```

---

## 使用示例

```python
# main.py
import asyncio
from dotenv import load_dotenv
from agent.tool_registry import registry
from agent.react_agent import run_react_agent

load_dotenv()

async def main():
    trace = await run_react_agent(
        question="帮我研究一下 2024 年最流行的 Python Agent 框架",
        tools=registry.get_tool_definitions(),
        tool_functions=registry.get_functions()
    )

    # 打印完整推理链
    trace.print_trace()

asyncio.run(main())
```

---

## Practice

1. 在 `ToolRegistry` 基础上，给每个工具添加 **调用次数统计**
2. 实现一个 `get_stats()` 方法，返回每个工具被调用了多少次
3. 在 `ReActTrace` 里加入总耗时统计

---

## Q&A

（在这里追加你学习过程中遇到的问题）
