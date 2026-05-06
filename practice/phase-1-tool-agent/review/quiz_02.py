# Phase 1 - Lesson 02 复习测验（第二份）
# 覆盖范围：get_recent_commits 实现 + 错误处理 + 工具注册
# 完成后告诉老师，我来批改
# ============================================================


# ============================================================
# 第 1 题 — 发现 bug
# 下面的工具函数有一个潜在问题，会在某些情况下让 Agent 崩溃。
# 找出问题并说明会在什么情况下触发。
# ============================================================

async def get_recent_commits(repo_name: str, per_page: int = 5) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_name}/commits?per_page={per_page}"
        )
        return [commit["sha"][:7] for commit in response.json()]

# 你的说明： 看不出来，是response.json()不是数组的时候吗？
#


# ============================================================
# 第 2 题 — 填空
# 下面代码执行工具时，空白处应该填什么？为什么不能直接传 tool_input？
# ============================================================

async def execute_tool(tool_name: str, tool_input: dict):
    tool_fn = TOOL_FUNCTIONS.get(tool_name)
    if tool_fn:
        result = await tool_fn(____________)  # 填空
    else:
        result = {"error": f"未知工具: {tool_name}"}
    return result

# 你的答案：
# 填空处：**tool_input
# 原因：因为tool_input需要展开才能匹配到命名的参数


# ============================================================
# 第 3 题 — 概念题
# Agent Loop 里，messages 列表会随着对话不断增长。
# 请描述：当 LLM 调用了一次工具之后，messages 里会新增几条记录？
# 分别是什么角色（role）和内容？
# ============================================================

# 你的答案：
# 两条： assistant 的 tool_use，然后是 user 的 tool_results


# ============================================================
# 第 4 题 — 设计题
# 假设你要给 Agent 加一个新工具 get_repo_contributors，
# 需要改动哪几个地方？每个地方改什么？（不需要写完整代码，列出步骤即可）
# ============================================================

# 你的答案：
# 两个地方，TOOLS增加新工具的表述对象，TOOL_FUNCTIONS增加工具函数的引用


# ============================================================
# 第 5 题 — 开放题
# 当前的 Agent Loop 是一个无限 while True 循环。
# 你觉得这会带来什么风险？你会怎么改进它？
# ============================================================

# 你的答案：风险在于用户的token和余额会被烧完，加一个门控，以请求次数或者消费token为判断条件，中止循环，向用户反馈当前的状态
#
