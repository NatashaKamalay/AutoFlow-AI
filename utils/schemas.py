from pydantic import BaseModel, Field
from typing import List, Optional


class TaskItem(BaseModel):
    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None


class MeetingAnalysis(BaseModel):
    summary: str
    decisions: List[str] = Field(default_factory=list)
    tasks: List[TaskItem] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)