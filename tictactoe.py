"""
Tic Tac Toe Player
"""

import math
import copy
import sys

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    in the initial game state, X has the starting move
    
    WORKS
    """
    no_of_X = no_of_O =  0
    for row in board:
        for element in row:
            if element ==  X:
                no_of_X+=1
            elif element == O:
                no_of_O +=1
    
    if (no_of_X - no_of_O) not in {0,1}:
        sys.exit("Error: There is some error in the logic. Either extra O or X")
    # if the board is empty or if there are equal plays by both sides, X makes the next move else, O does
    if (no_of_X == 0) or (no_of_X==no_of_O):
        return X
    else:
        return O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    WORKS
    """
    set_of_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_actions.add((i,j))
    
    return set_of_actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    
    WORKS
    """
    new_board = copy.deepcopy(board)
    i,j = action
    new_board[i][j]=player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    
    WORKS
    """
    side_that_won = EMPTY
    # we can make the following code more general but it isnt necessary as a tictactoe board will only have a 3x3 grid
    for i in range(3):
        # checking if rows are same
        if board[i][0]==board[i][1]==board[i][2]:
            side_that_won = board[i][0]
            break
        # checking if columns are same
        if board[0][i]==board[1][i]==board[2][i]:
            side_that_won = board[0][i]
            break
    if ((board[0][0]==board[1][1]==board[2][2]) or (board[2][0]==board[1][1]==board[0][2])):
        side_that_won = board[1][1]
    
    return side_that_won


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    
    WORKS
    """
    is_terminal = True
    for row in board:
        if EMPTY in row:
            is_terminal = False
    
    if winner(board) != EMPTY:
        is_terminal =  True
    
    return is_terminal


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    this function basically evaluates the state of a terminal game
    """
    side_that_won = winner(board)
    if side_that_won == X:
        return 1
    elif side_that_won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    In utility, we defined:
    X winning=1; O winning=-1; tie=0
    therefore if the ai plays as X, we maximise first else we minimise first
    
    This also implements alpha-beta pruning to increase efficiency
    
    eval is the evaluation of the state
    consideration is the max_eval(while minimising) that we pass on to the next layer to prune the layer and vice-versa
    """
    
    def algorithm(board,player_now,consideration):
        if terminal(board):
            return utility(board),None
        
        # we maximize
        if player_now == X:
            
            # we set eval to -10 instead of -infinity as the lowest utility is -1
            max_eval = -10
            for action in actions(board):
                eval_new, _ = algorithm(result(board,action),O,max_eval)
                
                if eval_new > max_eval:
                    max_eval=eval_new
                    action_to_take = tuple(action)
                
                if max_eval>=consideration: #dunno if it should be > or >=
                    break
            
            return max_eval,action_to_take
        
        # we minimize
        if player_now == O:
            
            # we set eval to +10 instead of +infinity as the highest utility is +1
            min_eval = +10
            for action in actions(board):
                eval_new, _ = algorithm(result(board,action),X,min_eval)
                
                if eval_new < min_eval:
                    min_eval=eval_new
                    action_to_take = tuple(action)

                if min_eval<=consideration: #dunno if it should be < or <=
                    break

            return min_eval,action_to_take
        
    player_now = player(board)
    if player_now == X:
        consideration = 10
    else:
        consideration = -10
    _ ,action_to_take = algorithm(board,player_now,consideration)
    return action_to_take

        
    
    
    '''
    def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    In utility, we defined:
    X winning=1; O winning=-1; tie=0
    therefore if the ai plays as X, we maximise first else we minimise first
    
    This is the minimax algorithm without alpha-beta pruning
    """
    def algorithm(board,player_now):
        if terminal(board):
            return utility(board),None
        
        # we maximise
        if player_now == X:
            
            # we set eval to -10 instead of -infinity as the lowest utility is -1
            eval = -10
            for action in actions(board):
                eval_new, _ = algorithm(result(board,action),O)
                
                if eval_new > eval:
                    eval=eval_new
                    action_to_take = tuple(action)
            
            return eval,action_to_take
        
        # we minimixe
        if player_now == O:
            
            # we set eval to +10 instead of +infinity as the highest utility is +1
            eval = +10
            for action in actions(board):
                eval_new, _ = algorithm(result(board,action),X)
                
                if eval_new < eval:
                    eval=eval_new
                    action_to_take = tuple(action)
            
            return eval,action_to_take
        
    _ ,action_to_take = algorithm(board,player(board))
    return action_to_take
    '''