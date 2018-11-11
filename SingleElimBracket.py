import math
import random

#Get how many teams are competing
print("Welcome to the Single-Elimination bracket!")
teams = input("How many people or teams are competing? ")
print("Assign each team a number from 1 to " + teams)

#Decides number of rounds in the tournament
teams = int(teams)
rounds = math.log2(float(teams))
pow2 = int(rounds) ** 2
if (rounds * 10) % 10 != 0:
    rounds = int(rounds) + 1

#Randomly shuffles the bracket
comp = list(range(1, teams))
random.shuffle(comp)

i = 0
while rounds > 0:
#Prints what round this is
    print("Round " + str(i + 1)
    i += int(i) + 1
    rounds -= 1
    roundcomp = 0

#Decides how many teams will be competing this round, and byes
    if (math.log2(teams) * 10) % 10 != 0:
        roundteams = teams - 2 * pow2
    else:
        roundteams = teams
    winners = losers = roundteams / 2

#List of people competing in the round
    if i == 1:
        roundcomp = []
        roundcomp = comp[:roundteams]

#Prints matchups
    j = 0
    while roundteams > 0:
        print(roundcomp[j:(j + 1)])
        j += 2
        roundteams = roundteams - 2

#Takes input of winners of the rounds
    winnerlist = []
    while winners > 0:
        x = input("Type the winners, one per line, in order!")
        winnerlist.append(x)
        winners -= 1

#Winners of this rounds are competing in the next
    roundcomp = winnerlist
