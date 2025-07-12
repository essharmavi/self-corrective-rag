import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core import UserQuery, WorkflowState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer_node(state: WorkflowState) -> WorkflowState:
    source = state.source
    if source == "arXiv":
        summary = state.arxiv_document
    else:
        summary = state.tavily_summary

    prompt = (
        "You are an academic research assistant. "
        "Given the following summary, rewrite it in a more polished, crsip, short, clear, and academic tone.\n\n"
        f"### Raw Summary:\n{summary}\n\n"
        "### Polished Answer:"
    )

    polished_output = llm.invoke(prompt).content.strip()
    state.final_answer = polished_output
    return state
