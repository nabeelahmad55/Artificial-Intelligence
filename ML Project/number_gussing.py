import random

def number_guessing_game():
    print("🎯 Welcome to the Number Guessing Game!")
    print("---------------------------------------")
    print("I'm thinking of a number between 1 and 100.")

    # Computer picks number
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("\nEnter your guess: "))
        except ValueError:
            print("❌ Please enter a valid number!")
            continue

        attempts += 1

        if guess < secret_number:
            print("⬆ Too low! Try again.")
        elif guess > secret_number:
            print("⬇ Too high! Try again.")
        else:
            print(f"🎉 Correct! The number was {secret_number}.")
            print(f"🏆 You guessed it in {attempts} attempts!")
            break

    print("\nThanks for playing!")

if __name__ == "__main__":
    number_guessing_game()
