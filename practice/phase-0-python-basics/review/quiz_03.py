# Phase 0 综合复习测验 — 进入 Phase 1 前的最终检查
# 覆盖范围：Pydantic / asyncio / Python OOP / 前置知识点
# 直接在下面每道题的 ??? 或代码块里写你的答案，写完告诉老师
# 不用运行代码，直接写出你的判断和答案

# ============================================================
# 第 1 题 — 发现 bug
# 下面的 Pydantic 模型有问题吗？找出所有问题并说明原因
# ============================================================

from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    name: str
    age: int
    email: Optional[str]
    tags: list = []

# 你的答案：错误，email没有设置默认值



# ============================================================
# 第 2 题 — 填空
# 用 *args 和 **kwargs 完成下面的函数
# 要求：打印所有位置参数，再打印所有关键字参数
# 示例调用：log("error", "timeout", level="WARN", code=500)
# 期望输出：
#   位置参数: ('error', 'timeout')
#   关键字参数: {'level': 'WARN', 'code': 500}
# ============================================================

# def log(???):
#     print(f"位置参数: {???}")
#     print(f"关键字参数: {???}")

# 你的答案（把 ??? 替换掉）：
def log(*args, **kwargs):
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")



# ============================================================
# 第 3 题 — 发现 bug
# 下面代码会输出什么？有没有 bug？
# ============================================================

import asyncio

async def load_data():
    await asyncio.sleep(0.1)
    return {"items": [1, 2, 3]}

async def process():
    data = load_data()   # 注意这里
    print(data["items"])

asyncio.run(process())

# 你的答案：有bug，执行load_data的时候没有使用await



# ============================================================
# 第 4 题 — 设计题
# 用 dict comprehension 完成下面的转换：
# 输入：[("apple", 3), ("banana", 5), ("cherry", 1)]
# 输出：{"apple": 3, "banana": 5, "cherry": 1}  (只保留数量 >= 2 的)
# ============================================================

items = [("apple", 3), ("banana", 5), ("cherry", 1)]

# result = ???

# 你的答案：
result = {}

for (fruit, number) in items:
    if number >= 2:
        result[fruit] = number


# ============================================================
# 第 5 题 — 概念题
# 用一句话解释下面两个概念的区别：
# (a) asyncio.gather vs 串行 await
# (b) Pydantic BaseModel vs 普通 Python class
# ============================================================

# (a) 你的答案：前者是并行，后者是串行

# (b) 你的答案：前者提供了类型检查能力，后者没有


# ============================================================
# 第 6 题 — 填空（装饰器）
# 下面是一个计时装饰器的骨架，把 ??? 补全
# 要求：打印函数执行耗时（用 time.time() 前后相减）
# ============================================================

# import time

# def timer(func):
#     async def wrapper(*args, **kwargs):
#         start = time.time()
#         result = ???          # 调用原函数，注意它是 async 的
#         elapsed = ???         # 计算耗时
#         print(f"{func.__name__} 耗时: {elapsed:.3f}s")
#         return result
#     return wrapper

# @timer
# async def slow_task():
#     await asyncio.sleep(0.2)
#     return "done"

# 你的答案（把 ??? 替换掉）：

import time

def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func()          # 调用原函数，注意它是 async 的
        elapsed = time.time() - start         # 计算耗时
        print(f"{func.__name__} 耗时: {elapsed:.3f}s")
        return result
    return wrapper

@timer
async def slow_task():
    await asyncio.sleep(0.2)
    return "done"
