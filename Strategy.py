'''
Created on May 4, 2018

@author: jiangng
'''
from copy import deepcopy
from Piece import Piece
from Board import Board
from Cell import Cell
from State import State

class Strategy:
    INFINITY = 123123123123
    num = 0
    
    @classmethod
    def alphabeta_cutoff_search(self, state, game, eval_fn, d=1, cutoff_test=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""
    
        
    
        # Functions used by alphabeta
        def max_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                #state.board.debug_board()
                self.num += 1
                return eval_fn(state)
            v = -self.INFINITY
            for a in game.actions(state):
              
              
                v = max(v, min_value(game.result(state, a),
                                     alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
    
        def min_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                #state.board.debug_board()
                self.num += 1
                return eval_fn(state)
            v = self.INFINITY
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a),
                                     alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
    
        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        # Self note: cutoff_test can have diff. implementation hence has a parameter
        cutoff_test = (cutoff_test or
                       (lambda state, depth: depth > d or
                        game.terminal_test(state)))
        #eval_fn = eval_fn or (lambda state: game.utility(state))
        best_score = -self.INFINITY
        beta = self.INFINITY
        best_action = None
        for a in game.actions(state):
            v = min_value(game.result(state, a), best_score, beta, 1)
            """
            list_best_score = 
            list_best_action = 
            best_action = b
            
            new_state = game.result(state, b)
            
            for (a in game.actions(new_state):
                
            
            """
            if v > best_score:
                best_score = v
                best_action = a
                
        #print(self.num)
        #print(game.result(state, best_action).board.debug_board())
        #print("best score = ", best_score)
        return best_action
        
    @staticmethod
    def cell_valid_empty(state, coord):
        board = state.board
        return board.check_cell_valid(coord, (Cell.CORNER, Cell.OFF_ZONE)) and board.get_cell(coord).is_empty()
    
    @staticmethod
    def cell_valid_not_empty(state, coord):
        board = state.board
        return board.check_cell_valid(coord, (Cell.CORNER, Cell.OFF_ZONE)) and not board.get_cell(coord).is_empty()
    
    @classmethod
    def defend_strategy(Strategy, state, coord):
        """
            check the piece at that coord and check strategy
        """
        # check whether cell is valid and not empty
        board = state.board
        if (not board.get_cell(coord).is_empty()):
            
            coord_colour = board.get_cell(coord).piece.get_colour()
        else:
            return None
       
        colour = state.max_colour
        

        if (coord_colour == colour):
            # check whether piece will be eliminated
            if (Strategy.enemy_adjacent(state, coord) is not None):
            
                # if they will be eliminated, check whether we can eliminate the enemy instead
                enemy_dir = Strategy.enemy_adjacent(state, coord)[0]
                #print("enemy_dir:", enemy_dir)
                enemy_coord = Strategy.enemy_adjacent(state, coord)[1]
                #print("enemy coord1: ", enemy_coord)
                
                coords_dict = board.directions(enemy_coord)
                east_coords = coords_dict[Board.EAST]
                west_coords = coords_dict[Board.WEST]
                north_coords = coords_dict[Board.NORTH]
                south_coords = coords_dict[Board.SOUTH] 
                
                if (enemy_dir == Board.WEST):
                    ally_coord = west_coords
                if (enemy_dir == Board.EAST):
                    ally_coord = east_coords
                if (enemy_dir == Board.SOUTH):
                    ally_coord = south_coords
                if (enemy_dir == Board.NORTH):
                    ally_coord = north_coords
                    
                if (Strategy.cell_valid_empty(state, ally_coord)):
                        
                    # if they can in turn eliminate the enemy, will they be eliminated in the process?
                   
                    #print("ally_coord1 = ", ally_coord)
                    check_board = deepcopy(board)
                    check_board.place(ally_coord, colour)
                    coords_eliminated = []
                    check_board.self_surrounded(ally_coord, coords_eliminated)
                    
                    if (not bool(coords_eliminated)):
                        #print("ally_coord2 = ", ally_coord)
                        return ally_coord
                            
                # if i can't eliminate the enemy in return, then protect ally backside
                else:
                    return Strategy.protect_ally(state, coord)
            
                
                
                
        return None
    
    @classmethod        
    def enemy_adjacent(Strategy, state, coord):
        board = state.board
        colour = board.get_cell(coord).piece.get_colour()
        oppo_colour = "white" if colour == "black" else "black"
        coords_dict = board.directions(coord)
        east_coords = coords_dict[Board.EAST]
        west_coords = coords_dict[Board.WEST]
        north_coords = coords_dict[Board.NORTH]
        south_coords = coords_dict[Board.SOUTH]
        
        
        if (Strategy.cell_valid_not_empty(state, east_coords) and board.is_enemy(east_coords, oppo_colour)):
            return (Board.EAST, east_coords)
        
        if (Strategy.cell_valid_not_empty(state, west_coords) and board.is_enemy(west_coords, oppo_colour)):
            return (Board.WEST, west_coords)
        
        if (Strategy.cell_valid_not_empty(state, south_coords) and board.is_enemy(south_coords, oppo_colour)):
            return (Board.SOUTH, south_coords)
        
        if (Strategy.cell_valid_not_empty(state, north_coords) and board.is_enemy(north_coords, oppo_colour)):
            return (Board.NORTH, north_coords)
        
        return None
    
    
    
    @classmethod
    def protect_ally(Strategy, state, coord):
        board = state.board
        colour = board.get_cell(coord).piece.get_colour()
        oppo_colour = "white" if colour == "black" else "black"
        coords_dict = board.directions(coord)
        east_coords = coords_dict[Board.EAST]
        west_coords = coords_dict[Board.WEST]
        north_coords = coords_dict[Board.NORTH]
        south_coords = coords_dict[Board.SOUTH]
        
        if (Strategy.cell_valid_empty(state, west_coords) and 
            (Strategy.cell_valid_not_empty(state, east_coords) and board.is_enemy(east_coords, oppo_colour))):
            return west_coords
        elif (Strategy.cell_valid_empty(state, east_coords) and 
            (Strategy.cell_valid_not_empty(state, west_coords) and board.is_enemy(west_coords, oppo_colour))):
            return east_coords
        elif (Strategy.cell_valid_empty(state, north_coords) and 
            (Strategy.cell_valid_not_empty(state, south_coords) and board.is_enemy(south_coords, oppo_colour))):
            return north_coords
        elif (Strategy.cell_valid_empty(state, south_coords) and
            (Strategy.cell_valid_not_empty(state, north_coords) and board.is_enemy(north_coords, oppo_colour))):
            return south_coords
        
        return None
    
    @classmethod
    def placing_def(Strategy, state):
        
        """
            calculate strategy and then return action
        """
        
        colour = state.max_colour
        board = state.board
        
        # First, check all player pieces whether enemy eliminates ally
        
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):
                coord = (i, j)
                if (not board.get_cell(coord).is_empty()):
                    
                    if (board.get_cell(coord).piece.get_colour() == colour):
                        if (Strategy.defend_strategy(state, coord) is not None):
                            return Strategy.defend_strategy(state, coord)
            
                """
                if (bool(board.enemy_place)):
                    enemy_place = board.enemy_place
                    
                    coords_dict = board.directions(enemy_place)
                    for coord in coords_dict.values():
                        if (Strategy.cell_valid_not_empty(state, coord)):
                            if (Strategy.defend_strategy(state, coord) is not None):
                                return Strategy.defend_strategy(state, coord)
                """
        """
        # first, check all pieces whether can attack or need defend
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):
                if (self.board[i][j].piece is not None):
                        if (self.board[i][j].piece.get_colour() == colour):
                        # check existing player pieces whether they will be eliminated
                        coord = (i, j)
                        if (enemy_adjacent(state, coord) is not None):
                            # if they will be eliminated, check whether we can eliminate the enemy instead
                            enemy_coord = enemy_adjacent(state, coord)
                            if (enemy_adjacent(state, enemy_coord) is not None):
                                # if they can in turn eliminate the enemy, will they be eliminated in the process?
                                ally_coord = enemy_adjacent(state, enemy_coord)
                                if (enemy_adjacent(state, ally_coord) is not None):
                                    continue
                                
                                else:
                                    return ally_coord
                            # if i can't eliminate the enemy in return, then protect ally backside
                            else:
                                return protect_ally(state, coord)
        """
        
        
                            
        # Second, try to place a piece along the border of enemy off-zone
        # at the middle 4 pieces
        border_row = 2 if (colour == "white") else 5
        
        for x in (3, 4, 2, 5):
            coord = (x, border_row)
            if (Strategy.cell_valid_empty(state, coord)):
                
                check_board = deepcopy(board)
                check_board.place(coord, colour)
                coords_eliminated = []
                check_board.self_surrounded(coord, coords_eliminated)
                # place piece in proxy cell then test strategy
                if (not bool(coords_eliminated)):
                    return coord
                
                    
                    
                    
                    
        # Third, try to place adjacent to existing pieces
        risky_piece = []
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):
                if (not board.get_cell((i, j)).is_empty()):
                    if (board.get_cell((i, j)).piece.get_colour() == state.max_colour):
                        coords = (i, j)
                        adjacent_cell = board.directions(coords)
                        
                        for coord in adjacent_cell.values():
                            if (Strategy.cell_valid_empty(state, coord) == True):
                                
                                check_board = deepcopy(board)
                                check_board.place(coord, colour)
                                coords_eliminated = []
                                check_board.self_surrounded(coord, coords_eliminated)
                                
                                if (not bool(coords_eliminated)):
                                    
                                    check_state = State(check_board, state.max_colour, state.curr_move_colour)
                                    if (Strategy.enemy_adjacent(check_state, coord) is not None):
                                        risky_piece.append(coord)
                                        
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):
                if (not board.get_cell((i, j)).is_empty()):
                    if (board.get_cell((i, j)).piece.get_colour() == state.max_colour):
                        coords = (i, j)
                        adjacent_cell = board.directions(coords)
                        
                        for coord in adjacent_cell.values():
                            if (Strategy.cell_valid_empty(state, coord) == True):
                                
                                check_board = deepcopy(board)
                                check_board.place(coord, colour)
                                coords_eliminated = []
                                check_board.self_surrounded(coord, coords_eliminated)
                                
                                if (not bool(coords_eliminated) and coord not in risky_piece):
                                    #print("coord3 = ", coord)
                                    return coord
                
        # Forth, try to place along wall
        for i in range(Board.MAX_COL):
            for j in (0, 7):
                coords = (i, j)
                if (Strategy.cell_valid_empty(state, coord)):
                    check_board = deepcopy(board)
                    check_board.place(coord, colour)
                    coords_eliminated = []
                    check_board.self_surrounded(coord, coords_eliminated)
                    if (not bool(coords_eliminated)):
                        #print("coord4 = ", coord)
                        return coord
                    
        # Lastly, place randomly
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):
                
                coords = (i, j)
                if (Strategy.cell_valid_empty(state, coord)):
                    check_board = deepcopy(board)
                    check_board.place(coord, colour)
                    coords_eliminated = []
                    check_board.self_surrounded(coord, coords_eliminated)
                    if (not bool(coords_eliminated)):
                        #print("coord5 = ", coord)
                        return coord
        
          
        return None    
