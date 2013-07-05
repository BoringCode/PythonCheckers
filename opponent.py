#Rob Ruester
#Jesse Kanuchok

import cTurtle
from random import *
from math import *
from copy import *
EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)

def rowToLocation(row,size):
    return (4*size)-(size*row)

def colToLocation(col,size):
    return -(4*size)+(size*col)

def getPossibles(CB,player):
    possibles={}
    if player=="black":
        playerTokens=[3,4]
        opponentTokens=[1,2]
        rowInc=-1
    else:
        playerTokens=[1,2]
        opponentTokens=[3,4]
        rowInc=1
    possibles["jumps"]=findJumps(CB,player,playerTokens,opponentTokens,rowInc)
    if possibles["jumps"] == []: #only look for moves if no jumps exist
        possibles["moves"]=findMoves(CB,player,playerTokens,opponentTokens,rowInc)  #puts moves right into possibles D      
    else:
        possibles["moves"] = []
    return possibles

def findMoves(CB,player,playerTokens,opponentTokens,tempRowInc):
    moves=[] 
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens:
                rowInc = tempRowInc
                if isKing(CB,row,col):
                    for rowInc in INCs:
                        for colInc in INCs:
                            toRow=row+rowInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                    moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else:
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return moves

def findJumps(CB,player,playerTokens,opponentTokens,rowInc):
    oldJumps=findSingleJumps(CB,player,playerTokens,opponentTokens,rowInc)
    newJumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps
        newJumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    return newJumps

def findSingleJumps(CB,player,playerTokens,opponentTokens,tempRowInc):
    jumps=[]
    for row in range(8):
        for col in range(8):
            rowInc = tempRowInc
            if CB[row][col] in playerTokens: #if this is a player piece
                if isKing(CB,row,col):
                    for rowInc in INCs:
                        for colInc in INCs: #-1 and 1
                            jump=chr(row+65)+str(col)+":"
                            jumprow=row+rowInc
                            jumpcol=col+colInc
                            torow=row+2*rowInc
                            tocol=col+2*colInc
                            if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                            and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                                jumps.append(jump+chr(torow+65)+str(tocol))
                else:
                    for colInc in INCs: #-1 and 1
                        jump=chr(row+65)+str(col)+":"
                        jumprow=row+rowInc
                        jumpcol=col+colInc
                        torow=row+2*rowInc
                        tocol=col+2*colInc
                        if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                        and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]== EMPTY:
                            jumps.append(jump+chr(torow+65)+str(tocol))
    return jumps

def expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,tempRowInc):
    newJumps=[]
    for oldJump in oldJumps:
        originRow=ord(oldJump[0])-65
        originCol=int(oldJump[1])
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        rowInc = tempRowInc
        if isKing(CB,originRow,originCol):
            for rowInc in INCs:
                for colInc in INCs:
                    jumprow=row+rowInc
                    jumpcol=col+colInc
                    torow=row+2*rowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and CB[jumprow][jumpcol] in opponentTokens and (CB[torow][tocol]==EMPTY or [torow,tocol] == [originRow,originCol]) \
                    and chr(torow+65)+str(tocol) != oldJump[-5:-3] and oldJump[-2:]+":"+chr(torow+65)+str(tocol) not in oldJump \
                    and chr(torow+65)+str(tocol)+":"+oldJump[-2:] not in oldJump:
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
        else:
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
    return newJumps          
            
def strLocToInt(strLoc):
    row=ord(strLoc[0])-65
    col=int(strLoc[1])
    return [row,col]

def intLocToStr(row, col):
    return chr(row+65) + str(col)

def isKing(CB,row,col):
    if CB[row][col] in [2,4]:
        return True
    return False

def makeMove(CB,move,player):
    originRow=ord(move[0])-65
    originCol=int(move[1])
    if move[-2] == "A" and player == "black":
        CB[originRow][originCol] = 4
    elif move[-2] == "H" and player == "red":
        CB[originRow][originCol] = 2
    while len(move)>=5:
        fromRow=ord(move[0])-65
        fromCol=int(move[1])
        toRow=ord(move[3])-65
        toCol=int(move[4])
        temp=CB[fromRow][fromCol]
        CB[fromRow][fromCol]=0                         
        CB[toRow][toCol]=temp
        if fabs(fromRow-toRow)>1: #if jump...
            tweenRow=(fromRow+toRow)//2
            tweenCol=(fromCol+toCol)//2
            CB[tweenRow][tweenCol]=0
        move=move[3:]
        
def getJumpVal(CB, jump):
    points = 0
    indivList = jump.split(":")
    for i in range(len(indivList) - 1):
        jumpedRow = (strLocToInt(indivList[i])[0] + strLocToInt(indivList[i+1])[0]) // 2
        jumpedCol = (strLocToInt(indivList[i])[1] + strLocToInt(indivList[i+1])[1]) // 2
        if CB[jumpedRow][jumpedCol] in [2,4]:
            points += 5
        else:
            points += 3
    return points

def automatedMove(CB,player):
##    possibles=getPossibles(CB,player)
##    if len(possibles["jumps"])>0:
##        index=randint(0,len(possibles["jumps"])-1)
##        return possibles["jumps"][index]
##    index=randint(0,len(possibles["moves"])-1)
##    return possibles["moves"][index]

    #1. make jump if available (dealt with in getPossibles)
    possibles = getPossibles(CB,player)
    possibleList = possibles['moves'] + possibles['jumps']

    bestD = {}
    for move in possibleList:
        bestD[move] = 0

    #2. prefer to jump kings
    #3. prefer longest jumps
    giveJumpPoints(CB,bestD,possibles)
    
    #6. Prefer to avoid moving into jumps
    #7. and moving out of blocks
    #8. Strongly prefer to avoid moving kings into jumps
    #9. and getting kings jumped when moving out of blocks
    #10. save pieces by blocking
    #11. save kings by blocking
    #12. avoid remaining in jumps
    #13. avoid kings remaining in jumps
    blocksAndAvoids(CB,bestD,player)

    #14. Prefer crownings
    giveCrowningPoints(CB,bestD,player)

    #15. When no better alternatives, prefer to move reg pieces (to get more kings)
    #16. Added bonus based on proximity to kinging row
    giveRegMovePoints(CB,bestD,player)

    #17. When less than 
    convergance(CB,bestD,player,possibles)

    #Select a move at random from a list of moves which have the highest point total.
    bestList = []
    maxPoints = max(list(bestD.values()))
    for move in bestD:
        if bestD[move] == maxPoints:
            bestList.append(move)
    move = bestList[randrange(len(bestList))]
    return move

def findPieceCount(CB,player,c):
    #c= "s" for self, "e" for enemy, "a" for all
    if (player == "red" and c == "s") or (player == "black" and c == "e"):
        pieces = [1,2]
    else:
        pieces = [3,4]
    if c == "a":
        pieces = [1,2] + pieces
    pieceCount = 0
    for row in range(8):
        for col in range(8):
            if CB[row][col] in pieces:
                pieceCount += 1
    return pieceCount

def convergance(CB,bestD,player,possibles):
    pieceCount = findPieceCount(CB,player,"e")
    if player == "red":
        enemyPieces = [3,4]
    else:
        enemyPieces = [1,2]
    if pieceCount < 5 and possibles["jumps"] == []: #if we want to converge...
        enemyLocs = []
        for row in range(8):
            for col in range(8):
                if CB[row][col] in enemyPieces:
                    enemyLocs.append(intLocToStr(row,col))
        for move in bestD:
            distL = []
            for otherLoc in enemyLocs:
                distL.append(distance(move[:2],otherLoc))
##            avg = sum(distL) / len(distL)
            minSoFar = 100
            for dist in distL:
                if dist < minSoFar:
                    minSoFar = dist
            goTo = minSoFar
            distL = []
            for otherLoc in enemyLocs:
                distL.append(distance(move[-2:],otherLoc))
##            avg2 = sum(distL) / len(distL)
            minSoFar = 100
            for dist in distL:
                if dist < minSoFar:
                    minSoFar = dist
            if minSoFar < goTo:
##            if avg2 < avg:
                bestD[move] += .001

def distance(loc1,loc2):
    row1, col1 = strLocToInt(loc1)
    row2, col2 = strLocToInt(loc2)
    return sqrt(pow(row2-row1,2)+pow(col2-col1,2))
        
def giveJumpPoints(CB,bestD,possibles):
    if possibles['jumps'] != []:
        for jump in bestD:
            bestD[jump] += getJumpVal(CB, jump)

def blocksAndAvoids(CB,bestD,player):
    for move in bestD:    
        oldJumpTotal = 0
        newJumpTotal = 0
        othersJumps = findOthersJumps(CB,player)
        for jump in othersJumps:
            oldJumpTotal += getJumpVal(CB,jump)
        tempCB = simulateMove(CB,player,move)
        newOthersJumps = findOthersJumps(tempCB,player)
        for jump in newOthersJumps:
            newJumpTotal += getJumpVal(CB,jump)
        bestD[move] += oldJumpTotal - newJumpTotal

def giveCrowningPoints(CB,bestD,player):
    for crownMove in findCrownings(CB,player,bestD):
        bestD[crownMove] += 4

def giveRegMovePoints(CB,bestD,player):
    for move in bestD:
        if not isKing(CB,strLocToInt(move[:2])[0],strLocToInt(move[:2])[1]) and move not in findCrownings(CB,player,bestD) and findPieceCount(CB,player,"a") > 6:
            row = strLocToInt(move[:2])[0]
            if player == "black":
                row = 7 - row
            bestD[move] += row / 10 + .1

def findBlocks(CB,player,bestD):
    #Find jumps for opposing player
    othersJumps = findOthersJumps(CB,player)
    blocks = {}
    for move in bestD:
        blocks[move] = []
        for jump in othersJumps:
            for index in range(3,len(jump),3):
                if jump[index:index+2] == move[-2:]:
                    blocks[move].append(jump)
    return blocks

def findOthersJumps(CB,ownPlayer):
    if ownPlayer=="black":
        player="red"
    else:
        player="black"    
    if player=="black":
        playerTokens=[3,4]
        opponentTokens=[1,2]
        rowInc=-1
    else:
        playerTokens=[1,2]
        opponentTokens=[3,4]
        rowInc=1
    return findJumps(CB,player,playerTokens,opponentTokens,rowInc)
   
def findCrownings(CB,player,bestD):
    crownings=[]
    empties=[]
    if player=="black":
        for col in range(1,8,2):
            if CB[0][col]==EMPTY:
                empties.append("A"+str(col))
    else:
        for col in range(0,8,2):
            if CB[7][col]==EMPTY:
                empties.append("H"+str(col))
    if len(empties)!=0:
        for move in bestD:
            row, col = strLocToInt(move[:2])
            if move[-2:] in empties and CB[row][col] not in [2,4]:
                crownings.append(move)
    return crownings

def simulateMove(CB,player,move):
    tempCB = deepcopy(CB)
    makeMove(tempCB,move,player)
    return tempCB
