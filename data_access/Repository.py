import uuid
from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional

from pydantic.v1 import UUID1


class Repository(BaseModel):
    id : UUID = Field(default_factory=uuid.uuid4)
    repo_url : str
    name : str
    description : str
    langaage : List[str]

class RepositoryList(BaseModel):
    repositories: List[Repository]