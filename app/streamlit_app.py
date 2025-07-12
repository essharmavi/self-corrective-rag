import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core import WorkflowState
from query.retrieve_arxiv import load_arxiv_documents
from workflow.workflow import build_graph


st.title("🎓 Academic Research Assistant (Self-Corrective RAG)")

get_category = st.text_input(
    "Enter your academic research area (e.g., Machine Learning):"
)


if get_category:
    if st.button("🔄 Load Papers from arXiv"):
        with st.spinner("📚 Fetching and indexing papers..."):
            load_arxiv_documents(get_category)
            st.success(f"Papers related to '{get_category}' loaded successfully.")


get_query = st.text_input("Now enter a specific query related to this area:")


if get_category and get_query:
    if st.button("🔍 Search for Answers"):
        with st.spinner("🤖 Searching relevant information..."):
            query_obj = UserQuery(category=get_category, query=get_query)
            initial_state = WorkflowState(user_query=query_obj)
            graph = build_graph()
            result = graph.invoke(initial_state)
            st.json(result if isinstance(result, dict) else result.dict())
            print(result)

            st.markdown("### 📄 Final Answer:")
            st.write(result.final_answer)

            st.markdown("### 🔗 Source:")
            st.write(result.source)