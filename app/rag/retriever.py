from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embeddings


def get_vectorstore():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        "data/vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search_documents(question: str, k: int = 3):

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    return results
