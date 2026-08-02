from pydantic import BaseModel
from typing import List
class TechStack(BaseModel):
    tech_stac : List[str]

