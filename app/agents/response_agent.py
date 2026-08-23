from app.llm import llm
from app.utils import extract_text


def response_agent(
    question: str,
    agent_result: str,
) -> str:

    prompt = f"""
You are the final response agent for a customer support AI.

Create a clear, concise and helpful response for the user.

Do not invent information.

User question:
{question}

Information produced by the specialized agent:
{agent_result}
"""

    response = llm.invoke(prompt)

    return extract_text(response)
