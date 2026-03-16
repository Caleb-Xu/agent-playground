---
topic: Python for JavaScript Developers
concepts: [语法对比, 变量, 函数, 类, 模块, 常用数据结构]
prerequisites: []
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Python for JavaScript Developers

## Why This Matters
你已经会 JS/TS，Python 语法其实 90% 都能类比过去。
这篇教程的目标不是"从零学 Python"，而是帮你快速建立**JS → Python 的心智映射**，
让你能在 1 周内开始读懂 Agent 项目的代码。

---

## 核心心智模型

> Python 和 JavaScript 解决的是同一类问题，只是用了不同的"方言"。
> 你的目标不是重新学一门语言，而是学会"翻译"。

---

## 对照表：JS vs Python

### 变量 & 基本类型

```javascript
// JavaScript
const name = "Alice"
let age = 25
const isActive = true
const scores = [1, 2, 3]
const config = { host: "localhost", port: 8080 }
```

```python
# Python（无需声明关键字，无分号，无大括号）
name = "Alice"
age = 25
is_active = True          # 注意：True/False 大写
scores = [1, 2, 3]
config = {"host": "localhost", "port": 8080}
```

**关键差异：**
- Python 变量命名用 `snake_case`，不用 `camelCase`
- 布尔值：`True` / `False`（首字母大写）
- `null` → `None`
- 没有 `const`/`let`，所有变量都可以重新赋值

---

### 函数

```javascript
// JavaScript
function greet(name, greeting = "Hello") {
  return `${greeting}, ${name}!`
}

// 箭头函数
const add = (a, b) => a + b
```

```python
# Python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# lambda（相当于箭头函数，但只能写单个表达式）
add = lambda a, b: a + b
```

**关键差异：**
- 用缩进代替 `{}`，不要用 Tab 和 Space 混用
- f-string：`f"{name}"` 和 JS 的 `` `${name}` `` 一样
- 默认参数语法相同

---

### 类

```typescript
// TypeScript
class Agent {
  name: string
  tools: string[]

  constructor(name: string) {
    this.name = name
    this.tools = []
  }

  addTool(tool: string): void {
    this.tools.push(tool)
  }

  describe(): string {
    return `Agent ${this.name} has ${this.tools.length} tools`
  }
}
```

```python
# Python
class Agent:
    def __init__(self, name: str):
        self.name = name
        self.tools: list[str] = []

    def add_tool(self, tool: str) -> None:
        self.tools.append(tool)

    def describe(self) -> str:
        return f"Agent {self.name} has {len(self.tools)} tools"
```

**关键差异：**
- `constructor` → `__init__`
- 每个方法第一个参数是 `self`（相当于 `this`，但必须显式写出来）
- 方法命名用 `snake_case`
- `push` → `append`

---

### 条件 & 循环

```javascript
// JavaScript
if (score > 90) {
  console.log("A")
} else if (score > 80) {
  console.log("B")
} else {
  console.log("C")
}

for (const item of items) {
  console.log(item)
}

// 数组 map
const doubled = items.map(x => x * 2)
```

```python
# Python
if score > 90:
    print("A")
elif score > 80:   # 注意：elif，不是 else if
    print("B")
else:
    print("C")

for item in items:
    print(item)

# 列表推导式（比 map 更 Pythonic）
doubled = [x * 2 for x in items]
```

---

### 模块导入

```javascript
// JavaScript (ES modules)
import { readFile } from "fs/promises"
import axios from "axios"
import type { Message } from "./types"

export function myFunction() {}
export default class MyClass {}
```

```python
# Python
from pathlib import Path          # 标准库
import httpx                       # 第三方（类似 axios）
from typing import Optional        # 类型工具

# 导出：Python 没有 export，直接定义就行，import 时用 from xxx import yyy
def my_function():
    pass
```

---

### 字符串处理

```javascript
// JavaScript
const msg = `Hello, ${name}!`
const upper = name.toUpperCase()
const parts = "a,b,c".split(",")
const joined = parts.join("-")
const trimmed = "  hello  ".trim()
```

```python
# Python
msg = f"Hello, {name}!"
upper = name.upper()
parts = "a,b,c".split(",")
joined = "-".join(parts)       # 注意：join 在分隔符上调用，不是在数组上
trimmed = "  hello  ".strip()  # trim → strip
```

---

### 错误处理

```javascript
// JavaScript
try {
  const result = await fetch(url)
} catch (error) {
  console.error("Failed:", error.message)
} finally {
  cleanup()
}
```

```python
# Python
try:
    result = httpx.get(url)
except httpx.RequestError as e:
    print(f"Failed: {e}")
finally:
    cleanup()
```

---

### 类型注解（对 TS 开发者很重要）

```typescript
// TypeScript
function process(items: string[], limit: number = 10): string[] {
  return items.slice(0, limit)
}

interface Config {
  host: string
  port: number
  debug?: boolean
}
```

```python
# Python（类型注解是可选的，但 Agent 项目里普遍使用）
def process(items: list[str], limit: int = 10) -> list[str]:
    return items[:limit]

# TypeScript interface → Python 用 TypedDict 或 Pydantic（后面会学）
from typing import TypedDict, Optional

class Config(TypedDict):
    host: str
    port: int
    debug: Optional[bool]   # Optional 表示可能为 None
```

---

## Python 特有的常用技巧

### 解包（类似 JS 解构）

```javascript
// JavaScript 解构
const [first, ...rest] = items
const { name, age } = person
```

```python
# Python 解包
first, *rest = items
# 字典没有直接解构，需要用 .get() 或 **
name = person["name"]
age = person["age"]
```

### 字典操作（类似 JS Object）

```python
config = {"host": "localhost", "port": 8080}

# 访问
host = config["host"]           # 不存在会报 KeyError
host = config.get("host")       # 不存在返回 None（安全方式）
host = config.get("host", "default")  # 带默认值

# 合并（Python 3.9+）
merged = {**config, "debug": True}   # 类似 JS 的 {...config, debug: true}

# 遍历
for key, value in config.items():   # 类似 Object.entries()
    print(f"{key}: {value}")

keys = list(config.keys())          # Object.keys()
values = list(config.values())      # Object.values()
```

---

## 常见陷阱（JS 开发者容易踩）

| 陷阱 | 错误做法 | 正确做法 |
|------|---------|---------|
| 比较 None | `x == None` | `x is None` |
| 字典不存在的键 | `d["missing"]`（报错） | `d.get("missing")` |
| 复制列表 | `b = a`（引用同一个对象） | `b = a.copy()` 或 `b = a[:]` |
| 整数除法 | `5 / 2 = 2.5`（Python 3 是浮点） | 想要整数用 `5 // 2 = 2` |
| 没有 `undefined` | - | Python 只有 `None` |

---

## Practice

完成以下练习，熟悉 Python 基本语法：

**练习 1：** 把下面这段 JS 翻译成 Python
```javascript
function analyzeRepo(repoName, language = "unknown") {
  const stats = {
    name: repoName,
    language: language,
    score: 0
  }

  if (language === "Python") {
    stats.score = 10
  } else if (language === "JavaScript") {
    stats.score = 8
  }

  return `${stats.name} (${stats.language}): score ${stats.score}`
}
```

**练习 2：** 用列表推导式，从一个字符串列表里过滤出长度大于 5 的项
```python
repos = ["react", "langchain", "ai", "anthropic", "vue"]
# 期望输出：["langchain", "anthropic"]
```

**练习 3：** 写一个 `Agent` 类，有 `name`、`tools` 属性，和 `run(task: str) -> str` 方法

---

## Q&A

（在这里追加你学习过程中遇到的问题）
