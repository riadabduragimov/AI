"""
    Author: Riyad Abdurahimov
    Description: This module defines the NPuzzle class which represents the N-Puzzle problem. 
    It provides methods to validate the grid, check solvability, generate neighbors, and calculate 
    the Manhattan distance for the puzzle. The class also helps in managing the puzzle's state and 
    solving process.
"""

import logging
from typing import List, Tuple
from utils import generate_goal_state, find_blank

class NPuzzle:
    """Represents the N-Puzzle problem. Provides methods to check solvability, generate neighbors, and calculate Manhattan distance."""

    def __init__(self, grid: List[List[int]]):
        """Initializes the N-Puzzle with a given grid and ensures it's a valid configuration."""
        self.grid = grid                        # The puzzle grid
        self.n = len(grid)                      # Grid size (n x n)

        self._validate_grid_size()              # Validate grid size (must be between 3x3 and 6x6)
        self._validate_grid_elements(grid)      # Validate grid elements (must be correct integers and unique)

        self.goal = generate_goal_state(self.n) # Generate the goal state for comparison
        self.blank_pos = find_blank(self.grid)  # Find the position of the blank space (0)

        logging.debug(f"Initialized NPuzzle with grid: {grid}")
    
    def _validate_grid_size(self):
        """Validates that the grid size is between 3x3 and 6x6."""
        if not (3 <= self.n <= 6):
            raise ValueError(f"Invalid grid size: {self.n}x{self.n}. Grid must be square and between 3x3 and 6x6.")
        if any(len(row) != self.n for row in self.grid):
            raise ValueError("All rows in the grid must have the same length as the number of columns.")

    def _validate_grid_elements(self, grid: List[List[int]]):
        """Validates that the grid contains the correct elements (numbers from 0 to n^2-1)."""
        flat_grid = [num for row in grid for num in row]                   # Flatten the grid into a single list
        if len(flat_grid) != self.n * self.n:
            raise ValueError(f"Grid must contain exactly {self.n * self.n} elements, but found {len(flat_grid)}.")
        if sorted(flat_grid) != list(range(self.n * self.n)):
            raise ValueError(f"Grid must contain all numbers from 0 to {self.n * self.n - 1} exactly once.")

    def is_solvable(self) -> bool:
        """Checks if the puzzle is solvable based on the inversion count and the row of the blank space."""
        flat_list = [num for row in self.grid for num in row if num != 0]  # Flatten grid excluding the blank space (0)
        # Count inversions
        inv_count = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])  
        blank_row = self.blank_pos[0]                                      # Row position of the blank space
        
        # If grid size is odd, solvability depends on inversion count
        if self.n % 2 == 1:
            return inv_count % 2 == 0
        # If grid size is even, solvability depends on both inversion count and blank space row position
        return (inv_count + blank_row) % 2 == 1

    def get_neighbors(self, state: List[List[int]], blank_pos: Tuple[int, int]) -> List[Tuple[List[List[int]], Tuple[int, int]]]:
        """Generates all possible next moves (neighbors) from the current state."""
        x, y = blank_pos                            # Coordinates of the blank space
        neighbors = []                              # List to store the neighboring states
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible moves for the blank space (up, down, left, right)
        
        # Try all possible moves
        for dx, dy in moves:
            nx, ny = x + dx, y + dy                                                      # New coordinates after the move
            if 0 <= nx < self.n and 0 <= ny < self.n:                                    # Check if the move is within bounds
                new_state = [row[:] for row in state]                                    # Create a copy of the current state
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]  # Swap the blank space with the adjacent tile
                neighbors.append((new_state, (nx, ny)))                                  # Add the new state and blank position to neighbors
        
        return neighbors

    def _calculate_tile_distance(self, val: int, i: int, j: int) -> int:
        """Calculates the Manhattan distance for a single tile, given its value and position."""
        goal_x = (val - 1) // self.n                                        # Row of the tile in the goal state
        goal_y = (val - 1) % self.n                                         # Column of the tile in the goal state
        return abs(goal_x - i) + abs(goal_y - j)                            # Manhattan distance: sum of row and column differences

    def manhattan_distance(self) -> int:
        """Computes the Manhattan distance heuristic for the current grid."""
        distance = 0
        # Iterate over each tile in the grid
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val != 0:                                              # Skip the blank space
                    distance += self._calculate_tile_distance(val, i, j)  # Add the distance for each non-blank tile
        logging.debug(f"Manhattan distance for current grid: {distance}")
        return distance
