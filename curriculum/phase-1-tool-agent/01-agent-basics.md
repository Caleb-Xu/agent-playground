---
topic: Agent 基础概念
concepts: [LLM, Tool Calling, Agent Loop, Function Calling]
prerequisites: [phase-0-python-basics/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Agent 基础：LLM + Tool = Agent

## Why This Matters

在你开始写代码之前，必须先理解一件事：

> Agent 不是魔法。它就是一个 **while 循环** + **LLM** + **一些函数**。

理解了这个模型，你就不会再觉得 "Agent" 是什么神秘的东西。

---

## 核心心智模型

```
普通 LLM 调用（聊天）：

用户输入
   ↓
LLM 生成回复
   ↓
输出


Agent 调用（工具 + 循环）：

用户输入
   ↓
LLM 思考："我需要用工具 X 查一下"
   ↓
执行工具 X
   ↓
把结果返回给 LLM
   ↓
LLM 思考："我还需要用工具 Y"
   ↓
执行工具 Y
   ↓
LLM 思考："我已经有足够信息了"
   ↓
输出最终答案
```

**Agent = LLM + Tools + Loop**

---

## 什么是 Tool Calling（工具调用）

LLM 本身不能执行代码、访问网络、查数据库。
但你可以告诉它："我有这些工具，你可以调用它们。"

```python
# 你告诉 LLM：这是一个工具
{
    "name": "get_repo_info",
    "description": "获取 GitHub 仓库的基本信息",
    "input_schema": {
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "仓库名称，格式：owner/repo"
            }
        },
        "required": ["repo_name"]
    }
}
```

LLM 不会真正"调用"这个工具，它只会说：
> "我想调用 `get_repo_info`，参数是 `{'repo_name': 'facebook/react'}`"

然后你的代码真正执行这个函数，把结果传回给 LLM。

---

## Agent Loop 的代码骨架

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def agent_loop(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    tools = [get_repo_info_tool_definition]   # 工具列表

    while True:
        # 1. 让 LLM 思考下一步
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # 2. 把 LLM 的回复加入消息历史
        messages.append({"role": "assistant", "content": response.content})

        # 3. 检查 LLM 是否要调用工具
        if response.stop_reason == "end_turn":
            # LLM 说"我说完了"，退出循环
            return response.content[0].text

        if response.stop_reason == "tool_use":
            # LLM 要调用工具
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    # 4. 执行工具
                    result = await execute_tool(block.name, block.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # 5. 把工具结果传回给 LLM，继续循环
            messages.append({"role": "user", "content": tool_results})
```

这就是 **Agent Loop** 的全部核心逻辑。

---

## 三个关键概念

### 1. Messages（消息历史）
Agent 的"记忆"就是这个消息列表。每一步都往里加内容。

```python
messages = [
    {"role": "user", "content": "分析 facebook/react 这个 repo"},
    {"role": "assistant", "content": [...]},  # LLM 说要调用工具
    {"role": "user", "content": [{"type": "tool_result", ...}]},  # 工具结果
    {"role": "assistant", "content": "根据分析，react 是..."},  # 最终回答
]
```

### 2. stop_reason（停止原因）
LLM 每次回复都会告诉你为什么停止：
- `"end_turn"`：回答完成，不需要更多工具
- `"tool_use"`：需要执行工具，等待结果

### 3. Tool Definition（工具定义）
就是一个 JSON Schema，描述工具的名称、用途、参数。

---

## 为什么这对前端开发者来说很好理解？

```javascript
// 前端：事件驱动循环
while (app.running) {
  const event = waitForEvent()
  const action = processEvent(event)
  render(action)
}

// Agent：推理驱动循环
while (agent.running) {
  const llmDecision = await askLLM(messages)
  const toolResult = await executeTool(llmDecision)
  messages.push(toolResult)
}
```

都是循环 + 处理 + 更新状态。只是 Agent 里的"决策者"是 LLM。

---

## Practice

**练习：用伪代码描述 Agent Loop**

不用写真实代码，用你自己的语言描述：
1. 用户说"帮我分析 GitHub 上的 react 仓库"
2. Agent 接下来的每一步是什么？
3. 什么时候 loop 结束？

写完后和这篇教程的描述对比一下，看看你的理解是否正确。

---

## Q&A

（在这里追加你学习过程中遇到的问题）
