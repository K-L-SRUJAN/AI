import copy

class PuzzleState:
    """Represents a state in the 8-puzzle problem."""
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board  # 2D list representing the puzzle board
        self.parent = parent  # Parent PuzzleState
        self.move = move  # Move that led to this state (e.g., "Up", "Down")
        self.depth = depth  # Depth of this state in the search tree
        self.blank_pos = self._find_blank()

    def _find_blank(self):
        """Finds the coordinates of the blank tile (0)."""
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    return r, c
        return -1, -1 # Should not happen in a valid 8-puzzle

    def __eq__(self, other):
        """Compares two PuzzleState objects based on their board configuration."""
        return self.board == other.board

    def __hash__(self):
        """Generates a hash for the PuzzleState based on its board configuration."""
        return hash(tuple(tuple(row) for row in self.board))

    def get_neighbors(self):
        """Generates valid neighboring states by moving the blank tile."""
        neighbors = []
        br, bc = self.blank_pos
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]

        for dr, dc, move_name in moves:
            new_br, new_bc = br + dr, bc + dc
            if 0 <= new_br < 3 and 0 <= new_bc < 3:
                new_board = copy.deepcopy(self.board)
                new_board[br][bc], new_board[new_br][new_bc] = new_board[new_br][new_bc], new_board[br][bc]
                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1))
        return neighbors

def dls(start_node, goal_board, limit):
    """Depth-Limited Search (DLS) algorithm."""
    stack = [(start_node, [start_node.board])] # (node, path_boards)
    
    while stack:
        current_node, path_boards = stack.pop()

        if current_node.board == goal_board:
            return current_node # Solution found

        if current_node.depth < limit:
            for neighbor in current_node.get_neighbors():
                if neighbor.board not in path_boards: # Avoid cycles within the current path
                    stack.append((neighbor, path_boards + [neighbor.board]))
    return None # No solution found within the depth limit

def iddfs(initial_board, goal_board):
    """Iterative Deepening Depth-First Search (IDDFS) algorithm."""
    depth = 0
    while True:
        print(f"Searching with depth limit: {depth}")
        start_node = PuzzleState(initial_board)
        result = dls(start_node, goal_board, depth)
        if result:
            return result # Solution found
        depth += 1

def print_solution(goal_node):
    """Prints the path from the initial state to the goal state."""
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    
    path.reverse()
    for i, state in enumerate(path):
        print(f"Step {i} (Move: {state.move if state.move else 'Start'}):")
        for row in state.board:
            print(row)
        print()

if __name__ == "__main__":
    initial_board = [[1,2,3], [4, 5, 6], [0,7, 8]]
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print("Initial State:")
    for row in initial_board:
        print(row)
    print("\nGoal State:")
    for row in goal_board:
        print(row)
    print("\nSolving...")

    solution_node = iddfs(initial_board, goal_board)

    if solution_node:
        print("\nSolution Found!")
        print_solution(solution_node)
    else:
        print("\nNo solution found.")
