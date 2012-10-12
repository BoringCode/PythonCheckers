import cTurtle
turtle = cTurtle.Turtle()
import board
#some setup vars
size = 60

def drawPieces(color, size, t) :
    #set the center
    halfS = size * 4
    t.goto(-halfS, -halfS)
    t.left(90)
    t.forward(size)
    t.right(90)
    t.forward(size // 2)
    #set the color of the circle
    t.color("white")
    t.fillcolor(color)
    radius = size // 2
    #fill in the circle with the color
    t.begin_fill()
    circ = 2*3.14159*radius
    Len = circ / radius
    turnAngle = 360 / radius
    #start looping around the circle
    for i in range(radius):
        t.forward(Len)
        t.right(turnAngle)
    t.end_fill()
    t.forward(size * 2)
board.draw(size)
drawPieces("red", size, turtle)
