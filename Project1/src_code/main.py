""" 
    Author: Riyad Abdurahimov
    Description: Main entry point for the N-Puzzle solver. This script reads puzzle configurations from input files,
    solves each puzzle using the A* algorithm, and then saves the solution to output files. It handles logging, 
    file input/output, and ensures that the output folder is correctly set up. The solver also checks if the puzzle 
    is solvable before attempting to find a solution.
"""

import os
import logging
from typing import List
from puzzle import NPuzzle
from solver import solve_puzzle
from utils import generate_goal_state

def setup_logging():
    """Sets up logging configuration for the puzzle solver."""
    logging.basicConfig(level=logging.DEBUG, filename="puzzle_solver.log", filemode='w')
    logging.info("Starting puzzle solver...")

input_folder = os.path.join(os.path.dirname(__file__), '..', 'input')
output_folder = os.path.join(os.path.dirname(__file__), '..', 'output')

def read_puzzle(filename: str) -> List[List[int]]:
    """Reads the puzzle from a file and converts it into a 2D grid."""
    logging.info(f"Reading puzzle from file: {filename}")
    with open(filename, 'r') as file:
        grid = [[int(num) for num in line.strip().split()] for line in file]  # Convert each line into a list of integers
    logging.debug(f"Puzzle grid read: {grid}")
    return grid

def save_solution(filename: str, puzzle: NPuzzle, solution: List[List[List[int]]]):
    """Saves the solution of the puzzle to a file in the output folder."""
    ensure_output_folder_exists()                                             # Ensure the output directory exists
    output_filename = os.path.join(output_folder, filename.replace(".txt", "_solution.txt"))
    logging.info(f"Saving solution to {output_filename}")
    
    # Write the initial state, goal state, and the solution steps to the output file
    with open(output_filename, "w") as file:
        write_initial_and_goal_state(file, puzzle)                            # Write initial and goal states to file
        file.write(f"\nNumber of Moves: {len(solution)}\n")                   # Write the number of moves
        write_moves(file, solution)                                           # Write the move steps

    logging.info(f"Solution saved to {output_filename}")

def ensure_output_folder_exists():
    """Checks if the output folder exists, and creates it if it doesn't."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)                                            # Create the directory if it does not exist
        logging.info(f"Created output directory: {output_folder}")

def write_initial_and_goal_state(file, puzzle: NPuzzle):
    """Writes the initial and goal state of the puzzle to the file."""
    file.write("Initial State:\n")
    for row in puzzle.grid:
        file.write('\t'.join(map(str, row)) + "\n")                           # Write each row of the puzzle
        
    goal_state = generate_goal_state(puzzle.n)                                # Generate the goal state based on puzzle size
    file.write("\nGoal State:\n")
    for row in goal_state:
        file.write('\t'.join(map(str, row)) + "\n")                           # Write goal state to file

def write_moves(file, solution: List[List[List[int]]]):
    """Writes each step of the solution to the file."""
    file.write("\nMoves:\n")
    for step in solution:
        for row in step:
            file.write('\t'.join(map(str, row)) + "\n")                       # Write each step of the solution
        file.write("\n")                                                      # Separate each move step with a newline

def solve_puzzle_from_file(filename: str):
    """Solves the puzzle from the specified file and saves the solution."""
    puzzle_grid = read_puzzle(os.path.join(input_folder, filename))           # Read puzzle grid from the file
    
    try:
        puzzle = NPuzzle(puzzle_grid)                                         # Initialize NPuzzle object with the grid
        logging.debug(f"Initialized NPuzzle object with grid: {puzzle_grid}")
    except ValueError as e:
        logging.error(f"Error with puzzle {filename}: {e}")                   # Log any errors with the puzzle
        return
    
    if not puzzle.is_solvable():
        logging.warning(f"The puzzle from {filename} is not solvable.")       # Check if the puzzle is solvable
        return
    
    solution = solve_puzzle(puzzle.grid, puzzle.n)                            # Solve the puzzle
    if solution:
        logging.info(f"Solution found for {filename} in {len(solution)} moves.")  # If solution is found, save it
        save_solution(filename, puzzle, solution)
    else:
        logging.warning(f"No solution found for {filename}.")                     # Log a warning if no solution is found

def process_puzzles():
    """Processes all puzzles in the input folder by solving them one by one."""
    logging.info(f"Reading puzzles from {input_folder}")
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):                                             # Process only .txt files
            logging.info(f"Solving puzzle from {filename}...")
            solve_puzzle_from_file(filename)                                      # Solve the puzzle and save the solution

def main():
    """Main function that initiates the puzzle-solving process."""
    setup_logging()          # Set up logging
    process_puzzles()        # Process all puzzles

if __name__ == "__main__":
    main()                   # Run the main function
