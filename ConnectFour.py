import sys
board = []
for x in range(6): board.append(["_" for x in range(7)])

def print_board(field):
    for row in field:
        print(" ".join(row))

print("Welcome to Connect Four!")
player1name = input("Player 1's Name: ")
while True:
    player1symbol = input("Player 1 Piece Symbol: ")
    if len(player1symbol) != 1:
        print("Your symbol needs to be one letter only.")
    else:
        break
player2name = input("Player 2's Name: ")
while True:
    player2symbol = input("Player 2 Piece Symbol: ")
    if len(player2symbol) != 1:
        print("Your symbol needs to be one letter only.")
    else:
        break

class player():
    def __init__(self, piece, name):
        self.piece = str(piece)
        self.name = str(name)

    def player_turn(self):
        print("It's " + self.name + "'s turn!")
        piece_placed = False
        while not piece_placed:
            column_choice = input("What column would you like to place your piece in? ")
            if column_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                column_choice = int(column_choice) - 1
                for x in range(6):
                    if board[x][column_choice] != "_":
                        if x == 0:
                            print("That column is full! Please choose another one.")
                            break
                        elif x != 0:
                            print("Piece placed!")
                            piece_placed = True
                            board[x - 1][column_choice] = self.piece
                            break
                if board[5][column_choice] is "_":
                    board[5][column_choice] = self.piece
                    print("Piece placed!")
                    piece_placed = True
            else:
                print("That's not a valid choice for a column. Try again!")

    def four_check(self):
        connect_four = False
        for column in range(3):
            for row in range(6):
                if board[row][column] is board[row][column+1] is board[row][column+2] is board[row][column+3] is self.piece:
                    connect_four = True
        for row in range(3):
            for column in range(6):
                if board[row][column] is board[row+1][column] is board[row+2][column] is board[row+3][column] is self.piece:
                    connect_four = True
        for row in range(3):
            for column in range(4):
                if board[row][column] is board[row+1][column+1] is board[row+2][column+2] is board[row + 3][
                    column+3] is self.piece:
                    connect_four = True
        for row in range(3):
            for column in range(3, 7):
                if board[row][column] is board[row+1][column-1] is board[row+2][column-2] is board[row + 3][
                    column-3] is self.piece:
                    connect_four = True
        if connect_four is True:
            print(self.name + " wins!")
            sys.exit()

player1 = player(player1symbol, player1name)
player2 = player(player2symbol, player2name)

if __name__ == "__main__":
    while True:
        player1.player_turn()
        print_board(board)
        player1.four_check()
        player2.player_turn()
        player2.four_check()
        print_board(board)