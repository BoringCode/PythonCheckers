#Find all blocks (moving out of a jump or moving a checker to block a jump)
#This may need some modification to work with Dr. White's program, I made it for my own version of checkers.
#For player moves, I just pass in: possibles["jumps"] + possibles["moves"]
def findBlocks(CB, opponent, playerMoves) :
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
    #THIS IS THE REAL MAGIC
    #Get the opponent jumps
    jumps = findMoves(CB, opponent, opponentPieces, playerPieces, jumpInc, jumpIncs)
    #start looping through the jumps
    for jump in jumps :
        #Future proof, can handle multiple jumps
        moves = jump.split(":")
        #loop through each part of the jump, starting at the second part (I only want the "resting" place of the jump, so I can move to it and block it)
        #This will work for ANY part of a multi-jump, so I could perhaps turn a multi-jump into a normal jump.
        for i in range(1, len(moves)) :
            #loop through the moves that my player can make
            for playerMove in playerMoves :
                #check if final resting place of this move is also the finishing location of the jump
                if playerMove[-2:] == moves[i] :
                    #Hey, put it in the blocks list
                    if (playerMove not in blocks) :
                        blocks.append(playerMove)
    return blocks
