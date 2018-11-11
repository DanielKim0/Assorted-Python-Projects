from tkinter import *
from tkinter import ttk
import sys

another = False
placements = {}
current_turn = 0
player1pieces = 12
player2pieces = 12

def make_widgets():
    root = Tk()
    board_text = Text(root, height = 15, width = 15)
    player_turn_label = Label(root, text = " ")
    message_label = Label(root, text = " ")
    enter_box = Entry(root)
    enter_button = Entry(root, text = "Enter?")
    player_time_1 = Label(root, text = " ")
    player_time_2 = Label(root, text = " ")
    retire_button = Button(root, text = "Retire?")
    board_text.grid(row=0, column=0, rowspan=8, columnspan=8, stick = "nsew")
    player_turn_label.grid(row=0, column=8, columnspan=8, stick="nsew")
    message_label.grid(row=1, column=8, columnspan=8, stick="nsew")
    enter_box.grid(row=2, column=8, columnspan=8, stick="nsew")
    enter_button.grid(row=3, column=8, columnspan=8, stick="nsew")
    player_time_1.grid(row=4, column=8, columnspan=8, stick="nsew")
    player_time_2.grid(row=5, column=8, columnspan=8, stick="nsew")
    retire_button.grid(row=6, column=8, rowspan=2, columnspan=8, stick="nsew")
    root.mainloop()

make_widgets()

def piece_captured(player):
    global player1pieces, player2pieces
    if player == 1:
        player1pieces -= 1
        if player1pieces == 0:
            end_game(1)
    elif player == 2:
        player2pieces -= 1
        if player2pieces == 0:
            end_game(2)

def end_game(player):
    if player == 1:
        print("Player 2 Wins!")
    elif player == 2:
        print("Player 1 Wins!")
    sys.exit()

class Piece():
    def __init__(self, player, placement, king = False):
        self.player = player
        # players: 0 for none, 1 for first, 2 for second, 3 for unusable spots
        self.king = king
        self.placement = placement

    def __str__(self):
        if self.player == 1 and self.king is True:
            return "8"
        elif self.player == 2 and self.king is True:
            return "W"
        elif self.player == 1 and self.king is False:
            return "O"
        elif self.player == 2 and self.king is False:
            return "V"
        else:
            return "_"

    def get_valid_moves(self, capture = False):
        valid_moves = []

        try:
            if self.king == True or self.player is 1:
                if placements[self.placement + 4][0].player not in [0, 3, self.player] and placements[self.placement + 8][0].player == 0:
                    valid_moves.append(self.placement + 8)
                if placements[self.placement + 5][0].player not in [0, 3, self.player] and placements[self.placement + 10][0].player == 0:
                    valid_moves.append(self.placement + 10)
        except KeyError: pass

        try:
            if self.king == True or self.player is 2:
                if placements[self.placement - 4][0].player not in [0, 3, self.player] and placements[self.placement - 8][0].player == 0:
                    valid_moves.append(self.placement - 8)
                if placements[self.placement - 5][0].player not in [0, 3, self.player] and placements[self.placement - 10][0].player == 0:
                    valid_moves.append(self.placement - 10)
        except KeyError: pass

        try:
            if len(valid_moves) == 0 and capture == False:
                if self.king is True or self.player is 1:
                    if placements[self.placement + 4][0].player == 0:
                        valid_moves.append(self.placement + 4)
                    if placements[self.placement + 5][0].player == 0:
                        valid_moves.append(self.placement + 5)
        except KeyError: pass

        try:
            if len(valid_moves) == 0 and capture == False:
                if self.king is True or self.player is 2:
                    if placements[self.placement - 4][0].player == 0:
                        valid_moves.append(self.placement - 4)
                    if placements[self.placement - 5][0].player == 0:
                        valid_moves.append(self.placement - 5)
        except KeyError: pass

        return valid_moves

    def movement(self, move):
        global another
        placements[self.placement][0] = Piece(0, self.placement)
        if self.player == 1 and move in [36, 35, 34, 33]:
            self.king = True
            print("Kinged!")
        if self.player == 2 and move in [1, 2, 3, 4]:
            self.king = True
            print("Kinged!")
        placements[move][0] = Piece(self.player, move, self.king)

        if abs(move - self.placement) > 5:
            print("Capture!")
            placements[(move + self.placement) / 2][0] = Piece(0, (move + self.placement) / 2)
            if self.player == 1:
                piece_captured(2)
            elif self.player == 2:
                piece_captured(1)
            another = True
        else:
            another = False

        self.placement = move

    def player_choice(self):
        piece_number = self.player
        valid_moves = self.get_valid_moves()
        if self.player != current_turn:
            print("You cannot do that!")
            return False
        elif valid_moves == []:
            print("There are no valid moves for this piece.")
            return False
        else:
            print("Piece chosen!")
            return valid_moves

    def player_turn(self):
        global another
        valid_moves = placements[self.placement][0].get_valid_moves(another)
        another = False
        if len(valid_moves) > 0:
            for x in valid_moves:
                for item in placements[x][1]:
                    print(str(item + 1), end = " ")
                print()
            print("Choose your move! Enter in a number for the move out of the list you want to choose.")
            x = int(input("Type in 1 for the first move, 2 for the second move, etc."))
            move_chosen = valid_moves[x - 1]
            self.movement(move_chosen)

        while another:
            self.player_turn()

class Player():
    def __init__(self, player_name, player_number):
        self.player_name = player_name
        self.player_number = player_number

    def player_turn(self):
        global current_turn, another
        another = False
        self.movement_check()
        print("It's " + self.player_name + "'s turn!")
        current_turn = self.player_number
        while True:
            print_places(placements)
            choice = self.convert_to_board_spot()
            possible_moves = placements[choice][0].player_choice()
            if possible_moves: break
        placements[choice][0].player_turn()

    def convert_to_board_spot(self):
        while True:
            print("Insert the row and column of the piece that you wish to move this turn.")
            row = int(input("What row?")) - 1
            column = int(input("What column?")) - 1
            if row not in range(1,9) or column not in range(1, 9):
                print("This piece deos not exist!")
            else:
                try:
                    for item in iter(placements):
                        if placements[item][1] == [row, column]:
                            return item
                except IndexError:
                    print("This is not a valid move!")

    def movement_check(self):
        has_moves_left = False
        for x in placements:
            if placements[x][0].player == self.player_number:
                if placements[x][0].get_valid_moves() != []:
                    has_moves_left = True
        if has_moves_left == False:
            end_game(self.player_number)

def print_places(places):
    items = set(range(37)) - set(range(5, 34, 9))
    for x in range(1, 30, 9):
        print(str(places[x][0]) + " _ " + str(places[x+1][0]) + " _ " + str(places[x+2][0]) + " _ " + str(places[x+3][0]) + " _")
        print("_ " + str(places[x+5][0]) + " _ " + str(places[x+6][0]) + " _ " + str(places[x+7][0]) + " _ " + str(places[x+8][0]))

def initialize_board():
    print("Welcome to Checkers!")
    player1name = input("Player 1's Name: ")
    print("Your symbol will be O for regular pieces and 8 for kings.")
    player2name = input("Player 2's Name: ")
    print("Your symbol will be V for regular pieces and W for kings.")

    # Initialize the board
    player1places = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]
    player2places = [36, 35, 34, 33, 31, 30, 29, 28, 27, 26, 25, 24]
    unusuableplaces = [5, 14, 23, 32]

    for x in range(1, 37):
        placements[x] = [Piece(0, x, king=False)]
    for x in player1places:
        placements[x] = [Piece(1, x, king=False)]
    for x in player2places:
        placements[x] = [Piece(2, x, king=False)]
    for x in unusuableplaces:
        placements[x] = [Piece(3, x, king=False)]

    coordinates = []
    for row in range(8):
        if row % 2 == 0:
            for column in range(0, 7, 2):
                coordinates.append([row, column])
        else:
            for column in range(1, 8, 2):
                coordinates.append([row, column])

    items = list(set(range(1, 37)) - set(range(5, 34, 9)))

    for x in range(32):
        item = items[x]
        coordinate = coordinates[x]
        placements[item].append(coordinate)
    for x in range(5, 34, 9):
        placements[x].append([-1, -1])

    player1 = Player(player1name, 1)
    player2 = Player(player2name, 2)

    if __name__ == "__main__":
        while True:
            player1.player_turn()
            player2.player_turn()

initialize_board()

