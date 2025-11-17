#!/usr/bin/env python3
"""
Tic-Tac-Toe with GUI + AI (Minimax with alpha-beta pruning)

- UI matches the TicTacToe style you provided.
- Modes: Human vs Human, Human vs Computer, Computer vs Computer.
- Difficulty: Easy (random) / Hard (minimax + alpha-beta).
"""

import tkinter as tk
from tkinter import messagebox
import random
import math

# UI constants
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#ffffff"
BTN_ACTIVE = "#d9ffd9"
WIN_COLOR = "#90ee90"
FONT_MAIN = ("Arial", 26, "bold")
FONT_SCORE = ("Arial", 14)
TITLE_FONT = ("Arial", 30, "bold")
MENU_BTN_FONT = ("Arial", 14)

# AI autoplay delay (ms) for Computer vs Computer
AI_MOVE_DELAY_MS = 500

# Winning combos (indices)
WIN_COMBOS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=BG_COLOR)

        # Persistent scores
        self.score_x = 0
        self.score_o = 0

        # Mode/difficulty state
        self.mode = None                # 'hvh', 'hvc', 'cvc'
        # difficulty map: 'X' -> 'easy'/'hard'/'human', 'O' -> likewise
        self.difficulty = {'X': 'human', 'O': 'human'}

        # Game state
        self.board = [""] * 9
        self.buttons = []
        self.current_player = "X"
        self.ai_running = False        # for cvc autoplay
        self.hvc_ai_first = False      # if hvc and ai chosen to go first

        # Launch menu
        self.build_menu()

    # ----------- MENU -----------
    def build_menu(self):
        for w in self.root.winfo_children():
            w.destroy()

        title = tk.Label(self.root, text="Tic Tac Toe", font=TITLE_FONT, bg=BG_COLOR)
        title.pack(pady=12)

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=8)

        btn_hvh = tk.Button(frame, text="Human vs Human", font=MENU_BTN_FONT,
                            width=22, bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                            command=lambda: self.show_start_options('hvh'))
        btn_hvc = tk.Button(frame, text="Human vs Computer", font=MENU_BTN_FONT,
                            width=22, bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                            command=lambda: self.show_start_options('hvc'))
        btn_cvc = tk.Button(frame, text="Computer vs Computer", font=MENU_BTN_FONT,
                            width=22, bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                            command=lambda: self.show_start_options('cvc'))

        btn_hvh.grid(row=0, column=0, padx=6, pady=6)
        btn_hvc.grid(row=1, column=0, padx=6, pady=6)
        btn_cvc.grid(row=2, column=0, padx=6, pady=6)

        note = tk.Label(self.root, text="Choose mode. Then pick difficulty if needed.",
                        font=("Arial", 11), bg=BG_COLOR)
        note.pack(pady=8)

        self.score_label_menu = tk.Label(self.root,
                                         text=f"Player X: {self.score_x}   |   Player O: {self.score_o}",
                                         font=FONT_SCORE, bg=BG_COLOR)
        self.score_label_menu.pack(pady=6)

    def show_start_options(self, mode):
        self.mode = mode
        top = tk.Toplevel(self.root)
        top.title("Start Options")
        top.configure(bg=BG_COLOR)
        top.grab_set()

        lbl = tk.Label(top, text="Start Options", font=("Arial", 18, "bold"), bg=BG_COLOR)
        lbl.pack(pady=8)

        if mode == 'hvh':
            tk.Label(top, text="Human vs Human — press Start to play.", bg=BG_COLOR).pack(pady=6)
            start_btn = tk.Button(top, text="Start", bg="#add8e6",
                                  command=lambda: [top.destroy(), self.start_game()])
            start_btn.pack(pady=8)
        elif mode == 'hvc':
            # Choose AI difficulty and who goes first, also let human choose symbol
            tk.Label(top, text="AI Difficulty:", bg=BG_COLOR).pack(pady=4)
            diff_var = tk.StringVar(value="hard")
            tk.Radiobutton(top, text="Easy (random)", variable=diff_var, value="easy", bg=BG_COLOR).pack()
            tk.Radiobutton(top, text="Hard (minimax)", variable=diff_var, value="hard", bg=BG_COLOR).pack()

            tk.Label(top, text="Who goes first?", bg=BG_COLOR).pack(pady=6)
            first_var = tk.StringVar(value="human")
            tk.Radiobutton(top, text="Human (X)", variable=first_var, value="human", bg=BG_COLOR).pack()
            tk.Radiobutton(top, text="Computer (X)", variable=first_var, value="ai", bg=BG_COLOR).pack()

            tk.Label(top, text="If Computer goes first it will play X.", bg=BG_COLOR, font=("Arial", 9)).pack(pady=4)

            start_btn = tk.Button(top, text="Start",
                                  bg="#add8e6",
                                  command=lambda: [self.set_hvc_options(diff_var.get(), first_var.get()), top.destroy(), self.start_game()])
            start_btn.pack(pady=8)
        else:  # cvc
            tk.Label(top, text="AI (X) Difficulty:", bg=BG_COLOR).pack(pady=4)
            var_x = tk.StringVar(value="hard")
            tk.Radiobutton(top, text="Easy (random)", variable=var_x, value="easy", bg=BG_COLOR).pack()
            tk.Radiobutton(top, text="Hard (minimax)", variable=var_x, value="hard", bg=BG_COLOR).pack()

            tk.Label(top, text="AI (O) Difficulty:", bg=BG_COLOR).pack(pady=6)
            var_o = tk.StringVar(value="hard")
            tk.Radiobutton(top, text="Easy (random)", variable=var_o, value="easy", bg=BG_COLOR).pack()
            tk.Radiobutton(top, text="Hard (minimax)", variable=var_o, value="hard", bg=BG_COLOR).pack()

            start_btn = tk.Button(top, text="Start",
                                  bg="#add8e6",
                                  command=lambda: [self.set_cvc_options(var_x.get(), var_o.get()), top.destroy(), self.start_game()])
            start_btn.pack(pady=8)

    def set_hvc_options(self, ai_difficulty, first):
        # Human will be 'human' for whichever symbol; default human = X unless AI first chosen
        if first == 'ai':
            # AI will be X and human O
            self.difficulty = {'X': ai_difficulty, 'O': 'human'}
            self.hvc_ai_first = True
        else:
            self.difficulty = {'X': 'human', 'O': ai_difficulty}
            self.hvc_ai_first = False

    def set_cvc_options(self, dx, do):
        self.difficulty = {'X': dx, 'O': do}

    # ----------- GAME START / UI -----------
    def start_game(self):
        for w in self.root.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.root, bg=BG_COLOR)
        top_bar.pack(pady=6)

        title = tk.Label(top_bar, text="Tic Tac Toe", font=TITLE_FONT, bg=BG_COLOR)
        title.grid(row=0, column=0, columnspan=3)

        self.score_label = tk.Label(top_bar, text=self._score_text(), font=FONT_SCORE, bg=BG_COLOR)
        self.score_label.grid(row=1, column=0, columnspan=3, pady=6)

        grid_frame = tk.Frame(self.root, bg=BG_COLOR)
        grid_frame.pack()

        self.board = [""] * 9
        self.buttons = []
        for i in range(9):
            btn = tk.Button(grid_frame, text="", width=6, height=3, font=FONT_MAIN,
                            bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                            command=lambda i=i: self.on_cell_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        ctl_frame = tk.Frame(self.root, bg=BG_COLOR)
        ctl_frame.pack(pady=10)
        restart_btn = tk.Button(ctl_frame, text="Restart Game", font=("Arial", 14),
                                bg="#add8e6", command=self.restart_game)
        menu_btn = tk.Button(ctl_frame, text="Back to Menu", font=("Arial", 14),
                             bg="#f7c6c6", command=self.back_to_menu)
        restart_btn.grid(row=0, column=0, padx=8)
        menu_btn.grid(row=0, column=1, padx=8)

        self.current_player = "X"
        self.ai_running = False

        # Mode-specific setup
        if self.mode == 'hvh':
            self.difficulty = {'X': 'human', 'O': 'human'}
        elif self.mode == 'hvc':
            # If AI was set to go first, ai is X
            if getattr(self, 'hvc_ai_first', False):
                # difficulty already set such that X is AI
                self.current_player = "X"
                # schedule AI if X is AI
                self.root.after(300, self.ai_move_if_needed)
            else:
                # human X, AI O
                pass
        elif self.mode == 'cvc':
            # both AI; start autoplay
            self.ai_running = True
            self.root.after(AI_MOVE_DELAY_MS, self.ai_autoplay_step)

    def _score_text(self):
        return f"Player X: {self.score_x}   |   Player O: {self.score_o}"

    # ----------- Interaction -----------
    def on_cell_click(self, index):
        # ignore if occupied or game ended
        if self.buttons[index]["text"] != "" or self.check_winner() is not None:
            return

        # If current player is human, allow move
        if self.difficulty.get(self.current_player) == 'human':
            self.make_move(index, self.current_player)
            if self._handle_post_move():
                return
            # If opponent is AI, schedule AI move
            if self.difficulty.get(self.current_player) != 'human':
                # shouldn't happen: just in case
                self.root.after(200, self.ai_move_if_needed)
            else:
                # switch player and possibly AI moves next
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.root.after(200, self.ai_move_if_needed)
        else:
            # Click during AI turn ignored
            return

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)

    def _handle_post_move(self):
        winner = self.check_winner()
        if winner:
            player, combo = winner
            self.highlight_winner(combo)
            if player == 'X':
                self.score_x += 1
            else:
                self.score_o += 1
            self.update_score()
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            return True
        if "" not in self.board:
            messagebox.showinfo("Draw", "It's a draw!")
            return True
        return False

    # ----------- AI / Autoplay -----------
    def ai_move_if_needed(self):
        """Make a single AI move if current player is an AI and game not over."""
        if self.check_winner() or "" not in self.board:
            return

        role = self.difficulty.get(self.current_player)
        if role == 'human':
            return

        if role == 'easy':
            moves = [i for i, v in enumerate(self.board) if v == ""]
            if moves:
                move = random.choice(moves)
                self.make_move(move, self.current_player)
        else:
            # Hard: minimax with alpha-beta (respecting your CLI logic)
            opponent = 'O' if self.current_player == 'X' else 'X'
            move = self.best_move_alpha_beta(self.board.copy(), self.current_player, opponent)
            if move is not None:
                self.make_move(move, self.current_player)

        if self._handle_post_move():
            return

        # switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_autoplay_step(self):
        """For Computer vs Computer mode: repeated scheduled moves."""
        if not self.ai_running:
            return
        if self.check_winner() or "" not in self.board:
            self.ai_running = False
            self._handle_post_move()
            return
        # Ensure it's AI turn (both are AI in cvc)
        self.ai_move_if_needed()
        # schedule next step
        self.root.after(AI_MOVE_DELAY_MS, self.ai_autoplay_step)

    # ----------- Minimax with alpha-beta (adapted from your CLI) -----------
    def check_winner_simple(self, board):
        """Return 'X' or 'O' if winner, 'Draw' if draw, else None"""
        for a,b,c in WIN_COMBOS:
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]
        if "" not in board:
            return 'Draw'
        return None

    def minimax_ab(self, board, maximizing, ai_player, human_player, alpha=-math.inf, beta=math.inf):
        """
        Return (score, best_move)
        score: +1 ai win, -1 human win, 0 draw
        """
        winner = self.check_winner_simple(board)
        if winner == ai_player:
            return 1, None
        elif winner == human_player:
            return -1, None
        elif winner == 'Draw':
            return 0, None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for i, cell in enumerate(board):
                if cell == "":
                    board[i] = ai_player
                    eval_score, _ = self.minimax_ab(board, False, ai_player, human_player, alpha, beta)
                    board[i] = ""
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = i
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return int(max_eval), best_move
        else:
            min_eval = math.inf
            for i, cell in enumerate(board):
                if cell == "":
                    board[i] = human_player
                    eval_score, _ = self.minimax_ab(board, True, ai_player, human_player, alpha, beta)
                    board[i] = ""
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = i
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return int(min_eval), best_move

    def best_move_alpha_beta(self, board, ai_player, human_player, difficulty='hard'):
        if difficulty == 'easy':
            avail = [i for i, v in enumerate(board) if v == ""]
            return random.choice(avail) if avail else None
        score, move = self.minimax_ab(board, True, ai_player, human_player)
        if move is None:
            avail = [i for i, v in enumerate(board) if v == ""]
            return random.choice(avail) if avail else None
        return move

    # ----------- Utilities -----------
    def check_winner(self):
        for combo in WIN_COMBOS:
            a,b,c = combo
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                return self.board[a], combo
        return None

    def highlight_winner(self, combo):
        for idx in combo:
            self.buttons[idx].config(bg=WIN_COLOR)

    def update_score(self):
        self.score_label.config(text=self._score_text())
        if hasattr(self, 'score_label_menu'):
            try:
                self.score_label_menu.config(text=self._score_text())
            except:
                pass

    def restart_game(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg=BTN_COLOR)
        self.current_player = "X"
        # restart autoplay if in cvc
        if self.mode == 'cvc':
            self.ai_running = True
            self.root.after(AI_MOVE_DELAY_MS, self.ai_autoplay_step)
        if self.mode == 'hvc' and getattr(self, 'hvc_ai_first', False):
            self.root.after(300, self.ai_move_if_needed)

    def back_to_menu(self):
        self.ai_running = False
        self.build_menu()

# ----------- Run -----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
