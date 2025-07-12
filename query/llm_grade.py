import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langsmith import Client
from langchain_openai import ChatOpenAI
from app.core import Summary, Grade, UserQuery, FinalAnswer
from dotenv import load_dotenv
from typing import Union

load_dotenv()


client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
model = ChatOpenAI(model="gpt-4.1-2025-04-14", api_key=os.getenv("OPENAI_API_KEY"))
prompt = client.pull_prompt(
    "miracle/par_grading_documents_prompt_public", include_model=True
)


def llm_grade(state: Summary)  -> Union[Grade, FinalAnswer]:
    question = state.user_query.query
    documents = state.relevant_doc

    chain = prompt | model
    output = chain.invoke({"documents": documents, "question": question}).content
    print(output)
    if output.startswith("yes"):
        return FinalAnswer(final_answer=documents, source="arXiv")
    elif output.startswith("no"):
        grade = "No"
        return Grade(grade=grade)
