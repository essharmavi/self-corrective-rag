from pydantic import BaseModel, Field
from typing import Literal, Optional

class UserQuery(BaseModel):
    category: str = Field(description="Enter Research Area Category")
    query: str = Field(description="Enter user query based on the category selected")


class WorkflowState(BaseModel):
    user_query: UserQuery
    arxiv_document: Optional[str] = None
    grade: Optional[str] = None
    tavily_summary: Optional[str] = None
    final_answer: Optional[str] = None
    source: Optional[str] = None
