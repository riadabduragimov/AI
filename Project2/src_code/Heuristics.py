"""
Author: Riyad Abdurahimov
Description: 
    This module contains the Heuristics class used to implement various
    heuristic strategies for tile placement in the CSP problem, including 
    the Minimum Remaining Values (MRV) heuristic. It helps guide the 
    search algorithm by selecting the most constrained square.
"""

from typing import List
from operator import attrgetter
from Square import Square

class Heuristics:
    """
    This class encapsulates the heuristic strategies for tile placement in the CSP problem.
    """

    def __init__(self, squares: List['Square']):
        """
        Initializes the Heuristics class with a list of Square objects, sorted by the number
        of bushes in descending order.
        
        Args:
            squares (List[Square]): List of Square objects.
        """
        # Sorting squares by NumberOfBushes in descending order
        self.squares = sorted(squares, key=attrgetter('number_of_bushes'), reverse=True)

    def get_mrv(self) -> 'Square':
        """
        Returns the square with the least number of remaining values (tiles) 
        that hasn't been assigned a tile (MRV heuristic).
        
        Returns:
            Square: The square with the least remaining values (tiles).
                    Returns None if no unassigned squares are available.
        """
        # Filter squares that haven't been assigned a tile
        unassigned_squares = [square for square in self.squares if square.assigned_tile is None]

        # If no unassigned squares are found, return None
        if not unassigned_squares:
            return None
        
        # Sort by remaining available tiles, number of bushes (descending), and position
        unassigned_squares.sort(key=lambda square: (len(square.available_tiles), 
                                                    -square.number_of_bushes, 
                                                    square.x, square.y))

        # Return the square with the least available tiles (MRV)
        return unassigned_squares[0]
