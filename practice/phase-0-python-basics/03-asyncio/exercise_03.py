# =============================================================================
# 练习 3：流式处理——边获取边打印
# =============================================================================
#
# 目标：修改获取 repos 的逻辑，改为流式打印——每获取到一个 repo 立刻打印，
#       而不是等全部加载完再打印。
#
# 注意：GitHub API 实际上是一次性返回整个 JSON，不支持真正的流式传输。
# 本练习用 asyncio.sleep 模拟"逐个处理"的效果，让你理解流式处理的思维模式。
# 这个模式在后面用 LLM 流式 API 时会完全一样。
#
# JS 对比（Node.js 流式处理）：
#   async function* streamRepos(username) {
#     const repos = await getUserRepos(username)
#     for (const repo of repos) {
#       await delay(50)  // 模拟处理延迟
#       yield repo
#     }
#   }
#   for await (const repo of streamRepos("torvalds")) {
#     console.log(repo.name)
#   }
#
# Python 里用 async for 遍历"异步生成器"（async generator）实现同样效果。
#
# 本练习新知识点：
#   - async for：遍历异步可迭代对象（相当于 JS 的 for await...of）
#   - asyncio.sleep(n)：异步等待 n 秒，不阻塞 event loop（对比：time.sleep 会阻塞）
#   - end="" 和 flush=True 参数：控制 print 的行为（不换行、立刻输出）
# =============================================================================

import asyncio
import httpx
from exercise_01 import get_user_repos


async def stream_repos(username: str):
    """
    流式打印用户仓库名称——每处理一个就立刻打印。

    用 asyncio.sleep(0.05) 模拟每个 repo 的处理延迟，
    演示"边处理边输出"的效果，不等所有数据加载完毕。

    这个模式和后面调用 LLM streaming API 完全一样：
        async for chunk in stream.text_stream:
            print(chunk, end="", flush=True)

    Args:
        username: GitHub 用户名
    """
    print(f"开始获取 {username} 的仓库...")

    # Step 1：获取所有仓库（这一步一次性完成）
    repos = await get_user_repos(username)

    if not repos:
        print(f"没有找到 {username} 的仓库，或请求失败")
        return

    print(f"共 {len(repos)} 个仓库，开始逐个处理：\n")

    # Step 2：逐个处理，模拟流式输出
    for i, repo in enumerate(repos):
        # asyncio.sleep 是异步等待，不会阻塞整个程序
        # 对比：time.sleep(0.05) 会冻结整个 event loop
        await asyncio.sleep(0.05)

        # 取出仓库名称和描述
        # 注意：repo 是 dict，取值要用方括号
        name = repo['name']

        # description 可能是 None（没有描述）
        # 用 or "" 提供默认值，和 JS 的 repo.description || "" 一样
        description = repo['description'] or "(无描述)"

        # print 的 flush=True 参数：立刻刷新输出缓冲区，确保立刻显示
        # 没有 flush=True 的话，输出可能会积累在缓冲区里，不会立刻出现
        print(f"[{i + 1:2d}] {name}: {description}", flush=True)

    print(f"\n处理完毕！")


async def compare_sync_vs_async():
    """
    演示 asyncio.sleep vs time.sleep 的区别。
    （选做：理解了再做）
    """
    import time

    print("=== 演示异步 sleep vs 同步 sleep ===\n")

    # 异步版本：两个任务同时等待，总时间约 1 秒
    print("异步版本（两个任务并发等待）：")
    start = time.time()

    async def task(name: str, seconds: float):
        print(f"  {name} 开始等待 {seconds}s")
        await asyncio.sleep(seconds)  # 异步等待，不阻塞
        print(f"  {name} 完成")

    await asyncio.gather(
        task("任务A", 1.0),
        task("任务B", 1.0),
    )

    elapsed = time.time() - start
    print(f"  总耗时：{elapsed:.2f}s（应该约 1s，两个任务并发）\n")

    # 如果用 time.sleep，两个任务会串行，总时间约 2 秒
    # （这里不演示，避免阻塞，你可以自己试试）
    print("如果换成 time.sleep(1)，总耗时会是约 2s（因为会阻塞 event loop）")


async def main():
    # 主练习：流式打印 torvalds 的仓库
    await stream_repos("torvalds")

    print("\n" + "=" * 50 + "\n")

    # 选做：运行对比演示
    await compare_sync_vs_async()


if __name__ == "__main__":
    asyncio.run(main())
