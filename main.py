#Graphical stuff
import cTurtle
import random
import time
t = cTurtle.Turtle()
t.ht()
t.up()

runs = 10
wins = {"light": 0, "dark": 0}

#Game setup
light = "white"
dark = "#C40003"
size = 60
debugger = False
EMPTY = 0
VALID_RANGE = range(8)
maxMoves = 10000

#The game tracker
CB = []

#PLAYER CODE
def getPossibles(CB, player):
    possibles = {}
    #column checks
    incs = [-1, 1]
    jumpIncs = [-2, 2]
    #set up the variables depending upon the player
    if player == 3 :
        playerPieces = [3,4]
        opponentPieces= [1,2]
        rowInc = -1
        jumpInc = -2
        opponent = 1
    else :
        playerPieces = [1,2]
        opponentPieces = [3,4]
        rowInc = 1
        jumpInc = 2
        opponent = 3
    #First get all the possible moves (1 row and 1 col diagonal moves)
    possibles["moves"] = findMoves(CB, player, playerPieces, opponentPieces, rowInc, incs)
    #Next get all the possible jumps (2 row and 2 col diagonal moves that go over an opponent)
    possibles["jumps"] = findMoves(CB, player, playerPieces, opponentPieces, jumpInc, jumpIncs)
    #Calculate if there are any crownings in any of my moves or jumps
    possibles["crownings"] = findCrownings(CB, player, possibles["moves"] + possibles["jumps"])
    #Calculate if any of my jumps or moves can block the opponent from jumping
    possibles["blocks"] = findBlocks(CB, opponent, possibles["moves"] + possibles["jumps"])
    return possibles
def findBlocks(CB, opponent, playerMoves) :
    #Bascially I'm calling a block a move that prevents a jump, this means that a block can include moving away from the opponent.
    blocks = []
    jumpIncs = [-2, 2]
    #This is a little verbose, but this is used to calculate the jumps that the opponent can make
    if opponent == 3 :
        opponentPieces = [3,4]
        playerPieces= [1,2]
        jumpInc = -2
        player = 1
    else :
        opponentPieces = [1,2]
        playerPieces = [3,4]
        jumpInc = 2
        player = 3
    #Get the opponent jumps
    jumps = findMoves(CB, opponent, opponentPieces, playerPieces, jumpInc, jumpIncs)
    #start looping through the jumps
    for jump in jumps :
        #Future proof, can handle multiple jumps
        moves = jump.split(":")
        #loop through each part of the jump, starting at the second part (I only want the "resting" place of the jump, so I can move to it and block it)
        for i in range(1, len(moves)) :
            #loop through the moves that my player can make
            for playerMove in playerMoves :
                #check if final resting place of this move is also the finishing location of the jump
                if playerMove[-2:] == moves[i] :
                    #Hey, put it in the blocks list
                    if (playerMove not in blocks) :
                        blocks.append(playerMove)
    return blocks                 
def findCrownings(CB, player, moves) :
    crownings = []
    #Loop through all possible moves (including jumps)
    for move in moves :
        #Split each move down the middle
        subMoves = move.split(":")
        #Check to make sure the piece isn't already a king
        if (CB[getRow(subMoves[0][0], False)][getCol(subMoves[0][1], False)] != player + 1) :
            #loop through each of the submoves (could be a jump or multiple jump)
            for subMove in subMoves :
                #If the player is red (black) and has just landed on the A row, king it. If player is white and has landed on the H row, king it.
                if (player == 3 and subMove[0] == "A") or (player == 1 and subMove[0] == "H") :
                    if (move not in crownings) :
                        crownings.append(move)
    return crownings
def findMoves(CB, player, playerPieces, opponentPieces, rowInc, INCs) :
    moves=[]
    #process all board positions
    for row in VALID_RANGE :
        for col in VALID_RANGE :
            if CB[row][col] in playerPieces :
                if CB[row][col] not in [2,4] : #not a king
                    for colInc in INCs :
                        toRow = row + rowInc
                        toCol = col + colInc
                        move = str(chr(row + 65) + str(col + 1) + ":" + chr(toRow + 65) + str(toCol + 1))
                        #Basic check to make sure the move is valid
                        if (toCol in VALID_RANGE and toRow in VALID_RANGE and CB[toRow][toCol] == EMPTY ) :
                            #Detect a jump
                            if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                #Is a valid jump?
                                if (CB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                    #The jump is good!
                                    copyCB = copyList(CB)
                                    #set the game tracker
                                    startPiece = copyCB[row][col]
                                    copyCB[row][col] = 0
                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                    copyCB[toRow][toCol] = startPiece
                                    newRow = toRow
                                    newCol = toCol
                                    jump = True
                                    #While I can still jump, continue to search for a new jump (multi jumps)
                                    while (jump) :
                                        row = newRow
                                        col = newCol
                                        jump = False
                                        for colInc in INCs :
                                            #if there are multiple directions to go, I want only the first one
                                            if not(jump) :
                                                toRow = row + rowInc
                                                toCol = col + colInc
                                                if (toCol in VALID_RANGE and toRow in VALID_RANGE and copyCB[toRow][toCol] == EMPTY ) :
                                                    #Detect a jump
                                                    if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                                        #Is a valid jump?
                                                        if (copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                                            #set the game tracker
                                                            startPiece = copyCB[row][col]
                                                            copyCB[row][col] = 0
                                                            copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                            copyCB[toRow][toCol] = startPiece
                                                            newRow = toRow
                                                            newCol = toCol
                                                            jump = True
                                                            move += ":" + chr(newRow + 65) + str(newCol + 1)
                                    moves.append(move)
                            #Not a jump? Okay, it must be a valid move. Continue.
                            else :
                                moves.append(move)
                else: #is a king
                    for rInc in INCs :
                        for colInc in INCs :
                            toRow = row + rInc
                            toCol = col + colInc
                            move = str(chr(row + 65) + str(col + 1) + ":" + chr(toRow + 65) + str(toCol + 1))
                            if (toCol in VALID_RANGE and toRow in VALID_RANGE and CB[toRow][toCol] == EMPTY ) :
                                #jump
                                if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                    if (CB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                        jump = True
                                        copyCB = copyList(CB)
                                        startPiece = copyCB[row][col]
                                        copyCB[row][col] = 0
                                        copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                        copyCB[toRow][toCol] = startPiece
                                        newRow = toRow
                                        newCol = toCol
                                        while (jump) :
                                            row = newRow
                                            col = newCol
                                            jump = False
                                            for rInc in INCs :
                                                for colInc in INCs :
                                                    if not(jump) :
                                                        toRow = row + rInc
                                                        toCol = col + colInc
                                                        if (toCol in VALID_RANGE and toRow in VALID_RANGE and copyCB[toRow][toCol] == EMPTY ) :
                                                            #Detect a jump
                                                            if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                                                #Is a valid jump?
                                                                if (copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                                                    #set the game tracker
                                                                    startPiece = copyCB[row][col]
                                                                    copyCB[row][col] = 0
                                                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                                    copyCB[toRow][toCol] = startPiece
                                                                    newRow = toRow
                                                                    newCol = toCol
                                                                    jump = True
                                                                    move += ":" + chr(newRow + 65) + str(newCol + 1)
                                        moves.append(move)
                                else :
                                    moves.append(move)
    return moves
#ACTUAL GAME
def getRow(c, coor = True) :
    c = str(c)
    topY = 4*size
    if (ord(c) >= 65 and ord(c) <= 72) :
        #return Y val if true, return 0 - 7 if not
        if (coor == True) :
            return topY - ((abs(65 - ord(c))) * size)
        else :
            return abs(65 - ord(c))
    return "failed"
def getCol(c, coor = True) :
    #handle errors
    try :
        c = int(c)
        topX = -4*size
        if (c >= 1 and c <= 8) :
            #Return X val if true, return 0 - 7 if not
            if (coor == True) :
                return topX + ((c - 1) * size)
            else :
                return (c - 1)
        return "failed"
    except :
        return "failed" 
#give me a square!
def drawSquare(t,x,y,size,color) :
    t.tracer(False)
    t.up()
    t.goto(x,y)
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    for i in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()
#give me a circle!
def drawPiece(t, x, y, size, color, king = False) :
    t.tracer(False)
    radius = size / 2.5
    t.up()
    t.goto(x + (0.5*size), y - (0.12 * size))
    t.setheading(0)
    t.down()
    t.width(2)
    t.color("#200000")
    t.fillcolor(color)
    t.begin_fill()
    circumference= 2 * 3.14159 * radius
    Len = circumference / 360
    for i in range(360):
        t.forward(Len)
        t.right(1)
    t.end_fill()
    t.width(1)
    #king me
    if (king == True) :
        t.up()
        t.goto(x + (0.35*size), y - size * 0.75)
        #type a "K" for king of course
        t.write("K",font=("Arial",12,"bold"))
        t.down()
def drawDarkLightRow(t,x,y,size) :
    for i in range(4):
        drawSquare(t,x,y,size,"#D18B47")
        x=x+size
        drawSquare(t,x,y,size,"#FFCE9E")
        x=x+size
def drawLightDarkRow(t,x,y,size) :
    for i in range(4):
        drawSquare(t,x,y,size,"#FFCE9E")
        x=x+size
        drawSquare(t,x,y,size,"#D18B47")
        x=x+size
def labelBoard(t, size) :
    t.up()
    t.goto(-(3.6*size),(4.1*size))
    t.pencolor('#000000')
    for i in range(1, 9):
        t.write(str(i),font=("Arial",12,"bold"))
        t.forward(size)
    t.goto(-(4.5*size),(3.4*size))
    for i in range(8):
        t.write(chr(65+i),font=("Arial",12,"bold"))
        t.goto(-(4.5*size),((4*size)+(i*-size)-(1.7*size)))
def drawCheckerBoard(t,x,y,size) :
    for i in range(4):
        drawLightDarkRow(t,x,y,size)
        y = y-size
        drawDarkLightRow(t,x,y,size)
        y = y-size
def initialState(t, size) :
    for row in range(0, len(CB)) :
        y = getRow(chr(row + 65))
        for col in range(0, len(CB[row])) :
            x = getCol(col + 1)
            if (CB[row][col] in range(1, 5)) :
                if (CB[row][col] in range(1, 3)) :
                    color = light
                else :
                    color = dark
                if (CB[row][col] == 2 or CB[row][col] == 4) :
                    king = True
                else :
                    king = False
                if (runs < 2) :
                    drawPiece(t, x, y, size, color, king)
def moveChecker(move) :
    t.tracer(False)
    king = False
    moves = move.split(":")
    currRow = getRow(moves[0][0], False)
    currCol = getCol(moves[0][1], False)
    currY = getRow(moves[0][0])
    currX = getCol(moves[0][1])
    currPiece = CB[currRow][currCol]
    for move in range(1, len(moves)) :
        #remove the current piece
        if (runs < 2) :
            drawSquare(t, currX, currY, size, "#D18B47")
        CB[currRow][currCol] = 0
        #move the piece
        evalRow = getRow(moves[move][0], False)
        evalCol = getCol(moves[move][1], False)
        evalY = getRow(moves[move][0])
        evalX = getCol(moves[move][1])
        #calculate if double jump
        if (abs(evalRow - currRow) == 2) and (abs(evalCol - currCol) == 2) :
            CB[currRow + (evalRow - currRow) // 2][currCol + (evalCol - currCol) // 2] = 0
            eraseY = getRow(chr((currRow + (evalRow - currRow) // 2) + 65))
            eraseX = getCol((currCol + 1) + ((evalCol - currCol) // 2))
            if (runs < 2) :
                drawSquare(t, eraseX, eraseY, size, "#D18B47")
        if currPiece == 1 or currPiece == 2 :
            color = light
            #king me
            if (evalRow == 7) or (currPiece == 2) :
                currPiece = 2
                king = True
        else :
            color = dark
            if (evalRow == 0) or (currPiece == 4) :
                currPiece = 4
                king = True
        if (runs < 2) :
            drawPiece(t, evalX, evalY, size, color, king)
        CB[evalRow][evalCol] = currPiece
        #I want to evaluate the current position next time
        currRow = evalRow
        currCol = evalCol
        currY = evalY
        currX = evalX
        currPiece = CB[evalRow][evalCol]
        if (runs < 2) :
            updateState()
#I'm too lazy to type t.tracer(True)
def updateState() :
    t.tracer(True)
#Is it over yet?
def gameOver() :
    lightCount = 0
    darkCount = 0
    for row in CB :
        for col in row :
            if (col == 1 or col == 2) :
                lightCount += 1
            elif (col == 3 or col == 4) :
                darkCount += 1
    if (lightCount == 0) :
        msg("Dark player has won!", "success")
        wins["dark"] += 1
        return True
    elif (darkCount == 0) :
        msg("Light player has won!", "success")
        wins["light"] += 1
        return True
    lightPlayer = getPossibles(CB, 1)
    darkPlayer = getPossibles(CB, 3)
    if (len(lightPlayer["jumps"]) + len(lightPlayer["moves"]) == 0) and (len(darkPlayer["jumps"]) + len(darkPlayer["moves"]) == 0) :
        msg("Neither player can make a move, draw.", "success")
        return True
    elif (len(lightPlayer["jumps"]) + len(lightPlayer["moves"]) == 0) :
        msg("Light player can't make a move, dark player wins!", "success")
        wins["dark"] += 1
        return True
    elif (len(darkPlayer["jumps"]) + len(darkPlayer["moves"]) == 0) :
        msg("Dark player can't make a move, light player wins!", "success")
        wins["light"] += 1
        return True        
    return False
#I got tired of making my info messages pretty(ish)
def msg(msg, typeM) :
    if (typeM == "error") :
        print("ERROR - " + msg)
    else :
        print("SUCCESS - " + msg)
#verification of moves
def validMove(move, player) :
    possibles = getPossibles(CB, player)
    if len(possibles["jumps"]) > 0 :
        if move not in possibles["jumps"] :
            msg("A jump must be taken!", "error")
            return False
    elif move not in possibles["moves"]: #includes crowning and blocking moves
        msg("Invalid move!", "error")
        return False
    return True
#make a complete copy of a list, including internal lists
def copyList(inList):
    if isinstance(inList, list):
        return list( map(copyList, inList) )
    return inList
def showBoard(CB) :
    print("  1 2 3 4 5 6 7 8")
    row = 65
    for i in range(8) :
        print(chr(row), end=" ")
        for item in range(len(CB[i])) :
            print(CB[i][item], end=" ")
        print()
        row += 1
def importGame() :
    if (runs < 2) :
        filename = input("Enter a filename => ")
    else :
        filename = ""
    while filename[-4:] != ".txt" and filename != "" or filename == ".txt" :
        print("Invalid filename")
        filename = input("Enter a filename => ")
    if (filename != "") :
        gamefile = open(filename, "r")
        currentPlayer = gamefile.readline().replace("\n", "")
        row = 0
        for aline in gamefile :
            CB.append([])
            for i in range(8) :
                if (ord(aline[i]) in range(48, 53)) :
                    #no invalid board locations
                    if (row % 2 != i % 2) :
                        CB[-1].append(int(aline[i]))
                    else :
                        CB[-1].append(0)
            row += 1
        print("File imported.")
        gamefile.close
    else :
        currentPlayer = "white"
        for team in range(1, 4, 2) :
            for i in range(3) :
                CB.append([])
                for r in range(4) :
                    if (i % 2 == 0 and team == 1) or (i % 2 != 0 and team == 3) :
                        CB[-1].append(0)
                        CB[-1].append(team)
                    else :
                        CB[-1].append(team)
                        CB[-1].append(0)
        CB.insert(3, [0, 0, 0, 0, 0, 0, 0, 0])
        CB.insert(4, [0, 0, 0, 0, 0, 0, 0, 0])
        print("Default board set up.")
    return currentPlayer
#The smart one
def automatedMove(color) :
    if (color == "white") :
        player = 1
    elif (color == "black") :
        player = 3
    else :
        player = color
    possibles = getPossibles(CB, player)
    if player == 3 :
        opponent = 1
    else :
        opponent = 3
    #Jumps are required, so if there are jumps those are my only options
    if (len(possibles["jumps"]) > 0) :
        options = possibles["jumps"]
    else :
        options = possibles["moves"]
    #Okay, I've decided on my best bet so far (jumps or moves)
    #Now I need to actually think ahead, see around corners
    #Pick some moves, more advanced!
    #each move is weighted, the move(s) with the lowest weighting gets to go forward
    weighting = []
    if (debugger) :
        print("Current options -", options)
    #I only have one option, why bother checking to see if it is good?
    if (len(options) > 1) :
        #All the variables that I take into account:
        #If I'm moving to a "safe" spot (col 0 or 7)
        #If I'm moving to a crowning location
        #If I'm blocking a jump
        #Whether I could be jumped if I move to a particular spot.
        #If I could be jumped in a multi jump if I move
        #Am I a king? Then I don't want to be jumped if possible.
        #If moving would remove a block and enable a jump.
        #If moving would allow a crowning
        #Am I a king? Try to make sure I move towards my closest opponent
        #####
        #What does this get me? A very defensive player that thinks carefully before moving.
        for i in range(len(options)) :
            if (debugger) :
                print("Possible move -", options[i])
            weighting.append(0)
            #is the move a crowning or a block?
            if options[i] in possibles["crownings"] :
                weighting[-1] += -2
                if (debugger) :
                    print("Moving would result in a crowning, decreasing weighting by 1")
            if (options[i] in possibles["blocks"]) :
                weighting[-1] += -3
                if (debugger) :
                    print("Moving would result in a block, decreasing weighting by 2")
            #Multi jumps
            if (len(options[i]) > 5) :
                weighting[-1] += -1
                if (debugger) :
                    print("Multi jump, decreasing weighting by 1")
            #Simulate the move in a copy of the game tracker
            moves = options[i].split(":")
            #Get a copy of the game tracker
            copyCB = copyList(CB)
            #Adjust the game tracker
            currRow = getRow(moves[0][0], False)
            currCol = getCol(moves[0][1], False)
            currSquare = copyCB[currRow][currCol]
            origSquare = currSquare
            for move in range(1, len(moves)) :
                toRow = getRow(moves[move][0], False)
                toCol = getCol(moves[move][1], False)
                copyCB[currRow][currCol] = 0
                if (abs(toRow - currRow) == 2) and (abs(toCol - currCol) == 2) :
                    copyCB[toRow + (currRow - toRow) // 2][toCol + (currCol - toCol) // 2] = 0
                if (toRow in [0, 7]) :
                    currSquare = player + 1
                copyCB[toRow][toCol] = currSquare
                currRow = toRow
                currCol = toCol
            #If I'm moving to a "safe" spot, prefer it
            if (currCol in [0, 7]) :
                weighting[-1] += -2
                if (debugger) :
                    print("Moving would move to a safe spot, decreasing weighting by 2")
            #Finished adjusting game tracker, let's get down to business
            #Get the opponent moves
            opponentPossibles = getPossibles(copyCB, opponent)
            if (debugger) :
                if (len(opponentPossibles["jumps"]) > 0) :
                    print("Possible jumps -", opponentPossibles["jumps"])
            for jump in opponentPossibles["jumps"] :
                #If my jump is better then his, leave my jump in.
                if (len(options[i]) > len(jump)) :
                    weighting[-1] += -3
                    if (debugger) :
                        print("My jump is a better multiple jump, decreasing weighting by 3")
                else :
                    movesOp = jump.split(":")
                    currRowOp = getRow(movesOp[0][0], False)
                    currColOp = getCol(movesOp[0][1], False)
                    for move in range(len(moves)) :
                        toRowOp = getRow(movesOp[move][0], False)
                        toColOp = getCol(movesOp[move][1], False)
                        #Check to make sure I'm not moving into a jump
                        if (toRowOp + (currRowOp - toRowOp) // 2 == toRow) and (toColOp + (currColOp - toColOp) // 2 == toCol) :
                            weighting[-1] += 3
                            if (debugger) :
                                print("Moving would allow a jump, increasing weighting by 3")
                            #multi jump, weight it even higher because I would prefer a different move
                            if (len(jump) > 5) :
                                weighting[-1] += 2
                                if (debugger) :
                                    print("Moving would allow a multi jump, increasing weighting by 2")
                            #king, I would prefer this not be jumped
                            if (currSquare in [2, 4]) :
                                weighting[-1] += 1
                                if (debugger) :
                                    print("Piece is a king and could be jumped during this move, increasing weighting by 1")
                        #Check to make sure I'm not removing a block
                        if (toRowOp == getRow(moves[0][0], False) and toColOp == getCol(moves[0][1], False)) :
                            #check to see if jumped piece is one of my other pieces
                            if (toRowOp + (currRowOp - toRowOp) // 2 != toRow) or (toColOp + (currColOp - toColOp) // 2 != toCol) :
                                weighting[-1] += 3
                                if (debugger) :
                                    print("Piece is blocking a jump, increasing weighting by 3")
                                #multi jump, weight it even higher because I would prefer a different move
                                if (len(jump) > 5) :
                                    weighting[-1] += 2
                                    if (debugger) :
                                        print("Removing this block would allow a multi jump, increasing weighting by 2")
                        currRowOp = toRowOp
                        currColOp = toColOp
            #check if moving would allow a crowning
            if (debugger) :
                if (len(opponentPossibles["crownings"]) > 0) :
                    print("Possible crownings -", opponentPossibles["crownings"])
            for crown in opponentPossibles["crownings"] :
                if (crown.find(moves[0][0] + moves[0][1]) != -1) :
                    weighting[-1] += 2
                    if (debugger) :
                        print("Moving would allow an opponent crowning, increasing weighting by 2")
            #Basic path finding, move in direction of nearest piece
            if (options[i] in possibles["moves"] and options[i] not in possibles["blocks"] and origSquare == player + 1) :
                locations = []
                for row in VALID_RANGE :
                    for col in VALID_RANGE :
                        if (CB[row][col] in [opponent, opponent + 1]) :
                            locations.append([row, col])
                if (len(locations) > 0) :
                    closest = [locations[0][0], locations[0][1]]
                    #get the closest piece
                    for location in locations :
                        #is this piece jumpable?
                        if (location[0] not in [0, 7]) and (location[1] not in [0, 7]) :
                                rowDiff = abs(location[0] - getRow(moves[0][0], False))
                                colDiff = abs(location[1] - getCol(moves[0][1], False))
                                if (rowDiff <= abs(closest[0] - getRow(moves[0][0], False))) and (colDiff <= abs(closest[1] - getCol(moves[0][1], False))) :
                                    closest[0] = location[0]
                                    closest[1] = location[1]
                    if (closest[0] > getRow(moves[0][0], False) and (getRow(moves[0][0], False) - getRow(moves[-1][0], False) > 0)) or (closest[0] < getRow(moves[0][0], False) and (getRow(moves[0][0], False) - getRow(moves[-1][0], False) < 0)) :
                        weighting[-1] += 1
                        if (debugger) :
                            print("Piece is moving row away from nearest piece, increasing weighting by 1")
                        #Detect moving a column
                        if (closest[1] >= getCol(moves[-1][1], False) and (getCol(moves[0][1], False) - getCol(moves[-1][1], False) > 0)) or (closest[1] >= getCol(moves[-1][1], False) and (getCol(moves[0][1], False) - getCol(moves[-1][1], False) < 0)) :
                            weighting[-1] += 1
                            if (debugger) :
                                print("Piece is moving col away from nearest piece, increasing weighting by 1")
            if (debugger) :
                print()
    #The final moves list, these are the "best of the best"
    final = []
    if (len(weighting) != 0) :
        if (debugger) :
            print("Weighting -", weighting)
        for i in range(len(weighting)) :
            #Is the current value the lowest value in the list? If so append the parrell value in the options list to the final moves list
            if (weighting[i] == min(weighting)) :
                final.append(options[i])
    else :
        final = options
    #random for now
    if (debugger) :
        print("Ideal moves -", final)
    if (len(final) > 0) :
        #There could be more than one, but in theory they are all equal in how "good" they are. Pick one randomly
        index = random.randint(0, len(final) - 1)
        return final[index]
    else :
        #There were no moves (unlikely, must be a bug)
        return False

#The slightly smarter one
def automatedMoveSmartish(player) :
    possibles = getPossibles(CB, player)
    jumpIncs = [-2, 2]
    if player == 3 :
        opponent = 1
        opponentPieces = [1,2]
        playerPieces= [3,4]
        jumpInc = 2
    else :
        opponent = 3
        opponentPieces = [3,4]
        playerPieces = [1,2]
        jumpInc = -2
    ideal = []
    #Jumps are required, so if there are jumps those are my only options
    if (len(possibles["jumps"]) > 0) :
        options = possibles["jumps"]
    else :
        options = possibles["moves"]
    #Okay, I prefer crownings and blocks.
    for move in options :
        if move in possibles["crownings"] or move in possibles["blocks"] :
            ideal.append(move)
    #If I still haven't decided on a perfect move, just give me all the options
    if (len(ideal) == 0) :
        ideal = options
    #Okay, I've decided on my best bet so far (jumps, crownings, blocks)
    #Now I need to actually think ahead, see around corners
    #Pick some moves, more advanced!
    i = 0
    while (i < len(ideal)) :
        popped = False
        #Get a copy of the game tracker
        copyCB = copyList(CB)
        #Adjust the game tracker
        currSquare = copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)]
        copyCB[getRow(ideal[i][-2], False)][getCol(ideal[i][-1], False)] = currSquare
        copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)] = 0
        #Get the opponent jumps
        opponentJumps = findMoves(copyCB, opponent, opponentPieces, playerPieces, jumpInc, jumpIncs)
        for jump in opponentJumps :
            subJumps = jump.split(":")
            currRow = getRow(subJumps[0][0], False)
            currCol = getCol(subJumps[0][1], False)
            #Loop through each jump the opponent could make
            for subJump in range(1, len(subJumps)) :
                evalRow = getRow(subJumps[subJump][0], False)
                evalCol = getCol(subJumps[subJump][1], False)
                #I don't like this move, remove it.
                if (copyCB[currRow + (evalRow - currRow) // 2][currCol + (evalCol - currCol) // 2] == currSquare) and (i < len(ideal)) and (len(ideal) > 1) :
                    ideal.pop(i)
                    popped = True
                currRow = evalRow
                currCol = evalCol
        if not(popped) :
            i += 1
    #random for now, someday I will weight it based upon how the player could play against my move
    if (len(ideal) > 0) :
        index = random.randint(0, len(ideal) - 1)
        return ideal[index]
    else :
        return False
#Manual player
def manual(player) :
    move = input("Please enter a move => ")
    while not(validMove(move, player)) :
        move = input("Please enter a move => ")
    return move
#The dumb one
def automatedMoveDumb(player) :
    possibles = getPossibles(CB, player)
    if (len(possibles["jumps"]) > 0) :
        option = possibles["jumps"]
    elif (len(possibles["moves"]) > 0) :
        option = possibles["moves"]
    else :
        return False
    index = random.randint(0, len(option) - 1)
    return option[index]
#Where the magic happens!
def checkers(t, size, p1, p2) :
    currentPlayer = importGame()
    if (runs < 2) :
        drawCheckerBoard(t,-4*size,4*size,size)
    #draw the board based upon the game state
    initialState(t, size)
    if (runs < 2) :
        labelBoard(t, size)
        updateState()
    if (currentPlayer == "white") :
        player = 1
        if (debugger) :
            start = time.time()
        move = p1(player)
        if (debugger) :
            print("Move execution:", time.time() - start)
    else :
        player = 3
        if (debugger) :
            start = time.time()
        move = p2(player)
        if (debugger) :
            print("Move execution:", time.time() - start)
    moves = 0
    while not(gameOver()) and moves < maxMoves:            
        if (debugger == True) :
            print("About to move " + currentPlayer + " player - " + move)
            input("Press enter to continue... ")
        if not(validMove(move, player)) :
            print("Invalid move, game over.")
            return
        moveChecker(move)
        if (debugger == True) :
            showBoard(CB)
            print()
        #switch the player for the next run through
        if (player == 1) :
            player = 3
            currentPlayer = "black"
            if (debugger) :
                start = time.time()
            move = p2(player)
            if (debugger) :
                print("Move execution:", time.time() - start)
        else :
            player = 1
            currentPlayer = "white"
            if (debugger) :
                start = time.time()
            move = p1(player)
            if (debugger) :
                print("Move execution:", time.time() - start)
        moves += 1
    if (moves >= maxMoves) :
        msg("Max number of moves reached, neither player wins.", "success")
            
for i in range(runs) :
    print("Run #" + str(i + 1))
    checkers(t, size, automatedMove, automatedMoveDumb)
    CB = []
if (runs > 1) :
    print("Light player won " + str(wins["light"]) + " times.")
    print("Dark player won " + str(wins["dark"]) + " times.")
    print("Light player won " + str((wins["light"] / runs) * 100) + "% of the time.")
    print("Dark player won " + str((wins["dark"] / runs) * 100) + "% of the time.")
