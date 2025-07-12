from pydantic import BaseModel, Field
from typing import Literal, Optional

class UserQuery(BaseModel):
    category: str = Field(description="Enter Research Area Category")
    query: str = Field(description="Enter user query based on the category selected")

class Grade(BaseModel):
    grade: str = Literal["Yes", "No"]

class FinalAnswer(BaseModel):
    final_answer: str = Field(description="Final answer to be shown to the user")
    source: str = Field(default="Unknown", description="Source for the answer")

class WorkflowState(BaseModel):
    user_query: UserQuery
    document: Optional[str] = None
    grade: Optional[Grade] = None
    final_answer: Optional[str] = None
    source: Optional[str] = None
