from app.rag.qa import answer_question


def knowledge_agent(question: str) -> str:
    return answer_question(question)
