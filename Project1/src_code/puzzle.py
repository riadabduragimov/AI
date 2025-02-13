import logging
from typing import List, Tuple
from utils import generate_goal_state, find_blank

class NPuzzle:
    def __init__(self, grid: List[List[int]]):
        """Initializes the N-Puzzle with a given grid and ensures it's a valid configuration."""
        
        self.n = len(grid)  

        if not (3 <= self.n <= 6):
            raise ValueError(f"Invalid grid size: {self.n}x{self.n}. Grid must be square and between 3x3 and 6x6.")
        
        if any(len(row) != self.n for row in grid):
            raise ValueError("All rows in the grid must have the same length as the number of columns.")
        
        flat_grid = [num for row in grid for num in row]

        if len(flat_grid) != self.n * self.n:
            raise ValueError(f"Grid must contain exactly {self.n * self.n} elements, but found {len(flat_grid)}.")
        
        if sorted(flat_grid) != list(range(self.n * self.n)):
            raise ValueError(f"Grid must contain all numbers from 0 to {self.n * self.n - 1} exactly once.")

        self.grid = grid
        self.goal = generate_goal_state(self.n)  
        self.blank_pos = find_blank(self.grid)  
        logging.debug(f"Initialized NPuzzle with grid: {grid}")

    def is_solvable(self) -> bool:
        """Checks if the puzzle is solvable based on the inversion count."""
        flat_list = [num for row in self.grid for num in row if num != 0]
        inv_count = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
        blank_row = self.blank_pos[0]
        
        if self.n % 2 == 1:
            return inv_count % 2 == 0
        return (inv_count + blank_row) % 2 == 1

    def get_neighbors(self, state: List[List[int]], blank_pos: Tuple[int, int]) -> List[Tuple[List[List[int]], Tuple[int, int]]]:
        """Generates all possible next moves from the current state."""
        x, y = blank_pos
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n:
                new_state = [row[:] for row in state]  
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append((new_state, (nx, ny)))
        
        return neighbors

    def manhattan_distance(self) -> int:
        """Computes the Manhattan distance heuristic for the current grid, excluding the blank space (0)."""
        distance = 0
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val != 0:  
                    goal_x = (val - 1) // self.n  
                    goal_y = (val - 1) % self.n   
                    distance += abs(goal_x - i) + abs(goal_y - j)
        logging.debug(f"Manhattan distance for current grid: {distance}")
        return distance
