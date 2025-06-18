import random
import math
import time
import tracemalloc
import statistics

def calculate_conflicts(board, n):
    """
    Calculates the total number of attacking pairs of queens. (Same as Hill Climbing)
    """
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts

def solve_simulated_annealing(n, initial_temp=1000, cooling_rate=0.995):
    """
    Solves N-Queens using Simulated Annealing.
    """
    # Start with a random board
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_conflicts = calculate_conflicts(current_board, n)
    
    temp = initial_temp

    # Limit the number of iterations to prevent excessively long runs
    max_iterations = 20000 
    for _ in range(max_iterations):
        if not (temp > 0.1 and current_conflicts > 0):
            break

        # Choose a random queen to move
        col_to_move = random.randint(0, n - 1)
        original_row = current_board[col_to_move]
        
        # Choose a new random row for this queen
        new_row = random.randint(0, n - 1)
        
        # Make a temporary move
        current_board[col_to_move] = new_row
        new_conflicts = calculate_conflicts(current_board, n)
        
        # Calculate the change in energy (conflicts)
        delta_e = new_conflicts - current_conflicts
        
        # Decide whether to accept the move
        if delta_e < 0: # Always accept a better state
            current_conflicts = new_conflicts
        else:
            # Accept a worse state with a certain probability
            acceptance_probability = math.exp(-delta_e / temp)
            if random.random() < acceptance_probability:
                current_conflicts = new_conflicts
            else:
                # Revert the move if not accepted
                current_board[col_to_move] = original_row
        
        # Cool the temperature
        temp *= cooling_rate

    return current_board, current_conflicts

if __name__ == '__main__':
    # --- Configuration ---
    N = 200 # Change N for testing (e.g., 10, 30, 50, 100, 200)
    TOTAL_RUNS = 10

    # --- Data Collection Lists ---
    execution_times = []
    peak_memories = []
    success_count = 0

    print(f"--- Running Simulated Annealing for N={N} over {TOTAL_RUNS} trials ---")

    # --- Main Testing Loop ---
    for i in range(TOTAL_RUNS):
        print(f"Starting Trial {i + 1}/{TOTAL_RUNS}...")

        # Start tracking for this trial
        tracemalloc.start()
        start_time = time.perf_counter()

        # Run the algorithm
        solution, conflicts = solve_simulated_annealing(N)

        # Stop tracking for this trial
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Store the results of this trial
        execution_times.append(end_time - start_time)
        peak_memories.append(peak)

        # Check if this trial was successful
        if conflicts == 0:
            success_count += 1
            print(f"  -> Trial {i + 1} Result: SUCCESS")
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