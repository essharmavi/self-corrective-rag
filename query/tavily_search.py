import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langchain_tavily import TavilySearch
from app.core import Summary, FinalAnswer
from dotenv import load_dotenv

load_dotenv()


def tavily_search(state: Summary) -> FinalAnswer:
    tool = TavilySearch(
        max_results=2, topic="general", tavily_api_key=os.getenv("TAVILY_API_KEY")
    )

    response = tool.invoke(state.user_query.query)

    all_content = " ".join([r["content"] for r in response["results"]])
    return FinalAnswer(final_answer=all_content, source="Tavily")
