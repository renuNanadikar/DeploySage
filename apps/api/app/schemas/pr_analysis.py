from pydantic import BaseModel


class PRAnalyzeRequest(BaseModel):
    repository_owner: str
    repository_name: str
    pr_number: int
    pr_title: str
    diff: str


class PRAnalyzeResponse(BaseModel):
    generated_title: str
    generated_description: str
    provider: str
    github_ready: bool

#Schemas validate request and response data. They make the API predictable and generate automatic docs.#