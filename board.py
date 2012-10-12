def checkers(size) :
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
    #show the changes
    board.tracer(1, 1)
        
#run function
checkers(60)
