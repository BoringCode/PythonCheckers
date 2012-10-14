def draw(size) :
    import cTurtle
    board = cTurtle.Turtle()
    #instant draw
    board.tracer(0, 0)
    board.ht()
    board.up()
    #set the center
    halfS = size * 4
    board.goto(-halfS, -halfS)
    #the function will draw the row below this point, I need to move the turtle so I can get the board to line up with the exact 0, 0
    board.left(90)
    board.forward(size)
    board.right(90)
    #set some control variables
    color = "black"
    state = 0
    #loop through rows
    for i in range(8) :
        #loop through squares in each row
        for i in range(8) :
            if (color == "red") :
                color = "black"
            else :
                color = "red"
            #draw the square
            board.fillcolor(color)
            board.begin_fill()
            for l in range(4) :
                board.forward(size)
                board.right(90)
            board.end_fill()
            board.forward(size)
        #the turtle needs to turn a different direction for each row
        if (state == 0) :
            board.left(180)
            state = 1
        else :
            board.right(90)
            board.forward(size * 2)
            board.right(90)
            state = 0
    #draw the pieces
    board.goto(-halfS, -halfS)
    board.left(90)
    board.forward(size)
    board.right(90)
    board.forward(size / 2)
    color = "red"
    for i in range(2) :
        for i in range(12) :
            #set the color of the circle
            board.color("white")
            board.fillcolor(color)
            radius = size // 2
            board.down()
            #fill in the circle with the color
            board.begin_fill()
            circ = 2*3.14159*radius
            Len = circ / radius
            turnAngle = 360 / radius
            #start looping around the circle
            for r in range(radius) :
                board.forward(Len)
                board.right(turnAngle)
            board.end_fill()
            board.up()
            if (i == 3) :
                board.forward(size)
                board.left(180)
            elif (i == 7) :
                board.forward(size)
                board.right(90)
                board.forward(size * 2)
                board.right(90)
            else :
                board.forward(size * 2)
        #getting fancy
        color = "black"
        #this positions the turtle at the bottom of the top right red square
        board.goto(halfS - (size / 2), halfS - size)
        #this will cause the turtle to draw in reverse
        board.left(180)
    #show the changes
    #reset position of turtle
    board.goto(0, 0)
    board.tracer(1, 1)

size = 60
draw(size)
