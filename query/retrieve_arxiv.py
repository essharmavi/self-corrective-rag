import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arxiv
from pydantic import BaseModel
from query.load_summaries import load_arxiv_data, chunk_summaries


def load_arxiv_documents(category):
    client = arxiv.Client()

    search_category = arxiv.Search(
        query=category,  
        max_results=25,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    summaries = [
        result.title + "\n" + result.summary
        for result in client.results(search_category)
    ]
    chunks = chunk_summaries(summaries)
    vector_store = load_arxiv_data(chunks)
    return vector_store
