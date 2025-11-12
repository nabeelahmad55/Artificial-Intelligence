import random

options = ["rock", "paper", "scissors"]
history = {"rock": 0, "paper": 0, "scissors": 0}

def ai_choice():
    # Predict player’s most common move and counter it
    most_common = max(history, key=history.get)
    if most_common == "rock":
        return "paper"
    elif most_common == "paper":
        return "scissors"
    else:
        return "rock"

while True:
    user = input("\nEnter rock, paper, scissors (or 'q' to quit): ").lower()
    if user == 'q':
        break
    if user not in options:
        print("Invalid choice.")
        continue

    history[user] += 1
    computer = ai_choice()
    print(f"Computer chose: {computer}")

    if user == computer:
        print("It's a tie!")
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        print("You win!")
    else:
        print("Computer wins!")
