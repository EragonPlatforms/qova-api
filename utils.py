from helpers import get_db_client


def retrieve_rag_query(query: str, k: int = 5, style: str = "informal", language: str = "english"):
    retrieved_docs = get_db_client().similarity_search(query=query, k=k)
    retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    retrieved_docs_text_str = "\n".join(retrieved_docs_text)

    query_and_context = (
        "These docs can help you with your questions. If you have no answer, simply say 'I have no answer'."
        f"Question: {query}\n"
        f"Relevant docs: {retrieved_docs_text_str}"
    )

    return [
        ("system", f"""You are an expert assistant providing information strictly based on the context provided
        to you. Your task is to answer questions or provide information only using the details given in the current
        context. Do not reference any external knowledge or information not explicitly mentioned in the context.
        If the context does not contain sufficient information to answer a question, clearly state that the
        information is not available in the provided context. Always keep your answers to not more than 100 words.
        You should answer in a {style} style and in {language} language."""),
        ("human", query_and_context)
    ]
