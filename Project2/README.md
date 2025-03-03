<h1 align = center>Tile Placement CSP Solver </h1>

# Table of Contents
1. [Introduction](#introduction)
2. [Classes and Methods](#classes-and-methods)
3. [Algorithms and Heuristics](#algorithms-and-heuristics)
4. [How to Run the Project](#how-to-run-the-project)
5. [How to Test the Project](#how-to-test-the-project)

---

# Introduction

This project addresses the Tile Placement problem using Constraint Satisfaction Problem (CSP) algorithms. The goal is to place tiles of varying shapes on a square landscape, ensuring that a target number of visible bushes of each color are maintained after tile placement. The tiles are of size 4x4, and the landscape size varies depending on the number of tiles. 

I wrote a solution that uses a backtracking algorithm enhanced with several CSP techniques, such as Minimum Remaining Values (MRV), Least Constraining Value (LCV), and Arc Consistency (AC-3). These heuristics help make the search process more efficient. The project also includes tie-breaking rules to handle cases where multiple tile placements are possible.

---
# Classes and Methods


The core classes in this project are:

## **State Class**
The `State` class represents the state of a 4x4 grid during the tile placement process. It supports backtracking by maintaining references to previous states, enabling the algorithm to undo tile placements when necessary. I wrote methods such as `__init__` to initialize the state and `__copy__` to create shallow copies of the state for backtracking.

## **Landscape Class**
The `Landscape` class models the environment where tile placement occurs. I used this class to parse input text and build the landscape, including grid layout and tile counts. Methods like `build`, `parse_tiles`, `parse_sections`, and `tokenize` were used to process the input and divide the grid into 4x4 squares for tile placement.

## **Solver Class**
The `Solver` class is the core of the algorithm. It implements the backtracking search algorithm and incorporates heuristics such as MRV, LCV, and AC-3 to efficiently solve the tile placement problem. I used this class to manage tile placement, ensure consistency, and maintain backtracking during the search process.

## **Square Class**
The `Square` class represents a 4x4 section of the landscape grid. It helps manage the bushes in each square and supports tracking the number of bushes within it. The `Square` class also works in conjunction with the `Landscape` class to divide the landscape into smaller sections for easier tile placement. The `Least Constraining Value` (LCV) heuristic is also implemented in this class to select the tile that constrains the least number of neighboring squares, improving the efficiency of the search. This class helps make the backtracking algorithm more efficient by guiding the decision-making process during tile placement.

## **Heuristics Class**
The `Heuristics` class defines heuristic methods used to guide the search process. I wrote the MRV (Minimum Remaining Values) heuristic in this class to prioritize the tile placements based on the fewest available tile options.

---
# Algorithms and Heuristics

To solve the tile placement problem efficiently, I implemented the following techniques:

1. **Backtracking Algorithm**: I used backtracking as the main search strategy. This algorithm recursively places tiles and checks for constraint violations at each step. If a violation occurs, it backtracks to the previous state and tries a different tile placement.

2. **Minimum Remaining Values (MRV)**: I used the MRV heuristic to select the variable (square) with the fewest available tile options. This approach helps reduce the search space by prioritizing the most constrained variables.

3. **Least Constraining Value (LCV)**: I applied the LCV heuristic to select the tile that constrains the least number of neighboring squares. This helps maintain flexibility for future tile placements, making the algorithm more efficient.

4. **Arc Consistency (AC-3)**: To ensure consistency during the search process, I implemented the AC-3 algorithm. This technique revises the domains of variables and checks for constraint violations. It ensures that no tile placement will result in an unsolvable configuration.

5. **Tie-breaking Rules**: I used tie-breaking rules to resolve cases where multiple tile placements are possible. These rules ensure that the algorithm selects the most appropriate tile, even when multiple options are available.

---

# How to Run the Project

To run the tile placement solver, you need to execute the `main.py` script with an input file from the `input` folder. For example, to run the solver with the `input1.txt` file, you would use the following command:

```bash
python src_code/main.py input/input1.txt
```
---

# How to Test the Project

To ensure the functionality of the CSP solver, I wrote unit tests in the test_csp.py file. These tests cover various components of the system, including the landscape parsing, heuristics, and solver behavior.

To run the tests, use the following command:

```bash
python -m unittest src_code/test_csp.py
```
This will run all the test cases defined in `test_csp.py`, and you will see the results in the terminal. If all tests pass, it confirms that the individual components of the solver are working correctly.
 
