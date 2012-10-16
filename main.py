import cTurtle
t = cTurtle.Turtle()
t.ht()
t.up()
t.tracer(False)

size = 60

def getCoordY(c, size) :
    topY = 4*size
    if (ord(c) >= 65 and ord(c) <= 72) :
        return topY - ((abs(65 - ord(c))) * size)
    else :
        return False
def getCoordX(c, size) :
    topX = -4*size
    if (c >= 1 and c <= 8) :
        return topX + ((c - 1) * size)
    else :
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

def moveChecker(t, size, fromRow,fromCol,toRow,toCol) :
    fromX = getCoordX(fromCol, size)
    fromY = getCoordY(fromRow, size)
    if (fromX % 2 == 0 and fromY % 2 != 0) :
        color = "#FFCE9E"
    else :
        color = "#D18B47"
    drawSquare(t, fromX, fromY, size, color)
    toX = getCoordX(toCol, size)
    toY = getCoordY(toRow, size)
    #actual color will be calculated eventually
    drawPiece(t, toX, toY, size, "red")
    
def checkers(t, size):
    drawCheckerBoard(t,-4*size,4*size,size)

checkers(t, size)
#moveChecker(t, size, "A", 1, "D", 2)

t.tracer(True)
