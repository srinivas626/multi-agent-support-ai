from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embeddings


def create_vectorstore(chunks):

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore


def save_vectorstore(vectorstore, path="data/vectorstore"):

    vectorstore.save_local(path)
