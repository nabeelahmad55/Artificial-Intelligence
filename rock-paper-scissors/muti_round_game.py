import random

choices = ["rock", "paper", "scissors"]
user_score = 0
comp_score = 0

while True:
    user = input("\nEnter rock, paper, scissors (or 'q' to quit): ").lower()
    if user == 'q':
        break
    if user not in choices:
        print("Invalid choice! Try again.")
        continue

    computer = random.choice(choices)
    print(f"Computer chose: {computer}")

    if user == computer:
        print("It's a tie!")
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        print("You win this round!")
        user_score += 1
    else:
        print("Computer wins this round!")
        comp_score += 1

    print(f"Score -> You: {user_score} | Computer: {comp_score}")

print("\nFinal Scores:")
print(f"You: {user_score} | Computer: {comp_score}")
print("Goodbye!")
