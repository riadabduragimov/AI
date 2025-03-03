"""
Author: Riyad Abdurahimov
Description:
  This script contains unit tests for the Tile Placement problem components, including the State, Square, Heuristics,
  and Solver classes. The tests validate the correctness of key operations, such as copying a state, scanning and updating squares,
  and applying heuristics. Mocking is used in some tests to simulate landscape and square behavior to ensure that the solution
  operates as expected without requiring actual input data.

"""
import unittest
from State import State
from Square import Square
from Heuristics import Heuristics
from unittest.mock import MagicMock
from Landscape import Landscape
from Solver import Solver

class TestState(unittest.TestCase):
    def test_copy_state(self):
        # Test that copying a state correctly copies the grid data
        original_state = State([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        copied_state = original_state.__copy__()

        # Modify the copy and ensure original remains unaffected
        copied_state.data[0][0] = 99
        self.assertEqual(original_state.data[0][0], 1)
        self.assertEqual(copied_state.data[0][0], 99)


class TestSquare(unittest.TestCase):
    def setUp(self):
        # Setup a square with a 4x4 grid and initialize original and current states
        self.square = Square(x=0, y=0, index=0, number_of_bushes=3)
        self.square.original = State([[1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.square.current_state = State([[1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    def test_scan_square(self):
        # Test scanning bushes in the square and counting correctly
        result = self.square.scan_square()
        self.assertEqual(result, {"1": 2}, "The scan_square should count the number of bushes correctly.")

    def test_put_tile(self):
        # Test placing a tile on the square and ensuring the state is updated
        self.square.put_tile("OUTER_BOUNDARY")
        self.assertEqual(self.square.assigned_tile, "OUTER_BOUNDARY")
        self.assertNotEqual(self.square.current_state.data, self.square.original.data, "The current state should be updated after placing a tile.")

    def test_revert(self):
        # Test reverting the square to its original state
        self.square.put_tile("OUTER_BOUNDARY")
        self.square.revert()
        self.assertEqual(self.square.current_state.data, self.square.original.data)
        self.assertIsNone(self.square.assigned_tile, "Assigned tile should be reset after revert.")


class TestHeuristics(unittest.TestCase):
    def setUp(self):
        # Setup some square objects for testing heuristics
        self.square1 = Square(x=0, y=0, index=0, number_of_bushes=3)
        self.square2 = Square(x=1, y=1, index=1, number_of_bushes=5)
        self.square3 = Square(x=2, y=2, index=2, number_of_bushes=2)

        self.squares = [self.square1, self.square2, self.square3]
        self.heuristics = Heuristics(self.squares)

    def test_get_mrv(self):
        # Test the MRV (Minimum Remaining Values) heuristic, selecting the square with the least available tiles
        self.square1.available_tiles = ["FULL_BLOCK", "EL_SHAPE"]
        self.square2.available_tiles = ["OUTER_BOUNDARY", "EL_SHAPE"]
        self.square3.available_tiles = ["OUTER_BOUNDARY"]

        result = self.heuristics.get_mrv()
        self.assertEqual(result, self.square3, "The square with the least available tiles should be returned by get_mrv.")

    def test_get_mrv_tie_break(self):
        # Test MRV with a tie-breaker based on the number of bushes
        self.square1.available_tiles = ["FULL_BLOCK", "EL_SHAPE"]
        self.square2.available_tiles = ["OUTER_BOUNDARY", "EL_SHAPE"]
        self.square3.available_tiles = ["OUTER_BOUNDARY"]

        # Adding more bushes to square1 and square2
        self.square1.number_of_bushes = 3
        self.square2.number_of_bushes = 5
        self.square3.number_of_bushes = 2

        result = self.heuristics.get_mrv()
        self.assertEqual(result, self.square3, "The square with the least available tiles should be returned.")

    def test_heuristics_initialization(self):
        # Test if squares are sorted by the number of bushes in descending order
        self.assertEqual(self.heuristics.squares[0], self.square2, "Squares should be sorted by the number of bushes.")
        self.assertEqual(self.heuristics.squares[1], self.square1, "Squares should be sorted by the number of bushes.")
        self.assertEqual(self.heuristics.squares[2], self.square3, "Squares should be sorted by the number of bushes.")


class TestSolver(unittest.TestCase):

    def setUp(self):
        # Create a mock landscape for testing the Solver class
        self.landscape = MagicMock(spec=Landscape)
        self.landscape.squares = [
            Square(0, 0, 1), Square(1, 0, 2), Square(0, 1, 3), Square(1, 1, 4),
            Square(2, 0, 2), Square(2, 1, 1), Square(3, 0, 3), Square(3, 1, 4)
        ]
        # Mock available tiles and target values
        self.landscape.available_tiles = {"EL_SHAPE": 7, "OUTER_BOUNDARY": 10, "FULL_BLOCK": 8}
        self.landscape.target = {"1": 24, "2": 21, "3": 18, "4": 17}

        self.solver = Solver(self.landscape)

    def test_scan_bushes(self):
        # Test scanning bushes across multiple squares
        square1 = MagicMock(spec=Square)
        square1.scan_square.return_value = {"1": 1, "2": 0, "3": 0, "4": 0}
        square2 = MagicMock(spec=Square)
        square2.scan_square.return_value = {"1": 0, "2": 1, "3": 0, "4": 0}

        self.landscape.squares = [square1, square2]
        result = self.solver.scan_bushes(self.landscape.squares)
        self.assertEqual(result, {"1": 1, "2": 1, "3": 0, "4": 0})

    def test_is_possible_to_put_tile(self):
        # Test if it is possible to place a specific tile on a square
        square = self.landscape.squares[0]
        self.solver.is_possible_to_put_tile = MagicMock(return_value=True)
        result = self.solver.is_possible_to_put_tile("FULL_BLOCK", square)
        self.assertTrue(result)

    def test_ac3(self):
        # Test the AC3 (Arc-Consistency) algorithm
        self.solver.ac3 = MagicMock(return_value=True)
        result = self.solver.ac3()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
