# 练习 2：定义 AgentStep 模型
#
# 字段要求：
#   - step_number: 整数
#   - thought: 字符串（Agent 的思考过程）
#   - action: 可选字符串（要执行的工具名）
#   - action_input: 可选字典（工具的输入参数）
#   - observation: 可选字符串（工具执行结果）

from pydantic import BaseModel
from typing import Optional, Any

# TODO: 在这里定义 AgentStep 模型
class AgentStep(BaseModel):
    step_number: int
    thought: str
    action: Optional[str] = None
    action_input: Optional[dict] = None
    observation: Optional[str] = None

# 测试代码（完成模型后取消注释）
step = AgentStep(
    step_number=1,
    thought="我需要搜索这个仓库的信息",
    action="search_github",
    action_input={"query": "langchain"},
)
print(step)
print(step.model_dump())
