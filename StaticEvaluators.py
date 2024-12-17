########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2024, Swarthmore College
########################################

import numpy as np
from random import choice
from Mancala import Mancala
from Breakthrough import Breakthrough

def nimBasicEval(nim_game):
    """returns +1 or -1 on win/loss, else returns 0
    This is basically a 'dummy' eval function, it will run,
    but it won't do anything useful if you can't expand the 
    whole tree (but with Nim, the branching factor is only 3,
    so that's probably ok)
    """
    if nim_game.isTerminal:
        return nim_game.winner
    else:
        return 0

def mancalaBasicEval(mancala_game):
    """Difference between the scores for each player.
    Returns +9999 if player +1 has won.
    Returns -9999 if player -1 has won.

    Otherwise returns (player +1's score) - (player -1's score).

    Remember that the number of houses and seeds may vary."""
    
    if mancala_game.isTerminal:
        if mancala_game.winner == 1:
            return 9999
        else:
            return -9999
    else:
        return mancala_game.scores[0] - mancala_game.scores[1]


def breakthroughBasicEval(breakthrough_game):
    """Measures how far each player's pieces have advanced
    and returns the difference.

    Returns +9999 if player +1 has won.
    Returns -9999 if player -1 has won.

    Otherwise finds the rank of each piece (number of rows onto the board it
    has advanced), sums these ranks for each player, and
    returns (player +1's sum of ranks) - (player -1's sum of ranks).

    An example on a 5x3 board:
    ------------
    |  0  1  1 |  <-- player +1 has two pieces on rank 1
    |  1 -1  1 |  <-- +1 has two pieces on rank 2; -1 has one piece on rank 4
    |  0  1 -1 |  <-- +1 has (1 piece * rank 3); -1 has (1 piece * rank 3)
    | -1  0  0 |  <-- -1 has (1*2)
    | -1 -1 -1 |  <-- -1 has (3*1)
    ------------
    sum of +1's piece ranks = 1 + 1 + 2 + 2 + 3 = 9
    sum of -1's piece ranks = 1 + 1 + 1 + 2 + 3 + 4 = 12
    state value = 9 - 12 = -3

    Remember that the height and width of the board may vary."""

    if breakthrough_game.isTerminal:
        if breakthrough_game.winner == 1:
            return 9999
        else:
            return -9999
    else:
        sumPlusOne = 0
        sumMinusOne = 0
        for row in range(len(breakthrough_game.board)):
           
            for col in range(len(breakthrough_game.board[0])):
                
                currSquare = breakthrough_game.board[row,col]
                if currSquare == 1:
                    sumPlusOne += row + 1
                elif currSquare == -1:
                    sumMinusOne += len(breakthrough_game.board) - row 
        
        return sumPlusOne - sumMinusOne

def breakthroughBetterEval(breakthrough_game):
    """A heuristic that generally wins agains breakthroughBasicEval.
    This must be a static evaluation function (no search allowed).

    our heuristic uses the same scaffolding as the basic heuristic,
    and also takes into account who has more pieces, how clear the path is
    ahead of the furthest-ahead piece, and how good the position of the 
    furthest-ahead piece is"""

    if breakthrough_game.isTerminal:
        if breakthrough_game.winner == 1:
            return 9999
        else:
            return -9999
    else:
        sumPlusOne = 0
        sumMinusOne = 0
        pieceCount = 0
        countP1 = 0
        countP2 = 0
        best1 = float('-inf')
        best2 = float('inf')
        for row in range(len(breakthrough_game.board)):
           
            for col in range(len(breakthrough_game.board[0])):
                
                currSquare = breakthrough_game.board[row,col]
                if currSquare == 1:
                    pieceCount += 1
                    sumPlusOne += row + 1
                    if row > best1:
                        best1 = row
                        countP1 += countFriendly(breakthrough_game, row, col, 1)

                elif currSquare == -1:
                    pieceCount -= 1
                    sumMinusOne += len(breakthrough_game.board) - row 
                    if row < best2:
                        best2 = row
                        countP2+= countFriendly(breakthrough_game, row, col, -1)
        return sumPlusOne + countP1 - sumMinusOne - countP2 + pieceCount + best1 + best2


def checkBounds(breakthrough_game,row,col):
    """ Checks whether a spot in a breakthrough game is a valid square on the board
    """
    return row > -1 and row < len(breakthrough_game.board) and col > -1 and col < len(breakthrough_game.board[0])

def countFriendly(breakthrough_game,row,col, currSquare):
    """ Counts how many of the spaces in front of a given breakthrough 
    piece are empty
    """
    count = 0
    if currSquare == 1:

        if checkBounds(breakthrough_game, row+1, col -1):
            if breakthrough_game.board[row+1, col -1] == 0: 
                count += 1
        if checkBounds(breakthrough_game, row+1, col ):
            if breakthrough_game.board[row+1, col ] == 0: 
                count += 1
        if checkBounds(breakthrough_game, row+1, col +1):
            if breakthrough_game.board[row+1, col +1] == 0: 
                count += 1
        
    else:
        if checkBounds(breakthrough_game, row-1, col -1):
            if breakthrough_game.board[row-1, col -1] == 0: 
                count -= 1
        if checkBounds(breakthrough_game, row-1, col ):
            if breakthrough_game.board[row-1, col] == 0: 
                count -= 1            
        if checkBounds(breakthrough_game, row-1, col +1):
            if breakthrough_game.board[ row-1, col +1] == 0: 
                count -= 1

    return count
     


if __name__ == '__main__':
    """
    Create a game of Mancala.  Try 10 random moves and check that the
    heuristic is working properly. 
    """
    print("\nTESTING MANCALA HEURISTIC")
    print("-"*50)
    game1 = Mancala()
    print(game1)
    for i in range(10):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = mancalaBasicEval(game1)
        print("basicEval score", score)

    # Add more testing for the Breakthrough

    print("\nTESTING BREAKTHROUGH HEURISTIC")
    print("-"*50)
    game1 = Breakthrough()
    print(game1)
    for i in range(15):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = breakthroughBasicEval(game1)
        print("basicEval score", score)

