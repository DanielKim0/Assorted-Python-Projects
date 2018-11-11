from collections import Counter
from random import sample, randrange


class Card:
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
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        return suits[self.suit] + str(numbers[self.number - 2])

    __repr__ = __str__


class Hand:
    score_order = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight",
                   "Three of a Kind", "Two Pair", "One Pair", "High Card"]

    def __init__(self, *args):
        self.cards = list(args)
        self.num_count = Counter()
        self.num_order = []
        self.suit_count = Counter()
        self.most_common = []
        self.score = 0

    def add_cards(self, card):
        self.cards.extend(card)

    def num_cards(self):
        for card in self.cards:
            self.num_count[card.number] += 1
            self.suit_count[card.suit] += 1

        self.num_order = list(reversed(sorted(list(set(self.num_count)))))
        self.most_common = self.num_count.most_common()

    def straight(self):
        if {2, 3, 4, 5, 14}.issubset(set(self.num_order)):
            return True
        else:
            for x in range(len(self.num_order) - 1):
                if self.num_order[x + 1] - self.num_order[x] != 1:
                    return False
            return True

    def find_score(self):
        self.num_cards()
        if self.suit_count.most_common()[0][1] == 5:
            if {14, 13, 12, 11, 10}.issubset(set(self.num_count)):
                self.score = 0
            elif self.straight():
                self.score = 1
            else:
                self.score = 4
        elif self.most_common[0][1] == 4:
            self.score = 2
        elif self.most_common[0][1] == 3 and self.most_common[1][1] == 2:
            self.score = 3
        elif self.straight():
            self.score = 5
        elif self.most_common[0][1] == 3:
            self.score = 6
        elif self.most_common[0][1] == 2 and self.most_common[1][1] == 2:
            self.score = 7
        elif self.most_common[0][1] == 2:
            self.score = 8
        else:
            self.score = 9

    def __lt__(self, other):
        self.find_score()
        other.find_score()
        if self.score > other.score:
            return True
        elif self.score < other.score:
            return False
        else:
            for x in range(len(self.num_order)):
                if self.num_order[x] < other.num_order[x]:
                    return True
                elif self.num_order[x] > other.num_order[x]:
                    return False
        return False

    def __gt__(self, other):
        self.find_score()
        other.find_score()
        if self.score < other.score:
            return True
        elif self.score > other.score:
            return False
        else:
            for x in range(len(self.num_order)):
                if self.num_order[x] > other.num_order[x]:
                    return True
                elif self.num_order[x] < other.num_order[x]:
                    return False
        return False

    def __eq__(self, other):
        return not (self > other or self < other)

    def __str__(self):
        card_string = ""
        for card in self.cards:
            card_string += str(card)
        return card_string


class Player:
    def __init__(self, name):
        self.points = 1000
        self.name = name
        self.hand = Hand()
        self.fold = False
        self.all_in = False

    def allin(self):
        print("You have gone all in! Good luck!")
        self.points = 0
        self.all_in = True

    def bet_input(self, min_bet, can_raise, pot):
        bet = input("What do you want to do? Type \"fold\" to fold, \"call\" to call, \"raise\" to raise, \n\"pot\" "
                    "to check the current pot, and \"all in\" to go all-in. ")
        if bet == "call":
            if self.points >= min_bet:
                if self.points == min_bet:
                    self.allin()
                else:
                    self.points -= min_bet
                return 0
            else:
                print("You do not have enough points to call!")
                return None
        elif bet == "fold":
            self.fold = True
            print("You have folded.")
            return "fold"
        elif bet == "raise":
            if not can_raise:
                print("The raise limit has been met. You cannot raise.")
                return None
            else:
                try:
                    amount = int(input("How much do you want to raise by? "))
                except ValueError:
                    print("You did not input an integer! Try again.")
                    return None
                else:
                    if amount + min_bet > self.points:
                        print("You don't have enough points for that.")
                        return None
                    else:
                        if self.points == amount + min_bet:
                            self.allin()
                        else:
                            self.points -= (amount + min_bet)
                        return amount
        elif bet == "all in":
            x = self.points
            self.allin()
            return x - min_bet
        elif bet == "pot":
            print("The current pot is " + str(pot) + " and the current bet is " + str(min_bet) + "\n")
        else:
            print("Invalid input. Try again.")
            return None

    def bet(self, min_bet, can_raise, pot):
        raise_amount = None
        while raise_amount is None:
            print("You have " + str(self.points) + " points.")
            raise_amount = self.bet_input(min_bet, can_raise, pot)
        return raise_amount

    def set_hand(self, cards):
        self.hand = Hand(cards[0], cards[1])

    def blind_money(self, num):
        self.points -= min(self.points, num)
        return min(self.points, num)

    def print_hand(self):
        print(self.hand)


class Game:
    def __init__(self):
        self.players = []
        self.pot = 0
        self.turn_count = 0
        self.card_list = []
        self.shown_cards = []
        self.starting_small_blind = 0
        self.small_blind = 0
        self.big_blind = 0

    def reset_players(self):
        for player in self.players:
            player.fold = False
            player.all_in = False

    def deal(self):
        dealt_cards = sample(self.card_list, len(self.players) * 2 + 5)
        for x in range(len(self.players)):
            self.players[x].set_hand(dealt_cards[x * 2: x * 2 + 2])
        self.shown_cards = dealt_cards[len(dealt_cards) - 5:]

    def blind_players(self):
        self.small_blind = (self.small_blind + 1) % len(self.players)
        self.big_blind = (self.big_blind + 1) % len(self.players)
        if self.small_blind == self.big_blind:
            self.big_blind = (self.small_blind + 1) % len(self.players)

    def blinds(self):
        blind = (self.turn_count // 5 + 1) * 5
        blind_pot = 0
        small = self.players[self.small_blind].blind_money(blind)
        big = self.players[self.big_blind].blind_money(blind * 2)
        blind_pot += small
        blind_pot += big
        self.pot += blind_pot

        print("\nTurn " + str(self.turn_count))
        print(self.players[self.small_blind].name + " is the small blind and paid " + str(small) + " points.")
        print(self.players[self.big_blind].name + " is the big blind and paid " + str(big) + " points.")

        return blind

    def fold_check(self):
        not_fold = 0
        for player in self.players:
            if not player.fold:
                not_fold += 1
            if not_fold > 1:
                return False
        return True

    def all_in_check(self):
        for player in self.players:
            if not player.all_in:
                return False
        return True

    def one_move_left(self):
        open_players = 0
        for player in self.players:
            if (not player.fold) and (not player.all_in):
                open_players += 1

        return open_players == 1

    def bet(self, blind=0, initial_bets=None, first=0):
        raises = 0
        calls = 0
        first_move = True
        bet_done = False
        one_move = False

        if initial_bets is None:
            current_bets = [0] * len(self.players)
            current_raise = 0
        else:
            current_bets = initial_bets
            current_raise = blind

        while True:
            for x in range(0, len(self.players)):
                current_player = (x + self.big_blind - first) % len(self.players)
                current = self.players[current_player]
                print("\nIt is " + current.name + "'s turn!")
                print("Current hand: " + str(current.hand))
                if (not current.fold) and (not current.all_in):
                    bet = current.bet(current_raise - current_bets[current_player],
                                      (raises < 3 or len(self.players) == 2), self.pot)
                    # print(bet)  # test
                    if bet == "fold":
                        print(current.name + " folds!")
                        calls += 1
                    elif bet > 0:
                        print(current.name + " bets " + str(bet + current_raise -
                                                            current_bets[current_player]) + " points and raises!")
                        raises += 1
                        calls = 0
                        current_raise += bet
                        current_bets[current_player] = current_raise
                    else:
                        print(current.name + " bets " + str(bet + current_raise -
                                                            current_bets[current_player]) + " points and calls!")
                        calls += 1
                        current_bets[current_player] = current_raise
                elif current.fold:
                    print(current.name + " has already folded!")
                    calls += 1
                else:
                    print(current.name + " has already gone all in!")
                    calls += 1

                if (calls >= len(self.players) - 1 and not first_move) or self.fold_check() or one_move:
                    bet_done = True
                    break

                if x == len(self.players) - 2:
                    first_move = False

                if self.one_move_left():
                    one_move = True

            if bet_done:
                break

        if initial_bets is None:
            self.pot += sum(current_bets)
        else:
            self.pot = sum(current_bets)
        print()

    def first_bet(self):
        bets = [0] * len(self.players)
        bets[self.small_blind] = (self.turn_count // 5 + 1) * 5
        bets[self.big_blind] = (self.turn_count // 5 + 1) * 5 * 2
        self.bet((self.turn_count // 5 + 1) * 5 * 2, bets, 2)

    def show_cards(self):
        print("Community cards: " + str(Hand(self.shown_cards[:])))
        for player in self.players:
            print(player.name + " had", end=" ")
            player.print_hand()

    def check_winner(self):
        if self.fold_check():
            for x in range(len(self.players)):
                if not self.players[x].fold:
                    print(self.players[x].name + " wins!")
                    return [x]
        else:
            for player in self.players:
                player.hand.add_cards(self.shown_cards)
            winners = [0]
            win_hand = self.players[0].hand
            for x in range(1, len(self.players)):
                if self.players[x].hand > win_hand:
                    winners = [x]
                elif self.players[x].hand == win_hand:
                    winners.append(x)
            for y in winners:
                print(self.players[y].name, end="")
            print(" wins with a " + str(Hand.score_order[self.players[winners[0]].hand.score]))
            return winners

    def closest_player(self, winners):
        for x in range(len(self.players)):
            if (x + self.small_blind) % len(self.players) in winners:
                return (x + self.small_blind) % len(self.players)

    def give_money(self, winners):
        for x in winners:
            self.players[x].points += self.pot // len(winners)
            print(self.players[x].name + " got " + str(self.pot // len(winners)) + " chips.")
        if self.pot % len(winners) != 0:
            self.players[self.closest_player(winners)] += self.pot % len(winners)
            print(self.players[self.closest_player(winners)].name + " got " +
                  str(self.pot % len(winners)) + " odd chips.")

    def bust_check(self):
        for player in self.players:
            if player.points == 0:
                print(player.name + " is broke!")
                self.players.remove(player)

    def new_turn(self):
        self.deal()
        self.reset_players()
        self.turn_count += 1
        self.pot = 0

    def bet_round(self, blind, x):
        if not self.fold_check() and not self.all_in_check() and not self.one_move_left():
            print("Community cards: " + str(Hand(self.shown_cards[:x])))
            self.bet(blind)

    def begin_turn(self):
        self.new_turn()
        self.blind_players()
        blind = self.blinds()

        self.first_bet()
        for x in range(3, 6):
            self.bet_round(blind, x)

        self.show_cards()
        self.give_money(self.check_winner())
        self.bust_check()

    def create_deck(self):
        for x in range(2, 15):
            for y in range(4):
                self.card_list.append(Card(y, x))

    def create_players(self):
        while True:
            player_name = input("Player " + str(len(self.players) + 1) + " name: ")
            self.players.append(Player(player_name))
            if len(self.players) >= 2:
                cont = input("Add another player? (y/n): ")
                if cont.lower() == "n":
                    break

    def set_blind_players(self):
        self.starting_small_blind = randrange(len(self.players))
        self.small_blind = self.starting_small_blind
        self.big_blind = (self.small_blind + 1) % len(self.players)

    def winner_check(self):
        if len(self.players) == 1:
            print(self.players[0].name + " has won!")
            return True
        return False

    def start_game(self):
        self.create_players()
        self.set_blind_players()
        self.create_deck()
        while True:
            self.begin_turn()
            if self.winner_check():
                print("The game is over.")
                break


texas = Game()
texas.start_game()

