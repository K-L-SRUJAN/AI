
board = [' ' for _ in range(9)]


def print_board(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def player_move(player_icon, board):
    while True:
        try:
            choice = int(input(f"Player {player_icon}, enter your move (1-9): "))
            if 1 <= choice <= 9 and board[choice - 1] == ' ':
                board[choice - 1] = player_icon
                break
            else:
                print("Invalid move. That space is either taken or out of range. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")


def check_win(board, player_icon):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == player_icon and \
           board[condition[1]] == player_icon and \
           board[condition[2]] == player_icon:
            return True
    return False


def check_draw(board):
    return ' ' not in board


def play_game():
    current_player = 'X'
    while True:
        print_board(board)
        player_move(current_player, board)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break


        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    play_game()
