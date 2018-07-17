'''
Created on May 6, 2018

@author: jiangng
'''
from copy import deepcopy
'''
Created on 2 May 2018
@author: xiang
'''
from Cell import Cell
from Board import Board
from platform import dist
from State import State
from copy import deepcopy

class Game:
      
    #def __init__(self, board):
        
    # start with making a minimax function and construct an eval function
    # search for features
    
    INFINITY = 123123123123
    
    
    
    @staticmethod    
    def actions(state):
        list_actions = []
        killer_moves = state.killer_moves
        
        if killer_moves.empty():
            board = state.board
            for i in range(Board.MAX_COL):
                for j in range(Board.MAX_ROW):
                    coords = (i, j)
                    curr_piece = board.get_cell(coords).piece
                    if (curr_piece is not None and curr_piece.get_colour() == state.curr_move_colour):
                        moves = board.possible_moves(coords)
                        for move in moves:
                            list_actions.append((coords, move))
        
        #Not gonna append prev pruned moves for now
        #just append Best_Action objects in killer moves            
        else:
            while not killer_moves.empty():
                list_actions.append(killer_moves.get())
        
        return list_actions
    
    @staticmethod
    def result(state, move):
        """
            return state after apply move 
        """
        new_board = deepcopy(state.board)
        new_board.update(move, state.curr_move_colour)
        curr_turns = state.turns + 1
        
        if curr_turns == (128, 192):
            new_board.board_shrink(curr_turns)
            new_board.corner_elimination(curr_turns)
            
        next_move_colour = "white" if state.curr_move_colour == "black" else "black"
        new_state = State(new_board, state.max_colour, next_move_colour, curr_turns)
        
        return new_state
    
    @staticmethod
    def to_move(state):
        return state.max_colour
    
    @classmethod
    def count_pieces(Game, state):
        board = state.board;
        max_num = 0
        min_num = 0
        
        for i in range(Board.MAX_COL):
            for j in range(Board.MAX_ROW):                            
                if (not board.get_cell((i, j)).is_empty()):
                    # check white
                    if (board.get_cell((i, j)).piece.get_colour() == state.max_colour):
                        max_num += 1
                    # check black
                    else:    
                        min_num += 1
                        
        return max_num, min_num
    
    @classmethod
    def terminal_test(Game, state):
        max_num, min_num = Game.count_pieces(state)
        
        if (max_num < 2 or min_num < 2):
            return True

        return False
    
    @classmethod
    def utility(Game, state):
        max_num, min_num = Game.count_pieces(state)
        
        if (max_num <2 and min_num < 2):
            return 0     
        elif (max_num < 2):
            return -Game.INFINITY
        elif (min_num < 2):
            return Game.INFINITY
        
            
    @staticmethod                        
    def eval_fn(state, w=[1, -1, 1, 1, -1, 0.5]):
        
        def f1(state):
            board = state.board;
            num_f1 = 0;
            for i in range(Board.MAX_COL):
                for j in range(Board.MAX_ROW):
                    curr_cell = board.get_cell((i, j))
                    if (not curr_cell.is_empty()):
                        # check for max player
                        if (curr_cell.piece.get_colour() == state.max_colour):
                            num_f1 += 1
                        # check for min player
                        else:
                            num_f1 -= 1
                            
        
            return num_f1;
        
        def body_f2_or_f3(state, colour):
            
            
            board = state.board
            opp_colour = "black" if colour == "white" else "white"
            
            num_features = 0
            for i in range(Board.MAX_COL):
                for j in range(Board.MAX_ROW):
                    curr_cell = board.get_cell((i, j))
                    # check white
                    if (not curr_cell.is_empty()):
                        if (curr_cell.piece.get_colour() == colour):
                            coord = (i, j)
                            
                            coords_dict = board.directions(coord)
                            east_coords = coords_dict[Board.EAST]
                            west_coords = coords_dict[Board.WEST]
                            north_coords = coords_dict[Board.NORTH]
                            south_coords = coords_dict[Board.SOUTH]
            
                            for direction, coords in coords_dict.items():
                                if (board.check_cell_valid(coords, (Cell.CORNER, Cell.SHRUNK))):
                                    curr_cell = board.get_cell(coords)
                                    if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                                        if (direction == Board.WEST):
                                            check_coords_dict = board.directions(east_coords)
                                            
                                            for direction, coords in check_coords_dict.items():
                                                if (direction != Board.WEST):
                                                    if (board.check_cell_valid(coords, (Cell.CORNER, Cell.SHRUNK))):
                                                        curr_cell = board.get_cell(coords)
                                                        if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                                                            num_features+= 1;
                                                    
                                                
                                        if (direction == Board.EAST):
                                            check_coords_dict = board.directions(west_coords)
                                            
                                            for direction, coords in check_coords_dict.items():
                                                if (direction != Board.EAST):
                                                    if (board.check_cell_valid(coords, (Cell.CORNER, Cell.SHRUNK))):
                                                        curr_cell = board.get_cell(coords)
                                                        if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                                                            num_features+= 1;
                                        
                                        if (direction == Board.NORTH):
                                            check_coords_dict = board.directions(south_coords)
                                            
                                            for direction, coords in check_coords_dict.items():
                                                if (direction != Board.NORTH):
                                                    if (board.check_cell_valid(coords, (Cell.CORNER, Cell.SHRUNK))):
                                                        curr_cell = board.get_cell(coords)
                                                        if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                                                            num_features+= 1;
                                            
                                        if (direction == Board.SOUTH):
                                            check_coords_dict = board.directions(north_coords)
                                            
                                            for direction, coords in check_coords_dict.items():
                                                if (direction != Board.SOUTH):
                                                    if (board.check_cell_valid(coords, (Cell.CORNER, Cell.SHRUNK))):
                                                        curr_cell = board.get_cell(coords)
                                                        if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                                                            num_features+= 1;
            return num_features;
        
        def f2(state):
            """
                offensive position by enemy
            """
            return body_f2_or_f3(state, state.max_colour)
        
        def f3(state):
            """
                offensive position by player
            """
            min_colour = "white" if state.max_colour == "black" else "black"
            return body_f2_or_f3(state, min_colour)
                            
        def body_f4_or_f5(state, colour):
            def manhattan_dist(player_coord, opponent_coord):
                '''
                    Find the manhattan distance between 2 coordinates 
                    input: 2 lists of coordinates
                    output: int
                '''
                
                X = 0
                Y = 1
                
                x_diff = abs(player_coord[X] - opponent_coord[X])
                y_diff = abs(player_coord[Y] - opponent_coord[Y])
                return x_diff + y_diff
            
            def find_closest_opponents(coord, state):
                '''
                    i) Find the closest opponent pieces to this piece according 
                    to their manhattan distances
                    ii) Find the total manhattan distances between the closest 
                    opponent pieces and this piece
                    input: A list of coordinates of a black piece, and the 2 
                            dictionaries of pieces
                    output: void
                '''
                
                MAX_DIST = 20
                CLOSEST = 0
                SECOND_CLOSEST = 1
                board = state.board;
                if (board.get_cell(coord).piece is None):
                    return None
                #if (black_dict[black_id][IS_ALIVE] == DEAD):
                #    return None
                colour = board.get_cell(coord).piece.get_colour()
                opp_colour = "white" if colour == "black" else "black"
                # Contain the ids of the closest and second closest whites
                opp_assigned = [None, None] 
                # Initialise the search for the 2 whites pieces
                closest_dist = MAX_DIST
                second_closest_dist = MAX_DIST
                
                
                for i in range(Board.MAX_COL):
                    for j in range(Board.MAX_ROW):
                        
                        curr_cell = board.get_cell((i, j))
                        if (not curr_cell.is_empty() and curr_cell.piece.get_colour() == opp_colour):
                            dist = manhattan_dist((i, j), coord)
                            if (dist < closest_dist):
                                second_closest_dist = closest_dist
                                opp_assigned[SECOND_CLOSEST] = opp_assigned[CLOSEST]
                                closest_dist = dist
                                opp_assigned[CLOSEST] = board.get_cell((i, j)).piece.piece_id
                            elif ((dist > closest_dist and dist < second_closest_dist) 
                                  or closest_dist == dist):
                                second_closest_dist = dist
                                opp_assigned[SECOND_CLOSEST] = board.get_cell((i, j)).piece.piece_id
                            
                """           
                for (key, white_stats) in white_dict.items():
                    if (white_stats[IS_ALIVE] == DEAD):
                        continue
                    else:
                        dist = manhattan_dist(white_stats[COORD], black_coord)
                        if (dist < closest_dist):
                            second_closest_dict = closest_dist
                            whites_assigned[SECOND] = whites_assigned[CLOSEST_WHITE]
                            closest_dist = dist
                            whites_assigned[CLOSEST_WHITE] = key
                        elif ((closest_dist < dist and dist < second_closest_dict) 
                              or closest_dist == dist):
                            second_closest_dict = dist
                            whites_assigned[SECOND] = key
                            
                black_dict[black_id][WHITES_ASSIGNED] = whites_assigned
                """
                
                
                # Calculate the TOTAL manhattan distances if 2 closest whites are found        
                if (bool(opp_assigned[CLOSEST]) and bool(opp_assigned[SECOND_CLOSEST])):
                    total_dist = closest_dist + second_closest_dist
                    
                # Take the single manhanttan distance if there's only 1 white piece on
                # board
                elif (bool(opp_assigned[CLOSEST])):
                    total_dist = closest_dist
                # No white pieces on board at all
                else:
                    total_dist = None
            
                return total_dist
            
            num_feature = 0
            board = state.board
            
            for i in range(Board.MAX_COL):
                for j in range(Board.MAX_ROW):
                    if (not board.get_cell((i, j)).is_empty()):
                        if (board.get_cell((i, j)).piece.get_colour() == colour):
                            if (find_closest_opponents((i, j), state) is not None and
                                find_closest_opponents((i, j), state) <= 4):
                                num_feature += 1;
            return num_feature
        
        def f4(state):
            """
                <=4 manhattan distance for player towards enemy
            """
            opponent_colour = "white" if state.max_colour == "black" else "black"
            return body_f4_or_f5(state, opponent_colour)
        
        def f5(state):
            """
                <=4 manhattan distance for player towards enemy
            """
            return body_f4_or_f5(state, state.max_colour)
        
        def f6(state):
    
            first_col = 2
            last_col = Board.MAX_COL - 3
            first_row = 2
            last_row = Board.MAX_ROW - 3
            
            board = state.board
            colour = state.max_colour
            num_feature = 0
                    
            """
            compare the number of player pieces within the 2nd shrinking board to the outermost of the board
            """
            
            for i in range(Board.MAX_COL):
                for j in range(Board.MAX_COL):
                    coords = (i, j)
                    if (not board.get_cell(coords).is_empty() and 
                        board.get_cell(coords).piece.get_colour() == colour):
                        if ((i < first_row and i > last_row) and (j < first_col and j > last_col)):
                            num_feature -= 2
                             
                        elif ((i >= first_row and i <= last_row) and (j >= first_col and j <= last_col)):
                            num_feature += 1
            
            return num_feature
        
        w = [5, -2, 1, 1, -2, 0.5]    
        w1 = w[0]
        w2 = w[1]
        w3 = w[2]
        w4 = w[3]
        w5 = w[4]
        w6 = w[5]
        result = (w1 * f1(state) + w2 * f2(state) + 
            w3 * f3(state) + w4 * f4(state) + 
            w5 * f5(state) + w6 * f6(state))
        """
        print("f1 = ", f1(state))
        print("f2 = ", f2(state))
        print("f3 = ", f3(state))
        print("f4 = ", f4(state))
        print("f5 = ", f5(state))
        print("eval_fn result: ", result)
        """
        #print("f6 = ", f6(state))
        if (result == None): result = 5
        return result
