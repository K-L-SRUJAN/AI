import math

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

# Initialize board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]


# ---------- Utility Functions ----------
def print_board(board, show_numbers=False):
    """Print the current board."""
    print()
    for i in range(3):
        row_display = []
        for j in range(3):
            if board[i][j] == EMPTY and show_numbers:
                row_display.append(str(i * 3 + j + 1))
            else:
                row_display.append(board[i][j])
        print(" | ".join(row_display))
        if i < 2:
            print("-" * 9)
    print()


def check_winner(board):
    """Return the winner ('X', 'O') or None."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def is_full(board):
    """Check if the board is full (draw)."""
    return all(cell != EMPTY for row in board for cell in row)


def box_to_coords(box):
    """Convert box number (1-9) to (row, col)."""
    box -= 1
    return box // 3, box % 3


# ---------- Alpha-Beta Minimax ----------
def minimax(board, depth, alpha, beta, is_maximizing):
    """Minimax algorithm with alpha-beta pruning."""
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        # Prune: no need to explore further
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        # Prune: no need to explore further
                        return min_eval
        return min_eval


def best_move(board):
    """Find the best move for the AI using alpha-beta minimax."""
    best_score = -math.inf
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


# ---------- Game Loop ----------
def play_game():
    print("Tic Tac Toe — You are O, AI is X")
    print("Select a box number (1–9):")
    print_board(board, show_numbers=True)

    while True:
        # Human move
        try:
            move = int(input("Enter box number (1–9): "))
            if move < 1 or move > 9:
                print("Invalid number! Choose between 1 and 9.")
                continue
            row, col = box_to_coords(move)
            if board[row][col] != EMPTY:
                print("That spot is taken! Try another.")
                continue
        except ValueError:
            print("Please enter a number (1–9).")
            continue

        board[row][col] = HUMAN
        print_board(board)

        if check_winner(board) == HUMAN:
            print("🎉 You win!")
            break
        elif is_full(board):
            print("It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        move = best_move(board)
        if move:
            board[move[0]][move[1]] = AI
            print_board(board)

        if check_winner(board) == AI:
            print("🤖 AI wins!")
            break
        elif is_full(board):
            print("It's a draw!")
            break


# ---------- Run ----------
if __name__ == "__main__":
    play_game()
