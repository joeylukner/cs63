########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2024, Swarthmore College
########################################

class MinMaxPlayer:
    """Gets moves by depth-limited minimax search."""
    def __init__(self, boardEval, depthBound):
        self.name = "MinMax"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root

    def getMove(self, game_state):
        """Create a recursive helper function to implement Minimax, and
        call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        self.bestMove = None
        bestValue =  self.boundedMinMax(game_state, 0)
        return self.bestMove

    def boundedMinMax(self, state, depth):
        """ Implements recursive MiniMax that goes until a certain depth bound
        """
        if depth == self.depthBound or state.isTerminal:
            return self.boardEval(state)
        
        bestValue  = state.turn * float('-inf')
        for move in state.availableMoves:
            nextState = state.makeMove(move)
            #recursive call

            value = self.boundedMinMax(nextState, depth+1)
            if state.turn == 1:
                if value > bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
            
            else: #minimizer
                if value < bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
        
        return bestValue



class PruningPlayer:
    """Gets moves by depth-limited minimax search with alpha-beta pruning."""
    def __init__(self, boardEval, depthBound):
        self.name = "Pruning"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root
        
    def getMove(self, game_state):
        """Create a recursive helper function to implement AlphaBeta pruning
        and call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        self.bestMove = None
        bestValue = self.minMaxPruning(game_state, float('-inf'), float('inf'), 0)
        return self.bestMove

    def minMaxPruning(self, game_state, alpha, beta, depth):
        """ Implements recursive Minimax with Alpha-Beta Pruning that goes 
        until a given depth bound
        """
        if depth == self.depthBound or game_state.isTerminal:
            return self.boardEval(game_state)
        elif game_state.turn == 1:
            for move in game_state.availableMoves:
                nextState = game_state.makeMove(move)
                value = self.minMaxPruning(nextState, alpha, beta, depth+1)
                if value >= beta:
                    return value
                elif value > alpha:
                    alpha = value
                    if depth == 0:
                        self.bestMove = move
            return alpha
        else:
            for move in game_state.availableMoves:
                nextState = game_state.makeMove(move)
                value = self.minMaxPruning(nextState, alpha, beta, depth+1)
                if value <= alpha:
                    return value
                elif value < beta:
                    beta = value
                    if depth == 0:
                        self.bestMove = move
            return beta


