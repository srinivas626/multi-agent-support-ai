from typing import TypedDict


class AgentState(TypedDict, total=False):

    question: str

    route: str

    role: str

    action: str

    action_arguments: dict

    permission_granted: bool

    approval_required: bool

    approved: bool

    agent_result: str

    final_response: str
