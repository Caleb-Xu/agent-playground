# Phase 0 复习测验
# 直接在下面每道题的 ??? 或代码块里写你的答案，不要运行，写完告诉老师

# ============================================================
# 第 1 题 — dict 操作
# 下面代码有没有问题？有的话在下方写出改正后的版本
# ============================================================

user = {"name": "Alice", "score": 95}
print(user.name)
user.score = 100
print(user.score)

# 你的答案（改正后的代码）：
user = {"name": "Alice", "score": 95}
print(user["name"])
user["score"] = 100
print(user["score"])


# ============================================================
# 第 2 题 — f-string
# 把下面这行改成正确的 Python f-string 写法
# ============================================================

name = "Bob"
age = 30
message = "用户 ${name} 今年 ${age} 岁"

# 你的答案：
# message = ???
message = f"用户 {name} 今年 {age} 岁"

# ============================================================
# 第 3 题 — 列表推导式
# 一行代码，筛选出分数 >= 80 的同学名字
# 期望结果：["Alice", "Charlie"]
# ============================================================

students = [
    {"name": "Alice", "score": 92},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 88},
    {"name": "Diana", "score": 60},
]

passed = [x["name"] for x in students if x["score"] >= 80]


# ============================================================
# 第 4 题 — Pydantic 模型
# 下面代码有 bug 吗？有的话在注释里说明，或者直接改代码
# ============================================================

from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    age: int
    bio: str = ""

profile = UserProfile(name="Alice", age=25)
print(profile.name)
print(profile.bio)

# 你的答案（说明 bug 或写"没有 bug"）：没有bug

# ============================================================
# 第 5 题 — Pydantic 验证
# 定义 Product 模型，并在注释里回答：传入 price=-5 时会发生什么？
# ============================================================

# 你的 Product 模型：

from pydantic import Field
class Product(BaseModel):
    name: str
    price: float = Field(gt=0)


# 传入 price=-5 时 Pydantic 会：报错
