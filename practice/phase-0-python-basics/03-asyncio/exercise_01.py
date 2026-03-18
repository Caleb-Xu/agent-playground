# =============================================================================
# 练习 1：异步 HTTP 请求 + 错误处理
# =============================================================================
#
# 目标：写一个异步函数，调用 GitHub API 获取某个用户的仓库列表。
#
# JS 对比：
#   async function getUserRepos(username) {
#     const response = await fetch(`https://api.github.com/users/${username}/repos`)
#     if (!response.ok) throw new Error(`HTTP ${response.status}`)
#     return await response.json()
#   }
#
# Python 版本要求：
#   - 用 httpx.AsyncClient 代替 fetch
#   - 用 async with 管理 client 生命周期
#   - 加上超时和 HTTP 错误处理
#   - 用 asyncio.run() 从同步代码启动
#
# 注意事项（常见坑）：
#   1. f-string 别忘了前面的 f，写成 f"...{username}..." 而不是 "...{username}..."
#   2. dict 的值要用方括号取：data["key"]，不是 data.key
#   3. 函数定义要写 async def，调用时要 await
# =============================================================================

import asyncio
import httpx


async def get_user_repos(username: str) -> list[dict]:
    """
    获取 GitHub 用户的仓库列表。

    Args:
        username: GitHub 用户名，例如 "torvalds"

    Returns:
        仓库信息的列表，每个元素是一个 dict。
        如果出错则返回空列表。
    """
    # 提示：URL 是 https://api.github.com/users/{username}/repos
    # 别忘了 f-string 的 f 前缀！
    url = f"https://api.github.com/users/{username}/repos"

    try:
        # async with 相当于 JS 里的 try/finally 自动关闭连接
        # 参数 timeout=10.0 设置 10 秒超时
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)

            # raise_for_status() 会在非 2xx 状态码时抛出异常
            # 相当于 JS 里的 if (!response.ok) throw new Error(...)
            response.raise_for_status()

            # response.json() 返回解析后的 Python 对象（list[dict]）
            return response.json()

    except httpx.TimeoutException:
        # 超时处理：打印提示，返回空列表
        print(f"Timeout: {url}")
        return []

    except httpx.HTTPStatusError as e:
        # HTTP 错误处理：打印状态码
        # e.response.status_code 是状态码，e.request.url 是请求的 URL
        # 注意：dict 的值要用方括号，但这里 e.response.status_code 是对象属性，用点语法
        print(f"HTTP error {e.response.status_code}: {url}")
        return []


async def main():
    # 测试：获取 torvalds 的仓库
    repos = await get_user_repos("torvalds")

    # repos 是 list[dict]，每个 dict 代表一个仓库
    # 打印仓库数量
    print(f"Found {len(repos)} repos")

    # 打印前 5 个仓库的名称
    # 提示：仓库名在每个 dict 的 "name" 键里
    # 注意：用方括号取值：repo["name"]，不是 repo.name
    for repo in repos[:5]:
        print(f"  - {repo['name']}")  # 填入正确的键名


if __name__ == "__main__":
    # asyncio.run() 是从同步代码启动异步程序的唯一正确方式
    # 相当于 Node.js 里不需要写这行，因为 Node 自己就是异步运行时
    asyncio.run(main())
