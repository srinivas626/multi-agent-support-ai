from typing import Literal


Role = Literal[
    "user",
    "support_agent",
    "admin",
]


PERMISSIONS = {

    "user": {
        "create_ticket",
    },

    "support_agent": {
        "create_ticket",
        "send_email",
    },

    "admin": {
        "create_ticket",
        "send_email",
    },
}


def has_permission(
    role: Role,
    action: str,
) -> bool:

    allowed_actions = PERMISSIONS.get(
        role,
        set(),
    )

    return action in allowed_actions
