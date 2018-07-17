'''
Created on 4 May 2018

@author: xiang
'''
import queue as Q

class State:
    '''
    classdocs
    '''
    
    class Best_Action:
        def __init__(self, state, action, eval_score):
            self.state = state
            self.action = action
            self.eval_score = eval_score #priority
        def __gt__(self, other):
            return self.eval_score < other.eval_score
    
    def __init__(self, board, max_colour, curr_move_colour, turns=None):
        '''
        Constructor
        '''
        
        self.board = board;
        self.max_colour = max_colour
        self.curr_move_colour = curr_move_colour
        self.turns = turns
        self.killer_moves = Q.PriorityQueue()
    
    def update(self, board):
        self.board = board
    
    def keep_result_state(self, state, action, eval_score):
        """
            input: Resultant state caused by this action, 
                    action that causes this resultant state,
                    evaluation score of this state
        """
        self.killer_moves.put(self.Best_Action(state, action, eval_score))
        
