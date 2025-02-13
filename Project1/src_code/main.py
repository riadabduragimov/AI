import os
import logging
from typing import List
from puzzle import NPuzzle
from solver import solve_puzzle

logging.basicConfig(level=logging.DEBUG, filename="puzzle_solver.log", filemode='w')
logging.info("Starting puzzle solver...")

input_folder = os.path.join(os.path.dirname(__file__), '..', 'input')
output_folder = os.path.join(os.path.dirname(__file__), '..', 'output')

def read_puzzle(filename: str) -> List[List[int]]:
    """Reads the puzzle from a file and converts it into a grid."""
    logging.info(f"Reading puzzle from file: {filename}")
    with open(filename, 'r') as file:
        grid = [[int(num) for num in line.strip().split()] for line in file]
    logging.debug(f"Puzzle grid read: {grid}")
    return grid

def generate_goal_state(n: int) -> List[List[int]]:
    """Generates the goal state for a given puzzle size n."""
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    logging.debug(f"Generated goal state: {goal_state}")
    return goal_state

def save_solution(filename: str, puzzle: NPuzzle, solution: List[List[List[int]]] ):
    """Saves the solution to a file in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output directory: {output_folder}")
    
    output_filename = os.path.join(output_folder, filename.replace(".txt", "_solution.txt"))
    logging.info(f"Saving solution to {output_filename}")
    with open(output_filename, "w") as file:
        file.write("Initial State:\n")
        for row in puzzle.grid:
            file.write('\t'.join(map(str, row)) + "\n")
        
        goal_state = generate_goal_state(puzzle.n)
        file.write("\nGoal State:\n")
        for row in goal_state:
            file.write('\t'.join(map(str, row)) + "\n")
        
        file.write(f"\nNumber of Moves: {len(solution)}\n")
        
        file.write("\nMoves:\n")
        for step in solution:
            for row in step:
                file.write('\t'.join(map(str, row)) + "\n")
            file.write("\n")
    
    logging.info(f"Solution saved to {output_filename}")

def main():
    """Main function to load the puzzle, solve it, and save the output."""
    logging.info(f"Reading puzzles from {input_folder}")
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            logging.info(f"Solving puzzle from {filename}...")
            puzzle_grid = read_puzzle(os.path.join(input_folder, filename))
            
            try:
                puzzle = NPuzzle(puzzle_grid)
                logging.debug(f"Initialized NPuzzle object with grid: {puzzle_grid}")
            except ValueError as e:
                logging.error(f"Error with puzzle {filename}: {e}")
                continue
            
            if not puzzle.is_solvable():
                logging.warning(f"The puzzle from {filename} is not solvable.")
                continue
            
            solution = solve_puzzle(puzzle.grid, puzzle.n)
            if solution:
                logging.info(f"Solution found for {filename} in {len(solution)} moves.")
                save_solution(filename, puzzle, solution)
            else:
                logging.warning(f"No solution found for {filename}.")

if __name__ == "__main__":
    main()
