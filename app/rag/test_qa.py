from app.rag.qa import answer_question


question = "What should I do if my VPN is not connecting?"

answer = answer_question(question)

print("\n==============================")
print("AI ANSWER")
print("==============================")

print(answer)
