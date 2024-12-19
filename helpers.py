from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_db_client():
    return Chroma(
        persist_directory="qovaDB",
        embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
        collection_name="online_safety_docs"
    )