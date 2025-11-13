# 🎮 Tic Tac Toe Game in Python (2 Player Version)

def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    # All possible win combinations
    combos = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for combo in combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board)

def tic_tac_toe():
    board = [" "] * 9
    current_player = "X"

    print("🎯 Welcome to Tic Tac Toe!")
    print("Player 1: X | Player 2: O")
    print_board(board)

    while True:
        try:
            move = int(input(f"Player {current_player}, choose your position (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != " ":
                print("❌ Invalid move, try again.")
                continue
        except ValueError:
            print("❌ Please enter a valid number (1-9).")
            continue

        board[move] = current_player
        print_board(board)

        if check_winner(board, current_player):
            print(f"🏆 Player {current_player} wins!")
            break

        if is_draw(board):
            print("🤝 It's a draw!")
            break

        # Switch turns
        current_player = "O" if current_player == "X" else "X"

    print("Game Over!")

if __name__ == "__main__":
    tic_tac_toe()
