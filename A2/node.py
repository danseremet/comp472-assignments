import copy

class BookeepingInfo:
    def __init__(self, move=None, current_cost=0):
        if move:
            self.tile_moved = move[0]
            self.cost_last_move = move[2]
            self.total_cost = move[2] + current_cost
        else:
            self.tile_moved = None
            self.cost_last_move = 0
            self.total_cost = current_cost
            
    def __repr__(self):
        """BookeepingInfo representation"""
        return "Tile moved = {}, Cost last move = {}, Total cost = {})".format(self.tile_moved, self.cost_last_move, self.total_cost)

    
class Node:
    rows = 0
    cols = 0
    
    def __init__(self, state, parent=None, bookeeping_info=BookeepingInfo()):
        self.state = state
        self.parent = parent
        self.bookeeping_info = bookeeping_info
        self.f = 0
        self.g = 0
        self.h = 0
        
        
    def __eq__(self, other):
        """Compare nodes by their state."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.state == other.state
    
    def __repr__(self):
        """Node representation"""
        return "({})   {}".format(self.get_formatted_state(), self.bookeeping_info)
    
    def get_formatted_state(self):
        return " ".join(self.state)
    
    def get_path_from_root(self):
        """Get nodes from root to current node."""
        if not self.parent:
            return [self]
        return self.parent.get_path_from_root() + [self]
    
    
    def get_successors(self):        
        rows = self.rows
        cols = self.cols
        
        # 0 find index of '0' 
        i_zero = self.state.index('0')
        
        # Move definition:
        # Move (number, index, cost)
        # e.g.
        # (2, 5, 1)
        # invalid move: -1

        
        # 1 find regular moves
        reg_up = -1
        reg_down = -1
        reg_left = -1
        reg_right = -1
        
        # find reg_left
        if i_zero % cols != 0:
            reg_left = (self.state[i_zero - 1], i_zero - 1, 1)
        
        # find reg_right
        if (i_zero + 1) % cols != 0:
            reg_right = (self.state[i_zero + 1], i_zero + 1, 1)
        
        # find reg_up
        if i_zero - cols >= 0:
            reg_up = (self.state[i_zero - cols], i_zero - cols, 1)
        
        # find reg_down
        if i_zero + cols < rows * cols:
            reg_down = (self.state[i_zero + cols], i_zero + cols, 1)
        
        def valid_index(index):
            return index != -1
  
        
        # 2 find wrapping moves
        top_left = 0
        top_right = cols - 1
        bottom_left = cols * (rows - 1)
        bottom_right = (cols * rows) - 1
        wrapping_indices = [top_left, top_right, bottom_left, bottom_right]
        
        wrap_up = -1
        wrap_down = -1
        wrap_left = -1
        wrap_right = -1
        
        if i_zero in wrapping_indices:
            if cols > 2:
                if i_zero % cols == 0:
                    wrap_right = (self.state[i_zero + cols - 1], i_zero + cols - 1, 2)

                if (i_zero + 1) % cols == 0:
                    wrap_left = (self.state[i_zero - cols + 1], i_zero - cols + 1, 2)

            if rows > 2:
                if i_zero in [0, cols - 1]:
                    wrap_down = (self.state[(rows - 1) * cols + i_zero], (rows - 1) * cols + i_zero, 2)
                
                if i_zero in [(rows - 1) * cols, rows * cols - 1]:
                    wrap_up = (self.state[i_zero - (rows - 1) * cols], i_zero - (rows - 1) * cols, 2)

        
        # 3 find diagonal moves

        diag_tl = -1
        diag_tr = -1
        diag_bl = -1
        diag_br = -1
        
        if i_zero == top_left:
            diag_tl = (self.state[bottom_right], bottom_right, 3)
            diag_br = (self.state[cols + 1], cols + 1, 3)
        elif i_zero == top_right:
            diag_tr = (self.state[bottom_left], bottom_left, 3)
            diag_bl = (self.state[top_right + cols - 1], top_right + cols - 1, 3)
        elif i_zero == bottom_left:
            diag_bl = (self.state[top_right], top_right, 3)
            diag_tr = (self.state[bottom_left - cols + 1], bottom_left - cols + 1, 3)
        elif i_zero == bottom_right:
            diag_br = (self.state[top_left], top_left, 3)
            diag_tl = (self.state[bottom_right - cols - 1], bottom_right - cols - 1, 3)

            
        regular_moves = list(filter(valid_index, [reg_up, reg_down, reg_left, reg_right]))
        wrapping_moves = list(filter(valid_index, [wrap_right, wrap_left, wrap_down, wrap_up]))
        diagonal_moves = list(filter(valid_index, [diag_tl, diag_tr, diag_bl, diag_br]))
        
        moves = regular_moves + wrapping_moves + diagonal_moves
        
#         print("Moves:")
#         print(moves)
        
        nodes = []
#         print("Node.state:")
#         print(self.state)
        for move in moves:
            new_state = copy.deepcopy(self.state)
            new_state[i_zero] = move[0]
            new_state[move[1]] = '0'

            new_bookeeping_info = BookeepingInfo(move, self.bookeeping_info.total_cost)
            new_node = Node(new_state, self, new_bookeeping_info)
            nodes.append(new_node)
        
#         print("New States:")
#         print(nodes)
        
        return nodes
    
    
