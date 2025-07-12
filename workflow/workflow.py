from langgraph.graph import START, END, StateGraph
from app.core import WorkflowState
from query.tavily_search import tavily_search
from query.llm_grade import llm_grade
from query.retreive_relevant_docs import get_relevant_docs
from query.generate_answer_node import generate_answer_node

def router_node(state: WorkflowState) -> str:
    if state.grade  == "Yes":
        return "generate_answer"
    else:
        return "tavily_search"




def build_graph():
    flow = StateGraph(WorkflowState)
    flow.add_node("get_relevant_docs", get_relevant_docs)
    flow.add_node("llm_grading", llm_grade)
    flow.add_node("tavily_search", tavily_search)
    flow.add_node("generate_answer_node", generate_answer_node)

    flow.set_entry_point("get_relevant_docs")
    flow.add_edge("get_relevant_docs", "llm_grading")

    flow.add_conditional_edges("llm_grading", router_node, {
        "generate_answer": "generate_answer_node",
        "tavily_search": "tavily_search"
    })

    flow.add_edge("tavily_search", "generate_answer_node")
    flow.add_edge("generate_answer_node", END)

    return flow.compile()
