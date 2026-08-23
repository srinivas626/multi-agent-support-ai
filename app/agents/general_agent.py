from app.llm import llm
from app.utils import extract_text


def general_agent(question: str) -> str:
    prompt = f"""
You are a helpful general-purpose AI assistant.

Answer the user's question clearly and accurately.

User question:
{question}
"""

    response = llm.invoke(prompt)

    return extract_text(response)
