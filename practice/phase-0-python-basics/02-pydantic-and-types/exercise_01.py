# 练习 1：定义 GitHubRepo Pydantic 模型
#
# 字段要求：
#   - name: 字符串，1-100 字符
#   - owner: 字符串
#   - stars: 整数，最小 0
#   - language: 可选字符串，默认 None
#   - topics: 字符串列表，默认空列表
#   - is_fork: 布尔值，默认 False
#
# 完成后运行：python practice/phase-0-python-basics/02-pydantic-and-types/exercise_01.py

from pydantic import BaseModel, Field
from typing import Optional

# TODO: 在这里定义 GitHubRepo 模型
class GitHubRepo(BaseModel):
    name: str = Field(min_length = 1, max_length = 100)
    owner: str
    stars: int = Field(ge = 0)
    language: Optional[str] = None
    topics: list[str] = []
    is_fork: bool = False

# 测试代码（完成模型后取消注释）
if __name__ == "__main__":
    repo = GitHubRepo(name="langchain", owner="langchain-ai", stars=75000)
    print(repo)
    print(repo.model_dump())

