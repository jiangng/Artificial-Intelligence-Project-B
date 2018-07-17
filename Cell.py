'''
Created on Apr 17, 2018

@author: jiangng
'''
class Cell:
    MY_ZONE = 0
    OFF_ZONE = 1
    SHRUNK = 2
    CORNER = 3
    
    def __init__(self, cell_type):
        #self.x = x
        #self.y = y
        self.cell_type = cell_type #my_zone, off_zone, shrunk_zone, corner
        self.piece = None
        
    def check_cell_type(self, cell_type):
        return self.cell_type == cell_type
    
    def is_empty(self):
        return self.piece is None
