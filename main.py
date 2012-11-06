#Graphical stuff
import cTurtle
t = cTurtle.Turtle()
t.ht()
t.up()

#Game setup
light = "white"
dark = "#C40003"
size = 60
gameRunning = False

#The game tracker
CB = []

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
    fromRow = getRow(move[0], False)
    fromCol = getCol(move[1], False)
    toRow = getRow(move[3], False)
    toCol = getCol(move[4], False)
    fromY = getRow(move[0])
    fromX = getCol(move[1])
    currentPiece = CB[getRow(move[0], False)][getCol(move[1], False)]
    drawSquare(t, fromX, fromY, size, "#D18B47")
    toY = getRow(move[3])
    toX = getCol(move[4])
    if (currentPiece == 1 or currentPiece == 2) :
        color = light
        #king me
        if (currentPiece == 1 and getRow(move[3], False) == 7) or (currentPiece == 2) :
            currentPiece = 2
            king = True
    else :
        color = dark
        #king me
        if (currentPiece == 3 and getRow(move[3], False) == 0) or (currentPiece == 4) :
            currentPiece = 4
            king = True
    #detect the jump!
    if (fromRow + 2 == toRow or fromRow - 2 == toRow) :
        print("Jump detected")
    drawPiece(t, toX, toY, size, color, king)
    #update internal game state
    CB[toRow][toCol] = currentPiece
    CB[fromRow][fromCol] = 0
    #show changes on board
    updateState()
#I'm too lazy to type t.tracer(True)
def updateState() :
    t.tracer(True)
#I got tired of making my info messages pretty(ish)
def msg(msg, typeM) :
    if (typeM == "error") :
        print("ERROR - " + msg)
    else :
        print("SUCCESS - " + msg)
#verification of moves
def isInvalidMove(move, player) :
    #allow for exit commands
    if (move == "exit") :
        return False    
    #get the moves
    moves = move.split(":")
    #evaluate each move
    currRow = getRow(moves[0][0], False)
    currCol = getCol(moves[0][1], False)
    if (currRow == "failed" or currCol == "failed") :
        msg("Invalid move, please try again.", "error")
        return True
    startPiece = CB[currRow][currCol]
    if (startPiece != player and startPiece != player + 1) :
        msg("You have to move your own piece loser!", "error")
        return True
    #evaluate the rest of the moves
    for move in range(1, len(moves)) :
        #get the current move and evalulate it
        evalRow = getRow(moves[move][0], False)
        evalCol = getCol(moves[move][1], False)
        #make sure it is the proper format
        if (evalRow == "failed" or evalCol == "failed") :
            msg("Invalid move, please try again.", "error")
            return True
        currSquare = CB[evalRow][evalCol]
        #check to make sure you are move to an empty square
        if (currSquare != 0) :
            msg("You need to move to an empty square.", "error")
            return True
        #check to see if current move is a double jump
        if (abs(evalRow - currRow) == 2) and (abs(evalCol - currCol) == 2) :
            #check to make sure piece is moving in the right direction
            if ((player == 1 and evalRow - currRow != 2) or (player == 3 and evalRow - currRow != -2)) and (startPiece != player + 1) :
                msg("You have to move forward with that piece.", "error")
                return True
            checkJump = CB[currRow + (evalRow - currRow) // 2][currCol + (evalCol - currCol) // 2]
            #check to make sure the player is jumping over a valid piece
            if (checkJump == 0 or checkJump == player or checkJump == player + 1) :
                msg("You have to jump over your opponent's piece.", "error")
                return True
        #if the move isn't a double jump, make sure it is a valid move
        elif ((player == 1 and evalRow - currRow != 1) or (player == 3 and evalRow - currRow != -1)) and (abs(evalCol - currCol) != 1) and (startPiece != player + 1) :
            msg("You can only move forward diagonally with that piece.", "error")
            return True
        elif (abs(evalRow - currRow) != 1) and (abs(evalCol - currCol) != 1) :
            msg("You can only move one row, diagonally with that piece.", "error")
            return True
        currRow = evalRow
        currCol = evalCol
        


    
    #must be multi jump
    #if (len(moves) > 2) :
        
    return True


    
##    #must be a jump of course!
##    if (fromRow + 2 == toRow or fromRow - 2 == toRow) :
##        print("Jump detected")
##
##    #since jumps basically override a lot of basic rules, I put an else statement in for checking anything else.
##    else :
##        if (player == 1 and currentMove != player + 1 and fromRow + 1 != toRow) or (player == 3 and currentMove != player + 1 and fromRow - 1 != toRow) :
##            msg("You can only move forward one row with that piece.", "error")
##            return True
##        elif (currentMove == player + 1 and fromRow + 1 != toRow and fromRow - 1 != toRow) :
##            msg("You can only move one row at a time silly!", "error")
##            return True
##        #check for diagonal move
##        if (fromCol + 1 != toCol) and (fromCol - 1 != toCol) :
##            msg("You have to move diagonally.", "error")
##            return True
##    #check for empty square
##    if (toMove != 0) :
##        msg("You need to move to an empty square my friend.", "error")
##        return True
    return False
def showBoard() :
    print("  1 2 3 4 5 6 7 8")
    row = 65
    for i in range(8) :
        print(chr(row), end=" ")
        for item in range(len(CB[i])) :
            print(CB[i][item], end=" ")
        print()
        row += 1
#Where the magic happens!
def checkers(t, size) :
    filename = input("Enter a filename => ")
    while filename.find(".txt") == -1 and filename != "" and filename == ".txt" :
        print("Invalid filename")
        filename = input("Enter a filename => ")
    if (filename != "") :
        gamefile = open(filename, "r")
        currentPlayer = gamefile.readline()
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
    drawCheckerBoard(t,-4*size,4*size,size)
    #draw the board based upon the game state
    initialState(t, size)
    labelBoard(t, size)
    updateState()
    gameRunning = True
    while (gameRunning == True) :
        p1 = input("Light Player, please enter a move => ")
        while isInvalidMove(p1, 1) == True :
            p1 = input("Light Player, please enter a move => ")
        if (p1 == "exit") :
            gameRunning = False
        else :
            moveChecker(p1)
            msg("Light player has made their move (" + p1 + ")\n----------------------------------", "success")
            #get player 2's move
            p2 = input("Dark Player, please enter a move => ")
            while isInvalidMove(p2, 3) == True :
                p2 = input("Dark Player, please enter a move => ")
            if (p2 == "exit") :
                gameRunning = False
            else :
                moveChecker(p2)
                msg("Dark player has made their move (" + p2 + ")\n----------------------------------", "success")
    msg("Game stopped!", "success")

checkers(t, size)
