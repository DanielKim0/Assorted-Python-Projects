import random
import math

#Tournament Pools
playernum = int(input("How many players are competing: "))
poolnum = int(input("How many pools: "))
roundnum = int(input("How many rounds: "))
finalnum = int(input("How many people in finals: "))
splitnum = math.ceil(playernum / poolnum)

def createrecords(playernum):
    matchhistory = {}
    for player in range(1, playernum + 1):
        matchhistory[player] = [0, 0, 0] #games, wins, points
    return matchhistory

def splitlist(poolnum, splitnum, players, pools):
    for num in range(poolnum):
        print(players[splitnum * num: splitnum * (num+1)])
        pools.append(players[splitnum * num: splitnum * (num+1)])

def poollist(pools, splitnum):
    totalmatch = 0
    for group in pools:
        poolmatch = []
        print()
        print("Pool " + str(pools.index(group) + 1) + ":")
        for num in range(0, len(group)):
            for x in range(num + 1, len(group)):
                poolmatch.append([group[x], group[num]])
                totalmatch += 1
        poolmatch = random.sample(poolmatch, len(poolmatch))
        for num in range(len(poolmatch)):
            print("Match " + str(num + 1) + ": " + str(poolmatch[num][0]) + " vs " + str(poolmatch[num][1]))
        if len(poolmatch) == 0:
            print("No matches for this pool!")
    return totalmatch
    
def matchresult(matchhistory):
    #draws
    confirm = False
    while not confirm:
        print("Please enter match stats!")
        draws = input("Was the match a draw? Type Y or N.")
        if draws is "Y" or draws is "y":
            player1 = int(input("Player 1: "))
            player2 = int(input("Player 2: "))
            player1points = float(input("Player 1's Points: "))
            player2points = float(input("Player 2's Points: "))
        else:
            winner = int(input("Winner: "))
            loser = int(input("Loser: "))
            winnerpoints = float(input("Winner's Points: "))
            loserpoints = float(input("Loser's Points: "))
        query = input("Confirm? Type Y or N.")
        if query is "Y":
            confirm = True
        else:
            confirm = False
    print("Match recorded!")
    if draws is "Y" or draws is "y":
        matchhistory[player1][0] += 1
        matchhistory[player2][0] += 1
        matchhistory[player1][1] += .5
        matchhistory[player2][1] += .5
        matchhistory[player1][2] += player1points
        matchhistory[player2][2] += player2points
    else:
        matchhistory[winner][0] += 1
        matchhistory[winner][1] += 1
        matchhistory[loser][0] += 1
        matchhistory[winner][2] += winnerpoints
        matchhistory[loser][2] += loserpoints

def decidefinals(finalnum, matchhistory, playernum):
    criteria = {}
    finals = []
    for player in range(1, playernum + 1):
        criteria[player] = matchhistory[1] / matchhistory[0]
    gameratio = set(criteria.values())
    while finals < finalnum:
        for item in criteria:
            if criteria[item] == max(gameratio):
                del(criteria[item])
                finals.append(item)
        gameratio.remove(max(gameratio))
        

def generatematch(playernum, poolnum, roundnum, splitnum):
    matchhistory = createrecords(playernum)
    print(matchhistory)
    for num in range(roundnum):
        pools = []
        players = random.sample(range(1, playernum + 1), playernum)
        splitlist(poolnum, splitnum, players, pools)
        print()
        print("Round " + str(num + 1) + ":")
        print(pools)
        for num in range(poollist(pools, splitnum)):
            matchresult(matchhistory)
    decidefinals(finalnum, matchhistory, playernum)

generatematch(playernum, poolnum, roundnum, splitnum)


