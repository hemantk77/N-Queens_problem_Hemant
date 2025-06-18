import random
import time
import tracemalloc
import statistics

def calculate_fitness(board, n):
    """
    Calculates fitness as the number of non-attacking pairs of queens.
    Max non-attacking pairs = N*(N-1)/2. A solution has this fitness.
    """
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    max_fitness = (n * (n - 1)) / 2
    return max_fitness - conflicts

def selection(population, fitnesses, k=3):
    """
    Tournament selection: select k individuals and return the best one.
    """
    best_individual = None
    best_fitness = -1
    for _ in range(k):
        idx = random.randint(0, len(population) - 1)
        if fitnesses[idx] > best_fitness:
            best_fitness = fitnesses[idx]
            best_individual = population[idx]
    return best_individual

def crossover(parent1, parent2, n):
    """
    Single-point crossover.
    """
    crossover_point = random.randint(1, n - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(board, mutation_rate, n):
    """
    Randomly changes a queen's position with a given probability.
    """
    if random.random() < mutation_rate:
        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        board[col] = row
    return board

def solve_genetic_algorithm(n, pop_size, mutation_rate, max_generations, verbose=False):
    """
    Solves N-Queens using a Genetic Algorithm.
    """
    max_fitness = (n * (n - 1)) / 2
    
    # Initialize population
    population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]

    for generation in range(max_generations):
        # Calculate fitness for the whole population
        fitnesses = [calculate_fitness(ind, n) for ind in population]

        # Check for a solution
        for i in range(pop_size):
            if fitnesses[i] == max_fitness:
                if verbose: print() # Clean up progress line
                return population[i], generation + 1

        # Print progress (optional)
        if verbose and (generation + 1) % 50 == 0:
            best_current_fitness = max(fitnesses)
            print(f"    (Generation {generation + 1}/{max_generations}, Best fitness: {best_current_fitness:.0f}/{max_fitness:.0f})", end='\r')


        # Create the next generation
        new_population = []
        for _ in range(pop_size):
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            child = crossover(parent1, parent2, n)
            child = mutate(child, mutation_rate, n)
            new_population.append(child)
        
        population = new_population

    # If no solution found after max generations, return the best one from the final population
    if verbose: print() # Clean up progress line
    fitnesses = [calculate_fitness(ind, n) for ind in population]
    best_fitness = max(fitnesses)
    best_individual = population[fitnesses.index(best_fitness)]
    return best_individual, max_generations

if __name__ == '__main__':
    # --- Configuration ---
    N = 50 # Change N for testing (e.g., 10, 30, 50, 100, 200)
    TOTAL_RUNS = 10
    
    # --- GA Hyperparameters ---
    POP_SIZE = 150
    MUTATION_RATE = 0.1
    MAX_GENERATIONS = 2000

    # --- Data Collection Lists ---
    execution_times = []
    peak_memories = []
    success_count = 0

    print(f"--- Running Genetic Algorithm for N={N} over {TOTAL_RUNS} trials ---")

    # --- Main Testing Loop ---
    for i in range(TOTAL_RUNS):
        print(f"Starting Trial {i + 1}/{TOTAL_RUNS}...")

        # Start tracking for this trial
        tracemalloc.start()
        start_time = time.perf_counter()

        # Run the algorithm
        solution, generations = solve_genetic_algorithm(
            N, POP_SIZE, MUTATION_RATE, MAX_GENERATIONS, verbose=True
        )

        # Stop tracking for this trial
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Store the results of this trial
        execution_times.append(end_time - start_time)
        peak_memories.append(peak)

        # Check if this trial was successful by calculating its fitness
        max_fitness = (N * (N - 1)) / 2
        solution_fitness = calculate_fitness(solution, N)

        if solution_fitness == max_fitness:
            success_count += 1
            print(f"  -> Trial {i + 1} Result: SUCCESS (found in {generations} generations)")
        else:
            print(f"  -> Trial {i + 1} Result: FAILURE (best fitness: {solution_fitness:.0f}/{max_fitness:.0f})")

    # --- Final Calculations and Reporting ---
    print("\n" + "="*40)
    print(f"      PERFORMANCE SUMMARY FOR N={N}")
    print("="*40)

    if execution_times:
        avg_time = statistics.mean(execution_times)
        print(f"Average Execution Time: {avg_time:.6f} seconds")
    else:
        print("No runs to calculate average time.")

    if peak_memories:
        avg_memory_mb = statistics.mean(peak_memories) / 10**6
        print(f"Average Peak Memory:    {avg_memory_mb:.6f} MB")
    else:
        print("No runs to calculate average memory.")
        
    success_rate = (success_count / TOTAL_RUNS) * 100
    print(f"Success Rate:           {success_rate:.1f}% ({success_count}/{TOTAL_RUNS} successful runs)")
    print("="*40 + "\n")