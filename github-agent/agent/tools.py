import httpx
from typing import Any

# --- 工具定义（给 LLM 看的 JSON Schema）---
TOOLS = [
    {
        "name": "get_repo_info",
        "description": "获取 GitHub 仓库的基本信息，包括语言、star 数、描述等",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "仓库全名，格式：owner/repo，例如：facebook/react"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_repo_languages",
        "description": "获取仓库使用的编程语言及其代码行数占比",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "仓库全名，格式：owner/repo"
                }
            },
            "required": ["repo_name"]
        }
    }
]

# --- 工具实现（真正执行的函数）---
async def get_repo_info(repo_name: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_name}",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        if response.status_code == 404:
            return {"error": f"仓库 {repo_name} 不存在"}
        data = response.json()
        return {
            "name": data["full_name"],
            "description": data.get("description", ""),
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "language": data.get("language", "Unknown"),
            "topics": data.get("topics", []),
            "created_at": data["created_at"]
        }

async def get_repo_languages(repo_name: str) -> dict[str, int]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo_name}/languages"
        )
        return response.json()

# 工具名 → 函数 的映射（用于 agent 执行时查找）
TOOL_FUNCTIONS = {
    "get_repo_info": get_repo_info,
    "get_repo_languages": get_repo_languages,
}
