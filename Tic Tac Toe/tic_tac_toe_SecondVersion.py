import tkinter as tk
from tkinter import messagebox

# Colors
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#ffffff"
BTN_ACTIVE = "#d9ffd9"
WIN_COLOR = "#90ee90"
FONT_MAIN = ("Arial", 26, "bold")
FONT_SCORE = ("Arial", 14)

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=BG_COLOR)

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.score_x = 0
        self.score_o = 0

        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 30, "bold"), bg=BG_COLOR)
        title.pack(pady=10)

        # Scoreboard
        self.score_label = tk.Label(
            self.root,
            text=f"Player X: {self.score_x}   |   Player O: {self.score_o}",
            font=FONT_SCORE,
            bg=BG_COLOR
        )
        self.score_label.pack(pady=5)

        # Game grid
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack()

        for i in range(9):
            btn = tk.Button(
                frame,
                text="",
                width=6,
                height=3,
                font=FONT_MAIN,
                bg=BTN_COLOR,
                activebackground=BTN_ACTIVE,
                command=lambda i=i: self.handle_click(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Restart button
        restart_btn = tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 14),
            bg="#add8e6",
            command=self.reset_game
        )
        restart_btn.pack(pady=15)

    def handle_click(self, index):
        if self.buttons[index]["text"] != "" or self.check_winner():
            return

        self.buttons[index]["text"] = self.current_player
        self.board[index] = self.current_player

        # Check if winner exists
        result = self.check_winner()

        if result:
            player, combo = result  # winner + squares

            self.highlight_winner(combo)

            # Update scores correctly
            if player == "X":
                self.score_x += 1
            else:
                self.score_o += 1

            self.update_score()

            messagebox.showinfo("Game Over", f"Player {player} wins!")
            return

        # Check draw
        if "" not in self.board:
            messagebox.showinfo("Draw", "It's a draw!")
            return

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"

    def highlight_winner(self, combo):
        for idx in combo:
            self.buttons[idx].config(bg=WIN_COLOR)

    def check_winner(self):
        win_combos = [
            [0,1,2], [3,4,5], [6,7,8],   # rows
            [0,3,6], [1,4,7], [2,5,8],   # columns
            [0,4,8], [2,4,6]             # diagonals
        ]

        for combo in win_combos:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a], combo  # return (Player, winning_cells)

        return None

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", bg=BTN_COLOR)

    def update_score(self):
        self.score_label.config(
            text=f"Player X: {self.score_x}   |   Player O: {self.score_o}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
