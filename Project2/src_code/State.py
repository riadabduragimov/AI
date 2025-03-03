"""
Author: Riyad Abdurahimov
Description: 
    This module defines the `State` class, which represents the state of a 4x4 grid. 
    It is used to track changes in the tile placement process for the CSP-based Tile Placement problem.
    Each state maintains a reference to its previous state to allow backtracking.

"""

from typing import List, Optional

class State:
    """
    Represents the state of a 4x4 grid, used in the CSP-based Tile Placement problem.
    It supports state transitions and backtracking by maintaining previous states.
    """

    def __init__(self, data: Optional[List[List[int]]] = None, previous: Optional['State'] = None):
        """
        Initializes a State object.

        Args:
            data (Optional[List[List[int]]]): A 4x4 grid representing the current state.
                                              Defaults to a 4x4 grid of zeros if not provided.
            previous (Optional['State']): A reference to the previous state for backtracking.
        """
        # If no data is provided, initialize with a 4x4 grid filled with zeros
        self.data = data if data else [[0] * 4 for _ in range(4)]
        self.previous = previous  # Keep track of the previous state for backtracking

    def __copy__(self):
        """
        Creates a shallow copy of the current state.

        Returns:
            State: A new State object with copied grid data and reference to the previous state.
        """
        # Copy the grid data to preserve the current state
        new_state = State(data=[row[:] for row in self.data], previous=self.previous)
        return new_state
