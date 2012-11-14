#Graphical stuff
import cTurtle
import random
t = cTurtle.Turtle()
t.ht()
t.up()

#Game setup
light = "white"
dark = "#C40003"
size = 60
debugger = False
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
    if (debugger == True) :
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
                                    startPiece = copyCB[row][col]
                                    copyCB[row][col] = 0
                                    copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                    copyCB[toRow][toCol] = startPiece
                                    jump = True
                                    king = False
                                    if (player == 1 and toRow == 7) or (player == 3 and toRow == 0) :
                                        king = True
                                    #While I can still jump, continue to search for a new jump (multi jumps)
                                    while (jump) :
                                        #If the move is a king, I can go in any direction
                                        if (king) :
                                            row = toRow
                                            col = toCol
                                            for rInc in INCs :
                                                for colInc in INCs :
                                                    toRow = row + rInc
                                                    toCol = col + colInc
                                                    jump = False
                                                    if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                                        if (toCol in VALID_RANGE and toRow in VALID_RANGE and copyCB[toRow][toCol] == EMPTY ) :
                                                            #The move.find() check is to make sure it doesn't attempt to go backwards and 
                                                            if (copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                                                jump = True
                                                                copyCB[row][col] = 0
                                                                copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                                copyCB[toRow][toCol] = startPiece
                                                                move += ":" + chr(toRow + 65) + str(toCol + 1)
                                        else :
                                            row = toRow
                                            col = toCol
                                            for colInc in INCs :
                                                toRow = row + rowInc
                                                toCol = col + colInc
                                                jump = False
                                                if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                                    if (toCol in VALID_RANGE and toRow in VALID_RANGE and copyCB[toRow][toCol] == EMPTY ) :
                                                        if (copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                                            jump = True
                                                            copyCB[row][col] = 0
                                                            copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                            copyCB[toRow][toCol] = startPiece
                                                            move += ":" + chr(toRow + 65) + str(toCol + 1)
                                                            if (player == 1 and toRow == 7) or (player == 3 and toRow == 0) :
                                                                king = True
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
                                        while (jump) :
                                            row = toRow
                                            col = toCol
                                            for rInc in INCs :
                                                for colInc in INCs :
                                                    toRow = row + rInc
                                                    toCol = col + colInc
                                                    jump = False
                                                    if (abs(toRow - row) == 2) and (abs(toCol - col) == 2) :
                                                        if (toCol in VALID_RANGE and toRow in VALID_RANGE and copyCB[toRow][toCol] == EMPTY ) :
                                                            if (copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] in opponentPieces) :
                                                                jump = True
                                                                copyCB[row][col] = 0
                                                                copyCB[toRow + (row - toRow) // 2][toCol + (col - toCol) // 2] = 0
                                                                copyCB[toRow][toCol] = startPiece
                                                                move += ":" + chr(toRow + 65) + str(toCol + 1)
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
        return True
    elif (darkCount == 0) :
        msg("Light player has won!", "success")
        return True
    lightPlayer = getPossibles(1)
    if (len(lightPlayer["jumps"]) == 0) and (len(lightPlayer["moves"]) == 0) :
        darkPlayer = getPossibles(3)
        if (len(darkPlayer["jumps"]) == 0) and (len(darkPlayer["moves"]) == 0) :
            msg("Neither player can make a move, draw.", "success")
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
def importGame() :
    filename = input("Enter a filename => ")
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
#The smart one
def automatedMove(player) :
    possibles = getPossibles(player)
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
        #If it is a multiple jump, I prefer it
        if len(move) > 5 :
            ideal = [move]
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
        if (debugger) :
            print("If I make this move: " + ideal[i] + " I would be open to these jumps - ", opponentJumps)
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
                    if (debugger) :
                        print("I almost did this move:", ideal[i])
                    ideal.pop(i)
                    popped = True
                currRow = evalRow
                currCol = evalCol
        if not(popped) :
            i += 1
    #random for now, someday I will weight it based upon how the player could play against my move
    if (debugger) :
        print(ideal)
    if (len(ideal) > 0) :
        index = random.randint(0, len(ideal) - 1)
        return ideal[index]
    else :
        return False
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
#Where the magic happens!
def checkers(t, size) :
    currentPlayer = importGame()
    drawCheckerBoard(t,-4*size,4*size,size)
    #draw the board based upon the game state
    initialState(t, size)
    labelBoard(t, size)
    updateState()
    if (currentPlayer == "white") :
        player = 1
        move = automatedMove(player)
    else :
        player = 3
        move = automatedMoveDumb(player)
    while not(gameOver()) :            
        if (debugger == True) :
            print("About to move " + currentPlayer + " player - " + move)
            input("Press enter to continue... ")
        if not(validMove(move, player)) :
            print("Invalid move, game over.")
            return
        moveChecker(move)
        if (debugger == True) :
            showBoard(CB)
        #switch the player for the next run through
        if (player == 1) :
            player = 3
            currentPlayer = "black"
            move = automatedMoveDumb(player)
        else :
            player = 1
            currentPlayer = "white"
            move = automatedMove(player)
checkers(t, size)
