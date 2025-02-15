"""
    Author: Riyad Abdurahimov
    Description: This module implements the A* search algorithm to solve the N-Puzzle problem. 
    It provides the `solve_puzzle` function that uses A* search to find the optimal solution, 
    considering the Manhattan distance as the heuristic. The module also includes methods to check 
    if a state is the goal state and calculate the cost for a given state.
"""

import heapq
import logging
from typing import List, Tuple, Optional
from utils import generate_goal_state, find_blank
from puzzle import NPuzzle

def solve_puzzle(grid: List[List[int]], n: int) -> Optional[List[List[List[int]]]]:
    """Uses A* search to find the optimal solution to the puzzle."""
    puzzle = NPuzzle(grid)                                              # Initialize the puzzle with the given grid and puzzle size
    pq = []                                                             # Initialize the priority queue with the start state. 
    heapq.heappush(pq, (puzzle.manhattan_distance(), 0, grid, find_blank(grid), []))  # Push a tuple (f_cost, g_cost, current_state, blank_position, path)
    visited = set()                                                     # Set to track visited states to avoid reprocessing the same state
    logging.info("Starting A* search for solving the puzzle.")
    
    # Main loop of A* search: process each state in the priority queue
    while pq:
        _, cost, state, blank_pos, path = heapq.heappop(pq)         # Pop the state with the lowest f_cost (f = g + h)
        state_tuple = tuple(tuple(row) for row in state)            # Convert the state to an immutable tuple so it can be added to the visited set
        if state_tuple in visited:                                  # If this state has been visited before, skip it
            continue
        
        visited.add(state_tuple)                                    # Mark this state as visited
        if is_goal_state(state, n):                                 # Check if the current state is the goal state
            logging.info("Solution found for the puzzle.")
            return path                                             # Return the solution path

        for new_state, new_blank in puzzle.get_neighbors(state, blank_pos):             # Explore all possible neighbors (valid moves)
            new_path = path + [new_state]                                               # Append the new state to the solution path
            puzzle.grid = new_state                                                     # Update the puzzle state
            new_cost = cost + 1 + puzzle.manhattan_distance()                           # New cost = g_cost + h_cost (Manhattan distance)
            heapq.heappush(pq, (new_cost, cost + 1, new_state, new_blank, new_path))    # Push the new state with its cost, position, and path to the priority queue

    logging.warning("No solution found for the puzzle.")                                # If no solution is found, log the failure
    return None                                                                         # Return None to indicate no solution

def is_goal_state(state: List[List[int]], n: int) -> bool:
    """Checks if the current state is the goal state."""
    
    # Compare the current state with the goal state generated for the puzzle size
    return state == generate_goal_state(n)

def calculate_cost(cost: int, puzzle: NPuzzle) -> int:
    """Calculates the total cost (current cost + heuristic)."""
    
    # The cost is the sum of the current cost (g) and the heuristic (h)
    return cost + 1 + puzzle.manhattan_distance()
