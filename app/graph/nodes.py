from pydantic import ValidationError

from app.graph.state import AgentState

from app.agents.router import route_question
from app.agents.knowledge_agent import knowledge_agent
from app.agents.general_agent import general_agent
from app.agents.action_agent import action_agent
from app.agents.response_agent import response_agent

from app.guardrails.permissions import has_permission
from app.guardrails.risk import requires_approval
from app.guardrails.validation import TicketInput, EmailInput

from app.tools.ticket_tool import create_ticket
from app.tools.email_tool import send_email


def router_node(state: AgentState):

    question = state["question"]

    route = route_question(question)

    return {
        "route": route
    }


def rag_node(state: AgentState):

    question = state["question"]

    result = knowledge_agent(question)

    return {
        "agent_result": result
    }


def general_node(state: AgentState):

    question = state["question"]

    result = general_agent(question)

    return {
        "agent_result": result
    }


def action_decision_node(state: AgentState):

    question = state["question"]

    decision = action_agent(question)

    return {
        "action": decision["action"],
        "action_arguments": decision.get(
            "arguments",
            {},
        ),
    }


def permission_node(state: AgentState):

    role = state.get(
        "role",
        "user",
    )

    action = state.get(
        "action",
    )

    if action == "none":

        return {
            "permission_granted": False
        }

    granted = has_permission(
        role,
        action,
    )

    return {
        "permission_granted": granted
    }


def route_after_permission(state: AgentState):

    if state.get(
        "permission_granted",
        False,
    ):
        return "execute"

    return "denied"


def denied_node(state: AgentState):

    action = state.get(
        "action",
        "none",
    )

    if action == "none":
        message = (
            "No action was requested, so nothing was executed."
        )
    else:
        role = state.get("role", "user")
        message = (
            f"Permission denied: role '{role}' is not allowed "
            f"to perform '{action}'."
        )

    return {
        "agent_result": message
    }


def approval_check_node(state: AgentState):

    action = state.get(
        "action"
    )

    required = requires_approval(
        action
    )

    if not required:

        return {
            "approval_required": False,
            "approved": True,
        }

    return {
        "approval_required": True,
        "approved": False,
    }


def route_after_approval(state: AgentState):

    if state.get(
        "approved",
        False,
    ):
        return "approved"

    return "pending"


def pending_approval_node(state: AgentState):

    action = state.get(
        "action",
        "this action",
    )

    message = (
        f"'{action}' is a sensitive action and requires human "
        "approval before it can be executed. It has not been "
        "performed yet."
    )

    return {
        "agent_result": message
    }


def tool_execution_node(state: AgentState):

    action = state["action"]

    arguments = state.get(
        "action_arguments",
        {},
    )

    if action == "create_ticket":

        try:
            validated = TicketInput(**arguments)
        except ValidationError as error:
            return {
                "agent_result": f"Ticket validation failed: {error}"
            }

        ticket = create_ticket(**validated.model_dump())

        return {
            "agent_result": str(ticket)
        }

    if action == "send_email":

        try:
            validated = EmailInput(**arguments)
        except ValidationError as error:
            return {
                "agent_result": f"Email validation failed: {error}"
            }

        email = send_email(**validated.model_dump())

        return {
            "agent_result": str(email)
        }

    return {
        "agent_result": "No action executed."
    }


def response_node(state: AgentState):

    question = state["question"]

    agent_result = state["agent_result"]

    final_response = response_agent(
        question=question,
        agent_result=agent_result,
    )

    return {
        "final_response": final_response
    }


def route_after_router(state: AgentState):

    route = state["route"]

    return route
