"""
Tic Tac Toe Player
"""

import math
import copy

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
    """
    #counting the number of xs and os
    X_count = sum(row.count(X)for row in board)
    O_count = sum(row.count(O)for row in board)

    #return the game to the player
    if X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    #checking for empty places
    for i in range(3):
        for j in range(3):
            if board [i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #when the action is invalid
    if not action in actions(board):
        raise Exception("invalid action")

    copy_board = copy.deepcopy(board)

    #insert the users move(action)
    copy_board[action[0]][action[1]] = player(board)

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #horizonal check
    for i in range(3):
        if board[i].count(X) == 3:
            return X
        if board[i].count(O) == 3:
            return O

    #diogonal check
    if board[0][0] ==board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] ==board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    for i in range(3):
        X_count = 0
        O_count = 0
        for j in range(3):
            if board[j][i] == X:
                X_count += 1
            if board[j][i] == O:
                O_count += 1

        if X_count == 3:
            return X
        if O_count == 3:
            return O
    #no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #if there is a winner
    if winner (board):
        return True

    #checking if there are any empty cells
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    #who is the winner
    if win == X:
        return 1
    elif win == 0:
        return -1
    else:
        return 0

def max_value(board):

    #checking if the game is over or not
    if terminal(board):
        return utility(board), None
    #assigning neg infinitity
    v = -math.inf

    best_action = None

    #finding max valueamong the values returned by the min value fucntion
    for action in actions(board):
        min_val, _ = min_value(result(board, action))

        if min_val > v:
            v= min_val
            best_action = action

    return v, best_action


def min_value(board):

    #checking if the game is over or not
    if terminal(board):
        return utility(board), None
    #assigning pos infinitity
    v = math.inf

    best_action = None

    #finding min valueamong the values returned by the max value fucntion
    for action in actions(board):
        max_val, _ = max_value(result(board, action))

        if max_val < v:
            v= max_val
            best_action = action

    return v, best_action

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    #idf the current player is maxplayer, suppose X
    if player(board) == X:
        _, optimal_action = max_value(board)
        return optimal_action

    else: 
        _, optimal_action = min_value(board)

        return optimal_action
