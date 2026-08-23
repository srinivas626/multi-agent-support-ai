from app.agents.router import route_question
from app.agents.knowledge_agent import knowledge_agent
from app.agents.general_agent import general_agent
from app.agents.action_agent import action_agent
from app.agents.response_agent import response_agent


def run_agent_system(question: str) -> str:

    route = route_question(question)

    if route == "rag":

        result = knowledge_agent(question)

    elif route == "general":

        result = general_agent(question)

    elif route == "action":

        result = action_agent(question)

    else:

        return "I could not determine how to handle your request."

    return response_agent(
        question=question,
        agent_result=str(result),
    )
