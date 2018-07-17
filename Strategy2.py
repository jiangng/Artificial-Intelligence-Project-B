'''
Created on May 9, 2018

@author: jiangng
'''

class Strategy2:
    INFINITY = 123123123123
    
    @classmethod
    def iterative_deepening_search(Strategy2, state, game, eval_fn, depth, cutoff_test=None):

        for d in range(1, depth + 1):
            best_action = Strategy2.alphabeta_cutoff_search(state, game, eval_fn, d)  #, cutoff_test)

        return best_action
    
    @classmethod
    def alphabeta_cutoff_search(Strategy2, state, game, eval_fn, d, cutoff_test=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""
        # Functions used by alphabeta
        def max_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            elif game.terminal_test(state):
                return game.utility(state)
            
            best_score = -Strategy2.INFINITY
            for a in game.actions(state):
                #action has not been explored; not from killer_moves
                if type(a) is tuple:
                    curr_state = game.result(state, a)
                    action_val = min_value(curr_state, alpha, beta, depth + 1)
                    #Store actions sorted by the eval score in descending order
                    state.keep_result_state(curr_state, a, action_val)  
                
                #Best_action object from killer_moves
                else:
                    curr_state = a.state
                    curr_action = a.action
                    action_val = min_value(curr_state, alpha, beta, depth + 1)
                    #Store actions sorted by the eval score in descending order
                    state.keep_result_state(curr_state, curr_action, action_val)
                
                best_score = max(best_score, action_val)
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)
                    
            return best_score
    
        def min_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            elif game.terminal_test(state):
                return game.utility(state)
            
            best_score = Strategy2.INFINITY
            for a in game.actions(state):
                #action has not been explored; not from killer_moves
                if type(a) is tuple:
                    curr_state = game.result(state, a)
                    action_val = max_value(curr_state, alpha, beta, depth + 1)
                    #Store actions sorted by the eval score in descending order
                    state.keep_result_state(curr_state, a, action_val)  
                
                #Best_action object from killer_moves
                else:
                    curr_state = a.state
                    curr_action = a.action
                    action_val = max_value(curr_state, alpha, beta, depth + 1)
                    #Store actions sorted by the eval score in descending order
                    state.keep_result_state(curr_state, curr_action, action_val)
                
                best_score = min(best_score, action_val)
                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)                     
        
            return best_score
    
        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        # Self note: cutoff_test can have diff. implementation hence has a parameter
        cutoff_test = (cutoff_test or
                       (lambda state, depth: depth >= d))
        #Self note: Changed the cutoff comparator from "greater" to "ge"; makes more sense
        best_score = -Strategy2.INFINITY
        beta = Strategy2.INFINITY
        best_action = None  
        
        for a in game.actions(state):
            #action has not been explored; not from killer_moves
            if type(a) is tuple:
                curr_state = game.result(state, a)
                action_val = min_value(curr_state, best_score, beta, 1)
                #Store actions sorted by the eval score in descending order
                state.keep_result_state(curr_state, a, action_val)
                
                if action_val > best_score:
                    best_score = action_val
                    best_action = a
            
            #Best_action object from killer_moves
            else:
                curr_state = a.state
                curr_action = a.action
                action_val = min_value(curr_state, best_score, beta, 1)
                #Store actions sorted by the eval score in descending order
                state.keep_result_state(curr_state, curr_action, action_val)
                
                if action_val > best_score:
                    best_score = action_val
                    best_action = curr_action
            
        return best_action
   
