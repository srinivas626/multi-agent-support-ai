import uuid
from datetime import datetime


def create_ticket(
    title: str,
    description: str,
    priority: str = "medium",
) -> dict:

    allowed_priorities = {
        "low",
        "medium",
        "high",
    }

    if priority not in allowed_priorities:
        raise ValueError(
            f"Invalid priority: {priority}"
        )

    ticket_id = (
        f"TICK-{uuid.uuid4().hex[:8].upper()}"
    )

    return {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
    }
