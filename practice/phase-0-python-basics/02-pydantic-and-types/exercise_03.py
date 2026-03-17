# 练习 3：从 JSON 解析数据，并验证能序列化回 JSON
#
# 把下面的 JSON 数据解析成 GitHubRepo 模型实例
# 然后验证能正确序列化回 JSON 字符串
#
# 提示：需要从 exercise_01.py 导入你定义的 GitHubRepo

import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from exercise_01 import GitHubRepo

data = {
    "name": "langchain",
    "owner": "langchain-ai",
    "stars": 75000,
    "language": "Python",
    "topics": ["ai", "llm", "agents"]
}

# TODO: 用 data 创建一个 GitHubRepo 实例
# TODO: 打印实例的各个字段
# TODO: 用 model_dump_json() 把它序列化成 JSON 字符串，打印出来
# TODO: 验证：把 JSON 字符串再解析回模型，确认数据没有丢失
repo = GitHubRepo.model_validate(data)
print(repo.name)
print(repo.stars)
print(repo.model_dump())
print(repo.model_dump_json())