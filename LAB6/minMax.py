import math

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

# Create the board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

# Print board with box numbers
def print_board(board, show_numbers=False):
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

# Check winner
def check_winner(board):
    # Rows and Columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

# Check if full
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Minimax
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    score = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_score = min(best_score, score)
        return best_score

# Find best move
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Convert box number (1-9) to (row, col)
def box_to_coords(box):
    box -= 1
    return box // 3, box % 3

# Game loop
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

# Run the game
if __name__ == "__main__":
    play_game()
