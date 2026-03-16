---
topic: Python Tooling - uv, venv, pyproject.toml
concepts: [uv, 虚拟环境, 包管理, pyproject.toml, 项目结构]
prerequisites: [01-python-for-js-devs.md]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# Python Tooling：uv & 项目工具链

## Why This Matters

前端开发者用 `npm` / `pnpm` 管理项目，Python 有自己的一套。
理解工具链是你能**独立启动项目**的前提——不然连环境都配不起来，代码写不了。

好消息：Python 工具链这几年进化了，现在有 **uv**，体验接近 pnpm，速度更快。

---

## 核心心智模型

```
前端工具链 → Python 工具链

npm / pnpm       →  uv
package.json     →  pyproject.toml
node_modules/    →  .venv/
npm install      →  uv sync
npm add xxx      →  uv add xxx
npm run dev      →  uv run python main.py
npx              →  uvx
```

---

## 安装 uv

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证安装：
```bash
uv --version
```

---

## 创建新项目

```bash
# 类比：npm init / pnpm create
uv init my-agent-project
cd my-agent-project
```

生成的结构：
```
my-agent-project/
├── pyproject.toml    ← 类比 package.json
├── .python-version   ← 指定 Python 版本
├── README.md
└── main.py
```

---

## pyproject.toml 解读

对比 `package.json`：

```json
// package.json
{
  "name": "my-agent",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

```toml
# pyproject.toml
[project]
name = "my-agent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## 常用命令对比

```bash
# 初始化项目
npm init                →  uv init

# 安装所有依赖
npm install             →  uv sync

# 添加依赖
npm add anthropic       →  uv add anthropic
npm add -D pytest       →  uv add --dev pytest

# 删除依赖
npm remove axios        →  uv remove httpx

# 运行脚本
npm run start           →  uv run python main.py
node index.js           →  uv run python main.py

# 运行一次性命令（不安装）
npx create-react-app    →  uvx some-tool
```

---

## 虚拟环境（类比 node_modules）

uv 会自动创建 `.venv` 目录，你不需要手动管理。

```bash
# uv sync 之后，.venv 自动创建
uv sync

# 项目结构
my-agent-project/
├── .venv/           ← 类比 node_modules/，不要提交到 git
├── pyproject.toml
├── uv.lock          ← 类比 package-lock.json / pnpm-lock.yaml
└── main.py
```

`.gitignore` 里加上：
```
.venv/
__pycache__/
*.pyc
.env
```

---

## 第一个 Agent 项目的完整初始化流程

```bash
# 1. 创建项目
uv init github-agent
cd github-agent

# 2. 添加依赖
uv add anthropic httpx pydantic python-dotenv

# 3. 创建 .env 文件（存放 API key）
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 4. 运行
uv run python main.py
```

---

## 读取环境变量

```python
# main.py
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API key loaded: {api_key[:8]}...")
```

---

## 项目结构推荐（Agent 项目）

```
github-agent/
├── .env                    ← API keys（不提交 git）
├── .gitignore
├── pyproject.toml
├── uv.lock
├── main.py                 ← 入口
├── agent/
│   ├── __init__.py
│   ├── core.py             ← Agent 主逻辑
│   └── tools.py            ← Tool 定义
└── tests/
    └── test_agent.py
```

**`__init__.py` 是什么？**
类比 JS 里的 `index.ts`，让目录变成一个"包"，可以被 import。
```python
# agent/__init__.py（可以是空文件，也可以导出公共接口）
from .core import Agent
from .tools import get_repo_info
```

---

## VS Code 配置

安装 Python 扩展后，让 VS Code 使用 `.venv`：

1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. 选择 `.venv` 里的 Python

或者在 `.vscode/settings.json` 里：
```json
{
  "python.defaultInterpreterPath": ".venv/Scripts/python.exe"
}
```

---

## Practice

**练习：** 从零搭建你的第一个 Agent 项目框架

1. 用 `uv init` 创建项目 `github-agent`
2. 添加依赖：`anthropic`, `httpx`, `pydantic`, `python-dotenv`
3. 创建以下文件结构：
   ```
   github-agent/
   ├── .env
   ├── main.py
   └── agent/
       ├── __init__.py
       └── core.py
   ```
4. 在 `main.py` 里写一个 `main()` 函数，读取 API key 并打印确认信息
5. 用 `uv run python main.py` 运行

完成后你就有了一个可以开始写 Agent 代码的项目环境。

---

## Q&A

（在这里追加你学习过程中遇到的问题）
