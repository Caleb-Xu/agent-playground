from pydantic import BaseModel

class CommitSummary(BaseModel):
    sha: str
    author: str
    message: str

class RepoReport(BaseModel):
    repo_name: str
    stars: int
    primary_language: str
    description: str
    top_languages: list[str]
    recent_commits: list[CommitSummary]
    summary: str
