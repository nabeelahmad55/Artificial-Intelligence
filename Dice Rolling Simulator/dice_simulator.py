import random

def roll_dice():
    """Returns a random dice value between 1 and 6."""
    return random.randint(1, 6)

def main():
    print("🎲 2-Player Dice Rolling Game")
    print("----------------------------")

    while True:
        user_input = input("Press Enter to roll for both players (or type 'q' to quit): ")

        if user_input.lower() == 'q':
            print("Goodbye!")
            break

        # Roll for both players
        player1 = roll_dice()
        player2 = roll_dice()

        print(f"\nPlayer 1 rolled: {player1}")
        print(f"Player 2 rolled: {player2}")

        # Decide winner
        if player1 > player2:
            print("🔥 Player 1 Wins!\n")
        elif player2 > player1:
            print("🔥 Player 2 Wins!\n")
        else:
            print("🤝 It's a tie! Roll again.\n")

if __name__ == "__main__":
    main()
