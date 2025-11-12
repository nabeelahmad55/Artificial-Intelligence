import tkinter as tk
import random

def play(choice):
    comp = random.choice(["rock", "paper", "scissors"])
    result = ""
    if choice == comp:
        result = "It's a tie!"
    elif (choice == "rock" and comp == "scissors") or \
         (choice == "paper" and comp == "rock") or \
         (choice == "scissors" and comp == "paper"):
        result = "You win!"
    else:
        result = "Computer wins!"
    lbl_result.config(text=f"Computer chose {comp}\n{result}")

root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("300x250")

lbl_title = tk.Label(root, text="Rock Paper Scissors", font=("Arial", 16))
lbl_title.pack(pady=10)

for option in ["rock", "paper", "scissors"]:
    tk.Button(root, text=option.title(), width=12,
              command=lambda opt=option: play(opt)).pack(pady=5)

lbl_result = tk.Label(root, text="", font=("Arial", 12))
lbl_result.pack(pady=20)

root.mainloop()
