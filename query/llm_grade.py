import os
import sys

from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langsmith import Client
from langchain_openai import ChatOpenAI
from app.core import UserQuery, WorkflowState
from dotenv import load_dotenv
from typing import Optional, Union

load_dotenv()


client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
model = ChatOpenAI(model="gpt-4.1-2025-04-14", api_key=os.getenv("OPENAI_API_KEY"))
prompt = client.pull_prompt(
    "miracle/par_grading_documents_prompt_public", include_model=True
)

def llm_grade(state: WorkflowState)  -> WorkflowState:
    question = state.user_query.query
    documents = state.arxiv_document

    if documents is None or documents.strip() == "":
        return WorkflowState(grade="No", arxiv_document = "No relevant data found", user_query=state.user_query)

    chain = prompt | model
    output = chain.invoke({"documents": documents, "question": question}).content

    if output.startswith("yes"):
        return WorkflowState(source="arXiv", arxiv_document = documents, grade ="Yes", user_query=state.user_query)
    elif output.startswith("no"):
        grade = "No"
        return WorkflowState(grade="No", arxiv_document = documents, user_query=state.user_query)
