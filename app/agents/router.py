from typing import Literal

from pydantic import BaseModel

from app.llm import llm


class RouteDecision(BaseModel):
    route: Literal["rag", "general", "action"]


router_llm = llm.with_structured_output(RouteDecision)


def route_question(question: str) -> str:

    prompt = f"""
You are a routing agent for a company support AI.

Classify the user's question into exactly one of these routes:

rag:
Use when the user needs information from company
documents, policies, procedures, or internal knowledge.

general:
Use for general knowledge questions that do not require
company-specific information.

action:
Use when the user explicitly asks the system to perform
an action such as creating a ticket or sending an email.

Important:
Do not classify a question as action simply because an
action might be useful.

Only use action when the user actually requests an action.

User request:
{question}
"""

    decision = router_llm.invoke(prompt)

    return decision.route
