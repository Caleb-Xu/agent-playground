# Phase 1 - Lesson 01 复习测验
# 在下面每道题的空白处写你的答案，写完告诉老师
#
# 覆盖范围：Agent 基础概念（LLM + Tools + Loop）
# ============================================================


# ============================================================
# 第 1 题 — 发现 bug
# 下面这个 agent_loop 有一个逻辑 bug，导致循环永远不会结束。
# 找出问题所在，在注释里说明，并写出修正后的代码。
# ============================================================

async def agent_loop(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            tools=tools,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            for block in response.content:
                result = await execute_tool(block.name, block.input)
                messages.append({"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                ]})

# 你发现的 bug：
# 没有判断 response.stop_reason == "end_turn" 的场景

# 修正后的代码（只需写出缺失的部分即可）：
#
if response.stop_reason == "end_turn":
    return

# ============================================================
# 第 2 题 — 填空
# 根据描述，填写 stop_reason 的值
# ============================================================

# 场景 A：用户问"今天天气怎么样"，LLM 决定调用 get_weather 工具
# stop_reason = "tool_use"

# 场景 B：LLM 拿到天气数据后，直接回答"今天晴，25度"
# stop_reason = "end_turn"

# 场景 C：LLM 调用了 get_location 工具，拿到结果后又调用了 get_weather 工具，
#          最后说"根据你的位置，今天晴，25度"
# 第一次停止时 stop_reason = "tool_use"
# 第二次停止时 stop_reason = "tool_use"
# 第三次停止时 stop_reason = "end_turn"


# ============================================================
# 第 3 题 — 发现 bug
# 下面两个工具定义，哪一个写法在实际发给 LLM 时会有问题？
# 说明原因，不需要改代码。
# ============================================================

import requests

def search_web(query: str) -> str:
    # 假设调用了某个搜索 API
    return "搜索结果..."

# 工具定义 A
tool_a = {
    "name": "search_web",
    "description": "搜索互联网上的信息",
    "function": search_web,
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    }
}

# 工具定义 B
tool_b = {
    "name": "search_web",
    "description": "搜索互联网上的信息",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    }
}

# 有问题的是：工具定义 __A_
# 原因：多了不必要的 function 参数
#


# ============================================================
# 第 4 题 — 排序题
# messages 列表是 Agent 的"记忆"。
# 下面是一次完整交互后的 messages，但顺序被打乱了。
# 把正确的顺序写在注释里（用序号表示，例如：正确顺序是 1→3→2→4）
# ============================================================

messages = [
    # 1
    {"role": "user", "content": "帮我查一下 facebook/react 的 star 数"},

    # 2
    {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "xyz", "content": "stars: 230000"}
    ]},

    # 3
    {"role": "assistant", "content": "facebook/react 目前有 230,000 个 star。"},

    # 4
    {"role": "assistant", "content": [
        {"type": "tool_use", "id": "xyz", "name": "get_repo_info",
         "input": {"repo_name": "facebook/react"}}
    ]},
]

# 正确顺序是：1 → 4 → 2 → 3
#
