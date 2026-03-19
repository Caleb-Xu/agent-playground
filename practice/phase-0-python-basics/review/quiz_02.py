# Phase 0 复习测验 — asyncio
# 直接在下面每道题的 ??? 或代码块里写你的答案，不要运行，写完告诉老师

# ============================================================
# 第 1 题 — async/await 基础
# 下面代码能正常运行吗？有问题的话说明原因并改正
# ============================================================

import asyncio

async def greet(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"Hello, {name}!"

result = greet("Alice")
print(result)

# 你的答案：不能，调用greet时没有使用asyncio.run


# ============================================================
# 第 2 题 — asyncio.gather
# 用 asyncio.gather 并发执行下面三个协程，把结果打印出来
# 期望结果类似：["result_a", "result_b", "result_c"]
# ============================================================

async def task_a():
    await asyncio.sleep(0.1)
    return "result_a"

async def task_b():
    await asyncio.sleep(0.1)
    return "result_b"

async def task_c():
    await asyncio.sleep(0.1)
    return "result_c"

async def main():
    results = ???
    print(results)

asyncio.run(main())

# 你的答案（填写 ??? 的内容）：asyncio.gather(task_a(), task_b(), task_c())


# ============================================================
# 第 3 题 — 异步 vs 同步 sleep
# 回答：下面两段代码各需要大约多长时间？为什么？
# ============================================================

# 代码 A
async def code_a():
    await asyncio.sleep(1)
    await asyncio.sleep(1)

# 代码 B
async def code_b():
    await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1),
    )

# 代码 A 耗时：2s，原因：异步任务串行
# 代码 B 耗时：1s，原因：异步任务并行


# ============================================================
# 第 4 题 — await 遗漏
# 下面代码有 bug 吗？有的话说明会发生什么
# ============================================================

async def fetch():
    await asyncio.sleep(0.5)
    return "data"

async def broken():
    result = fetch()   # 注意这里没有 await
    print(result)

# 你的答案：执行fetch()会触发运行时错误，但是print会打印什么我不太清楚


# ============================================================
# 第 5 题 — enumerate
# 用 enumerate 打印出带序号的列表，格式如下：
# 0: apple
# 1: banana
# 2: cherry
# ============================================================

fruits = ["apple", "banana", "cherry"]

# 你的答案：
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")