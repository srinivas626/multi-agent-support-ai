from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState

from app.graph.nodes import (
    router_node,
    rag_node,
    general_node,
    action_decision_node,
    permission_node,
    route_after_permission,
    denied_node,
    approval_check_node,
    route_after_approval,
    pending_approval_node,
    tool_execution_node,
    response_node,
    route_after_router,
)


builder = StateGraph(AgentState)


builder.add_node(
    "router",
    router_node,
)

builder.add_node(
    "rag",
    rag_node,
)

builder.add_node(
    "general",
    general_node,
)

builder.add_node(
    "action_decision",
    action_decision_node,
)

builder.add_node(
    "permission",
    permission_node,
)

builder.add_node(
    "denied",
    denied_node,
)

builder.add_node(
    "approval_check",
    approval_check_node,
)

builder.add_node(
    "pending_approval",
    pending_approval_node,
)

builder.add_node(
    "tool_execution",
    tool_execution_node,
)

builder.add_node(
    "response",
    response_node,
)


builder.add_edge(
    START,
    "router",
)


builder.add_conditional_edges(
    "router",
    route_after_router,
    {
        "rag": "rag",
        "general": "general",
        "action": "action_decision",
    },
)


builder.add_edge(
    "action_decision",
    "permission",
)


builder.add_conditional_edges(
    "permission",
    route_after_permission,
    {
        "execute": "approval_check",
        "denied": "denied",
    },
)


builder.add_conditional_edges(
    "approval_check",
    route_after_approval,
    {
        "approved": "tool_execution",
        "pending": "pending_approval",
    },
)


builder.add_edge(
    "rag",
    "response",
)

builder.add_edge(
    "general",
    "response",
)

builder.add_edge(
    "denied",
    "response",
)

builder.add_edge(
    "pending_approval",
    "response",
)

builder.add_edge(
    "tool_execution",
    "response",
)


builder.add_edge(
    "response",
    END,
)


graph = builder.compile()
