# 练习：uv & 工具链
#
# 任务：
# 1. 用 uv add 安装 rich（一个终端美化库）
# 2. 在下面写代码，用 rich 打印一个表格，包含以下数据：
#
#    | 包名    | 版本   | 用途           |
#    |---------|--------|----------------|
#    | pydantic| 2.x    | 数据验证       |
#    | httpx   | 0.28.x | 异步 HTTP 请求 |
#    | rich    | latest | 终端美化       |
#
# 提示：
#   from rich.table import Table
#   from rich import print
#   table = Table(title="项目依赖")
#   table.add_column("包名")
#   table.add_column("版本")
#   table.add_column("用途")
#   table.add_row("pydantic", "2.x", "数据验证")
#   print(table)
#
# 3. 运行：uv run practice/phase-0-python-basics/04-uv-toolchain/exercise_01.py

# 在这里写代码

from rich.table import Table
from rich import print
table = Table(title="项目依赖")
table.add_column("包名")
table.add_column("版本")
table.add_column("用途")
table.add_row("pydantic", "2.x", "数据验证")
table.add_row("httpx", "0.28.x", "异步 HTTP 请求")
table.add_row("rich", "latest", "终端美化")
print(table)