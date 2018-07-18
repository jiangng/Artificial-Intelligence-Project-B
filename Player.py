'''
Created on Apr 15, 2018

@author: jiangng
'''
from Board import Board
from State import State
from Strategy import Strategy
from Strategy2 import Strategy2
from Game import Game

class Player:
    NEW_POS = 1
    OLD_POS = 0
    PHASE_CHANGE = 24
    
    def __init__(self, colour):
        self.player_colour = colour
        self.board = Board(colour) #waiting for parameters
        self.opponent_colour = 'white' if self.player_colour == 'black' else 'black'
        self.turns = 0
        self.isMovingPhase = False
                
    def action(self, turns):
        
        if (self.player_colour == "white" and turns in (128, 192)):
            self.board.board_shrink(turns)
            self.board.corner_elimination(turns)
            
        
        if not self.isMovingPhase:
            #Placing pieces
            state = State(self.board, self.player_colour, self.player_colour)
            action = Strategy.placing_def(state);
          
        else:
            #Moving pieces
            
            action = self.board.player_move();
            state = State(self.board, self.player_colour, self.player_colour, turns)
            action = Strategy2.iterative_deepening_search(state, Game, Game.eval_fn, 2, cutoff_test=None)

        if (self.player_colour == "white" and turns == 22) or (self.player_colour == "black" and turns == 23):
            self.isMovingPhase = True
        
        self.turns += 1
        
        print("action: ", action)
        
        self.board.update(action, self.player_colour);
        
        if (self.player_colour == "black" and turns in (127, 191)):
            self.board.board_shrink(turns)
            self.board.corner_elimination(turns)
           
            
        #self.board.debug_board()

        return action
        
    def update(self, action):

        self.board.update(action, self.opponent_colour)
