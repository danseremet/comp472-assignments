# Assignment 2
# Team: Unlimited
# Dan Seremet
# Joey Abou Chaker

import os
import numpy as np

from datetime import datetime
import time
from puzzles_reader import PuzzlesReader
from puzzles_writer import PuzzlesWriter
from node import Node, BookeepingInfo

# Global state
rows = 2
cols = 4
Node.rows = rows
Node.cols = cols
goal_states = None

def print_list(lst):
    for element in lst:
            print(element)


def get_solution_output(solution, solution_time):
    if not solution:
        return "no solution"
    
    path = solution.get_path_from_root()
    output_lines = []
    for node in path:
        formatted_state = node.get_formatted_state()
        
        tile_moved = node.bookeeping_info.tile_moved
        tile_moved = tile_moved if tile_moved is not None else 0
        cost_last_move = node.bookeeping_info.cost_last_move
        
        output_line = "{} {} {}".format(tile_moved, cost_last_move, formatted_state)
        output_lines.append(output_line)
        
    output = "\n".join(output_lines)
    output += "\n{} {}".format(path[-1].bookeeping_info.total_cost, solution_time)
    return output
    
    
    
def get_search_output(closed_list):
    if not closed_list:
        return "no solution"
    
    output_lines = []
    for node in closed_list:
        formatted_state = node.get_formatted_state()
        
        f = node.f
        g = node.g
        h = node.h
        
        output_line = "{} {} {} {}".format(f, g, h, formatted_state)
        output_lines.append(output_line)
        
    output = "\n".join(output_lines)
    
    
    return output
    

    
def generate_goal_states(rows, cols):
    g1 = np.arange(1, rows * cols + 1).reshape(rows, cols)
    g1[-1][-1] = 0
    g1 = np.array(g1)
    g1 = np.vectorize(str)(g1)
    g1 = g1.reshape(1, rows * cols)
    g1 = list(g1[0])
    
    g2 = np.arange(1, rows * cols + 1).reshape(rows, cols, order='F')
    g2[-1][-1] = 0
    g2 = np.array(g2)
    g2 = np.vectorize(str)(g2)
    g2 = g2.reshape(1, rows * cols)
    g2 = list(g2[0])

    return [g1, g2]

    
def get_time_diff(time_start):
    return round((datetime.now() - time_start).total_seconds(), 3)


def generic_search_algo(start_node, algo, max_time=10):
    global goal_states
    global rows
    global cols
    goal_states = generate_goal_states(rows, cols)
    print("goal_states:")
    print_list(goal_states)
    
    # The beginning of searching. (START COUNTER)
    time_start = datetime.now()
    
    open_list = [start_node]
    closed_list = []
    
    solution_time = get_time_diff(time_start)
    
    while get_time_diff(time_start) < max_time:
        
        if not open_list:
            print("Open List is empty.")
            # exit with failure
            break 
        
        s = open_list.pop(0)
        closed_list.append(s)
        
        if s.state in goal_states:
            print("Final State: {}".format(s.state))
            # End of search. (STOP COUNTER)
            return (s, get_time_diff(time_start), closed_list)    
        
        successors = s.get_successors()
        for new_node in successors:
            if new_node not in open_list:
                open_list.append(new_node)

#         print("current_node: {}".format(s.state))
        algo.execute(s, open_list, closed_list)
        
        
    return (None, None, None)


class UCSAlgorithm:   
    def execute(self, node, open_list, closed_list):
        def sort_by_cost(n):
            n.g = n.bookeeping_info.total_cost
            return n.g
        
        open_list.sort(key=sort_by_cost)

        
class GBFSAlgorithm:
    def __init__(self, h):
        self.h = h
    
    def f(self, node):
        h_n = self.h(node) # estimate
        node.h = h_n
        
        return h_n
    
    def execute(self, node, open_list, closed_list):
        open_list.sort(key=self.f)


class AStarAlgorithm:
    def __init__(self, h):
        self.h = h
        
    def f(self, node):
        g_n = node.bookeeping_info.total_cost  # cost
        node.g = g_n
        
        h_n = self.h(node) # estimate
        node.h = h_n
        
        f_n = g_n + h_n # cost + estimate
        node.f = f_n
        
        return f_n
        
    def execute(self, node, open_list, closed_list):
        open_list.sort(key=self.f)
        
    
def h0(node):
    """Heuristic # 0 - Default heuristic for demo."""
    return 0 if node.state[-1] == '0' else 1

def h1(node):
    """Heuristic # 1 - Manhattan distance between node and 2 goal states."""
    global goal_states
    global rows
    global cols

    current_state = np.array(node.state).reshape(rows, cols)
    
    h_cost = [0, 0]
    
    for goal_i, goal_state in enumerate(goal_states):
        
        goal = np.array(goal_state).reshape(rows, cols)
        
        manh_dist = 0
        for i, row in enumerate(goal):
            for j, col in enumerate(row): # i, j goal indices
                indices = np.where(current_state == goal[i][j])
                x, y = indices[0][0], indices[1][0] # x, y current indices
                diff = abs(i - x) + abs(j - y) 
                manh_dist += diff
                
        h_cost[goal_i] = manh_dist

#     print("h_cost = {}".format(min(h_cost[0], h_cost[1])))
    return min(h_cost[0], h_cost[1])
    
    
def h2(node):
    """Heuristic # 2 - Count number of out of place values."""
    global goal_states
    global rows
    global cols
    
    current_state = np.array(node.state).reshape(rows, cols)
    
    h_cost = [0, 0]
    
    for goal_i, goal_state in enumerate(goal_states):
        goal = np.array(goal_state).reshape(rows, cols)
        h_cost[goal_i] = np.size(goal) - np.count_nonzero(current_state == goal)

#     print("h_cost = {}".format(min(h_cost[0], h_cost[1])))
    return min(h_cost[0], h_cost[1])

    

ucs = UCSAlgorithm()
gbfs0 = GBFSAlgorithm(h0)
gbfs1 = GBFSAlgorithm(h1)
gbfs2 = GBFSAlgorithm(h2)
astar0 = AStarAlgorithm(h0)
astar1 = AStarAlgorithm(h1)
astar2 = AStarAlgorithm(h2)


algo_names = ["ucs", "gbfs-h1", "gbfs-h2", "astar-h1", "astar-h2"]
algos = [ucs, gbfs1, gbfs2, astar1, astar2]


# --- DEMO
puzzles = PuzzlesReader("samplePuzzles.txt").puzzles
nodes = list(map(Node, puzzles))

# --- SCALE UP ---------------------- uncomment to run
# puzzles1 = PuzzlesReader("random_5_2x4_puzzles.txt").puzzles
# puzzles2 = PuzzlesReader("random_5_3x4_puzzles.txt").puzzles
# puzzles3 = PuzzlesReader("random_5_4x4_puzzles.txt").puzzles
# nodes1 = list(map(Node, puzzles1))
# nodes2 = list(map(Node, puzzles2))
# nodes3 = list(map(Node, puzzles3))

# # 2x4
# print("2x4")
# for puzzle_number, node in enumerate(nodes1):
#     solution, solution_time, closed_list = generic_search_algo(node, astar1, max_time=5)
#     solution_output = get_solution_output(solution, solution_time)        
#     print(solution_output)
# # 3x4
# rows = 3
# cols = 4
# Node.rows = rows
# Node.cols = cols
# print("3x4")
# for puzzle_number, node in enumerate(nodes2):
#     solution, solution_time, closed_list = generic_search_algo(node, astar1, max_time=60)
#     solution_output = get_solution_output(solution, solution_time)        
#     print(solution_output)
# # 4x4
# rows = 4
# cols = 4
# Node.rows = rows
# Node.cols = cols
# print("4x4")
# for puzzle_number, node in enumerate(nodes3):
#     solution, solution_time, closed_list = generic_search_algo(node, astar1, max_time=60)
#     solution_output = get_solution_output(solution, solution_time)        
#     print(solution_output)
# ----------------------------------

# # 50 Random puzzles -------------- uncomment to run
# puzzles = PuzzlesReader("random_50_puzzles.txt").puzzles
# nodes = list(map(Node, puzzles))
# # nodes = [nodes[0], nodes[1]]
# # print_list(nodes)

total_solution_length = [0, 0, 0, 0, 0]    # 1.
average_solution_length = [0, 0, 0, 0, 0]  # 1.

total_search_length = [0, 0, 0, 0, 0]      # 1.
average_search_length = [0, 0, 0, 0, 0]    # 1.

total_no_solution_count = [0, 0, 0, 0, 0]  # 2.
average_no_solution_count = [0, 0, 0, 0, 0]# 2.

total_cost = [0, 0, 0, 0, 0]               # 3.
average_total_cost = [0, 0, 0, 0, 0]       # 3.

total_execution_time = [0, 0, 0, 0, 0]     # 3.
average_total_execution_time = [0, 0, 0, 0, 0] # 3.

for puzzle_number, node in enumerate(nodes):
    
    for algo_index, algo in enumerate(algos):
        
        print("#{} Algo Running: {}".format(puzzle_number, algo_names[algo_index]))
        solution, solution_time, closed_list = generic_search_algo(node, algo)
        solution_output = get_solution_output(solution, solution_time)        
        search_output = get_search_output(closed_list)
        print(solution_output)
        print(search_output)
        PuzzlesWriter(puzzle_number, algo_names[algo_index], solution_output, search_output)
        
        # Analysis ---
        total_solution_length[algo_index] += len(solution_output.split("\n")) - 1
        total_search_length[algo_index] += len(search_output.split("\n"))
        
        no_solution_count = 0
        if solution_output == "no solution":
            total_no_solution_count[algo_index] += 1
        else:
            total_cost[algo_index] += int(solution_output.split("\n")[-1].split(" ")[0])
            total_execution_time[algo_index] += solution_time
        
        

n_nodes = len(nodes)
    
analysis = """
-------- ANALYSIS --------
Algo name: {}
1. 
Total Length of Solution Path:\t\t{}
Average Length of Solution Path:\t{}

Total Length of Search Path:\t\t{}
Average Length of Search Path:\t\t{}

2.
Total number of "no solution":\t\t{}
Average number of "no solution":\t{}

3.
Total Cost:\t\t\t\t{}
Average Total Cost:\t\t\t{}
Total Execution Time:\t\t\t{}
Average Execution Time:\t\t\t{}
"""

for i in range(5): # for each algo
    average_solution_length[i] = total_solution_length[i] / n_nodes
    average_search_length[i] = total_search_length[i] / n_nodes
    average_no_solution_count[i] = total_no_solution_count[i] / n_nodes
    average_total_cost[i] = total_cost[i] / n_nodes
    average_total_execution_time[i] = total_execution_time[i] / n_nodes
    
    print(analysis.format(
        algo_names[i], 
        total_solution_length[i], 
        average_solution_length[i], 
        total_search_length[i], 
        average_search_length[i], 
        total_no_solution_count[i], 
        average_no_solution_count[i], 
        total_cost[i], 
        average_total_cost[i], 
        total_execution_time[i], 
        average_total_execution_time[i]
    ))
        

