import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langsmith import Client
from langchain_openai import ChatOpenAI
from app.core import WorkflowState, Grade
from dotenv import load_dotenv
from typing import Union

load_dotenv()


client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
model = ChatOpenAI(model="gpt-4.1-2025-04-14", api_key=os.getenv("OPENAI_API_KEY"))
prompt = client.pull_prompt(
    "miracle/par_grading_documents_prompt_public", include_model=True
)

class WorkflowState(BaseModel):
    user_query: UserQuery
    document: Optional[str] = None
    grade: Optional[str] = None
    final_answer: Optional[str] = None
    source: Optional[str] = None


def llm_grade(state: WorkflowState)  -> WorkflowState:
    question = state.user_query.query
    documents = state.document
    if documents is None or documents.strip() == "":
        return WorkflowState(grade="No", document = "No relevant data found")

    chain = prompt | model
    output = chain.invoke({"documents": documents, "question": question}).content
    print(output)
    if output.startswith("yes"):
        return WorkflowState(final_answer=documents, source="arXiv", document = documents, grade ="Yes")
    elif output.startswith("no"):
        grade = "No"
        return WorkflowState(grade="No", document = documents)
