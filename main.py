import cTurtle
import math
import random

def drawSquare(t,x,y,size,color):
    t.up()
    t.goto(x,y)
    t.down()
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    for i in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()

def drawBlackRedRow(t,x,y,size):
    for i in range(4):
        drawSquare(t,x,y,size,"black")
        x=x+size
        drawSquare(t,x,y,size,"#009900")
        x=x+size

def drawRedBlackRow(t,x,y,size):
    for i in range(4):
        drawSquare(t,x,y,size,"#009900")
        x=x+size
        drawSquare(t,x,y,size,"black")
        x=x+size

def drawCheckerBoard(t,x,y,size):
    for i in range(4):
        drawRedBlackRow(t,x,y,size)
        y=y-size
        drawBlackRedRow(t,x,y,size)
        y=y-size

##def fillCheckerBoard(t,size,CB):
##    t.tracer(False)  
##    drawCheckerBoard(t,-4*size,4*size,size)
##    labelBoard(t,size)
##    for row in range(8):
##        for col in range(8):
##            if CB[row][col]!=0:
##                if CB[row][col] in [1,2]:
##                    color="red"
##                    player="red"
##                else:
##                    color="gray"
##                    player="black"
##                king=False
##                if CB[row][col] in [2,4]:
##                    king=True
##                drawChecker(t,row,col,color,size,king)
##    t.tracer(True)



def checkers(size):
    t=cTurtle.Turtle()
    t.tracer(False)  
    drawCheckerBoard(t,-4*size,4*size,size)
    t.tracer(True)

checkers(60)
