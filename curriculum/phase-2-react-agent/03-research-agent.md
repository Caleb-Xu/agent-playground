---
topic: Research Agent（Phase 2 项目）
concepts: [搜索工具集成, 多步推理, 内容摘要, 结构化研究报告]
prerequisites: [phase-2-react-agent/02-agent-loop.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# 项目：Research Agent

## 项目目标

输入一个研究问题，Agent 自动：
1. 拆解问题，确定需要搜索哪些内容
2. 多轮搜索收集信息
3. 综合整理，输出有引用来源的研究摘要

---

## 工具集设计

```python
# 这个项目需要的工具
tools = [
    "web_search",        # 搜索网络
    "get_page_content",  # 获取网页正文
    "summarize_text",    # 摘要长文本（用 LLM）
]
```

**注意：** 真实的 web search 需要接入搜索 API（如 Tavily、SerpAPI）。
学习阶段可以先 mock，专注于 Agent 逻辑。

---

## Mock 工具实现（学习用）

```python
# agent/mock_tools.py
import asyncio
from agent.tool_registry import registry

# Mock 搜索结果
MOCK_SEARCH_DATA = {
    "python agent frameworks 2024": [
        {"title": "LangChain Overview", "snippet": "LangChain 是最流行的 Agent 框架...", "url": "https://langchain.com"},
        {"title": "AutoGen by Microsoft", "snippet": "AutoGen 支持多 Agent 协作...", "url": "https://microsoft.github.io/autogen"},
        {"title": "CrewAI Framework", "snippet": "CrewAI 专注于角色扮演 Agent...", "url": "https://crewai.com"},
    ],
    "react agent pattern": [
        {"title": "ReAct Paper", "snippet": "ReAct: Synergizing Reasoning and Acting in Language Models...", "url": "https://arxiv.org"},
    ]
}

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
    await asyncio.sleep(0.1)  # 模拟网络延迟
    # 简单的关键词匹配
    results = []
    for key, data in MOCK_SEARCH_DATA.items():
        if any(word in query.lower() for word in key.split()):
            results.extend(data)
    if not results:
        results = [{"title": "通用结果", "snippet": f"关于 '{query}' 的相关信息...", "url": "https://example.com"}]
    return {"query": query, "results": results[:3]}
```

---

## Research Agent 的 System Prompt

```python
RESEARCH_SYSTEM = """
你是一个专业的研究助手，擅长收集和整理信息。

工作方式：
1. 分析用户的研究问题，确定需要搜索什么
2. 进行多次有针对性的搜索，逐步深入
3. 不要重复搜索相同的内容
4. 收集足够信息后，整理出结构化报告

报告格式：
## 研究报告：[主题]

### 核心发现
[3-5 个要点]

### 详细分析
[分节展开]

### 来源
[列出引用的来源]
"""
```

---

## 完成标准

- [ ] Agent 能进行至少 3 步搜索才给出最终答案
- [ ] 最终报告有清晰的结构
- [ ] 推理链（ReActTrace）完整记录了每一步
- [ ] 能切换到真实搜索 API（预留接口）

---

## 进阶挑战

将 Mock 搜索换成真实的 [Tavily API](https://tavily.com)（有免费额度）：

```bash
uv add tavily-python
```

```python
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def web_search(query: str) -> dict:
    result = tavily.search(query=query, max_results=5)
    return result
```

---

## Q&A

（在这里追加你学习过程中遇到的问题）
