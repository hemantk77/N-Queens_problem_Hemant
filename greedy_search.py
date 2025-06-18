import random
import time
import tracemalloc
import statistics

def calculate_conflicts(board, n):
    """
    Calculates the total number of attacking pairs of queens.
    This is the heuristic function h(n).
    """
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts

def solve_greedy(n, max_restarts=25, verbose=False): # Added a 'verbose' flag
    """
    Solves N-Queens using steepest-ascent hill climbing with random restarts.
    The board is represented as board[col] = row.
    """
    for restart in range(max_restarts):
        # --- NEW: Print progress for each restart attempt ---
        if verbose:
            # The '\r' character moves the cursor to the beginning of the line
            # The 'end=""' prevents it from printing a newline
            print(f"    (Restart attempt {restart + 1}/{max_restarts})", end='\r')

        current_board = [random.randint(0, n - 1) for _ in range(n)]
        current_conflicts = calculate_conflicts(current_board, n)

        if current_conflicts == 0:
            if verbose: print() # Print a newline to clean up the progress line
            return current_board, 0, restart + 1

        while True:
            best_move = None
            min_conflicts = current_conflicts

            for col_to_move in range(n):
                original_row = current_board[col_to_move]
                for row_to_move in range(n):
                    if current_board[col_to_move] == row_to_move:
                        continue

                    current_board[col_to_move] = row_to_move
                    new_conflicts = calculate_conflicts(current_board, n)

                    if new_conflicts < min_conflicts:
                        min_conflicts = new_conflicts
                        best_move = (col_to_move, row_to_move)
                    
                    current_board[col_to_move] = original_row

            if best_move is None:
                break
            
            col, new_row = best_move
            current_board[col] = new_row
            current_conflicts = min_conflicts

            if current_conflicts == 0:
                if verbose: print() # Print a newline
                return current_board, 0, restart + 1

    if verbose: print() # Print a newline
    return current_board, current_conflicts, max_restarts

if __name__ == '__main__':
    # --- Configuration ---
    N = 50 # Change N for testing
    TOTAL_RUNS = 10

    # --- Data Collection Lists ---
    execution_times = []
    peak_memories = []
    success_count = 0

    print(f"--- Running Greedy Search for N={N} over {TOTAL_RUNS} trials ---")

    # --- Main Testing Loop ---
    for i in range(TOTAL_RUNS):
        # --- NEW: Announce the start of the trial ---
        print(f"Starting Trial {i + 1}/{TOTAL_RUNS}...")

        tracemalloc.start()
        start_time = time.perf_counter()

        # Pass verbose=True to see the inner progress
        solution, conflicts, restarts = solve_greedy(N, verbose=True)

        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_times.append(end_time - start_time)
        peak_memories.append(peak)

        if conflicts == 0:
            success_count += 1
            print(f"  -> Trial {i + 1} Result: SUCCESS (found solution in {restarts} restarts)")
        else:
            print(f"  -> Trial {i + 1} Result: FAILURE (best board had {conflicts} conflicts)")

    # --- Final Calculations and Reporting ---
    print("\n" + "="*40)
    print(f"      PERFORMANCE SUMMARY FOR N={N}")
    print("="*40)

    if execution_times:
        avg_time = statistics.mean(execution_times)
        print(f"Average Execution Time: {avg_time:.6f} seconds")
    else:
        print("No successful runs to calculate average time.")

    if peak_memories:
        avg_memory_mb = statistics.mean(peak_memories) / 10**6
        print(f"Average Peak Memory:    {avg_memory_mb:.6f} MB")
    else:
        print("No runs to calculate average memory.")
        
    success_rate = (success_count / TOTAL_RUNS) * 100
    print(f"Success Rate:           {success_rate:.1f}% ({success_count}/{TOTAL_RUNS} successful runs)")
    print("="*40 + "\n")