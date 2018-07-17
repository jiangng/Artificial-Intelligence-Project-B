'''
Created on Apr 15, 2018

@author: jiangng
'''
from Board import Board
from State import State
from Strategy import Strategy
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
        self.game = Game()
        self.state = State(self.board, self.player_colour, self.player_colour)
        
    def action(self, turns):
        
        if (self.player_colour == "white" and turns in (128, 192)):
            self.board.board_shrink(turns)
            self.board.corner_elimination(turns)
            
        
        if not self.isMovingPhase:
            #Placing pieces
            action = self.board.player_place();
          
        else:
            #Moving pieces
            
            action = self.board.player_move();
            #self.state = State(self.board, self.player_colour, self.player_colour)
            #action = Strategy.alphabeta_cutoff_search(self.state, Game, Game.eval_fn, d=1, cutoff_test=None)

        if (self.player_colour == "white" and turns == 22) or (self.player_colour == "black" and turns == 23):
            self.isMovingPhase = True
        
        
        
        self.turns += 1
        
        print("action: ", action)
        
        self.board.update(action, self.player_colour);
        self.state.update(self.board)
        
        if (self.player_colour == "black" and turns in (127, 191)):
            self.board.board_shrink(turns)
            self.board.corner_elimination(turns)
           
            
        #self.board.debug_board()

        return action
        
    def update(self, action):
        """
        if type(action[0]) is int:
            #place enemy piece
            self.board.place(action, self.opponent_colour)
            #check elimination
            self.board.elimination(action)
            
        elif type(action[0]) is tuple:
            #shift enemy piece to the new loc
            self.board.shift(action)
            #check elimination
            self.board.elimination(action[Player.NEW_POS])
        self.turns += 1
        """
        self.board.update(action, self.opponent_colour)
