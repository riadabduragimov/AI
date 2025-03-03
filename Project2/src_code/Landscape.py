"""
Author: Riyad Abdurahimov
Description: 
This module defines the `Landscape` class, which represents the environment 
for the tile placement constraint satisfaction problem (CSP). 

The `Landscape` class:
- Parses and builds the landscape from a text input.
- Maintains information about the grid layout, available tiles, and target visibility for bushes.
- Processes the landscape into 4x4 squares for tile placement.
- Provides utility methods for parsing, tokenizing, and handling missing data.

The class interacts with the `Square` class, which represents individual sections of the landscape.
"""

import re
from typing import List, Dict, Tuple
from copy import deepcopy
from Square import Square  

class Landscape:
    """
    Represents the landscape grid, including tile availability and target bush visibility.
    It processes input text to construct a structured representation of the problem.
    """

    def __init__(self):
        """Initializes an empty landscape with layout, tile availability, target requirements, and squares."""
        self.layout: List[List[int]] = []  # 2D list representing the bush landscape grid
        self.available_tiles: Dict[str, int] = {}  # Dictionary storing available tile counts
        self.target: Dict[str, int] = {}  # Dictionary storing target visibility for bush colors
        self.squares: List[Square] = []  # List of 4x4 squares representing the landscape's divided sections

    @staticmethod
    def build(text: str) -> 'Landscape':
        """
        Parses the input text and constructs a `Landscape` object.
        
        Steps:
        1. Parses available tile counts.
        2. Extracts the landscape grid and target visibility requirements.
        3. Normalizes the landscape by ensuring uniform row lengths.
        4. Divides the landscape into 4x4 squares.

        Args:
            text (str): The raw text input describing the landscape.

        Returns:
            Landscape: A fully constructed `Landscape` object.
        """
        text = text.replace("\r", "")  # Normalize line endings for consistency
        sections = ["landscape", "tiles", "targets"]
        lines = text.split("\n")

        # Step 1: Parse tile availability
        tiles = Landscape.parse_tiles(text)

        # Step 2: Parse landscape grid and target bush visibility
        map_data, target = Landscape.parse_sections(lines, sections)

        # Step 3: Construct the landscape object
        landscape = Landscape()
        landscape.available_tiles = tiles
        landscape.target = target
        landscape.layout = [row for row in map_data]

        # Step 4: Normalize the layout with padding and fill squares
        landscape.layout = Landscape.add_additional_zeros(landscape.layout)
        landscape.fill_squares()

        return landscape

    @staticmethod
    def parse_tiles(text: str) -> Dict[str, int]:
        """
        Extracts available tile counts from the input text.

        Args:
            text (str): The raw input text containing tile information.

        Returns:
            Dict[str, int]: A dictionary mapping tile types to their available count.
        """
        tiles = {}
        tiles["OUTER_BOUNDARY"] = int(re.search(r"OUTER_BOUNDARY=(\d+)", text).group(1))
        tiles["EL_SHAPE"] = int(re.search(r"EL_SHAPE=(\d+)", text).group(1))
        tiles["FULL_BLOCK"] = int(re.search(r"FULL_BLOCK=(\d+)", text).group(1))
        return tiles

    @staticmethod
    def parse_sections(lines: List[str], sections: List[str]) -> Tuple[List[List[int]], Dict[str, int]]:
        """
        Parses the landscape grid and target visibility sections from the input text.

        Args:
            lines (List[str]): The list of lines from the input text.
            sections (List[str]): List of expected section names in the input.

        Returns:
            Tuple[List[List[int]], Dict[str, int]]: 
                - The parsed landscape grid as a 2D list.
                - The target visibility dictionary.
        """
        map_data = []
        target = {}
        cnt = -2  # Tracks the current section index

        for line in lines:
            if line == "":
                continue

            if line.startswith("#"):  # Detect section headers
                cnt += 1
                continue
            if cnt == 4:  # Stop parsing after known sections
                break

            current_section = sections[cnt]
            if current_section == "landscape":
                map_data.append(Landscape.tokenize(line))  # Convert grid line to list of integers
            elif current_section == "targets":
                words = line.split(":", 1)
                target[words[0]] = int(words[1])  # Extract target visibility for bush color

        return map_data, target

    @staticmethod
    def tokenize(line: str) -> List[int]:
        """
        Converts a row of the input landscape text into a list of integers.

        - Numbers represent different bush colors.
        - Spaces (gaps in input) are treated as zeros.

        Args:
            line (str): A row from the landscape text.

        Returns:
            List[int]: The processed row as a list of integers.
        """
        result = []
        for i in range(0, len(line), 2):
            if line[i] == ' ':
                result.append(0)  # Treat spaces as empty cells
            else:
                result.append(int(line[i]))  # Convert character to integer bush type
        return result

    @staticmethod
    def add_additional_zeros(arr: List[List[int]]) -> List[List[int]]:
        """
        Ensures all rows in the landscape grid have the same length by padding with zeros.

        Args:
            arr (List[List[int]]): The raw landscape grid.

        Returns:
            List[List[int]]: The landscape grid with uniform row lengths.
        """
        max_length = max(len(row) for row in arr)  # Determine the longest row
        for i in range(len(arr)):
            while len(arr[i]) < max_length:
                arr[i].append(0)  # Append zeros to ensure uniformity
        return arr

    def fill_squares(self):
        """
        Divides the landscape into 4x4 squares and stores them in `self.squares`.

        - Each square represents a distinct section of the landscape.
        - Each square keeps track of its original state and the number of bushes within it.
        """
        size = len(self.layout)
        index = 0

        for row in range(0, size, 4):
            for col in range(0, size, 4):
                new_square = Square(x=row, y=col, index=index)

                # Extract a 4x4 submatrix from the landscape grid
                new_square.current_state.data = [row[col:col + 4] for row in self.layout[row:row + 4]]

                # Save the original state of the square
                new_square.original = deepcopy(new_square.current_state)

                # Count the number of bushes in the square
                new_square.number_of_bushes = sum(1 for x in new_square.current_state.data for bush in x if bush > 0)

                self.squares.append(new_square)
                index += 1
