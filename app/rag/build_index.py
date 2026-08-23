from app.rag.loader import load_documents
from app.rag.chunker import split_documents
from app.rag.vectorstore import (
    create_vectorstore,
    save_vectorstore
)


documents = load_documents("data/documents")

print(f"Loaded documents: {len(documents)}")


chunks = split_documents(documents)

print(f"Created chunks: {len(chunks)}")


vectorstore = create_vectorstore(chunks)

save_vectorstore(vectorstore)

print("FAISS vector database created successfully.")
