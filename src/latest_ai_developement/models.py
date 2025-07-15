from pydantic import BaseModel, Field
from typing import List

class AMLReport(BaseModel):
    topic: str
    total_permutations: int
    total_queries: int
    summary: str
