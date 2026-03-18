# =============================================================================
# 练习 2：asyncio.gather 并发请求多个用户
# =============================================================================
#
# 目标：用 asyncio.gather 并发获取多个 GitHub 用户的仓库数量，
#       返回 {username: repo_count} 格式的字典。
#
# JS 对比：
#   async function analyzeMultipleUsers(usernames) {
#     const results = await Promise.all(usernames.map(u => getUserRepos(u)))
#     const counts = {}
#     usernames.forEach((u, i) => { counts[u] = results[i].length })
#     return counts
#   }
#
# Python asyncio.gather 就是 Promise.all 的等价物：
#   results = await asyncio.gather(coro1(), coro2(), coro3())
#
# 本练习的新知识点：
#   - asyncio.gather(*coroutines) 的用法（* 展开列表）
#   - return_exceptions=True 让部分失败不影响其他请求
#   - dict comprehension 或普通 for 循环构建结果字典
#   - isinstance(x, Exception) 检查某个结果是否是异常
# =============================================================================

import asyncio
import httpx
from exercise_01 import get_user_repos


# 直接复用练习 1 的函数（你可以直接把练习 1 的实现粘贴过来）
# async def get_user_repos(username: str) -> list[dict]:
#     """获取 GitHub 用户的仓库列表，出错返回空列表。"""
#     url = f"https://api.github.com/users/{username}/repos"
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, timeout=10.0)
#             response.raise_for_status()
#             return response.json()
#     except (httpx.TimeoutException, httpx.HTTPStatusError):
#         return []

async def analyze_multiple_users(usernames: list[str]) -> dict:
    """
    并发获取多个 GitHub 用户的仓库数量。

    Args:
        usernames: 用户名列表，例如 ["torvalds", "gvanrossum"]

    Returns:
        {username: repo_count} 的字典，例如 {"torvalds": 8, "gvanrossum": 30}

    提示步骤：
        1. 为每个 username 创建一个协程（coroutine），不要 await
        2. 用 asyncio.gather(*coroutines) 并发执行所有协程
        3. 遍历 usernames 和 results，构建结果字典
    """

    # Step 1：创建协程列表
    # 注意：这里不能写 await get_user_repos(u)，只是创建协程对象
    # JS 对比：Promise.all 里传的是 Promise 对象，不是已经 resolved 的值
    coroutines = [get_user_repos(u) for u in usernames]

    # Step 2：并发执行
    # asyncio.gather(*coroutines) 里的 * 是把列表展开成多个参数
    # 相当于 asyncio.gather(coro0, coro1, coro2, ...)
    # return_exceptions=True：某一个出错时，其他的继续执行，出错的那个结果是 Exception 对象
    results = await asyncio.gather(*coroutines, return_exceptions=True)

    # Step 3：构建结果字典
    # results 是列表，顺序和 usernames 一一对应
    # results[0] 对应 usernames[0]，results[1] 对应 usernames[1]，以此类推
    output = {}

    for i, username in enumerate(usernames):
        result = results[i]

        # 判断这个结果是否是异常
        if isinstance(result, Exception):
            # 出错了，记为 -1 或者 0，随你定
            print(f"Failed for {username}: {result}")
            output[username] = 0
        else:
            # result 是 list[dict]，仓库数量是 len(result)
            # 注意：output 是普通 dict，赋值用方括号：output["key"] = value
            output[username] = len(result)

    return output


async def main():
    usernames = ["torvalds", "gvanrossum", "yyx990803"]

    print("开始并发获取用户仓库数量...")
    counts = await analyze_multiple_users(usernames)

    print("\n结果：")
    # counts 是 dict，遍历时用 .items() 同时拿到 key 和 value
    # 注意：取 dict 的值用方括号：counts["key"]，但这里用循环解包更简洁
    for username, count in counts.items():
        print(f"  {username}: {count} repos")

    # 思考题：如果改成串行执行（不用 gather），代码要怎么写？时间会差多少？
    # 串行版本（注释掉，仅作对比参考）：
    # for username in usernames:
    #     repos = await get_user_repos(username)
    #     counts[username] = len(repos)


if __name__ == "__main__":
    asyncio.run(main())
