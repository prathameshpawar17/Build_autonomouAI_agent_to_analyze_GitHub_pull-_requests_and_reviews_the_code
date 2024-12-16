from pydantic import BaseModel

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str

class AnalysisResults(BaseModel):
    task_id: str
    status: str
    results: dict
