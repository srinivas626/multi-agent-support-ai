from app.rag.loader import load_documents
from app.rag.chunker import split_documents


documents = load_documents("data/documents")

print(f"Documents loaded: {len(documents)}")

chunks = split_documents(documents)

print(f"Chunks created: {len(chunks)}")

for i, chunk in enumerate(chunks):

    print("\n==============================")
    print(f"CHUNK {i + 1}")
    print("==============================")

    print(chunk.page_content)

