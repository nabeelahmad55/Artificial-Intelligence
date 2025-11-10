import random
import time

def print_header():
    print("=" * 40)
    print("🎮 Rock - Paper - Scissors Game 🎮")
    print("=" * 40)

def get_user_choice():
    print("\nChoices:")
    print("1. Rock")
    print("2. Paper")
    print("3. Scissors")
    choice = input("Enter your choice (1/2/3): ")

    choices = {"1": "rock", "2": "paper", "3": "scissors"}
    return choices.get(choice, None)

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def decide_winner(user, computer):
    if user == computer:
        return "tie"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        return "user"
    else:
        return "computer"

def play_round():
    user = get_user_choice()
    if user is None:
        print("❌ Invalid input! Please select 1, 2, or 3.")
        return None

    computer = get_computer_choice()

    print("\n🪨 Rock...")
    time.sleep(0.5)
    print("📄 Paper...")
    time.sleep(0.5)
    print("✂️ Scissors...")
    time.sleep(0.5)
    print("👊 Shoot!\n")
    time.sleep(0.5)

    print(f"You chose: {user.capitalize()}")
    print(f"Computer chose: {computer.capitalize()}")

    winner = decide_winner(user, computer)
    if winner == "tie":
        print("😐 It's a tie!")
    elif winner == "user":
        print("🎉 You win this round!")
    else:
        print("💻 Computer wins this round!")

    return winner

def main():
    print_header()
    user_score = 0
    computer_score = 0
    rounds = 0

    while True:
        winner = play_round()
        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1

        rounds += 1
        print(f"\n🏁 Score after {rounds} round(s): You {user_score} - {computer_score} Computer")

        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            print("\n🎯 Final Score:")
            print(f"You: {user_score} | Computer: {computer_score}")
            if user_score > computer_score:
                print("🏆 You are the overall winner!")
            elif user_score < computer_score:
                print("💻 Computer wins the game!")
            else:
                print("🤝 It's a tie game!")
            print("\nThanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
