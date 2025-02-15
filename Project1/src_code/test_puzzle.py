"""
    Author: Riyad Abdurahimov
    Description: Unit tests for the N-Puzzle solver. This module includes tests for the 
    NPuzzle class (solvability check, grid validation), the A* puzzle solver, and utility 
    functions such as generating the goal state. It ensures the correctness of the puzzle-solving 
    process and validation of edge cases (e.g., invalid grids, already solved puzzles).
"""
import unittest
from puzzle import NPuzzle
from solver import solve_puzzle
from utils import generate_goal_state

class TestNPuzzle(unittest.TestCase):

    def test_solvable(self):
        """Test if solvability check works correctly."""
        solvable_puzzle = [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ]
        puzzle = NPuzzle(solvable_puzzle)
        self.assertTrue(puzzle.is_solvable())

    def test_unsolvable(self):
        """Test if the solvability check correctly identifies unsolvable puzzles."""
        unsolvable_puzzle = [
            [1, 2, 3],
            [5, 4, 0],
            [7, 8, 6]
        ]
        puzzle = NPuzzle(unsolvable_puzzle)
        self.assertFalse(puzzle.is_solvable())

    def test_solver(self):
        """Test if the solver produces correct solutions."""
        puzzle = [
            [1, 2, 3],
            [4, 0, 5],
            [6, 7, 8]
        ]
        solution = solve_puzzle(puzzle, 3)
        self.assertIsNotNone(solution)             # Ensure the solver returns a solution
        self.assertGreater(len(solution), 0)       # Solution should have at least one move

    def test_goal_state(self):
        """Test if the goal state is correctly generated and recognized."""
        goal_state = generate_goal_state(3)
        solved_puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        puzzle = NPuzzle(solved_puzzle)
        self.assertEqual(puzzle.grid, goal_state)  # The puzzle grid should match the goal state

    def test_no_moves_needed(self):
        """Test if the solver recognizes already solved puzzle."""
        solved_puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        solution = solve_puzzle(solved_puzzle, 3)
        self.assertEqual(len(solution), 0)  # No moves should be needed

    def test_invalid_grid_size(self):
        """Test if invalid grid sizes (less than 3x3 or greater than 6x6) raise ValueError."""
        invalid_grid = [
            [1, 2],                         # 2x2 grid is invalid
            [0, 3]
        ]
        with self.assertRaises(ValueError):
            NPuzzle(invalid_grid)
    
    def test_invalid_grid_elements(self):
        """Test if grids with repeated or missing elements raise ValueError."""
        invalid_grid = [
            [1, 2, 3],
            [4, 5, 5],  # Repeated 5
            [7, 8, 6]
        ]
        with self.assertRaises(ValueError):
            NPuzzle(invalid_grid)

        invalid_grid_2 = [
            [1, 2, 9],
            [4, 0, 8],
            [7, 6, 3]   # Missing 5
        ]
        with self.assertRaises(ValueError):
            NPuzzle(invalid_grid_2)

        invalid_grid_3 = [
            [1,2,3,4],
            [7,5,6],
            [0,8]       # Number of Rows != Number of Columns
        ]
        with self.assertRaises(ValueError):
            NPuzzle(invalid_grid_3)
    

if __name__ == "__main__":
    unittest.main()
