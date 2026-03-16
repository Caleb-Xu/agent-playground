repos = ["react", "langchain", "ai", "anthropic", "vue"]
# 过滤出长度大于 5 的项
# 期望输出：["langchain", "anthropic"]
result = [x for x in repos if len(x) > 5]

print(result)
