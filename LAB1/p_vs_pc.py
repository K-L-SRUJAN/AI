import random

def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def player_move(board, player_symbol):
    """Handles player's move, including input and validation."""
    while True:
        try:
            move = int(input(f"Player {player_symbol}, enter your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] not in ("X", "O"):
                board[move] = player_symbol
                break
            else:
                print("Invalid move. That spot is already taken or out of bounds. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def computer_move(board, computer_symbol, player_symbol):
    """Handles the computer's move with a basic AI."""

    for i in range(9):
        if board[i] not in ("X", "O"):
            temp_board = list(board)
            temp_board[i] = computer_symbol
            if check_win(temp_board, computer_symbol):
                board[i] = computer_symbol
                return

  
    for i in range(9):
        if board[i] not in ("X", "O"):
            temp_board = list(board)
            temp_board[i] = player_symbol
            if check_win(temp_board, player_symbol):
                board[i] = computer_symbol
                return

    
    available_moves = [i for i, spot in enumerate(board) if spot not in ("X", "O")]
    if available_moves:
        move = random.choice(available_moves)
        board[move] = computer_symbol
    else:
        print("Computer cannot make a move (no empty spots).")

def check_win(board, player_symbol):
    """Checks if a player has won."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]            # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player_symbol:
            return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(spot in ("X", "O") for spot in board)

def main():
    """Main game loop."""
    board = [str(i + 1) for i in range(9)]
    player_symbol = "X"
    computer_symbol = "O"
    turn = 0

    print("Welcome to Tic-Tac-Toe!")

    while True:
        print_board(board)

        if turn % 2 == 0:
            player_move(board, player_symbol)
        else:
            computer_move(board, computer_symbol, player_symbol)

        if check_win(board, player_symbol):
            print_board(board)
            print(f"Congratulations! Player {player_symbol} wins!")
            break
        elif check_win(board, computer_symbol):
            print_board(board)
            print(f"Player {computer_symbol} (Computer) wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        turn += 1

if __name__ == "__main__":
    main()
