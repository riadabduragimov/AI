"""
Author: Riyad Abdurahimov
Description:
    This module defines the `Square` class, which represents a 4x4 grid unit in the landscape for the Tile Placement CSP problem.
    Each `Square` maintains information about its position, bush count, available tile options, and assigned tiles.
    It includes methods to manipulate and evaluate tile placements, scan the current state, and determine optimal tile choices.

"""

from typing import List, Dict, Optional
from State import State  # Importing the State class for managing the grid state

class Square:
    def __init__(self, x: int = 0, y: int = 0, index: int = 0, number_of_bushes: int = 0):
        """
        Initializes a Square object with position, index, and bush count.
        
        Args:
            x (int): X-coordinate of the square.
            y (int): Y-coordinate of the square.
            index (int): Unique index for the square.
            number_of_bushes (int): The initial number of bushes in the square.
        """
        self.x = x
        self.y = y
        self.index = index
        self.number_of_bushes = number_of_bushes
        self.original = State()  # Stores the original state of the square
        self.current_state = State()  # Stores the current state after tile placements
        self.assigned_tile: Optional[str] = None  # Tracks the tile assigned to this square
        self.available_tiles: List[str] = []  # List of tiles that can be placed in this square
        self.count_of_all_bushes_after_tile: Dict[str, int] = {}  # Stores bush count after placing each tile

    def __copy__(self):
        """
        Creates a copy of the Square object.
        
        Returns:
            Square: A new Square object with the same attributes.
        """
        new_square = Square(self.x, self.y, self.index, self.number_of_bushes)
        new_square.current_state = self.current_state
        new_square.original = self.original
        new_square.assigned_tile = self.assigned_tile
        return new_square

    def scan_square(self) -> Dict[str, int]:
        """
        Scans the square's current state and counts occurrences of each bush type.
        
        Returns:
            Dict[str, int]: A dictionary mapping bush types to their counts.
        """
        result = {}
        for row in self.current_state.data:
            for bush in row:
                if bush < 1:
                    continue
                bush_str = str(bush)
                result[bush_str] = result.get(bush_str, 0) + 1
        return result

    def put_tile(self, tile_key: str):
        """
        Places a tile on the square and updates its current state accordingly.
        
        Args:
            tile_key (str): The key representing the tile type to place.
        """
        new_data = [row[:] for row in self.current_state.data]

        # Define different tile placements based on type
        if tile_key == "OUTER_BOUNDARY":
            new_data[0] = [-1] * 4
            new_data[1][0] = new_data[1][3] = -1
            new_data[2][0] = new_data[2][3] = -1
            new_data[3] = [-1] * 4
        elif tile_key in ("L_SHAPE_1", "L_SHAPE_2", "L_SHAPE_3", "L_SHAPE_4"):
            self.apply_individual_l_shape(new_data, tile_key)
        elif tile_key == "FULL_BLOCK":
            new_data = [[-1] * 4 for _ in range(4)]
        elif tile_key == "EL_SHAPE":
            best_l_shape_key = self.get_best_l_shape()
            self.apply_individual_l_shape(new_data, best_l_shape_key)
    
        self.assigned_tile = tile_key
        self.current_state = State(data=new_data, previous=self.current_state)

    def apply_individual_l_shape(self, new_data, tile_key: str):
        """
        Applies a specific L_SHAPE tile to the square.
        
        Args:
            new_data (List[List[int]]): The modified grid data after tile placement.
            tile_key (str): The L_SHAPE variant being applied.
        """
        if tile_key == "L_SHAPE_1":
            new_data[0] = [-1] * 4
            new_data[1][0] = new_data[2][0] = new_data[3][0] = -1
        elif tile_key == "L_SHAPE_2":
            new_data[0] = [-1] * 4
            new_data[1][0] = new_data[1][1] = new_data[2][0] = -1
        elif tile_key == "L_SHAPE_3":
            new_data[0] = [-1] * 4
            new_data[0][3] = new_data[1][3] = new_data[2][3] = -1
        elif tile_key == "L_SHAPE_4":
            new_data[0] = [-1] * 4
            new_data[1][0] = new_data[2][1] = new_data[3][1] = -1

    def revert(self):
        """
        Reverts the square to its original state before any tile was placed.
        """
        self.current_state = self.original
        self.assigned_tile = None

    def get_best_l_shape(self) -> str:
        """
        Determines the best L_SHAPE tile based on the least bush coverage.
        
        Returns:
            str: The key of the optimal L_SHAPE variant.
        """
        coverage = {}
        for tile in ["L_SHAPE_1", "L_SHAPE_2", "L_SHAPE_3", "L_SHAPE_4"]:
            self.put_tile(tile)
            coverage[tile] = self.calculate_coverage()
            self.revert()

        return min(coverage, key=coverage.get)

    def calculate_coverage(self) -> int:
        """
        Calculates the number of visible bushes after tile placement.
        
        Returns:
            int: The number of uncovered bushes remaining.
        """
        return sum(1 for row in self.current_state.data for bush in row if bush > 0)

    def get_lcv(self) -> List[str]:
        """
        Determines the least constraining value (LCV) ordering of tiles.
        
        Returns:
            List[str]: A list of tile keys ordered by their impact on bush coverage.
        """
        self.put_tile("EL_SHAPE")
        el_shape = self.calculate_coverage()
        self.revert()

        self.put_tile("OUTER_BOUNDARY")
        outer_body = self.calculate_coverage()
        self.revert()

        if el_shape < outer_body:
            return ["EL_SHAPE", "OUTER_BOUNDARY", "FULL_BLOCK"]
        elif el_shape > outer_body:
            return ["OUTER_BOUNDARY", "EL_SHAPE", "FULL_BLOCK"]
        else:
            return ["EL_SHAPE", "OUTER_BOUNDARY", "FULL_BLOCK"] if self.x < self.y else ["OUTER_BOUNDARY", "EL_SHAPE", "FULL_BLOCK"]

    def print(self):
        """
        Prints the square's current state with '#' representing placed tiles.
        """
        for row in self.current_state.data:
            print(" ".join(str(bush) if bush > -1 else "#" for bush in row))
