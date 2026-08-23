from app.agents.action_agent import action_agent


questions = [
    "Please create a support ticket because my VPN is not working.",
    "Send an email to the support team about my VPN problem.",
    "What is a VPN?",
]


for question in questions:

    print("\n==============================")
    print("REQUEST")
    print("==============================")
    print(question)

    decision = action_agent(question)

    print("\nDECISION")
    print("==============================")
    print(decision)
