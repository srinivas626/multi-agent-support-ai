from app.rag.retriever import search_documents


question = "What should I do if my VPN is not connecting?"

results = search_documents(question)

print(f"Results found: {len(results)}")

for i, result in enumerate(results):

    print("\n==============================")
    print(f"RESULT {i + 1}")
    print("==============================")

    print(result.page_content)
