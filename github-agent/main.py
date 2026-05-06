import asyncio
from agent.core import run_agent
from agent.models import RepoReport

async def main():
    result = await run_agent("帮我分析一下 facebook/react 这个 GitHub 仓库")
    print("\n" + "=" * 40)
    if isinstance(result, RepoReport):
        print(f"仓库：{result.repo_name}")
        print(f"Stars：{result.stars}")
        print(f"主语言：{result.primary_language}")
        print(f"语言列表：{', '.join(result.top_languages)}")
        print(f"\n最近提交：")
        for c in result.recent_commits:
            print(f"  [{c.sha}] {c.author}: {c.message[:60]}")
        print(f"\n总结：{result.summary}")
    else:
        print(result)
    print("完成！")

asyncio.run(main())
