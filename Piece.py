'''
Created on 16 Apr 2018
@author: xiang
'''

class Piece:
    COLOUR = 0
    NUMBER = 1

    def __init__(self, x, y, piece_id, is_alive=True):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.piece_id = piece_id
        self.is_alive = is_alive
        
    def get_colour(self):
        return self.piece_id[self.COLOUR]
