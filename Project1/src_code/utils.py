"""
    Author: Riyad Abdurahimov
    Description: This module contains utility functions for the N-Puzzle solver. It includes the 
    `generate_goal_state` function to generate the goal state for any given puzzle size and the 
    `find_blank` function to locate the position of the blank tile (represented by 0) in the puzzle grid.
"""

from typing import List, Tuple
import logging

def generate_goal_state(n: int) -> List[List[int]]:
    """Generates the goal state for the puzzle."""
    
    # Generate a goal state in a row-major order (numbers 1 to n*n-1, with 0 at the end)
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    logging.debug(f"Goal state generated: {goal_state}")
    return goal_state

def find_blank(grid: List[List[int]]) -> Tuple[int, int]:
    """Finds the position of the blank tile (0)."""
    # Iterate through the grid to find the location of the blank tile (represented by 0)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                logging.debug(f"Found blank space at position: ({i}, {j})")
                return i, j  # Return the row and column indices of the blank tile
    
    # Raise an error if no blank tile is found in the grid
    raise ValueError("No blank space (0) found in the grid.")
