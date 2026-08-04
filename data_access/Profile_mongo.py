import uuid
from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional

from pydantic.v1 import UUID1

from data_access.Repository import Repository


class GitHubProfile(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    repository_url: list[Repository] = None
    followers: int = 0
    following: int = 0

