import json
import os
from .models import RepoReport
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from .tools import TOOLS, TOOL_FUNCTIONS

load_dotenv()
client = AsyncAnthropic()

async def run_agent(user_message: str, max_steps: int = 10) -> RepoReport | str:
    """
    运行 Agent，接受用户问题，返回最终回答。
    """
    print(f"\n用户：{user_message}")
    print("-" * 40)

    messages = [{"role": "user", "content": user_message}]

    # Agent Loop
    step = 0
    while step < max_steps:
        step += 1
        print(f"\n[Step {step}/{max_steps}] 调用 LLM...")

        response = await client.messages.create(
            model=os.environ.get("ANTHROPIC_DEFAULT_MODEL"),
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
            system = """
                你是一个 GitHub 仓库分析助手。使用提供的工具获取信息后，
                你必须以 JSON 格式输出最终报告，不要输出任何其他文字。

                JSON 格式如下：
                {
                "repo_name": "owner/repo",
                "stars": 12000,
                "primary_language": "TypeScript",
                "description": "仓库描述",
                "top_languages": ["TypeScript", "JavaScript"],
                "recent_commits": [
                    {"sha": "abc1234", "author": "张三", "message": "fix: 修复登录问题"}
                ],
                "summary": "一段 2-3 句话的综合分析"
                }
            """
        )

        print(f"  token 用量: input={response.usage.input_tokens}, output={response.usage.output_tokens}")

        # 把 LLM 回复加入历史
        messages.append({"role": "assistant", "content": response.content})

        # 判断下一步
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text") and block.text.strip():
                    data = json.loads(block.text)
                    report = RepoReport(**data)
                    return report

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
