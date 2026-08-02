from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
import uuid
from .Profile_mongo import GitHubProfile
class JobDescription(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    jobDescription: str
    tech : Optional[str]
    profile : Optional[GitHubProfile]