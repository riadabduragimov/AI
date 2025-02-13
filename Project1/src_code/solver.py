import heapq
import logging
from typing import List, Tuple, Optional
from utils import generate_goal_state, find_blank
from puzzle import NPuzzle

def solve_puzzle(grid: List[List[int]], n: int) -> Optional[List[List[List[int]]]]:
    """Uses A* search to find the optimal solution to the puzzle."""
    puzzle = NPuzzle(grid)
    pq = []
    heapq.heappush(pq, (puzzle.manhattan_distance(), 0, grid, find_blank(grid), []))  
    visited = set()
    logging.info("Starting A* search for solving the puzzle.")

    while pq:
        _, cost, state, blank_pos, path = heapq.heappop(pq)
        state_tuple = tuple(tuple(row) for row in state)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if state == generate_goal_state(n):
            logging.info("Solution found for the puzzle.")
            return path

        for new_state, new_blank in puzzle.get_neighbors(state, blank_pos):
            new_path = path + [new_state]
            puzzle.grid = new_state 
            heapq.heappush(pq, (cost + 1 + puzzle.manhattan_distance(), cost + 1, new_state, new_blank, new_path))

    logging.warning("No solution found for the puzzle.")
    return None 
