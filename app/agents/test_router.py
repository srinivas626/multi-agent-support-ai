from app.agents.router import route_question


questions = [
    "What should I do if my VPN is not connecting?",
    "What is Python?",
    "What is our company's VPN security policy?",
    "Explain recursion.",
]


for question in questions:

    route = route_question(question)

    print("\nQuestion:", question)
    print("Route:", route)
