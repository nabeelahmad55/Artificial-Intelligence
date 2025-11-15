questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A) London", "B) Paris", "C) Rome", "D) Madrid"],
        "answer": "B"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["A) Python", "B) Java", "C) PHP", "D) All of the above"],
        "answer": "D"
    },
    {
        "question": "What does RAM stand for?",
        "options": ["A) Random Access Memory", "B) Read Only Memory",
                    "C) Run Access Module", "D) None"],
        "answer": "A"
    }
]

score = 0

print("🧠 Quiz Game")
print("------------")

for q in questions:
    print("\n" + q["question"])
    for opt in q["options"]:
        print(opt)

    answer = input("\nYour answer (A/B/C/D): ").upper()

    if answer == q["answer"]:
        print("✔ Correct!")
        score += 1
    else:
        print("❌ Wrong! Correct answer is:", q["answer"])

print("\n🎉 Quiz Completed!")
print("Your total score:", score, "/", len(questions))
