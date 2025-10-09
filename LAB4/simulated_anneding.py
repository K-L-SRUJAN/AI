import random
import math
import copy

# Board size
N = 4

def generate_random_board(n):
    """
    Generates a random initial board configuration.
    The board is represented as an array where the index is the column
    and the value is the row of the queen in that column.
    """
    board = [random.randint(0, n - 1) for _ in range(n)]
    return board

def calculate_conflicts(board):
    """
    Calculates the number of conflicting pairs of queens.
    This is the energy or cost function to be minimized.
    """
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for horizontal conflicts (same row)
            if board[i] == board[j]:
                conflicts += 1
            # Check for diagonal conflicts
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_most_conflicting_queen(board):
    """
    Identifies the queen that is involved in the most conflicts.
    This helps to generate more effective neighbor states.
    """
    n = len(board)
    conflicts_per_queen = [0] * n
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # Check horizontal conflict
            if board[i] == board[j]:
                conflicts_per_queen[i] += 1
            # Check diagonal conflict
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts_per_queen[i] += 1

    # Find the queen with the maximum number of conflicts
    max_conflicts = max(conflicts_per_queen)
    if max_conflicts == 0:
        return -1 # No conflicts, any queen can be moved
    
    most_conflicting_queens = [i for i, conflicts in enumerate(conflicts_per_queen) if conflicts == max_conflicts]
    return random.choice(most_conflicting_queens)

def get_neighbor_optimized(board):
    """
    Generates a neighboring board state by moving a single queen,
    preferably one with the most conflicts.
    """
    n = len(board)
    new_board = list(board)
    
    col_to_move = get_most_conflicting_queen(board)
    if col_to_move == -1:
        col_to_move = random.randint(0, n - 1)
    
    current_row = new_board[col_to_move]
    new_row = random.randint(0, n - 1)
    while new_row == current_row:
        new_row = random.randint(0, n - 1)
        
    new_board[col_to_move] = new_row
    return new_board, col_to_move, current_row, new_row


def simulated_annealing(initial_board, initial_temperature, cooling_rate, max_no_improvement):
    """
    Solves the N-Queens problem with an optimized simulated annealing.
    Includes a restart mechanism to escape local optima.
    """
    current_board = copy.deepcopy(initial_board)
    current_energy = calculate_conflicts(current_board)
    temperature = initial_temperature
    iteration = 0
    no_improvement_count = 0
    best_board = current_board
    best_energy = current_energy
    
    while True:
        print(f"\n--- Iteration: {iteration}, Temperature: {temperature:.2f} ---")
        print("Current board:")
        print_board(current_board)
        print(f"Current conflicts: {current_energy}")
        
        if current_energy == 0:
            print("\nSolution found!")
            return current_board
        
        if temperature <= 0 or no_improvement_count > max_no_improvement:
            print(f"\nStuck in local optimum (no improvement for {max_no_improvement} steps). Restarting...")
            return simulated_annealing(generate_random_board(len(initial_board)), initial_temperature, cooling_rate, max_no_improvement)
            
        neighbor_board, col, old_row, new_row = get_neighbor_optimized(current_board)
        neighbor_energy = calculate_conflicts(neighbor_board)
        
        energy_difference = neighbor_energy - current_energy
        
        print(f"Attempting to move queen in column {col} from row {old_row} to row {new_row}.")
        
        if energy_difference < 0:
            print(f"Move accepted: New energy {neighbor_energy} is lower.")
            current_board = neighbor_board
            current_energy = neighbor_energy
            if current_energy < best_energy:
                best_energy = current_energy
                best_board = current_board
            no_improvement_count = 0
        else:
            acceptance_prob = math.exp(-energy_difference / temperature)
            if random.random() < acceptance_prob:
                print(f"Move accepted probabilistically: New energy {neighbor_energy} is higher, but accepted with probability {acceptance_prob:.4f}.")
                current_board = neighbor_board
                current_energy = neighbor_energy
            else:
                print(f"Move rejected: New energy {neighbor_energy} is higher.")
            no_improvement_count += 1
            
        temperature *= cooling_rate
        iteration += 1

def print_board(board):
    """Prints the board configuration."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)

if __name__ == "__main__":
    # N is defined at the top of the file
    initial_board = generate_random_board(N)
    
    print("Initial board:")
    print_board(initial_board)
    print("Initial conflicts:", calculate_conflicts(initial_board))
    
    # Tuned annealing parameters for faster convergence
    initial_temp = 100
    cooling_rate = 0.95  # Faster cooling rate
    max_no_improvement = 20 # Restart if no improvement in this many steps
    
    final_board = simulated_annealing(initial_board, initial_temp, cooling_rate, max_no_improvement)
    
    print("\n--- Final Solution ---")
    print_board(final_board)
    print("Final conflicts:", calculate_conflicts(final_board))
