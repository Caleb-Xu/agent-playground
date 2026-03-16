# Curriculum Mentor Memory

## Student Profile
- 5年前端经验，熟练 JS/TS（React/Vue）
- 目标：从前端转型 AI Agent 工程师
- 学习风格：直接动手边做边学
- 教学要点：Python 讲解要用 JS 做对比

## Current Progress
- 阶段：Phase 0 - Python 基础（第2课，共4课）
- 当前任务：phase-0-python-basics/02-pydantic-and-types.md（未开始）
- 已完成的课程任务：01-python-for-js-devs 全部（练习1、2、3）

## Topics Status
| 主题 | 状态 |
|------|------|
| Python 基础语法 (01) | 已完成 |
| Pydantic & 类型注解 (02) | 未开始 |
| asyncio (03) | 未开始 |
| uv & 工具链 (04) | 未开始 |
| Tool Agent | 未开始 |
| ReAct Agent | 未开始 |
| Plan-Execute | 未开始 |
| RAG | 未开始 |
| Multi-Agent | 未开始 |

## Teaching Notes
- 有 JS/TS 基础，Python 讲解要用 JS 做对比，减少认知摩擦
- 异步概念（async/await）已熟悉，Python asyncio 可快速迁移
- TS → Pydantic 是好的切入点
- 前端思维转 Agent 思维：把"组件/状态"换成"工具/推理循环"

## Project Structure
- 练习目录：`practice/`，结构镜像 `curriculum/`，各课练习放对应子目录
- 当前练习目录：`practice/phase-0-python-basics/01-python-for-js-devs/`
- 文件命名规范：`exercise_01.py`, `exercise_02.py` ...

## Student Weak Points
- **dict 点语法 vs 方括号**：多次把 `stats.score` 写成 JS 对象点语法，Python dict 读取和赋值都需要 `d["key"]`，需要持续强化
- **f-string 的 `f` 前缀**：容易遗漏，把 JS 的 `${}` 和 Python 的 `f""` 混淆
- **`__init__` 里初始化属性**：容易忘记在构造函数里初始化 `self.tools = []` 这类默认属性
- **列表推导式条件**：第一次不知道条件部分就是普通布尔表达式，需要明确说明

## Effective Teaching Approaches
（学习过程中记录）
