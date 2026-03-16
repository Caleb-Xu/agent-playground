---
topic: Python Async & asyncio
concepts: [async/await, asyncio, event loop, concurrent API calls, asyncio.gather]
prerequisites: [01-python-for-js-devs.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Python Async & asyncio

## Why This Matters

Agent 开发几乎全是 I/O 密集型操作：
- 调用 LLM API（等响应）
- 调用搜索 API（等结果）
- 读写文件（等 I/O）

如果用同步代码，这些操作会**阻塞**整个程序。
异步代码让你在等待一个 API 响应时，同时发起另一个请求，大幅提升效率。

好消息是：你已经会 JS 的 async/await，Python 的异步思路几乎一样。

---

## 核心心智模型

```
JavaScript async/await   ≈   Python asyncio + async/await

Node.js Event Loop       ≈   asyncio Event Loop

Promise.all([...])       ≈   asyncio.gather(...)

await fetch(url)         ≈   await httpx.AsyncClient().get(url)
```

**核心区别：**
- JS 的 event loop 是运行时内置的，你不需要手动启动
- Python 需要用 `asyncio.run()` 来启动 event loop
- 在 Agent 项目的入口文件里，你总会看到 `asyncio.run(main())`

---

## 基础语法对比

```javascript
// JavaScript
async function fetchRepoInfo(repoName) {
  const response = await fetch(`https://api.github.com/repos/${repoName}`)
  const data = await response.json()
  return data
}

// 使用
const info = await fetchRepoInfo("langchain-ai/langchain")
```

```python
# Python
import asyncio
import httpx

async def fetch_repo_info(repo_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.github.com/repos/{repo_name}")
        return response.json()

# 使用（在其他 async 函数里）
info = await fetch_repo_info("langchain-ai/langchain")

# 从同步代码启动（入口点）
asyncio.run(fetch_repo_info("langchain-ai/langchain"))
```

---

## 最常见的用法：调用 LLM API

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def ask_claude(question: str) -> str:
    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    )
    return message.content[0].text

async def main():
    answer = await ask_claude("什么是 AI Agent？")
    print(answer)

# 程序入口
asyncio.run(main())
```

---

## 并发请求：asyncio.gather（Agent 里最常用）

这是 Agent 开发中提升性能最重要的工具。

```javascript
// JavaScript：并行发多个请求
const [repo1, repo2, repo3] = await Promise.all([
  fetchRepo("react"),
  fetchRepo("vue"),
  fetchRepo("angular")
])
```

```python
# Python：同样的模式
import asyncio

async def fetch_repo(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.github.com/repos/{name}")
        return r.json()

async def main():
    # 并行发起 3 个请求，而不是串行等待
    repo1, repo2, repo3 = await asyncio.gather(
        fetch_repo("facebook/react"),
        fetch_repo("vuejs/vue"),
        fetch_repo("angular/angular")
    )
    print(repo1["stargazers_count"])

asyncio.run(main())
```

**性能差异：**
- 串行：3 个请求 × 500ms = 1500ms
- 并发：max(500ms, 500ms, 500ms) = 500ms

---

## 错误处理

```python
import asyncio
import httpx

async def safe_fetch(url: str) -> dict | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()  # 非 2xx 状态码会抛出异常
            return response.json()
    except httpx.TimeoutException:
        print(f"Timeout: {url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {url}")
        return None

# gather 时处理部分失败
async def main():
    results = await asyncio.gather(
        fetch_repo("react"),
        fetch_repo("invalid-repo-xyz"),   # 这个会失败
        return_exceptions=True   # 不让一个失败影响其他
    )

    for result in results:
        if isinstance(result, Exception):
            print(f"Failed: {result}")
        else:
            print(f"Success: {result['name']}")
```

---

## 流式响应（Streaming）

Agent 项目里经常用到 LLM 的流式输出：

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def stream_response(question: str):
    # 流式接收响应，边生成边打印
    async with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
    print()  # 换行

asyncio.run(stream_response("解释一下什么是 ReAct Agent"))
```

---

## 常见陷阱

| 陷阱 | 错误做法 | 正确做法 |
|------|---------|---------|
| 忘记 await | `result = async_func()` 返回协程对象 | `result = await async_func()` |
| 同步代码调用异步 | 直接调用 `async_func()` | `asyncio.run(async_func())` |
| 在异步函数里用同步 sleep | `time.sleep(1)` 会阻塞整个 loop | `await asyncio.sleep(1)` |
| 串行 await | 写两行 `await`，实际串行执行 | 用 `asyncio.gather()` 并发 |

---

## 关于 httpx vs requests

你可能见过 `requests` 库，这是旧的同步 HTTP 库：

```python
# 旧方式：同步，会阻塞
import requests
response = requests.get(url)

# 新方式：异步，不阻塞
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

**做 Agent 开发，用 httpx。**

---

## Practice

**练习 1：** 写一个异步函数 `get_user_repos(username: str) -> list[dict]`
- 调用 GitHub API：`https://api.github.com/users/{username}/repos`
- 返回仓库列表
- 加上错误处理（超时、HTTP 错误）

**练习 2：** 并发分析多个 GitHub 用户
```python
async def analyze_multiple_users(usernames: list[str]) -> dict:
    # 用 asyncio.gather 并发获取所有用户的 repos
    # 返回 {username: repo_count} 的字典
    pass
```

**练习 3：** 修改练习 1，改为流式打印每个找到的 repo 名称
```python
async def stream_repos(username: str):
    # 每找到一个 repo 立刻打印，不等全部加载完
    pass
```

---

## Q&A

（在这里追加你学习过程中遇到的问题）
