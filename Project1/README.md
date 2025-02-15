<h1 align = center>N-Puzzle Solver using A* Search Algorithm</h1> 

---

# Table of Contents
1. [Project Description](#project-description)
2. [What I Did](#what-i-did)
3. [Logging](#logging)
4. [How to Run the Project](#how-to-run-the-project)
5. [Unit Testing the N-Puzzle Solver](#unit-testing-the-n-puzzle-solver)
---
# Project Description

This project implements a solution for the N-puzzle problem, where the goal is to rearrange the tiles of an `n x n` grid to reach a goal configuration using the fewest possible moves. The puzzle consists of numbered tiles (from 1 to N) and one blank space (denoted as 0). The tiles can be moved horizontally and vertically into the blank space.

The project leverages the A* search algorithm to find the optimal solution for the puzzle. It supports grids ranging from 3x3 to 6x6 and can solve puzzles like the 8-puzzle (3x3 grid) and the 15-puzzle (4x4 grid).

The input consists of a file containing the puzzle configuration in an `n x n` grid format. The numbers are separated by tabs, and the blank space is denoted by `0`. An example input file for the 3x3 puzzle (8-puzzle) might look like this:

---
# What I Did

I implemented the N-puzzle solver using the A* algorithm. Here's a breakdown of the key tasks:

- **Heuristic Implementation**: I used the Manhattan distance as the heuristic for the A* algorithm. The Manhattan distance calculates the total distance between the current and goal positions of each tile, which guides the search process.
- **Algorithm**: I used A* search to explore all possible states of the puzzle. The algorithm selects the most promising states by prioritizing them based on the sum of the moves taken so far and the estimated distance to the goal (heuristic).
- **State Representation**: I represented the puzzle as a 2D list (grid), where each number corresponds to a tile, and `0` represents the blank space.
- **Solvability Check**: The program includes a check to determine if the puzzle is solvable. This check uses the inversion count method, which examines the number of inversions in the puzzle to determine solvability.
- **Input/Output Handling**: The puzzle configurations are read from input files, and the solution steps are saved in output files.


---
# Logging

I used the `logging` module to track the program's execution. The logs are saved in `puzzle_solver.log` and contain details about the puzzle-solving process:

- Puzzle reading and parsing
- A* search progress
- Solution saving
- Errors and warnings

---
# How to Run the Project

Follow these steps to run the project:

1. **Clone the Repository**: 
   - Use the following command to clone the project repository to your local machine:
   ```bash
   git clone https://github.com/riadabduragimov/AI/tree/main/Project1
   ```
2. **Ensure Python is Installed**: 
   - Make sure that Python is installed on your system.
     ```bash
     python --version
     ```

3. **Add Input Files**: 
   - If you have input files, place them into the `input` folder. 
   - The folder already contains 3 sample files, but you can add your own files as long as they meet the project requirements (proper format, size, and content).


4. **Run the Project**  
    - Navigate to the `src_code` directory and run the following command in your terminal:
   
   ```bash
   python main.py
   ```
5. **Check the Output**:
   - After running the script, check the `output/` directory for the solution file.

---
# Unit Testing the N-Puzzle Solver

I created a `test_puzzle.py` file for testing the key components of the solver and puzzle class. The tests include checking if the puzzle is solvable, testing the solver's ability to find a solution, validating goal state generation, and more.

### To Run the Tests:
1. Make sure that `unittest` is installed (it is included by default with Python).
2. In the command line, navigate to the directory containing the `test_puzzle.py` file.
3. Run the following command to execute the unit tests:

```bash
python -m unittest test_puzzle.py
