---
topic: Pydantic & Python Type System
concepts: [类型注解, BaseModel, 字段验证, 结构化输出, dataclass 对比]
prerequisites: [01-python-for-js-devs.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Pydantic & Python 类型系统

## Why This Matters

在 Agent 开发中，你会不断遇到这个问题：

> LLM 返回的是字符串，但你的代码需要结构化数据。

Pydantic 就是解决这个问题的标准答案。几乎所有主流 Agent 框架（LangChain、Anthropic SDK、FastAPI）都用 Pydantic 来定义数据结构。

对你来说更好的消息是：**Pydantic 就是 Python 版的 TypeScript Interface，而且功能更强。**

---

## 核心心智模型

```
TypeScript Interface   →   Pydantic BaseModel
    类型检查（编译时）          类型验证（运行时）
    只是类型标注               真正执行数据验证
```

TypeScript 的 interface 只在编译时检查，运行时不管。
Pydantic 的 BaseModel 在运行时真正验证数据，不符合就报错。

---

## 基础用法：从 TS Interface 到 Pydantic

```typescript
// TypeScript
interface Tool {
  name: string
  description: string
  parameters: Record<string, unknown>
}

interface AgentResponse {
  thought: string
  action: string | null
  result: string
  success: boolean
}
```

```python
# Python + Pydantic
from pydantic import BaseModel
from typing import Optional, Any

class Tool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]

class AgentResponse(BaseModel):
    thought: str
    action: Optional[str] = None   # Optional 且有默认值 None
    result: str
    success: bool
```

---

## 创建和使用

```python
from pydantic import BaseModel

class RepoInfo(BaseModel):
    name: str
    language: str
    stars: int
    description: Optional[str] = None

# 创建实例（类似 JS 的对象字面量）
repo = RepoInfo(
    name="langchain",
    language="Python",
    stars=75000
)

# 访问字段
print(repo.name)        # "langchain"
print(repo.stars)       # 75000

# 转成字典（类似 JSON.stringify 之前的步骤）
print(repo.model_dump())
# {'name': 'langchain', 'language': 'Python', 'stars': 75000, 'description': None}

# 转成 JSON 字符串
print(repo.model_dump_json())

# 从字典创建（类似 JSON.parse 之后的步骤）
data = {"name": "react", "language": "JavaScript", "stars": 220000}
repo2 = RepoInfo(**data)
# 或者
repo3 = RepoInfo.model_validate(data)
```

---

## 类型验证（这是 Pydantic 最强的地方）

```python
# Pydantic 会在运行时验证数据类型，并尝试自动转换
repo = RepoInfo(
    name="langchain",
    language="Python",
    stars="75000"    # 字符串传给 int 字段
)
print(repo.stars)   # 75000（int，自动转换了！）

# 无法转换时会报错
repo = RepoInfo(
    name="langchain",
    language="Python",
    stars="not-a-number"   # 这会抛出 ValidationError
)
```

---

## 嵌套模型

```python
# 在 Agent 开发中，消息结构非常常见
class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]

class Message(BaseModel):
    role: str           # "user" | "assistant" | "tool"
    content: str
    tool_calls: list[ToolCall] = []   # 默认空列表

# 嵌套使用
msg = Message(
    role="assistant",
    content="I'll search for that",
    tool_calls=[
        ToolCall(tool_name="search", arguments={"query": "python async"})
    ]
)

print(msg.tool_calls[0].tool_name)   # "search"
print(msg.model_dump())
```

---

## 字段验证和约束

```python
from pydantic import BaseModel, Field, field_validator

class AgentConfig(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Agent 名称")
    max_steps: int = Field(default=10, ge=1, le=100)  # ge=大于等于, le=小于等于
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    # 自定义验证器
    @field_validator("name")
    @classmethod
    def name_must_be_alphanumeric(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("name 只能包含字母、数字、横杠和下划线")
        return v.lower()   # 自动转小写

config = AgentConfig(name="My-Agent", max_steps=5)
print(config.name)   # "my-agent"（自动转小写了）
```

---

## 在 Agent 开发中最常见的用法：结构化输出

这是你在 Phase 1 就会用到的模式：

```python
from anthropic import Anthropic
from pydantic import BaseModel

# 定义你想从 LLM 得到的数据结构
class RepoAnalysis(BaseModel):
    main_language: str
    tech_stack: list[str]
    complexity: str  # "simple" | "medium" | "complex"
    summary: str

# 告诉 LLM 按这个格式输出
# （实际调用方式在 Phase 1 会详细讲）
```

---

## Pydantic vs TypedDict vs dataclass

你可能会看到 Python 代码里用不同方式定义数据结构，这里是对比：

| 特性 | Pydantic BaseModel | TypedDict | dataclass |
|------|-------------------|-----------|-----------|
| 运行时验证 | ✅ | ❌ | ❌ |
| 自动转换类型 | ✅ | ❌ | ❌ |
| JSON 序列化 | ✅（内置） | 需要手动 | 需要手动 |
| 性能 | 中等 | 快 | 快 |
| Agent 框架支持 | ✅ 大多数框架首选 | 部分支持 | 部分支持 |

**结论：做 Agent 开发，默认用 Pydantic BaseModel。**

---

## 安装

```bash
# 用 uv（推荐，快）
uv add pydantic

# 或者 pip
pip install pydantic
```

---

## Practice

**练习 1：** 定义一个 `GitHubRepo` Pydantic 模型
```
字段要求：
- name: 字符串，1-100 字符
- owner: 字符串
- stars: 整数，最小 0
- language: 可选字符串，默认 None
- topics: 字符串列表，默认空列表
- is_fork: 布尔值，默认 False
```

**练习 2：** 定义一个 `AgentStep` 模型表示 Agent 的一步操作
```
字段要求：
- step_number: 整数
- thought: 字符串（Agent 的思考过程）
- action: 可选字符串（要执行的工具名）
- action_input: 可选字典（工具的输入参数）
- observation: 可选字符串（工具执行结果）
```

**练习 3：** 把这个 JSON 解析成你定义的模型，并验证它能正确序列化回 JSON
```json
{
  "name": "langchain",
  "owner": "langchain-ai",
  "stars": 75000,
  "language": "Python",
  "topics": ["ai", "llm", "agents"]
}
```

---

## Q&A

（在这里追加你学习过程中遇到的问题）
