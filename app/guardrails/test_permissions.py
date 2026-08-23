from app.guardrails.permissions import has_permission


print(
    has_permission(
        "user",
        "create_ticket",
    )
)


print(
    has_permission(
        "user",
        "send_email",
    )
)


print(
    has_permission(
        "admin",
        "send_email",
    )
)
