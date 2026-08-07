from uuid import UUID
import uuid
from typing import List
from pydantic import BaseModel, Field


class ResumeRepo(BaseModel):
    resume: str
    question: List[str]


class ResumeList(BaseModel):
    repositories: List[ResumeRepo]