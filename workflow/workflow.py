from langgraph.graph import START, END, StateGraph
from app.core import UserQuery, Grade, FinalAnswer, Summary
from query.tavily_search import tavily_search
from query.llm_grade import llm_grade
from query.retreive_relevant_docs import get_relevant_docs

def router_node(state):
    if isinstance(state, FinalAnswer):
        return "END"
    elif isinstance(state, Grade):
        return "tavily_search"
    else:
        return "tavily_search"

def build_graph():
    flow = StateGraph(UserQuery)

    flow.add_node("get_relevant_docs", get_relevant_docs)
    flow.add_node("llm_grading", llm_grade)
    flow.add_node("tavily_search", tavily_search)

    flow.set_entry_point("get_relevant_docs")
    flow.add_edge("get_relevant_docs", "llm_grading")

    flow.add_conditional_edges("llm_grading", router_node, {
        "END": END,
        "tavily_search": "tavily_search"
    })

    flow.add_edge("tavily_search", END)

    return flow.compile()
