import random
import copy
from games import (GameState, Game, query_player, random_player,
                   alphabeta_player, play_game,
                   alphabeta_full_search, alphabeta_search)


# _______________________________________________________________________________
# Auxiliary functions

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            v = eval_fn(state, player)  # needs the max player
            return v
        v = -9999999
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        # print('max:',v)
        return v

    def min_value(state, alpha, beta, depth):
        # print('min_value')
        if cutoff_test(state, depth):
            v = eval_fn(state, player)  # needs the max player
            # print('min:',v)
            return v
        v = 99999999
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        # print('min:',v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth == d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -999999999
    beta = 99999999
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# _______________________________________________________________________________
# Blobs Game functions

class BlobsBoard(object):
    """Blobs game class to generate and manipulate boards"""

    def __init__(self):
        "creates a new random 6x6 board with 12 red and 12 green Blobs"
        # board limits
        self.left_border = 0
        self.right_border = 7
        self.top_border = 0
        self.bottom_border = 7
        self.red_blobs = None
        self.green_blobs = None
        self.new_random_board()

    def new_random_board(self):
        "generate 12 random positions for each Blob color on the board"
        positions = [(row, col) for row in range(1, 7) for col in range(1, 7)]
        random.shuffle(positions)
        self.red_blobs = set(positions[0:12])
        self.green_blobs = set(positions[12:24])

    def display(self):
        "displays the board"
        for row in range(1, 7):
            for col in range(1, 7):
                position = (row, col)
                if row <= self.top_border or row >= self.bottom_border or \
                                col <= self.left_border or col >= self.right_border:
                    print('o', end=' ')
                elif position in self.red_blobs:
                    print('R', end=' ')
                elif position in self.green_blobs:
                    print('G', end=' ')
                else:
                    print('.', end=' ')
            print()

    def update_borders(self):
        "update the positions of the board borders"
        # update left border: moves right on left empty columns
        # Right border, left border, Top_border, Bottom border
        contRB = 0
        contLB = 0
        contTB = 0
        contBB = 0

        blobs_union = self.red_blobs.union(self.green_blobs)
        for blob in blobs_union:
            x = blob[1]
            y = blob[0]
            if x == self.left_border + 1:
                contLB += 1
            elif x == self.right_border - 1:
                contRB += 1
            if y == self.top_border + 1:
                contTB += 1
            elif y == self.bottom_border - 1:
                contBB += 1
        if contRB == 0:
            self.right_border = self.right_border - 1
        if contLB == 0:
            self.left_border = self.left_border + 1
        if contTB == 0:
            self.top_border = self.top_border + 1
        if contBB == 0:
            self.bottom_border = self.bottom_border - 1

            # update bottom border: moves up on bottom empty rows

            # raise NotImplementedError

    def move(self, color, direction):
        "moves all the blobs of a color in a direction"
        # move blobs of the specified color eliminating those that fall out of the board
        arreglo_auxiliar = set()
        if color == 'R':
            for tuplaroja in self.red_blobs:
                x = tuplaroja[0]
                y = tuplaroja[1]
                if direction == 'L':
                    y = y - 1
                if direction == 'R':
                    y = y + 1
                if direction == 'U':
                    x = x - 1
                if direction == 'D':
                    x = x + 1
                # tupla_aux = tuple(x,y)
                arreglo_auxiliar.add((x, y))
            self.red_blobs = arreglo_auxiliar

        if color == 'G':

            for tuplaverde in self.green_blobs:
                x = tuplaverde[0]
                y = tuplaverde[1]
                if direction == 'L':
                    y = y - 1
                if direction == 'R':
                    y = y + 1
                if direction == 'U':
                    x = x - 1
                if direction == 'D':
                    x = x + 1
                arreglo_auxiliar.add((x, y))
            self.green_blobs = arreglo_auxiliar

        # Eliminating those who fall out the board
        if color == 'G':
            arreglo_auxiliar = set()
            for tuplaverde in self.green_blobs:
                x = tuplaverde[0]
                y = tuplaverde[1]
                if x <= self.left_border or x >= self.right_border:
                    continue
                if y <= self.top_border or y >= self.bottom_border:
                    continue
                arreglo_auxiliar.add(tuplaverde)
            self.green_blobs = arreglo_auxiliar

        if color == 'R':
            arreglo_auxiliar = set()
            for tuplaroja in self.red_blobs:
                x = tuplaroja[0]
                y = tuplaroja[1]
                if x <= self.left_border or x >= self.right_border:
                    continue
                if y <= self.top_border or y >= self.bottom_border:
                    continue
                arreglo_auxiliar.add(tuplaroja)
            self.red_blobs = arreglo_auxiliar

        # eliminate corresponding blobs of the opponent
        if color == 'R':
            arreglo_auxiliar = set()
            for tuplaverde in self.green_blobs:
                existe_verde = False
                xverde = tuplaverde[0]
                yverde = tuplaverde[1]

                for tuplaroja in self.red_blobs:
                    xroja = tuplaroja[0]
                    yroja = tuplaroja[1]

                    if xverde == xroja and yverde == yroja:
                        existe_verde = True
                if not existe_verde:
                    arreglo_auxiliar.add(tuplaverde)
            self.green_blobs = arreglo_auxiliar

        if color == 'G':
            arreglo_auxiliar = set()
            for tuplaroja in self.red_blobs:
                existe_roja = False
                xroja = tuplaroja[0]
                yroja = tuplaroja[1]

                for tuplaverde in self.green_blobs:
                    xverde = tuplaverde[0]
                    yverde = tuplaverde[1]
                    if xverde == xroja and yverde == yroja:
                        existe_roja = True
                if not existe_roja:
                    arreglo_auxiliar.add(tuplaroja)
            self.red_blobs = arreglo_auxiliar

        # update borders
        self.update_borders()
        # raise NotImplementedError
        #self.display()
        return self
        # other methods???


class Blobs12(Game):
    """Play Blobs on an 6 x 6 board, with Max (first player) playing the red
    Blobs with marker 'R'.
    A state has the player to move, a cached utility, a list of moves in
    the form of the four directions (left 'L', right 'R', up 'U', and down 'D'),
    and a board, in the form of a BlobsBoard object.
    Marker is 'R' for the Red Player and 'G' for the Green Player. An empty
    position appear as '.' in the display and a 'o' represents an out of the
    board position."""

    def __init__(self):
        self.initial = GameState(to_move='R', utility=0,
                                 board=BlobsBoard(), moves=['L', 'R', 'U', 'D'])


    def actions(self, state):
        "Legal moves are always all the four original directions."
        return state.moves
        # raise NotImplementedError
    def updateBoard(self,stateBoard):
        self.board=stateBoard

    def result(self, state, move):
        "returns the result of applying a move to a state"
        if state.to_move == "G":
            a = GameState(to_move="R", utility=self.computeUtility(state, "G"), board=state.board.move(state.to_move, move),
                          moves=['U', 'D', 'L', 'R'])
        else:
            a = GameState(to_move="G", utility=self.computeUtility(state, "R"), board=state.board.move(state.to_move, move),
                          moves=['U', 'D', 'L', 'R'])
        return a

        # raise NotImplementedError

    def utility(self, state):
        return state.utility

    def computeUtility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        if (player == "R"):
            if (self.terminal_test(state)):
                if len(state.board.red_blobs) > len(state.board.green_blobs):
                    return 1
                else:
                    return -1
            else:
                return 0
        if (player == "G"):
            if (self.terminal_test(state)):
                if len(state.board.red_blobs) < len(state.board.green_blobs):
                    return 1
                else:
                    return -1
            else:
                return 0

                # raise NotImplementedError

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        size = (state.board.right_border - state.board.left_border) * (
        state.board.bottom_border - state.board.top_border)
        len1 = len(state.board.red_blobs)
        len2 = len(state.board.green_blobs)
        if (len1 == 0 or len2 == 0 or size == len1 + len2):
            return True
        else:
            return False
            # raise NotImplementedError

    def display(self, state):
        "Displays the current state"
        print()
        state.board.display()
        print()


        # raise NotImplementedError


## YOU ALSO NEED TO CREATE AN EVAL_FN AND A PLAYER FOR YOUR GAME THAT USE
## ALPHABETA_SEARCH INSTEAD OF ALPHABETA_FULL_SEARCH.
## YOU DO NOT NEED A CUTOFF_TEST BECAUSE I WILL USE DEPTHS FOR CUTTING THE
## LOOK-AHEAD SEARCH.


def eval_fn12(state, player):
    risk=0
    alpha=1
    beta=0.8
    gamma=0.05
    print(state.board.red_blobs)
    print(state.board.green_blobs)
    for valR in state.board.red_blobs:
        for valG in state.board.green_blobs:
            if(abs(valG[0]-valR[0])==1 or abs(valG[1]-valR[1])==1):
                risk+=1
    if (player == "R"):
        value=alpha*len(state.board.red_blobs) - beta*len(state.board.green_blobs) - risk*gamma
        return value
    else:

        value=alpha*len(state.board.green_blobs) - beta*len(state.board.red_blobs) - risk*gamma
        return value
    """returns a positive value is the given player (red or green) is supposed
    to win the game or negative if the player is supposed to lose"""
    raise NotImplemented


# ______________________________________________________________________________
# Players for Games

def team_player12(depth, eval_fn):

    return (lambda game, state:
            alphabeta_search(state, game, d=depth, eval_fn=eval_fn))


def display_move(player, direction):
    "Display a player's move"
    if player == 'R':
        print('Red', end=' ')
    else:
        print('Green', end=' ')
    print('Blobs player moves', end=' ')
    if direction == 'U':
        print('UP')
    elif direction == 'D':
        print('Down')
    elif direction == 'L':
        print('Left')
    elif direction == 'R':
        print('Right')
    else:
        print('Wrong')


def play_game12(game, *players):
    """Plays a 2-player Blobs game."""
    state = game.initial

    print('INITIAL BOARD')
    plays = 0
    while plays < 30:  # Maximum number of plays to finish a game
        plays += 1
        print('PLAY #', plays)
        for player in players:

            game.display(state)
            state2=copy.deepcopy(state)
            move = player(game, state)
            display_move(state2.to_move, move)
            state = game.result(state2, move)
            if game.terminal_test(state):
                game.display(state)
                utility = game.computeUtility(state, game.to_move(game.initial))
                if utility > 0:
                    print('Red player wins!!')
                elif utility < 0:
                    print('Green player wins!!')
                else:
                    print('Tie: Nobody wins!!')
                return utility
    print('=> Reach maximum number of plays')
    utility = game.utility(state, game.to_move(game.initial))
    if utility > 0:
        print('Red player wins!!')
    elif utility < 0:
        print('Green player wins!!')
    else:
        print('Tie: Nobody wins!!')
    return utility


play_game12(Blobs12(), team_player12(3, eval_fn12), team_player12(3, eval_fn12))
