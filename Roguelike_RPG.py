#Program by Daniel Kim, started 2/5/2017

import random
import sys

#Player's level and stats, [MAX HP, ATK, DEF, SPD, MAX EXP]
#HP,EXP are changaable, these are just maxes
playerLevel = 1
playerStats = [25, 5, 3, 3, 10]
#change to [25, 3, 3, 3, 10] after testing

#Current state of player
#Only for stats that can change aside from level ups
playerCurrentHP = 25
playerCurrentEXP = 0
playerCurrentITEMS = []
currentFloorNumber = 1

def startgame():
    global currentFloorNumber
    print("You find yourself at the top of what seems to be a large pyramid.")
    print("All you have is a map, a bag, and your own intuition.")
    print("Will you escape the throes of the pyramid or perish in its clutches?")
    print()
    print("Movement controls: l to move left, r to move right, u to move up,")
    print("d to move down, b for bag, s for stats, m for map, h for help")
    print()
    print("Battle controls: a to attack, b for bag, s for your stats.")
    print("Good luck!")
    print()
    
    try:
        for x in range(1, 10):
            newFloor(x)
            currentFloorNumber += 1
        bossBattle("blueicyhydra", [100, 15, 10, 15])
    except SystemExit:
        print("Your health reached 0. Game over! You lose!")
    
def newFloor(floorNumber):
    #Determines floorsize, used for number of stairs and size of floors
    #Floorsize is 3x3 for floor 1, 5x5 for 2 and 3, 7x7 for 4 and 5, etc.
    floorSize = (floorNumber + 1) // 2 * 2
    
    #Determines location of stairs, which move to next floor
    stairLocation = []
    while len(stairLocation) < floorSize // 2 + 1:
        stairX = random.randrange(0, floorSize + 1)
        stairY = random.randrange(0, floorSize + 1)
        if abs(stairX - floorSize // 2) > 0 or abs(stairY - floorSize // 2) > 0:
            if [stairX, stairY] not in stairLocation:
                stairLocation.append([stairX, stairY])
    
    treasureLocation = []
    if floorNumber > 1:
        while len(treasureLocation) < floorSize * 2:
            treasureX = random.randrange(0, floorSize + 1)
            treasureY = random.randrange(0, floorSize + 1)
            if abs(treasureX - floorSize // 2) > 0 or abs(treasureY - floorSize // 2) > 0:
                if [treasureX, treasureY] not in stairLocation and\
                  [treasureX, treasureY] not in treasureLocation:
                    treasureLocation.append([treasureX, treasureY])
    
    debrisLocation = []
    if floorNumber > 2:
        while len(debrisLocation) < floorSize:
            debrisX = random.randrange(0, floorSize + 1)
            debrisY = random.randrange(0, floorSize + 1)
            if abs(debrisX - floorSize // 2) > 0 or abs(debrisY - floorSize // 2) > 0:
                if [debrisX, debrisY] not in stairLocation and\
                  [debrisX, debrisY] not in treasureLocation and\
                  [debrisX, debrisY] not in debrisLocation:
                    debrisLocation.append([debrisX, debrisY])
    
    trapLocation = []
    if floorNumber > 4:
        while len(trapLocation) < floorSize + 5:
            trapsX = random.randrange(0, floorSize + 1)
            trapsY = random.randrange(0, floorSize + 1)
            if abs(trapsX - floorSize // 2) > 0 or abs(trapsY - floorSize // 2) > 0:
                if [trapsX, trapsY] not in stairLocation and\
                  [trapsX, trapsY] not in treasureLocation and\
                  [trapsX, trapsY] not in debrisLocation and\
                  [trapsX, trapsY] not in trapLocation:
                    trapLocation.append([trapsX, trapsY])
    
    #Current location and floor number
    currentLocation = [floorSize // 2, floorSize // 2]
    print("Welcome to floor " + str(floorNumber) + "!")

    #Initialize map based on how big floor size is
    playerMap = []
    playerMapRow = []
    for num in range(floorSize + 1):
        playerMapRow.append("-")
    for n in range(floorSize + 1):
        playerMap.append(playerMapRow.copy())
    
    playerStep(currentLocation, stairLocation, treasureLocation, \
               debrisLocation, trapLocation, floorSize, playerMap, floorNumber)
    
    #Finding the stairs
    print("You found the stairs, and descended them!")

def playerStep(currentLocation, stairLocation, treasureLocation, \
               debrisLocation, trapLocation, floorSize, playerMap, floorNumber):
    global playerCurrentHP
    
    #Player moves a step
    possibleActions = ["l", "r", "u", "d", "s", "h", "m", "b"]
    while currentLocation not in stairLocation:
        playerMap[floorSize - currentLocation[1]][currentLocation[0]] = "O"
        currentStep = input("What direction would you like to go? ")
        if currentStep not in possibleActions:
            print("You didn't move anywhere!")
        elif currentStep == "l":
            currentLocation[0] -= 1
            print("You moved left.")
        elif currentStep == "r":
            currentLocation[0] += 1
            print("You moved right.")
        elif currentStep == "d":
            currentLocation[1] -= 1
            print("You moved down.")
        elif currentStep == "u":
            currentLocation[1] += 1
            print("You moved up.")
        
        #Player gets to see his stats
        elif currentStep == "s":
            print("Level:" + str(playerLevel))
            print("HP:" + str(playerCurrentHP) + "/" + str(playerStats[0]))
            print("ATK:" + str(playerStats[1]))
            print("DEF:" + str(playerStats[2]))
            print("SPD:" + str(playerStats[3]))
            print("EXP:" + str(playerCurrentEXP) + "/" + str(playerStats[4]))
            print("Floor number:" + str(currentFloorNumber))
        
        #Player gets to see his map
        elif currentStep == "m":
            for num in range(len(playerMap)):
                print("".join(playerMap[num]))
        
        #Player decides to open his bag
        elif currentStep == "b":
            print(playerCurrentITEMS)
            itemchoice = input("Type 1 to use the first item in your bag, 2 to use the second item, etc., or 0 to cancel.")
            inputInBag = False
            for x in range(1, len(playerCurrentITEMS) + 1):
                if str(x) == itemchoice:
                    inputInBag = True
            if inputInBag:
                useitemoverworld(playerCurrentITEMS[int(itemchoice) - 1], playerCurrentITEMS)
            
        #Current actions player can take
        elif currentStep == "h":
            print("""l to move left, r to move right,
                    u to move up, d to move down, stats to view stats, 
                    map to view map""")
        
        #Different scenarios for different types of tiles
        if abs(currentLocation[0]) > floorSize\
          or abs(currentLocation[1]) > floorSize\
          or currentLocation[0] < 0 or currentLocation[1] < 0:
            print("...but was stopped by the pyramid's wall.")
            if currentStep == "l":
                currentLocation[0] += 1
            elif currentStep == "r":
                currentLocation[0] -= 1
            elif currentStep == "d":
                currentLocation[1] += 1
            elif currentStep == "u":
                currentLocation[1] -= 1
        elif currentLocation in debrisLocation:
            playerMap[floorSize - currentLocation[1]][currentLocation[0]] = "D"
            print("...but was stopped by a large pile of debris.")
            if currentStep == "l":
                currentLocation[0] += 1
            elif currentStep == "r":
                currentLocation[0] -= 1
            elif currentStep == "d":
                currentLocation[1] += 1
            elif currentStep == "u":
                currentLocation[1] -= 1
        elif currentLocation in trapLocation:
            playerMap[floorSize - currentLocation[1]][currentLocation[0]] = "X"
            randomTrap = random.randrange(1, 2)
            #change aboove to (0, 9)
            #Different traps have different weights
            trapTypes = {0: "Spike Trap", 1: "Warp Trap", 2: "Attack Trap",\
                         3: "Poison Trap", 4: "Map Trap", 5: "Item Trap",\
                         6: "Spike Trap", 7: "Warp Trap", 8: "Attack Trap"}
            print("You triggered a random trap: " + trapTypes[randomTrap] + "!")
            if randomTrap == 0 or randomTrap == 6:
                playerCurrentHP -= 5
            elif randomTrap == 1 or randomTrap == 7:
                while currentLocation in stairLocation or\
                  currentLocation in treasureLocation or\
                  currentLocation in debrisLocation or\
                  currentLocation in trapLocation:
                    locationX = random.randrange(0, floorSize + 1)
                    locationY = random.randrange(0, floorSize + 1)
                    currentLocation = [locationX, locationY]
            elif randomTrap == 2 or randomTrap == 8:
                randomEncounter = random.randrange(0, 4)
                enemyEncounter(randomEncounter)
            elif randomTrap == 3:
                playerCurrentHP -= playerCurrentHP // 4
            elif randomTrap == 4:
                playerMap = []
                playerMapRow = []
                for num in range(floorSize + 1):
                    playerMapRow.append("-")
                for n in range(floorSize + 1):
                    playerMap.append(playerMapRow.copy())
            elif randomTrap == 5:
                if len(playerCurrentITEMS) > 0:
                    randomItem = random.randrange(0, len(playerCurrentITEMS) - 1)
                    del(playerCurrentITEMS[randomItem])
            playerLoss(playerCurrentHP)
        elif currentLocation in treasureLocation:
            if floorNumber in range(1, 4):
                floorTreasure = ["tiny potion", "potion", "throwing stone", "tiny potion", "tiny potion", "throwing stone"]
            elif floorNumber in range(4, 7):
                floorTreasure = ["potion", "big potion", "explosive rune", "potion", "potion", "explosive rune"]
            elif floorNumber in range(7, 10):
                floorTreasure = ["big potion", "big potion", "book of magic", "big potion", "big potion", "book of magic"]
            randomTreasure = floorTreasure[random.randrange(0, 6)]
            print("You found a treasure box and gained a " + randomTreasure + "!")
            playerCurrentITEMS.append(randomTreasure)
            treasureLocation.remove(currentLocation)
            
        #Roll for random enemy encounters on every step
        randomEncounter = random.randrange(0, 13)
        if randomEncounter <= 3:
            enemyEncounter(randomEncounter)

def useitemoverworld(item, playerCurrentITEMS):
    global playerCurrentHP
    
    if item == "lesser potion":
        playerCurrentHP += 5
        print("Used lesser potion!")
        print("Healed 5 HP!")
        
    elif item == "potion":
        playerCurrentHP += 10
        print("Used potion!")
        print("Healed 10 HP!")
    elif item == "big potion":
        playerCurrentHP += 20
        print("Used big potion!")
        print("Healed 20 HP!")
    else:
        print("Had no effect.")
    if playerCurrentHP > playerStats[0]:
        playerCurrentHP = playerStats[0]
    playerCurrentITEMS.remove(item)

def useitembattle(item, playerCurrentITEMS, currentEnemyStats):
    global playerCurrentHP
    
    if item == "lesser potion":
        playerCurrentHP += 5
        print("Used lesser potion!")
        print("Healed 5 HP!")
    elif item == "potion":
        playerCurrentHP += 10
        print("Used potion!")
        print("Healed 10 HP!")
    elif item == "big potion":
        playerCurrentHP += 20
        print("Used big potion!")
        print("Healed 20 HP!")
    elif item == "throwing stone":
        currentEnemyStats[0] -= 5
        print("Dealt 5 damage!")
    elif item == "explosive rune":
        currentEnemyStats[0] -= 10
        print("Dealt 10 damage!")
    elif item == "book of magic":
        currentEnemyStats[0] -= 20
        print("Dealt 20 damage!")
    if playerCurrentHP > playerStats[0]:
        playerCurrentHP = playerStats[0]
    playerCurrentITEMS.remove(item)

def playerLevelUp(stats):
    #Player gains 4 skill points to spend on stats TO ADD
    global playerLevel
    playerLevel += 1
    print("Reached level " + str(playerLevel) + "!")
    print("You gained 4 skill points!")
    skillpoints = 4

    #EXP to level up increases by 5 every level
    global playerCurrentEXP
    playerCurrentEXP -= playerStats[4]
    playerStats[4] += 5
    print("---------------")
    
    while skillpoints > 0:
        print("What will you decide to upgrade?")
        levelup = input("1 for HP, 2 for ATK, 3 for DEF, 4 for SPD: ")
        if levelup == "1":
            print("Your HP improved from " + str(stats[0]) +\
                  " to " + str(stats[0] + 3) + "!")
            stats[0] += 3
            skillpoints -= 1
        elif levelup == "2":
            print("Your ATK improved from " + str(stats[1]) +\
                  " to " + str(stats[1] + 1) + "!")
            stats[1] += 1
            skillpoints -= 1
        elif levelup == "3":
            print("Your DEF improved from " + str(stats[2]) +\
                  " to " + str(stats[2] + 1) + "!")
            stats[2] += 1
            skillpoints -= 1
        elif levelup == "4":
            print("Your SPD improved from " + str(stats[3]) +\
                  " to " + str(stats[3] + 1) + "!")
            stats[3] += 1
            skillpoints -= 1
        else:
            print("Invalid response, please try again!")

def enemyEncounter(enemyNumber):
    #Encounters are based on what floor player is in
    easyEnemies = {"Slime": [7, 3, 2, 2], "Minion": [7, 4, 1, 2],\
                "Snake": [7, 4, 2, 1], "Bat": [5, 4, 2, 2]}
    mediumEnemies = {"Goblin": [11, 5, 2, 2], "Soldier": [11, 4, 3, 2],\
                  "Orc": [11, 4, 2, 3], "Elf":[9, 5, 2, 3]}
    hardEnemies = {"Vampire": [13, 5, 3, 2], "Wraith": [13, 5, 2, 3],\
                "Demon": [13, 4, 3, 3], "Troll": [11, 5, 3, 3]}
    boss = ["Blue Icy Hydra", [150, 20, 10, 10]]

    #Game picks what enemy chart to draw from based on floor number
    global currentFloorNumber
    if currentFloorNumber in range(1, 4):
        currentEnemy = list(easyEnemies.keys())[enemyNumber]
        currentEnemyStats = easyEnemies[currentEnemy]
    elif currentFloorNumber in range(4, 7):
        currentEnemy = list(mediumEnemies.keys())[enemyNumber]
        currentEnemyStats = mediumEnemies[currentEnemy]
    elif currentFloorNumber in range(7, 10):
        currentEnemy = list(hardEnemies.keys())[enemyNumber]
        currentEnemyStats = hardEnemies[currentEnemy]
    else:
        currentEnemy = boss[0]
        currentEnemyStats = boss[1]

    #Levels of enemies scale to level of player
    #Enemy level-ups happen at random
    global playerLevel
    enemyLevel = playerLevel
    while enemyLevel >= 0:
        if random.random() <= 0.75:
            currentEnemyStats[0] += 1
        if random.random() <= 0.60:
            currentEnemyStats[1] += 1
        if random.random() <= 0.60:
            currentEnemyStats[2] += 1
        if random.random() <= 0.60:
            currentEnemyStats[3] += 1
        enemyLevel -= 1

    print("Enemy Encounter: " + currentEnemy + "!")
    print(currentEnemyStats)
    #remove after testing
    enemyCombat(currentEnemy, currentEnemyStats)

def enemyCombat(enemy, currentEnemyStats):
    #Global variables draw from player's state
    global playerStats
    global playerCurrentHP
    global playerCurrentEXP
    global playerMoves
    global currentFloorNumber
    statsum = sum(currentEnemyStats)
    
    #Decides who moves first
    if playerStats[3] >= currentEnemyStats[3]:
        playerAttack = True
    else:
        playerAttack = False

    #Determines who gets the first attack in a battle, based on speed
    if playerStats[3] - currentEnemyStats[3] >= 0:
        playerAttack = True
    else:
        playerAttack = False
        
    while True:
        if playerAttack == False:
            enemyFight(currentEnemyStats)
            playerAttack = True
        if playerAttack == True:
            playerFight(currentEnemyStats)
            playerAttack = False
        if currentEnemyStats[0] <= 0:
            break
        
    #Two outcomes of the battle
    if currentEnemyStats[0] <= 0:
        print("You win!")
        if random.random() <= .75:
            if currentFloorNumber in range(1, 4):
                floorTreasure = ["tiny potion", "potion", "throwing stone"]
            elif currentFloorNumber in range(4, 7):
                floorTreasure = ["potion", "big potion", "explosive rune"]
            elif currentFloorNumber in range(7, 10):
                floorTreasure = ["big potion", "big potion", "book of magic"]
            randomTreasure = floorTreasure[random.randrange(0, 3)]
            print("The enemy dropped a " + randomTreasure + "!")
            playerCurrentITEMS.append(randomTreasure)
        playerCurrentEXP += statsum
        if playerCurrentEXP >= playerStats[4]:
            playerLevelUp(playerStats)
    elif playerCurrentHP <= 0:
        playerLoss(playerCurrentHP)      

def playerFight(currentEnemyStats):
    #Player's attack and options
    speedMissPercent = playerStats[3] - currentEnemyStats[3]
    playerLoss(playerCurrentHP)
    
    currentAttack = input("What will you do? ")
    if currentAttack == "a":
        if random.random() > (speedMissPercent * -.03):
            if playerStats[1] - currentEnemyStats[2] > 0:
                damage = playerStats[1] - currentEnemyStats[2]
            else:
                damage = 1
            print("You do " + str(damage) + " damage!")
            currentEnemyStats[0] -= damage
        else:
            print("You miss!")
    elif currentAttack == "b":
        print(playerCurrentITEMS)
        itemchoice = input("Type 1 to use the first item in your bag, 2 to use the second item, etc., or 0 to cancel.")
        inputInBag = False
        for x in range(1, len(playerCurrentITEMS) + 1):
            if str(x) == itemchoice:
                inputInBag = True
        if inputInBag:
            useitembattle(playerCurrentITEMS[int(itemchoice) - 1], playerCurrentITEMS, currentEnemyStats)
        else:
            print("Can't use that right now!")
    elif currentAttack == "s":
            print("Level:" + str(playerLevel))
            print("HP:" + str(playerCurrentHP) + "/" + str(playerStats[0]))
            print("ATK:" + str(playerStats[1]))
            print("DEF:" + str(playerStats[2]))
            print("SPD:" + str(playerStats[3]))
            print("EXP:" + str(playerCurrentEXP) + "/" + str(playerStats[4]))
            print("Floor number:" + str(currentFloorNumber))
    else:
        print("You screwed up your attack!")
        damage = 1
        print("You do " + str(damage) + " damage!")
        currentEnemyStats[0] -= damage

def enemyFight(currentEnemyStats):
    global playerCurrentHP
    speedMissPercent = currentEnemyStats[3] - playerStats[3]
    if random.random() > (speedMissPercent * -.05) :
        if currentEnemyStats[1] - playerStats[2] > 0:
            damage = currentEnemyStats[1] - playerStats[2]
        else:
            damage = 1
        print("Enemy attacks!")
        print("Enemy does " + str(damage) + " damage!")
        playerCurrentHP -= damage
    else:
        print("Enemy misses!")

def bossBattle(boss, currentEnemyStats):
    print("You're finally at the end...but there is one thing blocking your path!")
    print("It's a gigantic blueicyhydra, the guardian of this place!")
    print("Only after you defeat him can you leave, so you begin the fight!")
    global playerStats
    global playerCurrentHP
    global playerCurrentEXP
    global playerMoves
    
    #Decides who moves first
    if playerStats[3] >= currentEnemyStats[3]:
        playerAttack = True
    else:
        playerAttack = False

    #Determines who gets the first attack in a battle, based on speed
    if playerStats[3] - currentEnemyStats[3] >= 0:
        playerAttack = True
    else:
        playerAttack = False
        
    while True:
        if playerAttack == False:
            bossFight(currentEnemyStats)
            playerAttack = True
        if playerAttack == True:
            playerFight(currentEnemyStats)
            playerAttack = False
        if currentEnemyStats[0] <= 0:
            break
        
    #Two outcomes of the battle
    if currentEnemyStats[0] <= 0:
        print("You have finally defeated the blueicyhydra and have escaped the pyramid!")

def bossFight(currentEnemyStats):
    global playerCurrentHP
    
    if random.random() < .50:
        if currentEnemyStats[1] - playerStats[2] > 0:
            damage = currentEnemyStats[1] - playerStats[2]
        else:
            damage = 1
        print("blueicyhydra attacks and does " + str(damage) + " damage!")
    elif random.random() < .75:
        damage = 10
        print("blueicyhydra uses dragonblade and does " + str(damage) + " damage!")
    else:
        damage = playerCurrentHP // 4
        print("blueicyhydra uses guillotine and does " + str(damage) + " damage!")
    playerCurrentHP -= damage
        

def playerLoss(currentPlayerHP):
    if currentPlayerHP <= 0:
        sys.exit()

startgame()