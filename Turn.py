'''
Created on 17 Apr 2018

@author: xiang
'''

class Turn:
    '''
    classdocs
    '''

    def __init__(self, turn=0, phase="", action=(), piece_id=[]):
        '''
        Constructor
        '''
        self.turn = turn;
        self.phase = phase;
        self.action = action;
        self.piece_id = piece_id;
        
    def getTurn(self):
        return self.turn
    
    def getPhase(self):
        return self.phase
    
    def getAction(self):
        return self.action
    
    def getPieceId(self):
        return self.piece_id
    
    def setTurn(self, turn):
        self.turn = turn
        
    def setPhase(self, phase):
        self.phase = phase
        
    def setAction(self, action):
        self.action = action
        
    def setPieceId(self, piece_id):
        self.piece_id = piece_id
