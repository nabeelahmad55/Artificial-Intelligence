import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time

# ------------------------------
# Utility Functions
# ------------------------------

GOAL_STATE = tuple(range(1, 16)) + (0,)  # 0 represents blank
SIZE = 4


def manhattan_distance(state):
    """Heuristic: Manhattan distance for A*."""
    distance = 0
    for i in range(16):
        if state[i] == 0:
            continue
        x1, y1 = divmod(i, SIZE)
        x2, y2 = divmod(state[i] - 1, SIZE)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def get_neighbors(state):
    """Return all possible moves from a given state."""
    neighbors = []
    zero_pos = state.index(0)
    x, y = divmod(zero_pos, SIZE)

    moves = []
    if x > 0: moves.append((-1, 0))
    if x < SIZE - 1: moves.append((1, 0))
    if y > 0: moves.append((0, -1))
    if y < SIZE - 1: moves.append((0, 1))

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        new_pos = nx * SIZE + ny
        new_state = list(state)
        new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
        neighbors.append(tuple(new_state))

    return neighbors


def a_star_solver(start):
    """A* Search to solve the puzzle."""
    pq = []
    heapq.heappush(pq, (manhattan_distance(start), 0, start, []))
    visited = set()

    while pq:
        f, g, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == GOAL_STATE:
            return path

        for neighbor in get_neighbors(current):
            heapq.heappush(pq, (
                g + 1 + manhattan_distance(neighbor),
                g + 1,
                neighbor,
                path + [neighbor]
            ))

    return None


# ------------------------------
# Tkinter Puzzle Game
# ------------------------------

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Slider Game (AI Solver)")
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.tiles = []
        self.state = list(GOAL_STATE)
        self.move_count = 0

        self.create_ui()
        self.draw_tiles()

    def create_ui(self):
        tk.Button(self.frame, text="Shuffle", font=("Arial", 14), command=self.shuffle).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(self.frame, text="Solve Puzzle (AI)", font=("Arial", 14), command=self.solve_with_ai).grid(row=0, column=2, columnspan=2, pady=10)

        self.move_label = tk.Label(self.frame, text="Moves: 0", font=("Arial", 14))
        self.move_label.grid(row=1, column=0, columnspan=4, pady=10)

    def draw_tiles(self):
        for btn in self.tiles:
            btn.destroy()
        self.tiles = []

        for index, number in enumerate(self.state):
            row, col = divmod(index, SIZE)
            if number == 0:
                button = tk.Button(self.frame, text="", width=6, height=3, state="disabled", bg="lightgray")
            else:
                button = tk.Button(
                    self.frame, text=str(number), width=6, height=3, font=("Arial", 18),
                    command=lambda idx=index: self.move_tile(idx)
                )
            button.grid(row=row + 2, column=col)
            self.tiles.append(button)

    def move_tile(self, index):
        zero_idx = self.state.index(0)

        # Validate if neighbor
        r1, c1 = divmod(index, SIZE)
        r2, c2 = divmod(zero_idx, SIZE)

        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return

        self.state[index], self.state[zero_idx] = self.state[zero_idx], self.state[index]
        self.move_count += 1
        self.move_label.config(text=f"Moves: {self.move_count}")

        self.draw_tiles()

        if tuple(self.state) == GOAL_STATE:
            messagebox.showinfo("Solved!", "Congratulations! You solved the puzzle!")

    def shuffle(self):
        random.shuffle(self.state)
        self.move_count = 0
        self.move_label.config(text="Moves: 0")
        self.draw_tiles()

    def solve_with_ai(self):
        start_state = tuple(self.state)
        solution = a_star_solver(start_state)

        if not solution:
            messagebox.showerror("Error", "No solution found!")
            return

        self.animate_solution(solution)

    def animate_solution(self, solution):
        for step in solution:
            self.state = list(step)
            self.draw_tiles()
            self.root.update()
            time.sleep(0.3)


# ------------------------------
# Run the Game
# ------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    PuzzleGame(root)
    root.mainloop()
