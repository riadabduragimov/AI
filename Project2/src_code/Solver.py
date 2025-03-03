"""
Author: Riyad Abdurahimov
Description:
    This module contains the Solver class, which implements a backtracking 
    algorithm with heuristics to solve the tile placement problem in the 
    context of the CSP problem. The solver utilizes the Minimum Remaining 
    Values (MRV) heuristic, Least Constraining Value (LCV), and AC-3 
    constraint propagation to efficiently search for a solution.

"""

from Landscape import Landscape
from Heuristics import Heuristics
from Square import Square
from collections import deque

class Solver:
    """
    Solver class implements the backtracking algorithm with heuristics and 
    constraint propagation for solving the tile placement problem in a landscape. 
    It uses strategies such as MRV (Minimum Remaining Values), LCV (Least Constraining Value),
    and AC-3 (Arc Consistency) to find a solution that satisfies the constraints.
    """

    def __init__(self, landscape: 'Landscape'):
        """
        Initializes the solver with a landscape, setting up the heuristic strategy 
        and initializing the number of iterations.
        
        Args:
            landscape (Landscape): The landscape containing squares and the target bush coverage.
        """
        self.landscape = landscape
        self.heuristics = Heuristics(landscape.squares)
        self.iterations = 0

    def backtrack(self, square: 'Square') -> bool:
        """
        Backtracking search algorithm with heuristics, applying AC3 before placing a tile
        and again during backtracking to restore consistency.
        
        Args:
            square (Square): The current square being processed.

        Returns:
            bool: True if a valid solution is found, otherwise False.
        """
        self.iterations += 1

        # Check if all squares have been assigned a tile
        if self.has_found_solution() and all(sq.assigned_tile is not None for sq in self.landscape.squares):
            return True

        if square is None:
            return False

        # Try each tile using the Least Constraining Value (LCV) strategy
        for tile_key in square.get_lcv():
            if self.landscape.available_tiles[tile_key] == 0:
                continue

            if self.is_possible_to_put_tile(tile_key, square):
                # Place the tile
                self.landscape.available_tiles[tile_key] -= 1
                square.put_tile(tile_key)

                # **Run AC3 before moving forward**
                if self.ac3():
                    # Select the next square with the Minimum Remaining Values (MRV) heuristic
                    next_square = self.heuristics.get_mrv()
                    if self.backtrack(next_square):
                        return True

                # **Backtracking: Remove tile & restore state**
                self.landscape.available_tiles[tile_key] += 1
                square.revert()

                # **Run AC3 again during backtracking** to restore arc consistency
                self.ac3()

        return False

    def has_found_solution(self) -> bool:
        """
        Check if the current configuration of squares meets the target bush coverage.
        
        Returns:
            bool: True if the solution matches the target, otherwise False.
        """
        current_bushes = self.scan_bushes(self.landscape.squares)

        # Check if the current bushes match the target bushes
        for item in current_bushes.keys():
            if current_bushes[item] != self.landscape.target[item]:
                return False

        return True

    def scan_bushes(self, squares: list) -> dict:
        """
        Scan the landscape squares and calculate the current count of bushes.
        
        Args:
            squares (list): List of squares in the landscape.
        
        Returns:
            dict: Dictionary of bush types and their counts in the landscape.
        """
        result = {"1": 0, "2": 0, "3": 0, "4": 0}

        # Iterate through each square to update the bush counts
        for square in squares:
            square_dict = square.scan_square()
            for key in square_dict.keys():
                if key in result:
                    result[key] += square_dict[key]

        return result

    def is_possible_to_put_tile(self, tile_name: str, square: 'Square') -> bool:
        """
        Check if it's possible to place a given tile on a square without violating the 
        target bush coverage.
        
        Args:
            tile_name (str): The tile to be placed.
            square (Square): The square where the tile will be placed.
        
        Returns:
            bool: True if placing the tile is possible, otherwise False.
        """
        square.put_tile(tile_name)
        current_bushes = self.scan_bushes(self.landscape.squares)

        # Ensure placing the tile does not violate the target bush coverage
        for item in current_bushes.keys():
            if current_bushes[item] < self.landscape.target[item]:
                square.revert()
                return False

        return True

    def ac3(self):
        """
        Apply Arc-Consistency (AC-3) algorithm to enforce constraints and prune the 
        domains of the squares based on neighbors' constraints.
        
        Returns:
            bool: True if AC-3 is successfully applied, False if no solution is possible.
        """
        queue = deque()

        # Initialize the queue with all (square, neighbor) pairs
        for square in self.landscape.squares:
            for neighbor in self.get_neighbors(square):
                queue.append((square, neighbor))

        while queue:
            square, neighbor = queue.popleft()
            if self.revise(square, neighbor):
                if not square.available_tiles:
                    return False  # Domain wipeout, no solution
                for other_neighbor in self.get_neighbors(square):
                    queue.append((other_neighbor, square))
        return True

    def revise(self, square, neighbor):
        """
        Revise the available tiles for a square based on the constraints from its neighbor.
        
        Args:
            square (Square): The square whose tiles need revision.
            neighbor (Square): The neighboring square that imposes constraints.
        
        Returns:
            bool: True if the square's domain was revised, otherwise False.
        """
        revised = False
        for tile in square.available_tiles[:]:  # Iterate over a copy of the available tiles
            if not any(self.is_consistent(tile, neighbor_tile) for neighbor_tile in neighbor.available_tiles):
                square.available_tiles.remove(tile)
                revised = True
        return revised

    def is_consistent(self, tile1, tile2):
        """
        Perform a stronger consistency check for tile placement, considering compatibility,
        bush coverage, and tile overlap.
        
        Args:
            tile1 (str): The first tile.
            tile2 (str): The second tile.
        
        Returns:
            bool: True if the tiles are consistent, otherwise False.
        """
        if not self.check_tile_compatibility(tile1, tile2):
            return False
        if not self.check_bush_coverage(tile1, tile2):
            return False
        if not self.check_tile_overlap(tile1, tile2):
            return False
        return True

    def check_tile_compatibility(self, tile1, tile2):
        """
        Ensure that tile1 and tile2 are compatible based on their shapes.
        
        Args:
            tile1 (str): The first tile.
            tile2 (str): The second tile.
        
        Returns:
            bool: True if the tiles are compatible, otherwise False.
        """
        if tile1 == 'Full Block' and tile2 == 'Outer Boundary':
            return False
        if tile1 == 'Outer Boundary' and tile2 == 'Full Block':
            return False
        # Add more compatibility checks here as needed
        return True

    def check_bush_coverage(self, tile1, tile2):
        """
        Ensure that placing tile1 and tile2 together does not violate the target bush coverage.
        
        Args:
            tile1 (str): The first tile.
            tile2 (str): The second tile.
        
        Returns:
            bool: True if placing the tiles does not violate the target bush coverage.
        """
        bush_coverage1 = self.get_bush_coverage(tile1)
        bush_coverage2 = self.get_bush_coverage(tile2)

        for bush_type, coverage in bush_coverage1.items():
            target = self.landscape.target[bush_type]
            current_coverage = self.scan_bushes(self.landscape.squares).get(bush_type, 0)
            if current_coverage + coverage > target:
                return False

        for bush_type, coverage in bush_coverage2.items():
            target = self.landscape.target[bush_type]
            current_coverage = self.scan_bushes(self.landscape.squares).get(bush_type, 0)
            if current_coverage + coverage > target:
                return False

        return True

    def check_tile_overlap(self, tile1, tile2):
        """
        Ensure that tiles do not overlap in their coverage of bushes.
        
        Args:
            tile1 (str): The first tile.
            tile2 (str): The second tile.
        
        Returns:
            bool: True if the tiles do not overlap, otherwise False.
        """
        covered_areas1 = self.get_covered_areas(tile1)
        covered_areas2 = self.get_covered_areas(tile2)

        if set(covered_areas1).intersection(covered_areas2):
            return False

        return True

    def get_bush_coverage(self, tile):
        """
        Return a dictionary of bush types and their coverage by a tile.
        
        Args:
            tile (str): The tile to check for coverage.
        
        Returns:
            dict: Dictionary of bush types and coverage amounts.
        """
        coverage = {}
        if tile == 'Full Block':
            coverage = {"1": 2, "2": 2}  # Example coverage
        elif tile == 'Outer Boundary':
            coverage = {"3": 1, "4": 1}  # Example coverage
        return coverage

    def get_covered_areas(self, tile):
        """
        Return the grid positions covered by a given tile.
        
        Args:
            tile (str): The tile to check for coverage.
        
        Returns:
            list: List of covered grid positions.
        """
        if tile == 'Full Block':
            return [(x, y) for x in range(4) for y in range(4)]
        elif tile == 'Outer Boundary':
            return [(x, 0) for x in range(4)] + [(x, 3) for x in range(4)]
        return []

    def get_neighbors(self, square):
        """
        Return the neighbors of a given square that are adjacent.
        
        Args:
            square (Square): The square for which neighbors are to be found.
        
        Returns:
            list: List of adjacent squares.
        """
        neighbors = []
        for other_square in self.landscape.squares:
            if other_square != square and self.are_adjacent(square, other_square):
                neighbors.append(other_square)
        return neighbors

    def are_adjacent(self, square1, square2):
        """
        Check if two squares are adjacent (horizontally or vertically).
        
        Args:
            square1 (Square): The first square.
            square2 (Square): The second square.
        
        Returns:
            bool: True if the squares are adjacent, otherwise False.
        """
        return abs(square1.x - square2.x) + abs(square1.y - square2.y) == 4
