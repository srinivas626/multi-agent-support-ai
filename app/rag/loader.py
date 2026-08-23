from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


def load_documents(directory: str):
    documents = []

    directory_path = Path(directory)

    for file in directory_path.glob("*"):

        if file.suffix.lower() == ".txt":
            loader = TextLoader(
                str(file),
                encoding="utf-8"
            )

            documents.extend(loader.load())

        elif file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))

            documents.extend(loader.load())

    return documents
