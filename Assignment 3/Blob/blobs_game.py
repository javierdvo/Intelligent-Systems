import random

from games import (GameState, Game, query_player, random_player, 
                    alphabeta_player, play_game,
                    alphabeta_full_search, alphabeta_search)

#_______________________________________________________________________________
# Auxiliary functions

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
        positions = [(row,col) for row in range(1, 7) for col in range(1, 7)]
        random.shuffle(positions)
        self.red_blobs = set(positions[0:12])
        self.green_blobs = set(positions[12:24])

#    def display(self):
#        "displays the board"
#        for row in range(1, 7):
#            for col in range(1, 7):
#                position = (row, col)
#                if row <= self.top_border or row >= self.bottom_border or \
#                   col <= self.left_border or col >= self.right_border:
#                    print('o', end=' ')
#                elif position in self.red_blobs: print('R', end=' ')
#                elif position in self.green_blobs: print('G', end=' ')
#                else: print('.', end=' ')
#            print()
    def display(self):    
        for col in range(1, 7):
            for row in range(1, 7):
                position = (row, col)
                if col <= self.top_border or col >= self.bottom_border or \
                   row <= self.left_border or row >= self.right_border:
                    print('o', end=' ')
                elif position in self.red_blobs: print('R', end=' ')
                elif position in self.green_blobs: print('G', end=' ')
                else: print('.', end=' ')
            print()

    def update_borders(self):
        "update the positions of the board borders"
        # update left border: moves right on left empty columns
        #Right border, left border, Top_border, Bottom border        
        contRB=0
        contLB=0
        contTB=0
        contBB=0
        
        blobs_union= self.red_blobs.union(self.green_blobs)
        for blob in blobs_union:
            x= blob[0]
            y= blob[1]
            if x == self.left_border+1:
                contLB+=1
            elif x == self.right_border-1:
                contRB+=1
            if y == self.top_border + 1:
                contTB+=1
            elif y == self.bottom_border-1:
                contBB +=1
        if contRB == 0:
            self.right_border = self.right_border-1
        if contLB == 0:
            self.left_border = self.left_border+1
        if contTB == 0:
            self.top_border= self.top_border+1
        if contBB == 0:
            self.bottom_border= self.bottom_border -1
                
        # update bottom border: moves up on bottom empty rows
        
        #raise NotImplementedError
    
    def move(self, color, direction):
        "moves all the blobs of a color in a direction"
        # move blobs of the specified color eliminating those that fall out of the board
        arreglo_auxiliar = set()        
        if color== 'R':
            
            for tuplaroja in self.red_blobs:
                x = tuplaroja[0]
                y = tuplaroja[1]
                if direction == 'U':
                    y = y - 1
                if direction == 'D':
                    y = y + 1
                if direction == 'L':
                    x = x - 1
                if direction == 'R':
                    x = x + 1
                tupla_aux = (x,y)
                arreglo_auxiliar.add(tupla_aux)
            self.red_blobs = arreglo_auxiliar 
           
        if color=='G':
            
            for tuplaverde in self.green_blobs:
                x = tuplaverde[0]
                y = tuplaverde[1]
                if direction == 'U':
                    y = y - 1
                if direction == 'D':
                    y = y + 1
                if direction == 'L':
                    x = x - 1
                if direction == 'R':
                    x = x + 1
                tupla_aux = tuple(x,y)
                arreglo_auxiliar.add(tupla_aux)
            self.green_blobs = arreglo_auxiliar
        
        #Eliminating those who fall out the board
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
                if y <= self.top_border or y >= self.bottom_border :
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
                        existe_verde=True
                if not existe_verde:
                    arreglo_auxiliar.add(tuplaverde)
            self.green_blobs= arreglo_auxiliar
            
        if color == 'G':
            arreglo_auxiliar = set()
            for tuplaroja in self.red_blobs:
                existe_roja = False
                xroja = tuplaroja[0]
                yroja = tuplaroja[1]
                
                for tuplaroja in self.red_blobs:
                    xverde = tuplaverde[0]
                    yverde = tuplaverde[1]
                    
                    if xverde == xroja and yverde == yroja:
                        existe_roja = True
                if not existe_roja:
                    arreglo_auxiliar.add(tuplaroja)
            self.red_blobs= arreglo_auxiliar
                    
        # update borders
        self.update_borders()
        #raise NotImplementedError
        self.display()
    # other methods???
        
class Blobs(Game):
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
                                 board=BlobsBoard(), moves=['L','R','U','D'])

    def actions(self, state):
        "Legal moves are always all the four original directions."
        if state.to_move == 'R':
            self.result(state,'R')
        #raise NotImplementedError

    def result(self, state, move):
        "returns the result of applying a move to a state"
        if move =='R':
            self.initial.board.move(self.initial.to_move, 'R')
        #raise NotImplementedError

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        raise NotImplementedError

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        raise NotImplementedError

    def display(self, state):
        "Displays the current state"
        self.initial.board.display()
        
        
        #raise NotImplementedError

## YOU ALSO NEED TO CREATE AN EVAL_FN AND A PLAYER FOR YOUR GAME THAT USE
## ALPHABETA_SEARCH INSTEAD OF ALPHABETA_FULL_SEARCH.
## YOU DO NOT NEED A CUTOFF_TEST BECAUSE I WILL USE DEPTHS FOR CUTTING THE
## LOOK-AHEAD SEARCH.

def main():
    print('Hola')
    movement = Blobs()
    movement.display(movement.initial)
    state = movement.actions(movement.initial)
    print("______________MOVIMIENTO DERECHA_____________________")
    movement.display(state)
     
if __name__ == "__main__":
    main()

