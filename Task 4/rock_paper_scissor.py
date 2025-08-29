import tkinter as tk
import random
from tkinter import messagebox

def play(user_choice):
    global user_score, computer_score

    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "😐 It's a Tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        result = "🎉 You Win!"
        user_score += 1
    else:
        result = "😢 You Lose!"
        computer_score += 1

    user_choice_label.config(text=f"Your Choice: {user_choice}")
    computer_choice_label.config(text=f"Computer's Choice: {computer_choice}")
    result_label.config(text=result)
    score_label.config(text=f"🏆 Score ➤ You: {user_score} | Computer: {computer_score}")

def reset_game():
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    user_choice_label.config(text="Your Choice: -")
    computer_choice_label.config(text="Computer's Choice: -")
    result_label.config(text="Let's Play! 😎")
    score_label.config(text="🏆 Score ➤ You: 0 | Computer: 0")

def exit_game():
    root.destroy()

root = tk.Tk()
root.title("🎮 Rock-Paper-Scissors")
root.attributes("-fullscreen", True) 
root.config(bg="#121212")

user_score = 0
computer_score = 0

tk.Label(root, text="🎮 Rock-Paper-Scissors", font=("Helvetica", 36, "bold"), bg="#121212", fg="#00ffcc").pack(pady=30)

frame = tk.Frame(root, bg="#121212")
frame.pack(pady=30)

rock_btn = tk.Button(frame, text="🪨\nROCK", width=12, height=6, font=("Arial", 20, "bold"),
                     bg="#3498db", fg="white", command=lambda: play("Rock"))
rock_btn.grid(row=0, column=0, padx=40)

paper_btn = tk.Button(frame, text="📄\nPAPER", width=12, height=6, font=("Arial", 20, "bold"),
                      bg="#2ecc71", fg="white", command=lambda: play("Paper"))
paper_btn.grid(row=0, column=1, padx=40)

scissors_btn = tk.Button(frame, text="✂️\nSCISSORS", width=12, height=6, font=("Arial", 20, "bold"),
                         bg="#e67e22", fg="white", command=lambda: play("Scissors"))
scissors_btn.grid(row=0, column=2, padx=40)

user_choice_label = tk.Label(root, text="Your Choice: -", font=("Arial", 22), bg="#121212", fg="white")
user_choice_label.pack(pady=10)

computer_choice_label = tk.Label(root, text="Computer's Choice: -", font=("Arial", 22), bg="#121212", fg="white")
computer_choice_label.pack(pady=10)

result_label = tk.Label(root, text="Let's Play! 😎", font=("Arial", 28, "bold"), bg="#121212", fg="#00ffcc")
result_label.pack(pady=20)

score_label = tk.Label(root, text="🏆 Score ➤ You: 0 | Computer: 0", font=("Arial", 24, "bold"), bg="#121212", fg="#ffcc00")
score_label.pack(pady=10)

bottom_frame = tk.Frame(root, bg="#121212")
bottom_frame.pack(pady=30)

reset_btn = tk.Button(bottom_frame, text="🔄 Reset Game", command=reset_game,
                      width=20, height=2, font=("Arial", 16, "bold"), bg="#ff6f61", fg="white")
reset_btn.grid(row=0, column=0, padx=30)

exit_btn = tk.Button(bottom_frame, text="❌ Exit Game", command=exit_game,
                     width=20, height=2, font=("Arial", 16, "bold"), bg="#e74c3c", fg="white")
exit_btn.grid(row=0, column=1, padx=30)

root.mainloop()
