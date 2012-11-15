#Graphical stuff
import cTurtle
import random
import time
t = cTurtle.Turtle()
t.ht()
t.up()

numRuns = 1
wins = {"lightWins": 0, "darkWins": 0}

#Game setup
light = "white"
dark = "#C40003"
size = 60
debugger = True
EMPTY = 0
VALID_RANGE = range(8)

#The game tracker
CB = []

#PLAYER CODE
def getPossibles(player):
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
    possibles["crownings"] = findCrownings(player, possibles["moves"] + possibles["jumps"])
    #Calculate if any of my jumps or moves can block the opponent from jumping
    possibles["blocks"] = findBlocks(opponent, possibles["moves"] + possibles["jumps"])
    if (debugger) :
        print(possibles)
    return possibles
def findBlocks(opponent, playerMoves) :
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
                    blocks.append(playerMove)
    return blocks                 
def findCrownings(player, moves) :
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
                    crownings.append(move)
    return crownings
#Keep repetitive code to minimum
def multiJump(copyCB, player, row, col, toRow, toCol, opponentPieces) :
    if (toCol in VALID_RANGE and toRow in VALID_RANGE and CB[toRow][toCol] == EMPTY ) :
        #Detect a jump
        if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
            #Is a valid jump?
            if (CB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                jump = True
                king = False
                if (player == 1 and toRow == 7) or (player == 3 and toRow == 0) :
                    king = True
                nextRow = toRow
                nextCol = toCol
                move = ":" + chr(toRow + 65) + str(toCol + 1)
                return [jump, king, move]
    return [False]
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
                            result = multiJump(CB, player, row, col, toRow, toCol, opponentPieces)
                            jump = result[0]
                            if (jump) :
                                #The jump is good!
                                copyCB = copyList(CB)
                                startPiece = copyCB[row][col]
                                copyCB[row][col] = 0
                                copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                copyCB[toRow][toCol] = startPiece
                                king = result[1]
                                nextRow = toRow
                                nextCol = toCol
                                #While I can still jump, continue to search for a new jump (multi jumps)
                                while (jump) :
                                    #Multi jumps
                                    row = nextRow
                                    col = nextCol
                                    if (king) :
                                        for rInc in INCs :
                                            for colInc in INCs :
                                                toRow = row + rInc
                                                toCol = col + colInc
                                                result = multiJump(copyCB, player, row, col, toRow, toCol, opponentPieces)
                                                jump = result[0]
                                                if (jump) :
                                                    nextRow = toRow
                                                    nextCol = toCol
                                                    copyCB[row][col] = 0
                                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                    copyCB[toRow][toCol] = startPiece
                                                    move += result[2]
                                    else :
                                        for colInc in INCs :
                                            toRow = row + rowInc
                                            toCol = col + colInc
                                            result = multiJump(copyCB, player, row, col, toRow, toCol, opponentPieces)
                                            jump = result[0]
                                            if (jump) :
                                                king = result[1]
                                                nextRow = toRow
                                                nextCol = toCol                                                
                                                copyCB[row][col] = 0
                                                copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                copyCB[toRow][toCol] = startPiece
                                                move += result[2]                                   
                                moves.append(move)
                            #Not a jump? Okay, it must be a valid move. Continue.
                            elif (rowInc not in [2, -2]) :
                                moves.append(move)
                else: #is a king
                    for rInc in INCs :
                        for colInc in INCs :
                            toRow = row + rInc
                            toCol = col + colInc
                            move = str(chr(row + 65) + str(col + 1) + ":" + chr(toRow + 65) + str(toCol + 1))
                            if (toCol in VALID_RANGE and toRow in VALID_RANGE and CB[toRow][toCol] == EMPTY ) :
                                #jump
                                result = multiJump(CB, player, row, col, toRow, toCol, opponentPieces)
                                jump = result[0]
                                if (jump) :
                                    #The jump is good!
                                    copyCB = copyList(CB)
                                    startPiece = copyCB[row][col]
                                    copyCB[row][col] = 0
                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                    copyCB[toRow][toCol] = startPiece
                                    king = result[1]
                                    nextRow = toRow
                                    nextCol = toCol
                                    while (jump) :
                                        for rInc in INCs :
                                            for colInc in INCs :
                                                toRow = row + rInc
                                                toCol = col + colInc
                                                result = multiJump(copyCB, player, row, col, toRow, toCol, opponentPieces)
                                                jump = result[0]
                                                if (jump) :
                                                    nextRow = toRow
                                                    nextCol = toCol
                                                    copyCB[row][col] = 0
                                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                    copyCB[toRow][toCol] = startPiece
                                                    move += result[2]
                                    moves.append(move)
                                elif (rowInc not in [2, -2]) :
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
        if (numRuns < 2) :
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
            if (numRuns < 2) :
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
        if (numRuns < 2) :
            drawPiece(t, evalX, evalY, size, color, king)
        CB[evalRow][evalCol] = currPiece
        #I want to evaluate the current position next time
        currRow = evalRow
        currCol = evalCol
        currY = evalY
        currX = evalX
        currPiece = CB[evalRow][evalCol]
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
        wins["darkWins"] += 1
        return True
    elif (darkCount == 0) :
        msg("Light player has won!", "success")
        wins["lightWins"] += 1
        return True
    lightPlayer = getPossibles(1)
    darkPlayer = getPossibles(3)
    if (len(lightPlayer["jumps"]) == 0) and (len(lightPlayer["moves"]) == 0) and (len(darkPlayer["jumps"]) == 0) and (len(darkPlayer["moves"]) == 0) :
            msg("Neither player can make a move, draw.", "success")
            return True
    elif (len(lightPlayer["jumps"]) == 0) and (len(lightPlayer["moves"]) == 0) :
        msg("Light player can't make any moves, dark player wins!", "success")
        wins["darkWins"] += 1
        return True
    elif (len(darkPlayer["jumps"]) == 0) and (len(darkPlayer["moves"]) == 0) :
        msg("Dark player can't make any moves, light player wins!", "success")
        wins["lightWins"] += 1
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
    if (move == False) :
        msg("Cannot make a move, other player wins.", "success")
        return False
    possibles = getPossibles(player)
    if len(possibles["jumps"]) > 0 :
        if move not in possibles["jumps"] :
            msg("A jump must be taken!", "error")
            return False
    elif move not in possibles["moves"]: #includes crowning and blocking moves
        print(move)
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
def importGame(filename) :
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
<<<<<<< HEAD
=======
def countPieces(CB, player) :
    if (player == 1) :
        pieces = [1, 2]
    else :
        pieces = [3, 4]
    count = 0
    for row in CB :
        for col in row :
            if (col in pieces) :
                count += 1
    return count
#----------------------------------------------------------------------------
>>>>>>> Tried to create auto test environment.
#The smart one
def automatedMove(player) :
    possibles = getPossibles(player)
    jumpIncs = [-2, 2]
    incs = [-1, 1]
    if player == 3 :
        opponent = 1
        opponentPieces = [1,2]
        playerPieces= [3,4]
        jumpInc = 2
        rowInc = 1
        playerJumpInc = -2
        playerRowInc = -1
        crowningRow = "A"
    else :
        opponent = 3
        opponentPieces = [3,4]
        playerPieces = [1,2]
        rowInc = -1
        jumpInc = -2
        playerJumpInc = 2
        playerRowInc = 1
        crowningRow = "H"
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
        #If it is a multiple jump, I prefer it
        if len(move) > 5 :
            nope = False
            #if there is another, better multiple jump. I want it.
            for jump in move :
                if (len(jump) > len(move)) :
                    nope = True
            if not(nope) :
                ideal = [move]
    #If I still haven't decided on a perfect move, just give me all the options
    if (len(ideal) == 0) :
        ideal = options    
    #Okay, I've decided on my best bet so far (jumps, crownings, blocks)
    #Now I need to actually think ahead, see around corners
    #Pick some moves, more advanced!
    i = 0
    while (i < len(ideal)) :
        #Check to make sure I can still remove moves from the ideal moves list
        if (i < len(ideal)) and (len(ideal) > 1) :
            remove = False
            #Get a copy of the game tracker
            copyCB = copyList(CB)
            #Adjust the game tracker
            currSquare = copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)]
            copyCB[getRow(ideal[i][-2], False)][getCol(ideal[i][-1], False)] = currSquare
            copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)] = 0
            #Get the opponent moves
            opponentMoves = findMoves(copyCB, opponent, opponentPieces, playerPieces, rowInc, incs)
            opponentJumps = findMoves(copyCB, opponent, opponentPieces, playerPieces, jumpInc, jumpIncs)
            print(opponentJumps)
            crownings = findCrownings(opponent, opponentMoves + opponentJumps)
            #check the jumps
            if (len(opponentJumps) > 0) :
                for jump in opponentJumps :
                    subJumps = jump.split(":")
                    currRow = getRow(subJumps[0][0], False)
                    currCol = getCol(subJumps[0][1], False)
                    #Loop through each jump the opponent could make
                    for subJump in range(1, len(subJumps)) :
                        evalRow = getRow(subJumps[subJump][0], False)
                        evalCol = getCol(subJumps[subJump][1], False)
                        #Check to see if making this move could result in a jump, or if moving would open up a block.
                        if (copyCB[currRow + (evalRow - currRow) // 2][currCol + (evalCol - currCol) // 2] == currSquare) or (copyCB[evalRow][evalCol] == currSquare) :
                                remove = True
            #check if moving would allow a crowning
            if (len(crownings) > 0) :
                for crowning in crownings :
                    subMoves = crowning.split(":")
                    #Is it a king?
                    if (copyCB[getRow(subMoves[0][0], False)][getCol(subMoves[0][1], False)] != opponent + 1) :
                        for subMove in range(1, len(subMoves)) :
                            #block the crowning, don't move from this spot
                            if (subMoves[subMove][0] == crowningRow) and (ideal[i][0] == crowningRow) :
                                remove = True
            #check to see if move will box me into a corner, no draws please.
            if (countPieces(CB, player) == 1) :
                copyCB = copyList(CB)
                #Adjust the game tracker
                currSquare = copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)]
                copyCB[getRow(ideal[i][-2], False)][getCol(ideal[i][-1], False)] = currSquare
                copyCB[getRow(ideal[i][0], False)][getCol(ideal[i][1], False)] = 0
                if (len(findMoves(copyCB, player, playerPieces, opponentPieces, playerRowInc, incs) + findMoves(copyCB, player, playerPieces, opponentPieces, playerJumpInc, jumpIncs)) == 0) :
                    remove = True
            if not(remove) :
                i += 1
            else :
                if (debugger) :
                    print("I almost did this move:", ideal[i], " - strikes: ", strikes)
                    print("There were these jumps:", opponentJumps)
                    print("There were these crownings:", crownings)
                ideal.pop(i)
        else :
            i += 1
    if (debugger) :
        print("Ideal moves - ", ideal)
    if (len(ideal) > 0) :
        index = random.randint(0, len(ideal) - 1)
        return ideal[index]
    else :
        return False
<<<<<<< HEAD
=======

#---------------------------------------------
>>>>>>> Tried to create auto test environment.
#The dumb one
def automatedMoveDumb(player) :
    possibles = getPossibles(player)
    if (len(possibles["jumps"]) > 0) :
        option = possibles["jumps"]
    elif (len(possibles["moves"]) > 0) :
        option = possibles["moves"]
    else :
        return False
    index = random.randint(0, len(option) - 1)
    return option[index]
<<<<<<< HEAD
=======


>>>>>>> Tried to create auto test environment.
#Where the magic happens!
def checkers(t, size) :
    if (numRuns < 2) :
        filename = input("Enter a filename => ")
    else :
        filename = ""
    currentPlayer = importGame(filename)
    if (numRuns < 2) :
        drawCheckerBoard(t,-4*size,4*size,size)
    #draw the board based upon the game state
    initialState(t, size)
    if (numRuns < 2) :
        labelBoard(t, size)
    updateState()
    if (currentPlayer == "white") :
        player = 1
<<<<<<< HEAD
        move = automatedMove(player)
    else :
        player = 3
        move = automatedMoveDumb(player)
    while not(gameOver()) :            
        if (debugger == True) :
=======
        if (debugger) :
            start = time.time()
        move = automatedMove(player)
        if (debugger) :
            print("Move execution:", time.time() - start)
    else :
        player = 3
        if (debugger) :
            start = time.time()
        move = automatedMove(player)
        if (debugger) :
            print("Move execution:", time.time() - start)
    while not(gameOver()) :
        if (debugger) :
            print()
>>>>>>> Tried to create auto test environment.
            print("About to move " + currentPlayer + " player - " + move)
            input("Press enter to continue... ")
        if not(validMove(move, player)) :
            print("Invalid move, game over.")
            return
        moveChecker(move)
        if (debugger) :
            showBoard(CB)
            print()
        #switch the player for the next run through
        if (player == 1) :
            player = 3
            currentPlayer = "black"
<<<<<<< HEAD
            move = automatedMoveDumb(player)
        else :
            player = 1
            currentPlayer = "white"
            move = automatedMove(player)
checkers(t, size)
=======
            if (debugger) :
                start = time.time()
            move = automatedMove(player)
            if (debugger) :
                print("Move execution:", time.time() - start)
        else :
            player = 1
            currentPlayer = "white"
            if (debugger) :
                start = time.time()
            move = automatedMove(player)
            if (debugger) :
                print("Move execution:", time.time() - start)
#Test case
for i in range(numRuns) :
    CB = []
    checkers(t, size)
    showBoard(CB)
print("Light won " + str(wins["lightWins"]) + " times.")
print("Dark won " + str(wins["darkWins"]) + " times.")
print("Light won " + str((wins["lightWins"] / numRuns) * 100) + "% of the time.")
print("Dark won " + str((wins["darkWins"] / numRuns) * 100) + "% of the time.")
>>>>>>> Tried to create auto test environment.
