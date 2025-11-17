import tkinter as tk
from tkinter import messagebox
import random

# Colors
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#ffffff"
BTN_ACTIVE = "#d9ffd9"
WIN_COLOR = "#90ee90"
FONT_MAIN = ("Arial", 26, "bold")
FONT_SCORE = ("Arial", 14)

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI Mode")
        self.root.configure(bg=BG_COLOR)

        self.player = "X"       # Human
        self.ai = "O"           # Computer
        self.board = [""] * 9
        self.buttons = []

        self.score_x = 0
        self.score_o = 0

        self.build_ui()

    # -------------------------------------------------------------
    def build_ui(self):

        title = tk.Label(self.root, text="Tic Tac Toe (AI)", 
                         font=("Arial", 30, "bold"), bg=BG_COLOR)
        title.pack(pady=10)

        self.score_label = tk.Label(
            self.root,
            text=f"Player X: {self.score_x}   |   AI (O): {self.score_o}",
            font=FONT_SCORE,
            bg=BG_COLOR
        )
        self.score_label.pack(pady=5)

        # Game Grid
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
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        restart_btn = tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 14),
            bg="#add8e6",
            command=self.reset_game
        )
        restart_btn.pack(pady=15)

    # -------------------------------------------------------------
    # CLICK HANDLER
    def handle_click(self, index):
        if self.buttons[index]["text"] != "" or self.check_winner():
            return

        # Player move
        self.make_move(index, self.player)

        if self.check_winner():
            winner, combo = self.check_winner()
            self.highlight_winner(combo)
            self.score_x += 1
            self.update_score()
            messagebox.showinfo("Game Over", "You (X) Win!")
            return

        # Draw?
        if "" not in self.board:
            messagebox.showinfo("Draw", "It's a draw!")
            return

        # AI Move
        self.root.after(200, self.ai_move)

    # -------------------------------------------------------------
    # AI MOVE (Minimax)
    def ai_move(self):
        best_score = -999
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                score = self.minimax(False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        self.make_move(best_move, self.ai)

        if self.check_winner():
            winner, combo = self.check_winner()
            self.highlight_winner(combo)
            self.score_o += 1
            self.update_score()
            messagebox.showinfo("Game Over", "AI (O) Wins!")
            return

        if "" not in self.board:
            messagebox.showinfo("Draw", "It's a draw!")

    # -------------------------------------------------------------
    # Minimax Algorithm
    def minimax(self, is_maximizing):
        winner = self.check_winner()
        if winner:
            if winner[0] == self.ai:
                return 1
            elif winner[0] == self.player:
                return -1

        if "" not in self.board:
            return 0

        if is_maximizing:
            best_score = -999
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.ai
                    score = self.minimax(False)
                    self.board[i] = ""
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = 999
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.player
                    score = self.minimax(True)
                    self.board[i] = ""
                    best_score = min(best_score, score)
            return best_score

    # -------------------------------------------------------------
    # Make a move on UI + board
    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)

    # -------------------------------------------------------------
    def highlight_winner(self, combo):
        for idx in combo:
            self.buttons[idx].config(bg=WIN_COLOR)

    # -------------------------------------------------------------
    def check_winner(self):
        combos = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]            # diagonal
        ]
        for combo in combos:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a], combo
        return None

    # -------------------------------------------------------------
    def update_score(self):
        self.score_label.config(
            text=f"Player X: {self.score_x}   |   AI (O): {self.score_o}"
        )

    # -------------------------------------------------------------
    def reset_game(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg=BTN_COLOR)

# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeAI(root)
    root.mainloop()
