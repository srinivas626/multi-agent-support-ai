def requires_approval(action: str) -> bool:

    high_risk_actions = {
        "send_email",
    }

    return action in high_risk_actions
