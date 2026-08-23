from app.graph.workflow import graph


questions = [
    "What should I do if my VPN is not connecting?",
    "What is Python?",
    "Create a support ticket because my VPN is not working.",
]


for question in questions:

    print("\n==============================")
    print("QUESTION")
    print("==============================")

    print(question)

    result = graph.invoke(
        {
            "question": question
        }
    )

    print("\nROUTE:")
    print(result.get("route"))

    print("\nFINAL RESPONSE:")
    print(result.get("final_response"))


print("\n==============================")
print("GRAPH STRUCTURE")
print("==============================")

print(
    graph.get_graph().draw_ascii()
)
