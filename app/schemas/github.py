from pydantic import BaseModel


class GitHubFiles(BaseModel):
    file: str
    content: str


class GitHubFilesResponse(BaseModel):
    files: list[GitHubFiles]
