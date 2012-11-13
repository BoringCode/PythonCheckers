import cTurtle
import math
import random

EMPTY=0
INCs = [-1,1]
VALID_RANGE= range(8)
VERBOSE=False

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
        
def labelBoard(t,size):
    t.up()
    t.goto(-(4*size)+8,(4.05*size))
    t.down()
    t.pencolor('#000000')
    for i in range(8):
        t.write("COL " + str(i),font=("Arial",12,"bold"))
        t.up()
        t.forward(size)
        t.down()
    t.up()
    t.goto(-(5.2*size),(3.4*size))
    t.down()
    for i in range(8):
        t.write("ROW " + chr(65+i),font=("Arial",12,"bold"))
        t.up()
        t.goto(-(5.2*size),((4*size)+(i*-size)-(1.7*size)))
        t.down()
        
def rowToLocation(row,size):
    return (4*size)-(size*row)

def colToLocation(col,size):
    return -(4*size)+(size*col)

def drawCircleCentered(t,radius):
    pos=t.position()
    t.up()
    t.forward(radius)
    t.down()
    t.lt(90)
    t.circle(radius)
    t.up()
    t.setpos(pos)
    t.down()

def drawChecker(t,row,column,color,size,isKing):
    t.tracer(False)
    t.color("black",color)
    t.up()
    y=rowToLocation(row, size)-(size//2)
    x=colToLocation(column,size)+(size//2)
    t.goto(x,y)
    t.down()
    t.begin_fill()
    ps=t.pensize()
    t.pensize(2)
    drawCircleCentered(t,size//2)
    t.end_fill()
    drawCircleCentered(t,size//3)
    drawCircleCentered(t,size//6)
    t.pensize(ps)
    if isKing:
        drawCrown(t,x,y,size)
    t.tracer(True)

def drawCrown(t,x,y,size):
    t.color("yellow","yellow")
    t.up()
    t.goto(x-(.16*size),y-(.24*size))
    t.down()
    t.begin_fill()
    t.setheading(108)
    t.forward(size//3)
    for i in range(5):
        t.right(72)
        t.forward(size//3)
    t.end_fill()    
        
def fillCheckerBoard(t,size,CB):
    t.tracer(False)  
    for row in VALID_RANGE:
        for col in VALID_RANGE:
            if CB[row][col]!=EMPTY:
                if CB[row][col] in [1,2]:
                    color="red"
                    player="red"
                else:
                    color="gray"
                    player="gray"
                king=False
                if CB[row][col] in [2,4]:
                    king=True
                drawChecker(t,row,col,color,size,king)
    t.tracer(True)

def moveChecker(t,size,move,color,CB):
    #parse the move
    fromRow=ord(move[0])-65
    fromCol=int(move[1])
    toRow=ord(move[3])-65
    toCol=int(move[4])
    isJump=False
    if fromRow-toRow in [2,-2] and fromCol-toCol in [2,-2]:
        isJump=True
    #get graphic x,y from row,col
    y=rowToLocation(fromRow, size)
    x=colToLocation(fromCol, size)
    #blank out the from square
    t.tracer(False)
    drawSquare(t,x,y,size,"black")
    t.tracer(True)
    #move the checker in the actual board
    if color=="red":
        if toRow != 7:
            CB[toRow][toCol]=CB[fromRow][fromCol]
            CB[fromRow][fromCol]=EMPTY
        else:
            CB[toRow][toCol]=2
            CB[fromRow][fromCol]=EMPTY
    else: #color is gray
        if toRow != 0:
            CB[toRow][toCol]=CB[fromRow][fromCol]
            CB[fromRow][fromCol]=EMPTY
        else:
            CB[toRow][toCol]=4
            CB[fromRow][fromCol]=EMPTY
    #draw the checker
    if CB[toRow][toCol] in [2,4]:
        isKing=True
    else:
        isKing=False
    drawChecker(t,toRow,toCol,color,size,isKing)
    if isJump: #Remove jumped checker
        CB[(fromRow+toRow)//2][(fromCol+toCol)//2]=EMPTY
        y=rowToLocation((fromRow+toRow)//2, size)
        x=colToLocation((fromCol+toCol)//2, size)
        #blank out the from square
        drawSquare(t,x,y,size,"black")        
           
def showBoard(CB):
    print("  0 1 2 3 4 5 6 7 ")
    for row in range(8):
        line=chr(row+65)+" "
        for col in range(8):
            line+=str(CB[row][col])+" "
        print(line)

def getPossibles(CB,player):
    possibles={}
    if player=="gray":
        playerTokens=[3,4]
        opponentTokens=[1,2]
        rowInc=-1
    else:
        playerTokens=[1,2]
        opponentTokens=[3,4]
        rowInc=1
    possibles["moves"]=findMoves(CB,player,playerTokens,opponentTokens,rowInc)  #puts moves into possibles Dictionary
    possibles["jumps"]=[]
    possibles["crownings"]=[]
    possibles["blocks"]=[]
    return possibles

def validMove(CB,move,player):
    possibles=getPossibles(CB,player)
    if len(possibles["jumps"])>0:
        if move not in possibles["jumps"]:
            print("A jump must be taken!!!")
            return False
        else:
            return True
    if move not in possibles["moves"]: #includes crowning and blocking moves
        print ("Invalid move!!!!")
        return False
    else:
        return True 

def findMoves(CB,player,playerTokens,opponentTokens,rowInc):
    moves=[]
    #process all board positions
    for row in VALID_RANGE:
        for col in VALID_RANGE:
            if CB[row][col] in playerTokens:
                if CB[row][col] not in [2,4]: #not a king
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                            moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return moves


def readCheckerFile(CB):
    fileName="gameboard.txt" #input("Enter a file name to start the game (prefix and .txt) => ")
    if fileName!="":
        inFile=open(fileName,"r")
        player=inFile.readline()
        for row in inFile:
            newRow=[]
            for item in row:
                if item !="\n":
                    newRow.append(int(item))
            CB.append(newRow)
        inFile.close()
        return player[:-1]
    else:
        newGame=[[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0], [0,1,0,1,0,1,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [3,0,3,0,3,0,3,0], [0,3,0,3,0,3,0,3], [3,0,3,0,3,0,3,0]]
        for row in newGame:
            CB.append(row)
        p=random.randint(0,1)
        if p==0:
            return "gray"
        else:
            return "red"
        
def gameIsOver(CB):
    redCount=0
    grayCount=0
    for row in CB:
        for token in row:
            if token in [1,2]:
                redCount+=1
            elif token in [3,4]:
                grayCount+=1
    if redCount==0:
        return True
    if grayCount==0:
        return True
    return False

def automatedMove(CB,player):
    possibles=getPossibles(CB,player)
    index=random.randint(0,len(possibles['moves'])-1)
    return possibles['moves'][index]
    
def switchPlayers(player):
    #switch players
    if player=="gray":
        player="red"
    else:
        player="gray"
    return player
   
def checkers(size):
    CB=[]
    player=readCheckerFile(CB)    
    sue=cTurtle.Turtle()
    sue.tracer(False)  
    drawCheckerBoard(sue,-4*size,4*size,size)
    labelBoard(sue,size)
    fillCheckerBoard(sue,size,CB)
    sue.tracer(True)
    while not(gameIsOver(CB)):
        move=automatedMove(CB,player)
        if VERBOSE:
            print("About to move "+player+" "+move)
            junk=input("Press enter to continue . . .")
        if not(validMove(CB,move,player)):
            print("Invalid Move - Game Over!")
            return
        else:
            moveChecker(sue,size,move,player,CB)
            if VERBOSE:
                showBoard(CB)
        player=switchPlayers(player)
       

checkers(60)
