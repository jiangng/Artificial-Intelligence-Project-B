'''
Created on 16 Apr 2018
@author: xiang
'''
from Piece import Piece
from Cell import Cell
from Turn import Turn
import random

class Board:
    
    X = 0
    Y = 1
    OLD_POS = 0
    NEW_POS = 1
    MAX_ROW = 8
    MAX_COL = 8
    MIN_ROW = 0
    MIN_COL = 0
    MAX_PIECE = 12
    INIT_CORNERS = ((0, 0), (7, 0), (0, 7), (7, 7))
    
    EAST = "east"
    WEST = "west"
    NORTH = "north"
    SOUTH = "south"
    
    WHITE_OFF_ROWS = (6, 7)
    BLACK_OFF_ROWS = (0, 1)
    SHRINK_ROUNDS = (128, 192)
    
    def __init__(self, colour):
        
        my_zone = self.determine_starting_zone(colour)
        self.board = [[None for i in range(self.MAX_ROW)] for j in range(self.MAX_COL)]
        for i in range(self.MAX_COL):
            for j in range(self.MAX_ROW):
                if (i, j) in self.INIT_CORNERS:
                    self.board[i][j] = Cell(Cell.CORNER)
                else:
                    if (i, j) in my_zone:
                        self.board[i][j] = Cell(Cell.MY_ZONE)
                    else:
                        self.board[i][j] = Cell(Cell.OFF_ZONE)
                
        self.curr_black_id = 0 #Used for assigning an id to every piece
        self.curr_white_id = 0
        self.dead_pieces = []
        self.player_colour = colour #For now unneeded
        self.opponent_colour = 'white' if self.player_colour == 'black' else 'black' #For now unneeded
        self.turns = [Turn(0, "place")]
    
    def determine_starting_zone(self, colour):
        """
        Find the starting zone for the player based on its colour
        input: player's colour
        output: list of legitimate placing positions
        """
        
        my_off_rows = self.WHITE_OFF_ROWS if colour=='white' else self.BLACK_OFF_ROWS
        my_zone = list()
        
        for i in range(self.MAX_COL):
            for j in range(self.MAX_ROW):
                if (i, j) in self.INIT_CORNERS:
                    continue
                elif j not in my_off_rows:
                    my_zone.append((i, j))
                    
        return my_zone
    
    def pick_player(self, piece_id):
        
        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if (self.board[i][j].piece is not None and self.board[i][j].piece.piece_id == piece_id):
                    return (i, j)                
        
        return None  
    
    def update(self, action, colour):
        
        if type(action[0]) is int:
            #place player piece
            self.place(action, colour)
            #check elimination
            coords_eliminated = self.elimination(action)
            
        elif type(action[0]) is tuple:
            #shift enemy piece to the new loc
            self.shift(action)
            #check elimination
            print(colour, action)
            coords_eliminated = self.elimination(action[self.NEW_POS])
            
        self.remove_pieces(coords_eliminated)
    
    def place(self, action, colour):
        """
        Place a new piece on the board during placing phase
        input: the placing coordinates and the player's colour
        """
        
        piece_x = action[self.X]
        piece_y = action[self.Y]
        prev_turn = self.turns[-1]
        #To place a new piece, instantiate a Piece object and assign to the corresponding cell object
        if (colour == "white"):
            if (self.get_cell(action).is_empty() and self.curr_white_id < self.MAX_PIECE):
                self.curr_white_id += 1          #To keep track of the id number assigned so far
                self.get_cell(action).piece = Piece(piece_x, piece_y, ("white", self.curr_white_id), True)
                
        else:
            if (self.get_cell(action).is_empty() and self.curr_black_id < self.MAX_PIECE):
                self.curr_black_id += 1
                self.get_cell(action).piece = Piece(piece_x, piece_y, ("black", self.curr_black_id), True)
        
        piece_id = self.board[piece_x][piece_y].piece.piece_id
        self.turns.append(Turn(prev_turn.turn + 1, "place", action, piece_id))
        
    def shift(self, action):
        """
        Shift a piece from its current position to a new legit position
        input: the old and new coordinates of the piece
        """
        old_pos = action[self.OLD_POS]
        new_pos = action[self.NEW_POS]
        
        new_x = new_pos[self.X]
        new_y = new_pos[self.Y]

        # remove the piece from the cell of the old position
        temp_piece = self.get_cell(old_pos).piece
        self.get_cell(old_pos).piece = None
                
        # assign the piece to the cell of the new position 
        temp_piece.x = new_x
        temp_piece.y = new_y
        self.get_cell(new_pos).piece = temp_piece
    
    def remove_pieces(self, coords_eliminated):
       
        for coords in coords_eliminated:
            self.get_cell(coords).piece = None
            
        
    def is_piece_eliminated(self, coords_eliminated, board_pos):
        """
            is_piece_eliminated checks whether the black piece in the 
            board in the function elimination has been eliminated before 
            checking whether the white piece should be eliminated
            input: eliminate, board_pos
            output: bool
        """
    
        for coords in coords_eliminated:
            # check whether the black position on board has been eliminated
            if (coords == board_pos):
                return True
            
        return False


    def piece_colour(self, coords):
        curr_piece = self.get_cell(coords).piece
        
        if curr_piece is not None:
            return curr_piece.get_colour()
        
        return None
        
    def is_enemy(self, coords, colour):
        return self.piece_colour(coords) == colour or self.get_cell(coords).cell_type == Cell.CORNER
    
    def is_ally(self, coords, colour):
        return self.piece_colour(coords) == colour or self.get_cell(coords).cell_type == Cell.CORNER
                
    def surround_opponent(self, coords, coords_eliminated):
        
        for coords in self.directions(coords).values():
            if (self.check_cell_valid(coords, (Cell.CORNER, ))):
                self.self_surrounded(coords, coords_eliminated)
    
    def self_surrounded(self, coords, coords_eliminated):
        
        piece = self.get_cell(coords).piece
        
        if (piece is not None):
            colour = piece.get_colour()
            opp_colour = "white" if colour == "black" else "black"
            
            coords_dict = self.directions(coords)
            east_coords = coords_dict[self.EAST]
            west_coords = coords_dict[self.WEST]
            north_coords = coords_dict[self.NORTH]
            south_coords = coords_dict[self.SOUTH]
            
            dir_pairs = [[east_coords, west_coords], [north_coords, south_coords]]
            DIR_1 = 0
            DIR_2 = 1
            for dir_pair in dir_pairs:
                if (self.check_cell_valid(dir_pair[DIR_1]) and self.is_enemy(dir_pair[DIR_1], opp_colour) 
                    and self.check_cell_valid(dir_pair[DIR_2]) and self.is_enemy(dir_pair[DIR_2], opp_colour)):
                    if ((self.is_piece_eliminated(coords_eliminated, dir_pair[DIR_1]) is False) and
                        (self.is_piece_eliminated(coords_eliminated, dir_pair[DIR_2]) is False)):   
                        coords_eliminated.append(coords)        

    def elimination(self, new_pos):
        """
            Returns a list of coordinates of pieces eliminated when a piece moves 
            to its new coordinates
            input: new coordinates of a piece
            output: a list of coordinates of pieces to be eliminated (eliminate)
        """
        
        # check if the given piece eliminates any enemy pieces when it moves toward its new coords
        coords_eliminated = []
        self.surround_opponent(new_pos, coords_eliminated)  
        # now we check whether the same piece is eliminated by enemy pieces 
        self.self_surrounded(new_pos, coords_eliminated)
                         
        return coords_eliminated
    
    def possible_moves(self, piece_pos):
        """
         Retrieve all possible moves for a given piece
         input: Coordinates of a piece
         output: a list of possible moves position
        """
        
        #Return the adjacent coordinates in the given direction of the given coordinates
        def neighbouring_coords(direction, coords):
            if direction == self.EAST:
                return (coords[self.X] + 1, coords[self.Y])
            
            elif direction == self.WEST:
                return (coords[self.X] - 1, coords[self.Y])
            
            elif direction == self.NORTH:
                return (coords[self.X], coords[self.Y] - 1)
            
            elif direction == self.SOUTH:
                return (coords[self.X], coords[self.Y] + 1)
            
        possible_moves_position = []
        
        for direction,coords in self.directions(piece_pos).items():
            if self.check_cell_valid(coords, (Cell.CORNER,)):
                if self.get_cell(coords).is_empty():
                    possible_moves_position.append(coords)
                else:
                    #Check if this piece can jump over another piece in the given direction
                    next_coords = neighbouring_coords(direction, coords)
                    if (self.check_cell_valid(next_coords, (Cell.CORNER,)) and 
                        self.get_cell(next_coords).is_empty()):
                        possible_moves_position.append(next_coords)
        
        return possible_moves_position
        
    def board_shrink(self, turns):
        # Make this cell unavailable and terminate any piece on this cell
        def shrink_cell(coords):
            self.get_cell(coords).cell_type = Cell.SHRUNK
            self.get_cell(coords).piece = None
        
        # body
        # when turns are in shrinking turns, then shrink board
        if (turns in (127, 128)):
            first_col = 0
            last_col = self.MAX_COL - 1
            first_row = 0
            last_row = self.MAX_ROW - 1
        else:
            first_col = 1
            last_col = self.MAX_COL - 2
            first_row = 1
            last_row = self.MAX_ROW - 2
        
        # remove leftmost column
        for i in range(self.MAX_ROW):
            coords = (first_col, i)
            shrink_cell(coords)
        
        # remove rightmost column
        for i in range(self.MAX_ROW):
            coords = (last_col, i)
            shrink_cell(coords)
        
        # remove top row
        for i in range(self.MAX_COL):
            coords = (i, first_row)
            shrink_cell(coords)
        
        # remove bottom row
        for i in range(self.MAX_COL):
            coords = (i, last_row)
            shrink_cell(coords)
    
    def corner_elimination(self, turns):
        if (turns in (127, 128)):
                    
            top_left = (1,1)
            top_right = (6, 1)
            bottom_left = (1, 6)
            bottom_right = (6, 6)
        else:
            top_left = (2, 2)
            top_right = (5, 2)
            bottom_left = (2, 5)
            bottom_right = (5, 5)
        
        new_corners = [top_left, bottom_left, bottom_right, top_right]

        for corner in new_corners:
            self.get_cell(corner).piece = None
            self.get_cell(corner).cell_type = Cell.CORNER
            
            for coords in self.directions(corner).values():
                coords_eliminated = []
                if self.check_cell_valid(coords):
                    self.self_surrounded(coords, coords_eliminated)
                    self.remove_pieces(coords_eliminated)
                    
    def debug_board(self):
        list_board = [["-" for x in range(8)] for y in range(8)]

        for i in range(self.MAX_COL):
            for j in range(self.MAX_ROW):
                
                # check shrink
                if (self.board[i][j].cell_type == Cell.SHRUNK):
                    list_board[j][i] = "#"

                # check corner
                if (self.board[i][j].cell_type == Cell.CORNER):
                    list_board[j][i] = "X"
                
                # check white
                if (self.board[i][j].piece is not None):
                    if (self.board[i][j].piece.get_colour() == "white"):
                        list_board[j][i] = "O"
                        
                    # check black
                    if (self.board[i][j].piece.get_colour() == "black"):
                        list_board[j][i] = "@"
            
        print("Debug Board")    
        for y in range(8):
            for z in range(8):
                print(list_board[y][z] + " ", end='')
            print() 
        
    def get_cell(self, coords):
        #print(coords[self.X], coords[self.Y], "\n")
        return self.board[coords[self.X]][coords[self.Y]]
            
    def directions(self, coords):
        """
        Helper function to retrieve all 4 adjacent coords of a coords
        input: coords
        output: dictionary of 4 coords with directions as keys
        """
        east = (coords[self.X] + 1, coords[self.Y])
        west = (coords[self.X] - 1, coords[self.Y])
        north = (coords[self.X], coords[self.Y] - 1)
        south = (coords[self.X], coords[self.Y] + 1)
        return {self.EAST:east, self.WEST:west, self.NORTH:north, self.SOUTH:south}
    
    def check_cell_valid(self, coords, invalid_cell_types=None):
        """
        Check if the cell at these given coordinates is within the playing zone of the board
        and if its type is not one of the given invalid cell types
        input: cell's coordinates and a list of invalid cell types
        output: yes/no; yes means the cell is valid and vice versa
        """
        
        #Check if a coords is within the board, and NOT within the shrunk zone
        def in_board(coords):
            return ((coords[self.X] >= self.MIN_COL and coords[self.X] < self.MAX_COL) and 
                        (coords[self.Y] >= self.MIN_ROW and coords[self.Y] < self.MAX_ROW) and
                        self.get_cell(coords).check_cell_type(Cell.SHRUNK) is False)
        
        #body
        if in_board(coords) is False:
            return False
        
        if invalid_cell_types is not None:
            for cell_type in invalid_cell_types:
                if self.get_cell(coords).check_cell_type(cell_type) is True:
                    return False
                
        return True
    

        
        

