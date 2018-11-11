from random import choice

class Card:  # taken from my Poker program
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __gt__(self, other):
        return self.number > other.number

    def __lt__(self, other):
        return self.number < other.number

    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        suits = ["\u2660", "\u2665", "\u2666", "\u2663"]
        return suits[self.suit] + self.number

    __repr__ = __str__


class Hand:
    def __init__(self):
        self.cards = []

    def has_num(self, num):
        return True in [card.number == num for card in self.cards]

    def get_score(self):
        total = 0
        for card in self.cards:
            if card.number in ["2", "3", "4", "5", "6", "7", "8", "9"]:
                total += int(card.number)
            elif card.number == "A":
                total += 1
            else:
                total += 10
        return total

    def get_bust(self):
        return self.get_score() > 21

    def add_card(self, num):
        for x in range(num):
            self.cards.append(Card(choice(list(range(4))), choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])))


class Player:
    def __init__(self, name):
        self.points = 1000
        self.name = name
        self.hand = Hand()
        self.turn_done = False
        self.ace = False
        self.bet = 0

    def print_hand(self):
        msg = self.name + "'s cards are " + str([str(card) for card in self.hand.cards])
        if self.hand.has_num("A") and self.hand.get_score() <= 11:
            return msg + " and " + self.name + "'s score is " + str(self.hand.get_score()) + " or " + str(self.hand.get_score() + 10)
        else:
            return msg + " and " + self.name + "'s score is " + str(self.hand.get_score())

    def check_blackjack(self):
        return self.hand.has_num("A") and self.hand.get_score() == 11

    def call(self):
        self.hand.add_card(1)

    def make_bet(self):
        valid_bet = False
        while not valid_bet:
            bet = input("You have " + str(self.points) + " points. How much do you want to bet: ")
            if not bet.isnumeric() or int(bet) > self.points or int(bet) < 1:
                print("Invalid bet!")
            else:
                self.bet = int(bet)
                self.points -= int(bet)
                valid_bet = True

    def start_turn(self):
        print("It is " + self.name + "'s turn!")
        self.turn_done = False
        self.hand = Hand()
        self.hand.add_card(2)

    def turn(self):
        self.start_turn()
        self.make_bet()
        if self.check_blackjack():
            print("You have a blackjack!")
            self.turn_done = True
        while not self.turn_done:
            print(self.print_hand())
            play = input("Hit or stay?")
            if play.lower() == "hit":
                self.call()
                if self.hand.get_bust():
                    self.turn_done = True
            else:
                self.turn_done = True
    def winnings(self, points):
        self.points += points

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def turn(self):
        self.start_turn()
        self.print_hand()
        if self.check_blackjack():
            print("Dealer has a blackjack!")
            self.turn_done = True
        while not self.turn_done:
            print(self.print_hand())
            if (self.hand.get_score() <= 16 or self.hand.has_num("A") and self.hand.get_score() <= 6) and not self.hand.get_bust():
                self.call()
                print("Dealer hits!")
                if self.hand.get_bust():
                    self.turn_done = True
            else:
                print("Dealer stays!")
                self.turn_done = True


class Game():
    def __init__(self):
        name = input("Write your name here: ")
        self.player = Player(name)
        self.dealer = Dealer()

    def get_scores(self, play):
        if play.hand.get_score() < 12 and play.hand.has_num("A"):
            return play.hand.get_score() + 10
        else:
            return play.hand.get_score()


    def play_game(self):
        while self.player.points > 0:
            self.player.turn()
            player_score = self.get_scores(self.player)
            if not self.player.hand.get_bust():
                self.dealer.turn()
                dealer_score = self.get_scores(self.dealer)

            if self.player.check_blackjack() and not self.dealer.check_blackjack():
                print("Player had a blackjack!")
                self.player.winnings(self.player.bet * 3)
            elif self.player.hand.get_bust() or player_score < dealer_score:
                print("Player has lost!")
                self.player.winnings(0)
            elif self.dealer.hand.get_bust() or dealer_score < player_score:
                print("Player has won!")
                self.player.winnings(self.player.bet * 2)
            else:
                print("Dealer and player tied!")
                self.player.winnings(self.player.bet)



game = Game()
game.play_game()