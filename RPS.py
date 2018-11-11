import tkinter
from tkinter import ttk, messagebox
from random import randrange

first_play = True
last_game = 2
root = tkinter.Tk()
computer_choice = 0

difficulty_choice = messagebox.askyesno(title = "Difficulty Choice", message = "Activate Hard Mode?")

ratio = [0, 0, 0] #wins, losses, ties
computer_choices = {1: "rock", 2: "paper", 0: "scissors"}
interface = ttk.Label(root, text = "Press a Button!")
ratio_label = ttk.Label(root, text = "This label will show your W/L ratio.")
computer_label = ttk.Label(root, text = "This label will show what the computer chooses.")

def choice(number):
    global first_play
    global last_game
    global computer_choice
    if difficulty_choice == False or first_play == True or last_game == 2:
        computer_choice = randrange(1, 4)
    computer_label.config(text = "Computer chose: " + computer_choices[int((computer_choice + 1) % 3)])
    print(computer_choice)
    if (computer_choice % 3) == number:
        interface.config(text = "It's a tie!")
        ratio[2] += 1
        last_game = 2
    elif (computer_choice % 3) == (number - 1):
        interface.config(text = "You win!")
        ratio[0] += 1
        last_game = 0
        computer_choice += 1
    else:
        interface.config(text = "You lose!")
        ratio[1] += 1
        last_game = 1
        computer_choice += 2
    ratio_label.config(text = "Wins: " + str(ratio[0]) + " Losses: " + str(ratio[1]) + " Ties: " + str(ratio[2]))
    first_play = False

Rock = ttk.Button(root, text = "Rock!", command = lambda: choice(0))
Paper = ttk.Button(root, text = "Paper!", command = lambda: choice(1))
Scissors = ttk.Button(root, text = "Scissors!", command = lambda: choice(2))

computer_label.grid(row = 1, column = 0, columnspan = 3, stick = "nsew")
interface.grid(row = 0, column = 0, columnspan = 3, stick = "nsew")
ratio_label.grid(row = 2, column = 0, columnspan = 3, stick = "nsew")
Rock.grid(row = 3, column = 0)
Paper.grid(row = 3, column = 1)
Scissors.grid(row = 3, column = 2)
root.mainloop()