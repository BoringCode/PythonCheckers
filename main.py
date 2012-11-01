#Graphical stuff
import cTurtle
t = cTurtle.Turtle()
t.ht()
t.up()

#Game setup
light = "white"
dark = "#C40003"
size = 60

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
    return False
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
        return False
    except :
        return False
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
def drawPiece(t, x, y, size, color) :
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
    t.tracer(False)
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
    t.tracer(False)
    y = 4*size
    x = -3*size
    t.goto(x, y)
    color = light
    state = 1
    team = 1
    for side in range(2) :
        for i in range(3) :
            CB.append([])
            for r in range(4) :
                drawPiece(t, x, y, size, color)
                x = x + (size * 2)
                if (i % 2 == 0 and team == 1) or (i % 2 != 0 and team == 3) :
                    CB[-1].append(0)
                    CB[-1].append(team)
                else :
                    CB[-1].append(team)
                    CB[-1].append(0)
            y = y - size
            if (i % 2 == 0) :
                x = -(3 + state)*size
            else :
                x = -(3 + side)*size
        color = dark
        y = -size
        x = -4*size
        state = 0
        team = 3
    #insert the two empty rows at the center of the board
    CB.insert(3, [0, 0, 0, 0, 0, 0, 0, 0])
    CB.insert(4, [0, 0, 0, 0, 0, 0, 0, 0])

def moveChecker(move) :
    t.tracer(False)
    fromY = getRow(move[0])
    fromX = getCol(move[1])
    if (fromY == False and fromX == False) :
        print("Invalid move")
        return
    currentPiece = CB[getRow(move[0], False)][getCol(move[1], False)]
    if (fromX % 2 == 0 and fromY % 2 != 0) :
        colorSqr = "#FFCE9E"
    else :
        colorSqr = "#D18B47"
    drawSquare(t, fromX, fromY, size, colorSqr)
    toY = getRow(move[3])
    toX = getCol(move[4])
    if (toY == False and toX == False) :
        print("Invalid move")
        return
    if (currentPiece == 1 or currentPiece == 2) :
        color = light
    else :
        color = dark
    drawPiece(t, toX, toY, size, color)
    #update internal game state
    CB[getRow(move[3], False)][getCol(move[4], False)] = currentPiece
    CB[getRow(move[0], False)][getCol(move[1], False)] = 0
    #show changes on board
    updateState()
def updateState() :
    t.tracer(True)

def msg(msg, typeM) :
    if (typeM == "error") :
        print("ERROR - ", msg)
    else :
        print("SUCCESS - ", msg)

#verification of moves
def isInvalidMove(move, player) :
    toY = getRow(move[3])
    toX = getCol(move[4])
    currentMove = CB[getRow(move[0], False)][getCol(move[1], False)]
    toMove = CB[getRow(move[3], False)][getCol(move[4], False)]
    #check for dark square
    if (toX % 2 != 0 and toY % 2 != 0) :
        msg("You need to move to a dark square my friend.", "error")
        error = True
    #check for valid checker move
    if (currentMove != player or currentMove != player + 1) :
        msg("Move your own checker loser!", "error")
        return True
    #check for empty square
    if (toMove != 0) :
        msg("You need to move to an empty square my friend.", "error")
        return True
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

#Where the magic happens    
def checkers(t, size) :
    drawCheckerBoard(t,-4*size,4*size,size)
    initialState(t, size)
    labelBoard(t, size)
    updateState()
    stop = False
    while (stop != True) :
        p1 = input("Light Player, please enter a move => ")
        while isInvalidMove(p1, 1) == True :
            p1 = input("Light Player, please enter a move => ")
        if (p1 != "exit") :
            moveChecker(p1)
            #get player 2's move
            p2 = input("Dark Player, please enter a move => ")
            while isInvalidMove(p2, 3) == True :
                p2 = input("Dark Player, please enter a move => ")
            if (p2 != "exit") :
                moveChecker(p2)
            else :
                print("Game Over")
                stop = True
        else :
            print("Game Over")
            stop = True

checkers(t, size)
