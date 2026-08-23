from app.agents.agent_system import run_agent_system


questions = [
    "What should I do if my VPN is not connecting?",
    "What is Python?",
]


for question in questions:

    print("\n==============================")
    print("QUESTION")
    print("==============================")
    print(question)

    answer = run_agent_system(question)

    print("\nANSWER")
    print("==============================")
    print(answer)
