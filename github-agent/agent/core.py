import json
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from .tools import TOOLS, TOOL_FUNCTIONS

load_dotenv()
client = AsyncAnthropic()

async def run_agent(user_message: str) -> str:
    """
    运行 Agent，接受用户问题，返回最终回答。
    """
    print(f"\n用户：{user_message}")
    print("-" * 40)

    messages = [{"role": "user", "content": user_message}]

    # Agent Loop
    step = 0
    while True:
        step += 1
        print(f"\n[Step {step}] 调用 LLM...")

        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
            system="你是一个 GitHub 仓库分析助手。使用提供的工具来获取信息，然后给出详细分析。"
        )

        # 把 LLM 回复加入历史
        messages.append({"role": "assistant", "content": response.content})

        # 判断下一步
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\n最终回答：\n{block.text}")
                    return block.text

        elif response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    print(f"  → 调用工具: {tool_name}({json.dumps(tool_input, ensure_ascii=False)})")

                    tool_fn = TOOL_FUNCTIONS.get(tool_name)
                    if tool_fn:
                        result = await tool_fn(**tool_input)
                    else:
                        result = {"error": f"未知工具: {tool_name}"}

                    print(f"  ← 工具结果: {json.dumps(result, ensure_ascii=False)[:100]}...")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            messages.append({"role": "user", "content": tool_results})

        else:
            print(f"  未知 stop_reason: {response.stop_reason}")
            break

    return "Agent 运行结束"
