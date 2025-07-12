from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, Field
from pinecone import Pinecone
from dotenv import load_dotenv
from app.core import WorkflowState
import os
import openai

load_dotenv()
# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))

try:
    indexes = pc.list_indexes()
    if not indexes:
        print("No indexes found in Pinecone")
        exit()

    index_name = indexes[0]["name"]
    index = pc.Index(index_name)
    print(f"Connected to index: {index_name}")

except Exception as e:
    print(f"Error connecting to Pinecone: {e}")
    exit()


def get_embedding(text, model="text-embedding-3-large"):
    try:

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(input=text, model=model)

        return response.data[0].embedding

    except Exception as e:
        print(f"OpenAI embedding error: {e}")
        return None


def get_relevant_docs(state: WorkflowState) -> WorkflowState:
    query_embedding = get_embedding(state.user_query.query)
    if query_embedding is None:
        return WorkflowState(error="Embedding generation failed.", user_query=state.user_query)

    try:
        results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True,
            include_values=False,
            namespace="__default__",
        )
    except Exception as e:
        print(f"Pinecone query error: {e}")
        return WorkflowState(error="Vector DB query failed.", user_query=state.user_query)

    if not results or not results["matches"]:
        return WorkflowState(error="No relevant documents found.", user_query=state.user_query)

    relevant_doc = results["matches"][0]["metadata"]["text"]

    return WorkflowState(arxiv_document=relevant_doc, user_query=state.user_query)

