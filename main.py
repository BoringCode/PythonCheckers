import cTurtle
t = cTurtle.Turtle()
t.ht()
t.up()
t.tracer(False)

size = 60

def getCoordY(c, size) :
    c = str(c)
    topY = 4*size
    if (ord(c) >= 65 and ord(c) <= 72) :
        return topY - ((abs(65 - ord(c))) * size)
    return False
def getCoordX(c, size) :
    c = int(c)
    topX = -4*size
    if (c >= 1 and c <= 8) :
        return topX + ((c - 1) * size)
    return False      
def drawSquare(t,x,y,size,color):
    t.up()
    t.goto(x,y)
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    for i in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()
def drawPiece(t, x, y, size, color) :
    radius = size / 2.5
    t.up()
    t.goto(x + (0.5*size), y - (0.12 * size))
    t.setheading(0)
    t.down()
    t.width(2)
    t.color("#200000")
    t.fillcolor(color)
    t.begin_fill()
    pos = t.position()
    circumference= 2 * 3.14159 * radius
    Len=circumference / 360
    turnAngle= 1
    for i in range(360):
        t.forward(Len)
        t.right(turnAngle)
    t.end_fill()
    t.width(1)
def drawDarkLightRow(t,x,y,size):
    for i in range(4):
        drawSquare(t,x,y,size,"#D18B47")
        x=x+size
        drawSquare(t,x,y,size,"#FFCE9E")
        x=x+size
def drawLightDarkRow(t,x,y,size):
    for i in range(4):
        drawSquare(t,x,y,size,"#FFCE9E")
        x=x+size
        drawSquare(t,x,y,size,"#D18B47")
        x=x+size
        
def labelBoard(t,size):
    t.up()
    t.goto(-(3.6*size),(4.1*size))
    t.down()
    t.pencolor('#000000')
    for i in range(1, 9):
        t.write(str(i),font=("Arial",12,"bold"))
        t.up()
        t.forward(size)
        t.down()
    t.up()
    t.goto(-(4.5*size),(3.4*size))
    t.down()
    for i in range(8):
        t.write(chr(65+i),font=("Arial",12,"bold"))
        t.up()
        t.goto(-(4.5*size),((4*size)+(i*-size)-(1.7*size)))
        t.down()
def drawCheckerBoard(t,x,y,size):
    for i in range(4):
        drawLightDarkRow(t,x,y,size)
        y = y-size
        drawDarkLightRow(t,x,y,size)
        y = y-size
    #draw the pieces on init
    y = 4*size
    x = -3*size
    t.goto(x, y)
    color = "white"
    state = 1
    for side in range(2) :
        for i in range(3) :
            for r in range(4) :
                drawPiece(t, x, y, size, color)
                x = x + (size * 2)
            y = y - size
            if (i % 2 == 0) :
                x = -(3 + state)*size
            else :
                x = -(3 + side)*size
        color = "#C40003"
        y = -size
        x = -4*size
        state = 0
    labelBoard(t, size)

def moveChecker(t, move, size) :
    fromY = getCoordY(move[0], size)
    fromX = getCoordX(move[1], size)
    if (fromX % 2 == 0 and fromY % 2 != 0) :
        color = "#FFCE9E"
    else :
        color = "#D18B47"
    drawSquare(t, fromX, fromY, size, color)
    toY = getCoordY(move[3], size)
    toX = getCoordX(move[4], size)
    #actual color will be calculated eventually
    drawPiece(t, toX, toY, size, "#C40003")
    
def checkers(t, size):
    drawCheckerBoard(t,-4*size,4*size,size)

checkers(t, size)

#The actual machine problem
#Row = letter (A - H)
#Col = number (1 - 8)
moveChecker(t, "A2:E2", size)
moveChecker(t, "H1:D3", size)
moveChecker(t, "G8:D7", size)

t.tracer(True)
