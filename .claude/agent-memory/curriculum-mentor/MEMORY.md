# Curriculum Mentor Memory

## Student Profile
- 5年前端经验，熟练 JS/TS（React/Vue）
- 目标：从前端转型 AI Agent 工程师
- 学习风格：直接动手边做边学
- 教学要点：Python 讲解要用 JS 做对比

## Current Progress
- 阶段：Phase 0 - Python 基础（第4课，共4课）
- 当前任务：phase-0-python-basics/04-uv-toolchain.md（未开始）
- 已完成的课程任务：01-python-for-js-devs 全部（练习1、2、3）；02-pydantic-and-types 全部（练习1、2、3）；03-async-python 全部（练习1、2、3 + 复习测验）

## Topics Status
| 主题 | 状态 |
|------|------|
| Python 基础语法 (01) | 已完成 |
| Pydantic & 类型注解 (02) | 已完成 |
| asyncio (03) | 已完成 |
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
- 当前练习目录：`practice/phase-0-python-basics/04-uv-toolchain/`
- 文件命名规范：`exercise_01.py`, `exercise_02.py` ...

## Student Weak Points
- **dict 点语法 vs 方括号**：多次把 `stats.score` 写成 JS 对象点语法，Python dict 读取和赋值都需要 `d["key"]`，需要持续强化
- **f-string 的 `f` 前缀**：容易遗漏，把 JS 的 `${}` 和 Python 的 `f""` 混淆
- **`__init__` 里初始化属性**：容易忘记在构造函数里初始化 `self.tools = []` 这类默认属性
- **列表推导式条件**：第一次不知道条件部分就是普通布尔表达式，需要明确说明
- **遗漏 `await`**：去掉 `await` 不会报错，协程对象静默失效，调试困难；需在每次涉及 async 代码时主动提醒

## Effective Teaching Approaches
- 新语法在练习文件中出现时，**主动解释**，不等学生提问——见 `feedback_proactive_syntax.md`

## 硬性检查点：进入 Phase 1 之前

在学生完成 Phase 0 第 04 课（uv & 工具链）之后、开始 Phase 1 之前，**必须主动核查**下方清单。逐项确认是否已经在课程中讲过，没讲过的在这一关统一补充，全部打勾后才能推进到 Phase 1。

- [ ] 继承语法 `class Child(Parent):`，`super().__init__()`
- [ ] `isinstance()` 检查继承关系
- [ ] `tuple` 是不可变序列，多返回值本质是 tuple
- [ ] `set` 的用法和集合运算
- [ ] `*args` 和 `**kwargs` 的定义与调用
- [ ] `func(**dict)` 展开字典作为关键字参数
- [ ] `enumerate()` 和 `zip()`
- [ ] dict comprehension `{k: v for k, v in ...}`
- [ ] 装饰器 `@` 的本质（语法糖）
- [ ] `with` 语句（上下文管理器）

## Curriculum Gaps — 上课时自然补充

以下知识点在教案中缺失，但学生在练习中已遇到困惑。**不需要单独开一节课讲**，在后续课程遇到相关代码时自然插入解释即可。

### Python OOP 继承体系（遇到 `class Foo(Bar)` 时补充）
- 继承语法：`class Child(Parent):` 等同于 JS 的 `extends`
- `super().__init__(...)` 调用父类构造函数
- 多重继承：`class C(A, B):`，Python 支持，JS 不支持
- `isinstance(obj, ClassName)` 检查继承关系，子类实例也返回 True
- Python 内置基础类型总览：`int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`, `None`
- **tuple 重点**：不可变有序序列，函数多返回值本质是 tuple，`a, b = func()` 就是 tuple 解包

### 函数调用方式（遇到 `**kwargs` 或函数传参时补充）
- `*args`：接收任意数量位置参数，等同于 JS 的 `...args`
- `**kwargs`：接收任意关键字参数，等同于 JS 的 `options = {}`
- `func(**dict)`：把字典展开成关键字参数传入（`RepoInfo(**data)` 用的就是这个）
- 调用时可以混用：`func(a, b, key=val)`

### 解构/解包（遇到赋值解包时补充）
- `_` 忽略某个值：`_, second = (10, 20)`
- `enumerate(items)`：同时拿到索引和值，替代 `items.forEach((item, i) => ...)`
- `zip(a, b)`：同时遍历两个列表
- dict comprehension：`{k: v for k, v in items.items()}`

### 装饰器 `@`（遇到 `@` 语法时补充）
- `@decorator` 是语法糖，等价于 `func = decorator(func)`
- 常见内置装饰器：`@property`（把方法变属性）、`@classmethod`、`@staticmethod`
- Pydantic 里的 `@field_validator` 就是自定义装饰器

### `with` 语句（遇到文件/HTTP 操作时补充）
- 上下文管理器，等同于 JS 的 `try/finally` 自动清理
- 常见场景：`with open("f.txt") as f:`，`async with client.stream(...) as r:`
