import time
import tracemalloc

def is_safe(board, row, col, n):
    """
    Checks if it's safe to place a queen at board[row][col].
    We only need to check for attacks in the upper part of the board
    as the lower rows are not yet filled.
    """
    # Check the column for a queen
    for i in range(row):
        if board[i] == col:
            return False

    # Check upper-left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i] == j:
            return False

    # Check upper-right diagonal
    for i, j in zip(range(row, -1, -1), range(col, n, 1)):
        if board[i] == j:
            return False

    return True

def solve_n_queens_util(board, row, n):
    """
    Recursive utility function to solve N-Queens problem.
    """
    # Base case: If all queens are placed, we have a solution.
    if row >= n:
        return True

    # Try placing a queen in each column of the current row
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            # Recur for the next row
            if solve_n_queens_util(board, row + 1, n):
                return True
            # If placing queen in board[row][col] doesn't lead to a solution,
            # then backtrack.
            board[row] = -1 # Backtrack
    
    return False

def solve_exhaustive(n):
    """
    Main function to solve the N-Queens problem using exhaustive search.
    """
    # board[i] = j means queen is at (row i, column j)
    board = [-1] * n
    if not solve_n_queens_util(board, 0, n):
        print(f"Solution does not exist for N={n}")
        return None
    return board

def print_solution(board):
    if board is None:
        return
    n = len(board)
    print(f"Solution for N={n}:")
    for i in range(n):
        row_str = ""
        for j in range(n):
            if board[i] == j:
                row_str += "Q "
            else:
                row_str += ". "
        print(row_str)
    print("-" * 2 * n)


if __name__ == '__main__':
    N = 30 # Change N for testing
    
    print(f"--- Exhaustive Search for N={N} ---")

    # Measure Time
    start_time = time.perf_counter()
    
    # Measure Memory
    tracemalloc.start()
    
    solution = solve_exhaustive(N)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if solution:
        # print_solution(solution) # Optional: print the board
        print(f"Solution found: {solution}")
    
    print(f"Execution Time: {execution_time:.6f} seconds")
    print(f"Peak Memory Usage: {peak / 10**6:.6f} MB")
    print("-" * 30 + "\n")
    