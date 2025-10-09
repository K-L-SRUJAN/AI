import random
import time

def calculate_attacking_queens(board):
    """
    Calculates the number of attacking queen pairs on the board.
    The board is a list where board[column] = row.
    """
    n = len(board)
    attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
           
            if board[i] == board[j]:
                attacking_pairs += 1
           
            if abs(board[i] - board[j]) == abs(i - j):
                attacking_pairs += 1
    return attacking_pairs

def get_neighboring_states(board):
    """
    Generates all possible neighboring states by moving one queen
    in its column.
    """
    n = len(board)
    neighbors = []
    for col in range(n):
        original_row = board[col]
    
        for row in range(n):
            if row != original_row:
                new_board = list(board)
                new_board[col] = row
                neighbors.append(new_board)
    return neighbors

def print_board(board):
    """
    Prints the chessboard in a readable format.
    """
    if board is None:
        return
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print("\n")

def hill_climbing_with_visualization(n=4, max_restarts=10):
    """
    Solves the N-Queens problem using hill climbing with random restarts and
    prints each step for visualization.
    """
    print(f"--- Starting Hill Climbing for {n}-Queens with Visualization ---\n")
    for restart_count in range(max_restarts):
       
        board = [random.randint(0, n - 1) for _ in range(n)]
        current_cost = calculate_attacking_queens(board)
        
        print(f"Random Restart #{restart_count + 1}")
        print("Initial board (colision: {}):".format(current_cost))
        print_board(board)

        while True:
           
            if current_cost == 0:
                print("Goal state reached! Solution found.")
                return board

           
            neighbors = get_neighboring_states(board)
            best_neighbor = None
            min_cost = current_cost

           
            for neighbor in neighbors:
                neighbor_cost = calculate_attacking_queens(neighbor)
                if neighbor_cost < min_cost:
                    min_cost = neighbor_cost
                    best_neighbor = neighbor

           
            if min_cost >= current_cost:
                print("Stuck in a local optimum (Cost: {}). Restarting...".format(current_cost))
                break 
            
          
            print(f"Moving from a colision of {current_cost} to a new min colision of {min_cost}.")
            board = best_neighbor
            current_cost = min_cost
            print_board(board)
            time.sleep(0.5) 
    
    print("Failed to find a solution within the maximum number of restarts.")
    return None

if __name__ == "__main__":
    solution = hill_climbing_with_visualization(n=4)
    if solution:
        print("Final Solution:")
        print_board(solution)

