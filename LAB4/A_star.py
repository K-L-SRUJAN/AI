import heapq

# The goal state for the 8-puzzle
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
BLANK = 0

class PuzzleState:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.g_score = 0
        self.h_score = self.manhattan_distance()
        self.f_score = self.g_score + self.h_score

    def __lt__(self, other):
        """Used for priority queue comparison based on f_score."""
        return self.f_score < other.f_score

    def __hash__(self):
        """Enables storing states in a set."""
        return hash(self.board)

    def __eq__(self, other):
        """Enables comparing states."""
        return self.board == other.board

    def manhattan_distance(self):
        """Calculates the sum of Manhattan distances for all misplaced tiles."""
        distance = 0
        for i in range(9):
            if self.board[i] != BLANK and self.board[i] != GOAL_STATE[i]:
                current_pos = i
                goal_pos = self.board.index(self.board[i])

                # Convert 1D index to 2D coordinates (row, col)
                current_row, current_col = divmod(current_pos, 3)
                goal_row, goal_col = divmod(goal_pos, 3)

                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def get_neighbors(self):
        """Generates all valid neighboring puzzle states."""
        neighbors = []
        blank_index = self.board.index(BLANK)
        blank_row, blank_col = divmod(blank_index, 3)


        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = blank_row + dr, blank_col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col

                new_board = list(self.board)
                new_board[blank_index], new_board[new_index] = new_board[new_index], new_board[blank_index]
                neighbors.append(PuzzleState(tuple(new_board), self, move=(dr, dc)))

        return neighbors

def reconstruct_path(current_state):
    """Traces back through parent pointers to find the solution path."""
    path = []
    while current_state:
        path.append(current_state.board)
        current_state = current_state.parent
    return path[::-1]

def a_star_solve(initial_board):
    """
    Finds the optimal solution to the 8-puzzle using the A* algorithm.

    Args:
        initial_board: A tuple representing the starting board configuration.

    Returns:
        A list of tuples representing the path from the initial to the goal state,
        or None if no solution is found.
    """
    initial_state = PuzzleState(initial_board)

    open_set = [initial_state]
    came_from = {}
    g_scores = {initial_state.board: 0}

    while open_set:
        current = heapq.heappop(open_set)

        if current.board == GOAL_STATE:
            return reconstruct_path(current)

        for neighbor in current.get_neighbors():
            tentative_g_score = g_scores[current.board] + 1

            if tentative_g_score < g_scores.get(neighbor.board, float('inf')):
                came_from[neighbor.board] = current
                neighbor.g_score = tentative_g_score
                neighbor.f_score = neighbor.g_score + neighbor.h_score

                g_scores[neighbor.board] = tentative_g_score
                heapq.heappush(open_set, neighbor)

    return None

def print_solution(path):
    if not path:
        print("No solution found.")
        return

    print("Solution path:")
    for i, board in enumerate(path):
        print(f"--- Step {i} ---")
        for j in range(0, 9, 3):
            print(board[j:j+3])
    print(f"\nSolved in {len(path) - 1} moves.")


initial_board = (1, 2, 3, 0, 4, 6, 7, 5, 8) 

solution_path = a_star_solve(initial_board)
print_solution(solution_path)
