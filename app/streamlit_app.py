import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core import UserQuery, WorkflowState
from app.categories_list import ARXIV_CATEGORIES
from query.retrieve_arxiv import load_arxiv_documents
from workflow.workflow import build_graph


st.title("🎓 Academic Research Assistant (Self-Corrective RAG)")

get_category = st.selectbox("Choose an arXiv Category:", ARXIV_CATEGORIES)


if get_category:
    if st.button("🔄 Load Papers from arXiv"):
        with st.spinner("📚 Fetching and indexing papers..."):
            load_arxiv_documents(get_category)
            st.success(f"Papers related to '{get_category}' loaded successfully.")


get_query = st.text_input("Now enter a specific query related to this area:")


if get_category and get_query:
    if st.button("🔍 Search for Answers"):
        with st.spinner("🤖 Searching relevant information..."):
            category=get_category.strip()
            query=get_query.strip()
            query_obj = UserQuery(category=category, query=query)
            initial_state = WorkflowState(user_query=query_obj)
            graph = build_graph()
            result = graph.invoke(initial_state)
            st.markdown("### 📄 Final Answer:")
            st.write(result['final_answer'])

            st.markdown("### 🔗 Source:")
            st.write(result['source'])