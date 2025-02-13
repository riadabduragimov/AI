from typing import List, Tuple
import logging

def generate_goal_state(n: int) -> List[List[int]]:
    """Generates the goal state for the puzzle."""
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    logging.debug(f"Goal state generated: {goal_state}")
    return goal_state

def find_blank(grid: List[List[int]]) -> Tuple[int, int]:
    """Finds the position of the blank tile (0)."""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                logging.debug(f"Found blank space at position: ({i}, {j})")
                return i, j
    raise ValueError("No blank space (0) found in the grid.")
