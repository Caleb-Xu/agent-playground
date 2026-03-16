---
topic: 实现第一个 Agent
concepts: [Anthropic SDK, tool definition, agent loop 实现, 错误处理]
prerequisites: [phase-1-tool-agent/01-agent-basics.md, phase-0-python-basics/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# 实现第一个 Agent

## Why This Matters

上一篇讲了概念，这篇我们写真实代码。
目标：用不到 100 行 Python，实现一个真正能调用工具的 Agent。

---

## 项目准备

```bash
# 如果还没建项目
uv init github-agent
cd github-agent
uv add anthropic httpx pydantic python-dotenv
```

`.env` 文件：
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Step 1：定义工具

工具分两部分：**定义**（告诉 LLM 工具是什么）和**实现**（真正执行逻辑）。

```python
# agent/tools.py
import httpx
from typing import Any

# --- 工具定义（给 LLM 看的 JSON Schema）---
TOOLS = [
    {
        "name": "get_repo_info",
        "description": "获取 GitHub 仓库的基本信息，包括语言、star 数、描述等",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "仓库全名，格式：owner/repo，例如：facebook/react"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_repo_languages",
        "description": "获取仓库使用的编程语言及其代码行数占比",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "仓库全名，格式：owner/repo"
                }
            },
            "required": ["repo_name"]
        }
    }
]

# --- 工具实现（真正执行的函数）---
async def get_repo_info(repo_name: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_name}",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        if response.status_code == 404:
            return {"error": f"仓库 {repo_name} 不存在"}
        data = response.json()
        return {
            "name": data["full_name"],
            "description": data.get("description", ""),
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "language": data.get("language", "Unknown"),
            "topics": data.get("topics", []),
            "created_at": data["created_at"]
        }

async def get_repo_languages(repo_name: str) -> dict[str, int]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_name}/languages"
        )
        return response.json()

# 工具名 → 函数 的映射（用于 agent 执行时查找）
TOOL_FUNCTIONS = {
    "get_repo_info": get_repo_info,
    "get_repo_languages": get_repo_languages,
}
```

---

## Step 2：实现 Agent Core

```python
# agent/core.py
import json
import asyncio
from anthropic import AsyncAnthropic
from .tools import TOOLS, TOOL_FUNCTIONS

client = AsyncAnthropic()

async def run_agent(user_message: str) -> str:
    """
    运行 Agent，接受用户问题，返回最终回答。
    """
    print(f"\n用户：{user_message}")
    print("-" * 40)

    messages = [{"role": "user", "content": user_message}]

    # Agent Loop
    step = 0
    while True:
        step += 1
        print(f"\n[Step {step}] 调用 LLM...")

        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
            system="你是一个 GitHub 仓库分析助手。使用提供的工具来获取信息，然后给出详细分析。"
        )

        # 把 LLM 回复加入历史
        messages.append({"role": "assistant", "content": response.content})

        # 判断下一步
        if response.stop_reason == "end_turn":
            # 完成，提取文本回复
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\n最终回答：\n{block.text}")
                    return block.text

        elif response.stop_reason == "tool_use":
            # 执行工具
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    print(f"  → 调用工具: {tool_name}({json.dumps(tool_input, ensure_ascii=False)})")

                    # 执行对应的工具函数
                    tool_fn = TOOL_FUNCTIONS.get(tool_name)
                    if tool_fn:
                        result = await tool_fn(**tool_input)
                    else:
                        result = {"error": f"未知工具: {tool_name}"}

                    print(f"  ← 工具结果: {json.dumps(result, ensure_ascii=False)[:100]}...")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # 把工具结果传回
            messages.append({"role": "user", "content": tool_results})

        else:
            # 其他情况，退出
            print(f"  未知 stop_reason: {response.stop_reason}")
            break

    return "Agent 运行结束"
```

---

## Step 3：入口文件

```python
# main.py
import asyncio
import os
from dotenv import load_dotenv
from agent.core import run_agent

load_dotenv()

async def main():
    # 测试一下
    result = await run_agent("帮我分析一下 facebook/react 这个 GitHub 仓库")
    print("\n" + "=" * 40)
    print("完成！")

asyncio.run(main())
```

---

## 运行和观察

```bash
uv run python main.py
```

你应该看到类似输出：
```
用户：帮我分析一下 facebook/react 这个 GitHub 仓库
----------------------------------------

[Step 1] 调用 LLM...
  → 调用工具: get_repo_info({"repo_name": "facebook/react"})
  ← 工具结果: {"name": "facebook/react", "stars": 220000, ...

[Step 2] 调用 LLM...
  → 调用工具: get_repo_languages({"repo_name": "facebook/react"})
  ← 工具结果: {"JavaScript": 4521234, "TypeScript": ...

[Step 3] 调用 LLM...

最终回答：
React 是一个由 Facebook 开发的前端 UI 库...
```

---

## 理解发生了什么

```
Step 1: LLM 决定先获取基本信息 → 调用 get_repo_info
Step 2: LLM 觉得需要语言信息 → 调用 get_repo_languages
Step 3: LLM 已有足够信息 → 写出最终分析
```

LLM 自己决定了调用哪些工具、调用几次、什么时候停止。
这就是 Agent 和普通 LLM 调用的本质区别。

---

## Practice

在现有代码基础上，添加第三个工具：

**`get_recent_commits`：获取最近 5 条提交记录**
```python
# 提示：GitHub API
# GET https://api.github.com/repos/{owner}/{repo}/commits?per_page=5
# 返回：[{sha, commit: {message, author: {name, date}}}]
```

添加之后，重新问 Agent："帮我了解一下 langchain-ai/langchain 最近的开发动态"，
看看它是否会自动调用新工具。

---

## Q&A

（在这里追加你学习过程中遇到的问题）
