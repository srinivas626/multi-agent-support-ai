from app.graph.workflow import graph


scenarios = [
    {
        "label": "user creates a ticket (allowed, no approval needed)",
        "question": "Please create a support ticket because my VPN is not working.",
        "role": "user",
    },
    {
        "label": "user tries to send an email (permission denied)",
        "question": "Send an email to the support team about my VPN problem.",
        "role": "user",
    },
    {
        "label": "support_agent tries to send an email (allowed, but requires approval)",
        "question": "Send an email to the support team about my VPN problem.",
        "role": "support_agent",
    },
]


for scenario in scenarios:

    print("\n==============================")
    print(scenario["label"])
    print("==============================")
    print("Question:", scenario["question"])
    print("Role:", scenario["role"])

    result = graph.invoke(
        {
            "question": scenario["question"],
            "role": scenario["role"],
        }
    )

    print("\nAction:", result.get("action"))
    print("Permission granted:", result.get("permission_granted"))
    print("Approval required:", result.get("approval_required"))
    print("Approved:", result.get("approved"))
    print("Agent result:", result.get("agent_result"))
    print("\nFinal response:")
    print(result.get("final_response"))
