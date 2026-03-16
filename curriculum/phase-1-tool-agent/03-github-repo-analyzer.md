---
topic: GitHub Repo 分析 Agent（Phase 1 项目）
concepts: [完整 Agent 项目, 报告生成, Pydantic 结构化输出, 多工具协作]
prerequisites: [phase-1-tool-agent/02-first-agent.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# 项目：GitHub Repo 分析 Agent

## 项目目标

输入一个 GitHub 仓库 URL，Agent 自动：
1. 获取仓库基本信息
2. 分析技术栈和语言分布
3. 查看最近提交活跃度
4. 生成一份结构化分析报告

---

## 项目结构

```
github-agent/
├── .env
├── pyproject.toml
├── main.py
└── agent/
    ├── __init__.py
    ├── core.py          ← Phase 1 已完成
    ├── tools.py         ← 扩展更多工具
    └── report.py        ← 新增：报告生成
```

---

## Milestone 1：项目初始化

Phase 0 已经完成，参考 [04-tooling-uv-venv.md](../phase-0-python-basics/04-tooling-uv-venv.md)。

---

## Milestone 2：扩展工具系统

在 `tools.py` 基础上增加工具：

```python
# 新增工具：获取最近提交
{
    "name": "get_recent_commits",
    "description": "获取仓库最近的提交记录，了解开发活跃度",
    "input_schema": {
        "type": "object",
        "properties": {
            "repo_name": {"type": "string"},
            "count": {"type": "integer", "default": 10}
        },
        "required": ["repo_name"]
    }
}

# 新增工具：获取 README
{
    "name": "get_readme",
    "description": "获取仓库的 README 内容，了解项目用途",
    "input_schema": {
        "type": "object",
        "properties": {
            "repo_name": {"type": "string"}
        },
        "required": ["repo_name"]
    }
}
```

---

## Milestone 3：Agent Loop（已在 02 完成）

重点确认你理解了循环的逻辑，在这个 milestone 里，试着：

1. 加一个 `max_steps` 参数，防止无限循环
2. 在每一步打印更清晰的日志

```python
async def run_agent(user_message: str, max_steps: int = 10) -> str:
    ...
    step = 0
    while step < max_steps:
        step += 1
        ...
```

---

## Milestone 4：结构化报告输出

用 Pydantic 定义报告结构，让 LLM 输出标准格式：

```python
# agent/report.py
from pydantic import BaseModel

class TechStack(BaseModel):
    primary_language: str
    languages: dict[str, float]  # 语言 → 占比百分比
    frameworks: list[str]

class ActivityMetrics(BaseModel):
    recent_commits: int
    last_commit_date: str
    contributors_estimate: str  # "active" | "moderate" | "inactive"

class RepoReport(BaseModel):
    repo_name: str
    description: str
    stars: int
    tech_stack: TechStack
    activity: ActivityMetrics
    summary: str
    recommendations: list[str]
```

在 System Prompt 里要求 LLM 输出 JSON：

```python
system_prompt = """你是一个 GitHub 仓库分析专家。

分析完成后，输出一份 JSON 格式的报告，严格遵循以下结构：
{
  "repo_name": "...",
  "description": "...",
  "stars": 0,
  "tech_stack": {
    "primary_language": "...",
    "languages": {"Python": 80.5, "Shell": 19.5},
    "frameworks": ["fastapi", "pydantic"]
  },
  "activity": {
    "recent_commits": 10,
    "last_commit_date": "2024-01-15",
    "contributors_estimate": "active"
  },
  "summary": "...",
  "recommendations": ["...", "..."]
}
"""
```

解析报告：

```python
import json
from .report import RepoReport

# 从 Agent 输出中提取 JSON
def parse_report(agent_output: str) -> RepoReport:
    # 找到 JSON 部分（可能被包含在 markdown 代码块里）
    import re
    json_match = re.search(r'\{.*\}', agent_output, re.DOTALL)
    if json_match:
        data = json.loads(json_match.group())
        return RepoReport.model_validate(data)
    raise ValueError("无法从输出中解析报告")
```

---

## 完整运行示例

```python
# main.py
import asyncio
from dotenv import load_dotenv
from agent.core import run_agent
from agent.report import parse_report

load_dotenv()

async def main():
    repos_to_analyze = [
        "langchain-ai/langchain",
        "microsoft/autogen",
        "anthropics/anthropic-sdk-python"
    ]

    for repo in repos_to_analyze:
        print(f"\n{'='*50}")
        print(f"分析：{repo}")
        print('='*50)

        output = await run_agent(f"请分析这个 GitHub 仓库：{repo}")

        try:
            report = parse_report(output)
            print(f"\n报告摘要：")
            print(f"  主要语言：{report.tech_stack.primary_language}")
            print(f"  Star 数：{report.stars}")
            print(f"  活跃度：{report.activity.contributors_estimate}")
            print(f"  总结：{report.summary[:100]}...")
        except Exception as e:
            print(f"  解析报告失败：{e}")

asyncio.run(main())
```

---

## 完成标准

- [ ] Agent 能自动调用多个工具，无需手动指定顺序
- [ ] 报告输出符合 Pydantic 模型结构
- [ ] 有 max_steps 保护，不会无限循环
- [ ] 能分析至少 3 个不同的 GitHub 仓库

---

## Q&A

（在这里追加你学习过程中遇到的问题）
