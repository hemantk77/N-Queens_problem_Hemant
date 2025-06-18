# N-Queens Problem: A Comparative Algorithm Study

> A comprehensive implementation and performance analysis of four distinct algorithms for solving the classic N-Queens problem. This project serves as a study in combinatorial optimization, exploring the trade-offs between exact, heuristic, and meta-heuristic search techniques.

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Table of Contents

* [About The Project](#about-the-project)
* [Algorithms Implemented](#algorithms-implemented)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Repository Structure](#repository-structure)
* [Results and Analysis](#results-and-analysis)
* [License](#license)
* [Acknowledgments](#acknowledgments)

## About The Project

[cite_start]The N-Queens problem is a classic puzzle that involves placing N queens on an $N \times N$ chessboard in such a way that no two queens threaten each other. [cite_start]This means no two queens can be on the same row, column, or diagonal. [cite_start]While simple to state, the problem's solution space grows exponentially, making it an ideal benchmark for evaluating the performance and scalability of various search and optimization algorithms.

This project implements four different algorithmic paradigms to solve the N-Queens problem and conducts a rigorous comparative analysis of their performance based on execution time, memory usage, and success rate across various board sizes ($N = 10, 30, 50, 100, 200$).

![N-Queens Problem Illustration](https://i.imgur.com/gZ2C1rG.png)
*Figure: The 10-Queens problem, showing an invalid arrangement with conflicts and a valid solution.*

### Algorithms Implemented

This study designs, implements, and compares the following four algorithms:

1.  **Exhaustive Search (Depth-First Search)**
    * A complete, brute-force algorithm that systematically explores every possible configuration using recursion and backtracking to guarantee a solution. It serves as the baseline for correctness.

2.  **Greedy Search (Steepest-Ascent Hill Climbing)**
    * A local search heuristic that attempts to minimize the number of queen conflicts by iteratively making the single best move. Random restarts are used to escape local minima.

3.  **Simulated Annealing**
    * An advanced, probabilistic local search algorithm. It improves upon hill climbing by sometimes accepting "worse" moves, allowing it to escape local optima and explore the search space more effectively.

4.  **Genetic Algorithm**
    * A meta-heuristic inspired by natural evolution. It evolves a population of candidate solutions over generations using selection, crossover, and mutation operators to find a valid solution. [cite_start]It is particularly effective for large-scale problems.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.x installed on your system.

### Installation

1.  Clone the repo
    ```sh
    git clone [https://github.com/your_username/your_repository_name.git](https://github.com/your_username/your_repository_name.git)
    ```
2.  Navigate to the project directory
    ```sh
    cd your_repository_name
    ```

## Usage

Each algorithm is contained in its own Python script. These scripts are designed as testing harnesses that run 10 trials for a given `N` and report the average performance.

To run a test for a specific algorithm:

```sh
python <algorithm_script_name>.py
