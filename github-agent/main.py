import asyncio
from agent.core import run_agent

async def main():
    result = await run_agent("帮我分析一下 facebook/react 这个 GitHub 仓库")
    print("\n" + "=" * 40)
    print("完成！")

asyncio.run(main())
