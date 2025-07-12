from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))


def chunk_summaries(texts):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))
    return chunks


def load_arxiv_data(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]

    index_name = "arxiv-summaries"
    if index_name in [i.name for i in pc.list_indexes()]:
        pc.delete_index(index_name)

    pc.create_index(
        name=index_name,
        dimension=3072,
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    index = pc.Index(host=pc.list_indexes()[0]["host"])
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    batch_size = 25
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        vector_store.add_documents(batch)

    return vector_store
