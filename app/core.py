from pydantic import BaseModel, Field
from typing import Literal

class UserQuery(BaseModel):
    category: str = Field(description="Enter Research Area Category")
    query: str = Field(description="Enter user query based on the category selected")


class Summary(BaseModel):
    user_query: UserQuery = Field(description="User Query and Category entered")
    relevant_doc: str = Field(description="Retreiver relevant document")

class Grade(BaseModel):
    grade: str = Literal["Yes", "No"]

class FinalAnswer(BaseModel):
    final_answer: str = Field(description="Final answer to be shown to the user")
    source: str = Field(default="Unknown", description="Source for the answer")
